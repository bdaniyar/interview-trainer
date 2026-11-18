"""Trusted fixture seed and constrained index installation. No raw SQL parameter."""
from dataclasses import asdict
import json
import sys

import psycopg
from psycopg import sql

from sql_runner.app.bootstrap import SOCKET
from index_lab.policy import indexes
from index_lab.workloads import CASES, fixture


def copy_rows(db, table, rows):
    with db.cursor().copy(sql.SQL("COPY lab.{} FROM STDIN").format(sql.Identifier(table))) as stream:
        for row in rows:
            stream.write_row(row)


def install_one(db, index, number):
    keys = []
    for key in index.keys:
        field = sql.Identifier(key.field)
        expression = sql.SQL("pg_catalog.lower({})").format(field) if key.expression == "lower" else field
        keys.append(expression + (sql.SQL(" DESC") if key.descending else sql.SQL("")))
    suffix = sql.SQL("")
    if index.includes:
        suffix += sql.SQL(" INCLUDE ({})").format(sql.SQL(", ").join(map(sql.Identifier, index.includes)))
    if index.active_only:
        suffix += sql.SQL(" WHERE status='new'")
    db.execute(sql.SQL("CREATE INDEX {} ON lab.{} USING btree ({})").format(
        sql.Identifier(f"candidate_{number}"), sql.Identifier(index.table),
        sql.SQL(", ").join(keys)
    ) + suffix)


def main(payload):
    case = payload["case"]
    if type(case) is not int or not 0 <= case < len(CASES):
        raise ValueError("Invalid fixture")
    # Revalidate and reconstruct from field enums. No student SQL is sent as
    # PostgreSQL superuser or used in an identifier after this point.
    design = indexes(payload["design"]) if "design" in payload else ()
    with psycopg.connect(host=SOCKET, user="postgres", dbname="lab", autocommit=True,
        options="-c statement_timeout=3500 -c lock_timeout=1500 -c search_path=lab,pg_catalog") as db:
        people, orders = fixture(case)
        copy_rows(db, "users", people)
        copy_rows(db, "orders", orders)
        if payload["mode"] == "optimize":
            # Alternate the stored tie order on one fixture. The same SQL
            # must consistently order by id, even when the access path does not.
            tie_key = sql.SQL("id DESC") if case == 4 else sql.SQL("id")
            db.execute(sql.SQL("CREATE INDEX orders_day ON lab.orders(created_at,{})").format(tie_key))
        db.execute("VACUUM (ANALYZE) lab.users")
        db.execute("VACUUM (ANALYZE) lab.orders")
        for number, index in enumerate(design):
            install_one(db, index, number)
        if design:
            db.execute("ANALYZE lab.users")
            db.execute("ANALYZE lab.orders")
        # Inspect catalog definitions and confirm that each index became valid.
        with db.cursor() as cursor:
            definitions = cursor.execute("""SELECT c.relname, pg_get_indexdef(c.oid)
                FROM pg_index i JOIN pg_class c ON c.oid=i.indexrelid
                JOIN pg_namespace n ON c.relnamespace = n.oid
                WHERE n.nspname='lab' AND i.indisvalid AND c.relname LIKE 'candidate_%'
                ORDER BY c.relname""").fetchall()
    assert len(definitions) == len(design)
    return {"indexes": [asdict(index) for index in design], "definitions": definitions}


if __name__ == "__main__":
    print(json.dumps(main(json.loads(sys.argv[1])), ensure_ascii=False))
