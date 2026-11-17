"""Controller-owned synthetic cases. Never accepted as SQL/path/image from a request."""

import json
import sys
import psycopg
from sql_runner.app.bootstrap import SOCKET

DML_CASES = ("public", "already-paid", "absent", "empty", "bigint", "many")
BOOK_CASES = (
    "public",
    "sold-out",
    "other-rooms",
    "single-room",
    "missing-room",
    "existing",
)


def install(kind, case):
    assert kind in {"dml", "booking"} and case in (
        DML_CASES if kind == "dml" else BOOK_CASES
    )
    with psycopg.connect(
        host=SOCKET, user="postgres", dbname="lab", autocommit=True
    ) as conn:
        conn.execute("SET search_path=lab,pg_catalog")
        if kind == "dml":
            conn.execute("TRUNCATE order_items,orders")
            rows = {
                "public": [(10, 1, "new", "10.00"), (11, 2, "cancelled", "99.00")],
                "already-paid": [(10, 1, "paid", "15.00"), (50, 4, "queued", "7.00")],
                "absent": [(9007199254740993, 2, "new", "10.00")],
                "empty": [],
                "bigint": [
                    (10, 4, "cancelled", "9999999999.99"),
                    (9007199254740993, 3, "paid", "0.00"),
                ],
                "many": [
                    (10, 1, "new", "1.00"),
                    (0, 1, "new", "1.00"),
                    (90, 2, "new", "2.00"),
                    (5, 4, "new", "3.00"),
                ],
            }[case]
            for i, u, status, total in rows:
                conn.execute(
                    "INSERT INTO orders VALUES (%s,%s,%s,%s,'2026-01-01')",
                    (i, u, status, total),
                )
        else:
            conn.execute("TRUNCATE reservations,inventory")
            rows = {
                "public": [(1, 1), (2, 1)],
                "sold-out": [(1, 0), (2, 1)],
                "other-rooms": [(1, 1), (9007199254740993, 9)],
                "single-room": [(1, 1)],
                "missing-room": [(2, 1)],
                "existing": [(1, 0), (2, 1)],
            }[case]
            for row in rows:
                conn.execute("INSERT INTO inventory VALUES(%s,%s)", row)
            if case == "existing":
                conn.execute("INSERT INTO reservations VALUES ('existing',1,true)")
    return {"ready": True}


if __name__ == "__main__":
    print(json.dumps(install(*sys.argv[1:3])))
