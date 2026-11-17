"""Fixed student-UID executor: real independent connections, no shell or Docker."""

from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack
import json
import sys
from threading import Barrier, Event
from time import monotonic

import psycopg
from pglast.stream import RawStream
from sql_runner.app.executor import collect, empty_result
from transaction_lab.policy import validate_script


def connect():
    return psycopg.connect(
        host="/var/run/postgresql",
        dbname="lab",
        user="student",
        autocommit=True,
        connect_timeout=2,
    )


def sql(conn, statement, params=None):
    with conn.cursor() as cursor:
        cursor.execute(statement, params)
        if cursor.description:
            return collect(cursor, conn)
        return empty_result() | {"command": cursor.statusmessage}


def snapshot(conn):
    # Only fixed synthetic tables. No student-selected SQL, table or filesystem path.
    return {
        table: sql(
            conn,
            "SELECT * FROM "
            + table
            + " ORDER BY "
            + ("request_key" if table == "reservations" else "id"),
        )
        for table in [
            "users",
            "orders",
            "products",
            "order_items",
            "inventory",
            "reservations",
        ]
        if table != "order_items"
    } | {
        "order_items": sql(
            conn, "SELECT * FROM order_items ORDER BY order_id,product_id"
        ),
        "slots": sql(
            conn,
            "SELECT id,lower(period) AS start,upper(period) AS finish FROM slots ORDER BY id",
        ),
    }


def script(conn, source, label="A", trace=None):
    trace = [] if trace is None else trace
    statements = validate_script(source)
    for raw in statements:
        statement = RawStream()(raw.stmt)
        try:
            result = sql(conn, statement)
            trace.append(dict(session=label, sql=statement, result=result))
            if result["truncated"]:
                raise ValueError("Result limit")
        except psycopg.Error as exc:
            trace.append(dict(session=label, sql=statement, sqlstate=exc.sqlstate))
            # Continue to permit explicit ROLLBACK TO SAVEPOINT recovery.
            # PostgreSQL keeps an aborted transaction failed until recovery.
            continue
    # Explicit transaction left open is rolled back, never silently committed.
    if conn.info.transaction_status != psycopg.pq.TransactionStatus.IDLE:
        conn.rollback()
        trace.append(dict(session=label, cleanup="uncommitted transaction rolled back"))
    return trace


def wait_blocked(observer, waiter, owner):
    deadline = monotonic() + 2
    while monotonic() < deadline:
        pids = observer.execute(
            "SELECT pg_catalog.pg_blocking_pids(%s)", (waiter.info.backend_pid,)
        ).fetchone()[0]
        if owner.info.backend_pid in pids:
            return
        Event().wait(0.01)
    raise RuntimeError("Expected lock dependency was not observed")


def booking(source):
    validate_script(source)
    gate = Barrier(2, timeout=3)

    def request(key):
        with connect() as connection:
            gate.wait()
            # Replace an exact quoted placeholder with a quoted server-owned test key.
            return script(
                connection, source.replace("'REQUEST_KEY'", "'" + key + "'"), key
            )

    with connect() as observer:
        before = snapshot(observer)
        with ThreadPoolExecutor(max_workers=2) as pool:
            a = pool.submit(request, "request-A")
            b = pool.submit(request, "request-B")
            traces = [a.result(timeout=12), b.result(timeout=12)]
        return dict(
            profile="pg-transaction-v1",
            connections=2,
            before=before,
            after=snapshot(observer),
            requests=traces,
        )


