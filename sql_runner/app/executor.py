"""Fixed in-container command. Untrusted SQL reaches only psycopg's protocol.

The control plane invokes this module as OS user student; peer authentication
cannot be used to connect as the bootstrap PostgreSQL superuser.
"""
from datetime import date, datetime, time, timedelta, timezone
from decimal import Decimal
import json
import sys
from time import monotonic
from uuid import UUID

import psycopg
from psycopg import sql as sql_compose

from .config import CELL_BYTES, LOCK_MS, RESULT_BYTES, ROW_LIMIT, STATEMENT_MS
from .datasets import PRIMARY_KEYS, TABLES
from .policy import PolicyError, TYPES, validate


class OutputError(ValueError):
    pass


def encode(value):
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, datetime):
        if value.tzinfo:
            return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        return value.isoformat()
    if isinstance(value, (date, time)):
        return value.isoformat()
    if isinstance(value, (int, Decimal, float, str, UUID, timedelta)):
        result = str(value)
        if len(result.encode("utf-8")) > CELL_BYTES:
            raise OutputError("A result cell exceeds 64 KiB")
        return result
    raise OutputError("Result contains an unsupported scalar type")


def json_bytes(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode()


def empty_result(error=None):
    return dict(command="SELECT", columns=[], rows=[], rows_returned=0,
                has_more=False, truncated=False, duration_ms=0, error=error)


def error_result(kind, code, message, **fields):
    return empty_result(dict(kind=kind, code=code, message=message[:2048], **fields))


def collect(cursor, connection, row_limit=ROW_LIMIT):
    columns = []
    if len(cursor.description) > 128:
        raise OutputError("At most 128 result columns are supported")
    for col in cursor.description:
        info = connection.adapters.types.get(col.type_code)
        if info is None or info.name not in TYPES:
            raise OutputError("Result contains an unsupported PostgreSQL type")
        columns.append(dict(name=col.name, pg_type=info.name,
                            type_oid=col.type_code))
    result = empty_result()
    result["columns"] = columns
    # Reserve envelope space for duration, generation, session ID and flags.
    used = len(json_bytes(result)) + 1024
    for index in range(row_limit + 1):
        row = cursor.fetchone()  # ServerCursor: one row on the wire, not full result.
        if row is None:
            break
        if index == row_limit:
            result["has_more"] = result["truncated"] = True
            break
        converted = [encode(v) for v in row]
        size = len(json_bytes(converted)) + 1
        if used + size > RESULT_BYTES:
            result["has_more"] = result["truncated"] = True
            break
        used += size
        result["rows"].append(converted)
    result["rows_returned"] = len(result["rows"])
    return result


def connect():
    return psycopg.connect(
        host="/var/run/postgresql", dbname="lab", user="student", connect_timeout=2,
        options="-c search_path=lab,pg_catalog -c default_transaction_read_only=on "
                f"-c statement_timeout={STATEMENT_MS} -c lock_timeout={LOCK_MS} "
                "-c idle_in_transaction_session_timeout=2000 -c transaction_timeout=5000 "
                "-c timezone=UTC",
    )


CATALOG_COLUMNS = """
SELECT c.relname, a.attnum, a.attname,
       pg_catalog.format_type(a.atttypid, a.atttypmod), NOT a.attnotnull
FROM pg_catalog.pg_class c
JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
JOIN pg_catalog.pg_attribute a ON a.attrelid = c.oid
WHERE n.nspname = 'lab' AND c.relname = ANY(%s)
  AND a.attnum > 0 AND NOT a.attisdropped
ORDER BY c.relname, a.attnum
"""
CATALOG_KEYS = """
SELECT c.relname, k.conname, k.contype, k.conkey,
       r.relname, k.confkey, k.confupdtype, k.confdeltype
FROM pg_catalog.pg_constraint k
JOIN pg_catalog.pg_class c ON c.oid = k.conrelid
JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
LEFT JOIN pg_catalog.pg_class r ON r.oid = k.confrelid
WHERE n.nspname = 'lab' AND c.relname = ANY(%s) AND k.contype IN ('p', 'f')
ORDER BY c.relname, k.conname
"""


def catalog(connection):
    tables = {name: dict(name=name, columns=[], primary_key=[], foreign_keys=[])
              for name in TABLES}
    attnames = {}
    with connection.cursor() as cur:
        # Trusted, fixed queries over four immutable tables. These metadata
        # results are bounded independently of arbitrary student SELECT output.
        cur.execute(CATALOG_COLUMNS, (list(TABLES),))
        for table, num, name, pg_type, nullable in cur:
            attnames[table, num] = name
            tables[table]["columns"].append(dict(name=name, pg_type=pg_type, nullable=nullable))
        cur.execute(CATALOG_KEYS, (list(TABLES),))
        actions = {"a": "NO ACTION", "r": "RESTRICT", "c": "CASCADE", "n": "SET NULL", "d": "SET DEFAULT"}
        for table, name, kind, local, ref, remote, update, delete in cur:
            columns = [attnames[table, number] for number in local]
            if kind == "p":
                tables[table]["primary_key"] = columns
            elif ref in TABLES:
                tables[table]["foreign_keys"].append(dict(
                    name=name, columns=columns, referenced_table=ref,
                    referenced_columns=[attnames[ref, number] for number in remote],
                    on_update=actions[update], on_delete=actions[delete]))
    return {"tables": list(tables.values())}


def execute(operation, payload):
    started = monotonic()
    position_offset = 0
    try:
        if operation == "run":
            query = payload["sql"]
            validate(query)  # Recheck inside the boundary as well as at admission.
            limit = ROW_LIMIT
            params = None
        elif operation == "browse":
            table, limit, offset = payload["table"], payload["limit"], payload["offset"]
            if table not in TABLES or not 1 <= limit <= 100 or not 0 <= offset <= 10000:
                raise ValueError("Invalid trusted browse arguments")
            query = sql_compose.SQL("SELECT * FROM {}.{} ORDER BY {} LIMIT %s OFFSET %s").format(
                sql_compose.Identifier("lab"), sql_compose.Identifier(table),
                sql_compose.SQL(", ").join(map(sql_compose.Identifier, PRIMARY_KEYS[table])))
            params = (limit + 1, offset)
        elif operation != "catalog":
            raise ValueError("Unknown executor operation")
        with connect() as connection:
            connection.read_only = True
            if operation == "catalog":
                return catalog(connection)
            with connection.cursor(name="bounded_result") as cursor:
                # psycopg prefixes DECLARE around the original query. PostgreSQL
                # reports positions in that statement; expose editor positions.
                position_offset = len('DECLARE "bounded_result" CURSOR FOR ')
                cursor.execute(query, params)
                result = collect(cursor, connection, limit)
    except PolicyError as exc:
        result = error_result("policy", exc.code, str(exc), position=exc.position, sqlstate=exc.sqlstate)
    except psycopg.Error as exc:
        diag = exc.diag
        result = error_result("postgres", "query_error", diag.message_primary or "PostgreSQL error",
                              sqlstate=exc.sqlstate,
                              position=max(1, int(diag.statement_position) - position_offset) if diag.statement_position else None,
                              hint=diag.message_hint[:512] if diag.message_hint else None)
    except OutputError as exc:
        result = error_result("resource", "output_limit", str(exc))
    result["duration_ms"] = round((monotonic() - started) * 1000)
    return result


if __name__ == "__main__":
    try:
        output = execute(sys.argv[1], json.loads(sys.argv[2]))
        wire = json_bytes(output)
        if len(wire) > RESULT_BYTES:
            raise OutputError("Result envelope exceeds limit")
    except Exception:
        # No traceback, connection string, query or filesystem paths on the wire.
        wire = json_bytes(error_result("infrastructure", "executor_failure", "SQL executor failed"))
    sys.stdout.buffer.write(wire)
