"""Bounded student-role query and plan collection in the dedicated lab."""
import json
from statistics import median
import sys

import psycopg

from index_lab.policy import select
from sql_runner.app.executor import collect, connect, json_bytes
from sql_runner.app.policy import PolicyError


def measure(connection, query):
    options = "EXPLAIN (ANALYZE, BUFFERS, TIMING OFF, FORMAT JSON) "
    raw = connection.execute(options + query).fetchone()[0][0]
    return dict(plan=raw["Plan"], execution_ms=raw["Execution Time"],
                planning_ms=raw["Planning Time"])


def prove(payload):
    source = select(payload["sql"])
    baseline = select(payload["baseline"]) if payload.get("baseline") else None
    with connect() as connection:
        connection.read_only = True
        if payload.get("estimated"):
            raw = connection.execute("EXPLAIN (FORMAT JSON) " + source).fetchone()[0][0]
            return {"plan": raw["Plan"], "estimated": True}
        with connection.cursor(name="index_result") as cursor:
            cursor.execute(source)
            result = collect(cursor, connection)
        plans = [measure(connection, source) for _ in range(payload["samples"])]
        before = [measure(connection, baseline) for _ in range(payload["samples"])] if baseline else []
        controlled = None
        if payload.get("path_proof"):
            connection.execute("SET LOCAL enable_seqscan = off")
            controlled = measure(connection, source)["plan"]
    return dict(result=result, plan=plans[0]["plan"],
                samples=[value["execution_ms"] for value in plans],
                median_ms=median(value["execution_ms"] for value in plans),
                baseline_samples=[value["execution_ms"] for value in before],
                baseline_plan=before[0]["plan"] if before else None, controlled=controlled,
                planning_ms=plans[0]["planning_ms"],
                baseline_planning_ms=before[0]["planning_ms"] if before else None)


if __name__ == "__main__":
    try:
        value = prove(json.loads(sys.argv[1]))
        data = json_bytes(value)
        if len(data) > 1024 * 1024:
            raise ValueError
    except PolicyError:
        data = json_bytes({"error": "policy"})
    except psycopg.Error as exc:
        data = json_bytes({"error": "postgres", "sqlstate": exc.sqlstate})
    except Exception:
        data = json_bytes({"error": "result_limit"})
    sys.stdout.buffer.write(data)
