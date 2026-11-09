"""Trusted sandbox PID 1, before any student connection is admitted."""
import os
from pathlib import Path
import signal
import subprocess
import time

import psycopg
from psycopg import sql

from .config import LOCK_MS, STATEMENT_MS
from .datasets import load_dataset
from .policy import FUNCTIONS, OPERATORS, TYPES

DATA = "/pgdata"
SOCKET = "/var/run/postgresql"


def initialize():
    subprocess.run(["initdb", "-D", DATA, "--auth-local=peer", "--auth-host=reject",
                    "--encoding=UTF8", "--locale=C", "--no-instructions"], check=True,
                   stdout=subprocess.DEVNULL)
    options = {
        "listen_addresses": "", "unix_socket_directories": SOCKET,
        "max_connections": "10", "shared_buffers": "32MB", "work_mem": "4MB",
        "temp_file_limit": "32MB", "max_parallel_workers_per_gather": "0",
        "max_worker_processes": "0", "jit": "off", "timezone": "UTC",
        "log_statement": "none", "log_min_error_statement": "panic",
        "statement_timeout": str(STATEMENT_MS), "lock_timeout": str(LOCK_MS),
        "idle_in_transaction_session_timeout": "2000", "transaction_timeout": "5000",
    }
    args = ["postgres", "-D", DATA]
    for name, value in options.items():
        args.extend(["-c", f"{name}={value}"])
    process = subprocess.Popen(args)
    return process


def seed():
    with psycopg.connect(host=SOCKET, user="postgres", dbname="postgres", autocommit=True) as conn:
        if conn.info.server_version // 10000 != 17:
            raise RuntimeError("The lesson_read profile requires PostgreSQL 17")
        conn.execute("CREATE DATABASE lab")
        conn.execute("REVOKE CONNECT, TEMPORARY ON DATABASE postgres, template1 FROM PUBLIC")
        conn.execute("REVOKE ALL ON DATABASE lab FROM PUBLIC")
        conn.execute("CREATE ROLE student LOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION NOBYPASSRLS")
        conn.execute("GRANT CONNECT ON DATABASE lab TO student")
    dataset = load_dataset()
    with psycopg.connect(host=SOCKET, user="postgres", dbname="lab", autocommit=True) as conn:
        conn.execute("REVOKE ALL ON SCHEMA public FROM PUBLIC")
        conn.execute("CREATE SCHEMA lab")
        conn.execute("SET search_path = lab, pg_catalog")
        conn.execute(dataset.schema, prepare=False)
        conn.execute(dataset.seed, prepare=False)
        conn.execute("GRANT USAGE ON SCHEMA lab TO student")
        conn.execute("GRANT SELECT ON ALL TABLES IN SCHEMA lab TO student")
        # Remove PUBLIC's ambient function and catalog access in this disposable
        # cluster. Only reviewed builtins and the Explorer's metadata are needed.
        conn.execute("REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA pg_catalog FROM PUBLIC")
        conn.execute("REVOKE SELECT ON ALL TABLES IN SCHEMA pg_catalog FROM PUBLIC")
        conn.execute("GRANT SELECT ON pg_catalog.pg_class, pg_catalog.pg_namespace, "
                     "pg_catalog.pg_attribute, pg_catalog.pg_constraint TO student")
        functions = conn.execute(
            "SELECT p.oid::regprocedure::text FROM pg_catalog.pg_proc p "
            "JOIN pg_catalog.pg_namespace n ON n.oid=p.pronamespace "
            "WHERE n.nspname='pg_catalog' AND p.proname = ANY(%s)",
            (list(FUNCTIONS | {"format_type"}),)).fetchall()
        for (signature,) in functions:
            # regprocedure is trusted catalog output, never student-controlled.
            conn.execute(sql.SQL("GRANT EXECUTE ON FUNCTION {} TO student").format(sql.SQL(signature)))
        # Coercions are permission-checked too: even LIMIT 2 needs int4 -> int8.
        # Grant only conversions between the reviewed builtin scalar types. This
        # does not add those function names to the student AST function allowlist.
        # name/oid/"char" are used only by the fixed Explorer queries; the AST
        # still forbids student catalog access and casts to these metadata types.
        scalar_types = list(TYPES | {"name", "oid", "char"})
        casts = conn.execute("""
            SELECT DISTINCT c.castfunc::regprocedure::text
            FROM pg_catalog.pg_cast c
            JOIN pg_catalog.pg_type source ON source.oid=c.castsource
            JOIN pg_catalog.pg_type target ON target.oid=c.casttarget
            WHERE c.castfunc<>0 AND source.typnamespace='pg_catalog'::regnamespace
              AND target.typnamespace='pg_catalog'::regnamespace
              AND source.typname=ANY(%s) AND target.typname=ANY(%s)
        """, (scalar_types, scalar_types)).fetchall()
        operators = conn.execute("""
            SELECT DISTINCT o.oprcode::regprocedure::text
            FROM pg_catalog.pg_operator o
            LEFT JOIN pg_catalog.pg_type l ON l.oid=o.oprleft
            LEFT JOIN pg_catalog.pg_type r ON r.oid=o.oprright
            WHERE o.oprnamespace='pg_catalog'::regnamespace AND o.oprcode<>0
              AND o.oprname=ANY(%s)
              AND (o.oprleft=0 OR (l.typnamespace='pg_catalog'::regnamespace AND l.typname=ANY(%s)))
              AND (o.oprright=0 OR (r.typnamespace='pg_catalog'::regnamespace AND r.typname=ANY(%s)))
        """, (list(OPERATORS), scalar_types, scalar_types)).fetchall()
        for (signature,) in casts + operators:
            conn.execute(sql.SQL("GRANT EXECUTE ON FUNCTION {} TO student").format(sql.SQL(signature)))
        conn.execute("ALTER ROLE student SET default_transaction_read_only = on")
        conn.execute("ALTER ROLE student SET search_path = lab, pg_catalog")
    Path(DATA, "ready").touch(mode=0o600)


def main():
    lifetime = min(int(os.environ.get("SQL_ABSOLUTE_SECONDS", "1800")), 1800)
    deadline = time.monotonic() + lifetime
    process = None

    def stop(*_):
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGALRM, stop)
    signal.alarm(max(1, lifetime))
    try:
        process = initialize()
        while time.monotonic() < deadline:
            if process.poll() is not None:
                raise RuntimeError("PostgreSQL exited during startup")
            try:
                with psycopg.connect(host=SOCKET, user="postgres", dbname="postgres", connect_timeout=1):
                    break
            except psycopg.OperationalError:
                time.sleep(0.05)
        else:
            raise RuntimeError("Provisioning expired")
        seed()
        while process.poll() is None and time.monotonic() < deadline:
            time.sleep(0.2)
    finally:
        if process and process.poll() is None:
            process.send_signal(signal.SIGINT)
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


if __name__ == "__main__":
    main()