def scenario(name):
    with ExitStack() as stack:
        a = stack.enter_context(connect())
        b = stack.enter_context(connect())
        observer = stack.enter_context(connect())
        trace = []
        out = dict(
            profile="pg-transaction-v1", scenario=name, connections=2, timeline=trace
        )

        def step(conn, label, statement):
            result = sql(conn, statement)
            trace.append(dict(session=label, sql=statement, result=result))
            return result["rows"]

        if name in {"read-committed", "repeatable-read", "mvcc"}:
            isolation = (
                "READ COMMITTED" if name == "read-committed" else "REPEATABLE READ"
            )
            step(a, "A", "BEGIN ISOLATION LEVEL " + isolation)
            out["first"] = step(a, "A", "SELECT available FROM inventory WHERE id=1")
            step(b, "B", "BEGIN")
            step(b, "B", "UPDATE inventory SET available=0 WHERE id=1")
            step(b, "B", "COMMIT")
            out["second"] = step(a, "A", "SELECT available FROM inventory WHERE id=1")
            step(a, "A", "ROLLBACK")
            out["current"] = step(
                observer, "observer", "SELECT available FROM inventory WHERE id=1"
            )
        elif name == "rollback-savepoint":
            step(a, "A", "BEGIN")
            step(a, "A", "UPDATE inventory SET available=0 WHERE id=1")
            step(a, "A", "SAVEPOINT local_change")
            step(a, "A", "UPDATE inventory SET available=0 WHERE id=2")
            step(a, "A", "ROLLBACK TO SAVEPOINT local_change")
            step(a, "A", "RELEASE SAVEPOINT local_change")
            out["inside"] = step(
                a, "A", "SELECT id,available FROM inventory ORDER BY id"
            )
            out["outside"] = step(
                b, "B", "SELECT id,available FROM inventory ORDER BY id"
            )
            step(a, "A", "ROLLBACK")
            out["after"] = step(
                b, "B", "SELECT id,available FROM inventory ORDER BY id"
            )
        elif name in {"nowait", "skip-locked", "blocking-update"}:
            step(a, "A", "BEGIN")
            step(a, "A", "SELECT id FROM inventory WHERE id=1 FOR UPDATE")
            step(b, "B", "BEGIN")
            if name == "nowait":
                try:
                    step(
                        b, "B", "SELECT id FROM inventory WHERE id=1 FOR UPDATE NOWAIT"
                    )
                except psycopg.Error as exc:
                    out["sqlstate"] = exc.sqlstate
                    trace.append(dict(session="B", sqlstate=exc.sqlstate))
                b.rollback()
                a.rollback()
            elif name == "skip-locked":
                out["claimed"] = step(
                    b,
                    "B",
                    "SELECT id FROM inventory ORDER BY id FOR UPDATE SKIP LOCKED",
                )
                b.rollback()
                a.rollback()
            else:
                with ThreadPoolExecutor(max_workers=1) as pool:
                    trace.append(dict(session="B", phase="attempting lock"))
                    pending = pool.submit(
                        step,
                        b,
                        "B",
                        "UPDATE inventory SET available=0 WHERE id=1 RETURNING id",
                    )
                    wait_blocked(observer, b, a)
                    out["blocked_observed"] = True
                    trace.append(dict(session="B", phase="blocked on A"))
                    step(a, "A", "COMMIT")
                    out["resumed"] = pending.result(timeout=4)
                step(b, "B", "ROLLBACK")
        elif name == "deadlock":
            step(a, "A", "BEGIN")
            step(b, "B", "BEGIN")
            step(a, "A", "UPDATE inventory SET available=available WHERE id=1")
            step(b, "B", "UPDATE inventory SET available=available WHERE id=2")

            def lock(conn, label, statement):
                try:
                    step(conn, label, statement)
                    return None
                except psycopg.Error as exc:
                    conn.rollback()
                    trace.append(dict(session=label, sqlstate=exc.sqlstate))
                    return exc.sqlstate

            with ThreadPoolExecutor(max_workers=1) as pool:
                first = pool.submit(
                    lock, a, "A", "UPDATE inventory SET available=available WHERE id=2"
                )
                wait_blocked(observer, a, b)
                second = lock(
                    b, "B", "UPDATE inventory SET available=available WHERE id=1"
                )
                # Release survivor's locks before waiting for the other session.
                b.rollback()
                out["states"] = [first.result(timeout=4), second]
                a.rollback()
        elif name == "serializable":
            step(a, "A", "BEGIN ISOLATION LEVEL SERIALIZABLE")
            step(b, "B", "BEGIN ISOLATION LEVEL SERIALIZABLE")
            step(a, "A", "SELECT SUM(available) FROM inventory")
            step(b, "B", "SELECT SUM(available) FROM inventory")
            states = []
            for conn, label, row in [(a, "A", 1), (b, "B", 2)]:
                try:
                    step(
                        conn, label, f"UPDATE inventory SET available=0 WHERE id={row}"
                    )
                    states.append(None)
                except psycopg.Error as exc:
                    states.append(exc.sqlstate)
                    conn.rollback()
            for conn, label in [(a, "A"), (b, "B")]:
                try:
                    step(conn, label, "COMMIT")
                except psycopg.Error as exc:
                    states.append(exc.sqlstate)
                    conn.rollback()
            out["states"] = states
            out["after"] = step(
                observer, "observer", "SELECT id,available FROM inventory ORDER BY id"
            )
        elif name == "lost-update":
            first = step(a, "A", "SELECT available FROM inventory WHERE id=1")[0][0]
            second = step(b, "B", "SELECT available FROM inventory WHERE id=1")[0][0]
            # Intentionally broken read/compute/write with both reads coordinated first.
            step(a, "A", f"UPDATE inventory SET available={int(first)+1} WHERE id=1")
            step(b, "B", f"UPDATE inventory SET available={int(second)+1} WHERE id=1")
            out["after"] = step(
                observer, "observer", "SELECT available FROM inventory WHERE id=1"
            )
            out["serial_expected"] = "3"
        elif name == "exclusion":
            step(a, "A", "BEGIN")
            step(b, "B", "BEGIN")
            step(a, "A", "INSERT INTO slots VALUES (1,'[1,3)'::int4range) RETURNING id")

            def overlap():
                try:
                    step(
                        b,
                        "B",
                        "INSERT INTO slots VALUES (2,'[2,4)'::int4range) RETURNING id",
                    )
                    return None
                except psycopg.Error as exc:
                    b.rollback()
                    return exc.sqlstate

            with ThreadPoolExecutor(max_workers=1) as pool:
                trace.append(dict(session="B", phase="attempting overlapping interval"))
                pending = pool.submit(overlap)
                wait_blocked(observer, b, a)
                out["blocked_observed"] = True
                step(a, "A", "COMMIT")
                out["sqlstate"] = pending.result(timeout=4)
            b.rollback()
            out["after"] = step(
                observer,
                "observer",
                "SELECT id,lower(period) AS start,upper(period) AS finish FROM slots ORDER BY id",
            )
        elif name == "indexes":
            out["plan"] = step(
                a,
                "A",
                "EXPLAIN SELECT id FROM orders WHERE user_id=1 ORDER BY created_at,id",
            )
            out["note"] = (
                "A small fixture may prefer Seq Scan; this is not a performance benchmark."
            )
        else:
            raise ValueError("Unknown controlled scenario")
        return out


def main(payload):
    operation = payload["operation"]
    if operation == "scenario":
        return scenario(payload["scenario"])
    if operation == "booking":
        return booking(payload["sql"])
    if operation == "script":
        with connect() as connection:
            before = snapshot(connection)
            trace = script(connection, payload["sql"])
            after = snapshot(connection)
            return dict(
                profile="pg-transaction-v1",
                connections=1,
                before=before,
                after=after,
                timeline=trace,
            )
    raise ValueError("Unknown operation")


if __name__ == "__main__":
    try:
        output = main(json.loads(sys.argv[1]))
        wire = json.dumps(output, ensure_ascii=False)
        print(
            wire
            if len(wire.encode()) <= 1024 * 1024
            else json.dumps({"error": "result_limit"})
        )
    except Exception as exc:
        print(
            json.dumps(
                {
                    "error": type(exc).__name__,
                    "sqlstate": getattr(exc, "sqlstate", None),
                }
            )
        )
