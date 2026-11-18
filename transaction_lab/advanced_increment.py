"""Separate durable Check contract for two stock adjustments on the same row."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier, Event
from time import monotonic
import json
import sys

from transaction_lab.execute import connect, script, snapshot
from transaction_lab.policy import validate_script

TASK = "pg.tx.11.11.stock-increment-v1"
STARTS = (1, 0, 4, 17, 101, 2)
REFERENCE = "UPDATE inventory SET available=available+1 WHERE id=1 RETURNING id,available"


def run(source, case):
    validate_script(source)
    if type(case) is not int or not 0 <= case < len(STARTS):
        raise ValueError("Unknown fixture")
    barrier = Barrier(3, timeout=2)
    with connect() as observer, connect() as a, connect() as b:
        observer.execute("UPDATE inventory SET available=%s WHERE id=1", (STARTS[case],))
        before = snapshot(observer)
        observer.execute("BEGIN")
        observer.execute("SELECT id FROM inventory WHERE id=1 FOR UPDATE")

        def execute(connection, side):
            barrier.wait()
            return script(connection, source, side)

        blocked = False
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(execute, connection, side)
                       for connection, side in [(a, "A"), (b, "B")]]
            barrier.wait()
            try:
                deadline = monotonic() + 0.8
                pids = [a.info.backend_pid, b.info.backend_pid]
                # First and second waiters may be linked by PostgreSQL's wait queue.
                while monotonic() < deadline and not any(f.done() for f in futures):
                    waits = observer.execute(
                        "SELECT pg_catalog.pg_blocking_pids(%s),pg_catalog.pg_blocking_pids(%s)", pids
                    ).fetchone()
                    if all(waits):
                        blocked = True
                        break
                    Event().wait(.015)
            finally:
                observer.execute("COMMIT")
            traces = [future.result(timeout=5) for future in futures]
        return dict(before=before, after=snapshot(observer), timelines=traces,
                    blocked=blocked, connections=2)


def passes(result, case):
    if result.get("error") or not result["blocked"]:
        return False
    before, after = result["before"], result["after"]
    expected = [["1", str(STARTS[case] + 2)], before["inventory"]["rows"][1]]
    if any(before[table]["rows"] != after[table]["rows"] for table in before if table != "inventory"):
        return False
    if after["inventory"]["rows"] != expected:
        return False
    returned = []
    for trace in result["timelines"]:
        if any("sqlstate" in event or "cleanup" in event for event in trace):
            return False
        results = [event["result"] for event in trace if event.get("result", {}).get("columns")]
        if not results:
            return False
        last = results[-1]
        if (last["truncated"] or last["has_more"]
                or [(col["name"], col["pg_type"]) for col in last["columns"]]
                != [("id", "int8"), ("available", "int4")] or len(last["rows"]) != 1):
            return False
        returned.extend(tuple(row) for row in last["rows"])
    return Counter(returned) == Counter({("1", str(STARTS[case] + step)): 1 for step in (1, 2)})


def check(source, namespace):
    from transaction_lab.control import attempt

    validate_script(source)
    succeeded = 0
    for case in range(len(STARTS)):
        with attempt(namespace) as (backend, handle):
            result = backend._command(handle, "transaction_lab.advanced_increment",
                [json.dumps({"sql": source, "case": case}, ensure_ascii=False)], student=True)
        succeeded += int(passes(result, case))
    return dict(task_id=TASK, revision=1, passed=succeeded == len(STARTS),
                tests_passed=succeeded, tests_total=len(STARTS))


if __name__ == "__main__":
    arguments = json.loads(sys.argv[1])
    print(json.dumps(run(arguments["sql"], arguments["case"]), ensure_ascii=False))
