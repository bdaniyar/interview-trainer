"""Trusted bootstrap for a DIFFERENT image; the SELECT image remains read-only."""

import os
from pathlib import Path
import signal
import time
import psycopg
from sql_runner.app.bootstrap import initialize, seed, SOCKET


def main():
    lifetime = min(90, max(1, int(os.getenv("SQL_ABSOLUTE_SECONDS", "60"))))

    def stop(*_):
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGALRM, stop)
    signal.alarm(lifetime)
    process = initialize()
    try:
        deadline = time.monotonic() + 15
        while True:
            try:
                with psycopg.connect(
                    host=SOCKET, user="postgres", dbname="postgres", connect_timeout=1
                ):
                    break
            except psycopg.OperationalError:
                if process.poll() is not None or time.monotonic() > deadline:
                    raise RuntimeError("PostgreSQL bootstrap expired")
                time.sleep(0.03)
        seed()
        with psycopg.connect(
            host=SOCKET, user="postgres", dbname="lab", autocommit=True
        ) as conn:
            conn.execute("SET search_path=lab,pg_catalog")
            conn.execute(
                "CREATE TABLE inventory (id bigint PRIMARY KEY,available integer NOT NULL CHECK(available>=0))"
            )
            conn.execute(
                "CREATE TABLE reservations (request_key text PRIMARY KEY,room_id bigint NOT NULL REFERENCES inventory(id),active boolean NOT NULL DEFAULT true)"
            )
            conn.execute(
                "CREATE UNIQUE INDEX one_active_booking ON reservations(room_id) WHERE active"
            )
            conn.execute(
                "CREATE TABLE slots (id integer PRIMARY KEY,period int4range NOT NULL,EXCLUDE USING gist (period WITH &&))"
            )
            conn.execute("GRANT SELECT,INSERT ON slots TO student")
            conn.execute(
                "CREATE INDEX orders_owner_time ON orders(user_id,created_at,id)"
            )
            conn.execute("INSERT INTO inventory VALUES (1,1),(2,1)")
            conn.execute("GRANT SELECT ON inventory,reservations TO student")
            conn.execute(
                "GRANT INSERT,UPDATE,DELETE ON orders,inventory,reservations TO student"
            )
            conn.execute("ALTER ROLE student SET default_transaction_read_only=off")
            conn.execute("ALTER ROLE student SET statement_timeout='3000ms'")
            conn.execute("ALTER ROLE student SET lock_timeout='1500ms'")
            conn.execute(
                "ALTER ROLE student SET idle_in_transaction_session_timeout='5000ms'"
            )
            conn.execute("ALTER ROLE student SET transaction_timeout='15000ms'")
            conn.execute("ALTER ROLE student SET deadlock_timeout='100ms'")
            # Read-only lock observation for the trusted deterministic scheduler.
            # The student AST still rejects this function and all catalog relations.
            conn.execute(
                "GRANT EXECUTE ON FUNCTION pg_catalog.pg_blocking_pids(integer) TO student"
            )
        Path("/pgdata/tx-ready").touch(mode=0o600)
        while process.poll() is None:
            time.sleep(0.1)
    finally:
        if process.poll() is None:
            process.send_signal(signal.SIGINT)
            try:
                process.wait(timeout=2)
            except Exception:
                process.kill()
                process.wait()


if __name__ == "__main__":
    main()
