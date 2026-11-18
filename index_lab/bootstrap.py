"""PostgreSQL init and watchdog for the dedicated index profile."""
import os
from pathlib import Path
import signal
from time import monotonic, sleep

import psycopg
from sql_runner.app.bootstrap import SOCKET, initialize, seed


def main():
    lifetime = min(60, max(1, int(os.getenv("SQL_ABSOLUTE_SECONDS", "60"))))

    def stop(*_):
        raise SystemExit

    for signum in (signal.SIGALRM, signal.SIGTERM, signal.SIGINT):
        signal.signal(signum, stop)
    signal.alarm(lifetime)
    process = initialize()
    try:
        deadline = monotonic() + 15
        while True:
            try:
                with psycopg.connect(host=SOCKET, user="postgres", dbname="postgres", connect_timeout=1):
                    break
            except psycopg.OperationalError:
                if process.poll() is not None or monotonic() >= deadline:
                    raise
                sleep(.05)
        seed()
        with psycopg.connect(host=SOCKET, user="postgres", dbname="lab", autocommit=True) as db:
            db.execute("DROP SCHEMA lab CASCADE")
            db.execute("CREATE SCHEMA lab")
            db.execute("GRANT USAGE ON SCHEMA lab TO student")
            db.execute("""CREATE TABLE lab.users(id bigint PRIMARY KEY, email text NOT NULL, region text NOT NULL);
                CREATE TABLE lab.orders(id bigint PRIMARY KEY, user_id bigint NOT NULL REFERENCES lab.users,
                hotel_id integer NOT NULL, arrival date NOT NULL, created_at timestamp NOT NULL,
                status text NOT NULL, total integer NOT NULL CHECK(total>0));
                GRANT SELECT ON ALL TABLES IN SCHEMA lab TO student""")
        Path("/pgdata/index-ready").touch(mode=0o600)
        while process.poll() is None:
            sleep(.1)
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
