"""Verify the reviewed Stage 11 SQL examples on a disposable PostgreSQL 17 instance."""
import json
from pathlib import Path
import re

from transaction_lab.control import attempt
from sql_runner.app.config import PYTHON

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = {
    "s11-primary-and-foreign-keys": [(["int4", "int4", "int4"], [[20, 2, 42]])],
    "s11-normalization": [(["int4", "text", "text", "int4"], [
        [40, "Чёрный чай", "Алматы", 2], [41, "Чёрный чай", "Астана", 1]
    ])],
    "s11-index-mental-model": ["plan", "plan", (["int4"], [[19907], [19807], [19707]])],
    "s11-postgresql-b-tree": ["plan", (["int4", "date", "int4"], [
        [2, "2026-11-08", 105], [3, "2026-11-08", 203]
    ])],
    "s11-selectivity": ["analysis", "analysis", (["text", "int8"], [["archived", 9990], ["new", 10]])],
    "s11-pagination": [(["int8"], [[13], [12]]), (["int8"], [[12], [11]]), (["int8"], [[11], [10]])],
    "s11-jsonb": [
        (["int4", "text", "bool"], [[1, "2", True]]), (["int4", "int4"], [[1, 3]]),
        (["int4", "bool", "text"], [[1, False, "null"], [2, True, None]]),
    ],
}

# This is a developer verification of checked-in DDL from reviewed notes.
# The application never forwards student input to this command.
VERIFY = r"""
import json
import sys
import psycopg
from psycopg import ClientCursor, sql

with psycopg.connect(host="/var/run/postgresql", user="postgres", dbname="lab",
        options="-c statement_timeout=3000 -c lock_timeout=1500 -c timezone=UTC",
        autocommit=True, cursor_factory=ClientCursor) as connection:
    answers = {}
    for i, (slug, source) in enumerate(json.loads(sys.argv[1]).items()):
        schema = sql.Identifier("reviewed_" + str(i))
        connection.execute(sql.SQL("CREATE SCHEMA {}").format(schema))
        connection.execute(sql.SQL("SET search_path = {}, pg_catalog").format(schema))
        with connection.cursor() as cursor:
            cursor.execute(source)
            output = []
            while True:
                if cursor.description:
                    types = [connection.adapters.types.get(col.type_code).name
                             for col in cursor.description]
                    output.append(dict(types=types, rows=cursor.fetchall()))
                if not cursor.nextset():
                    break
        answers[slug] = output
    connection.execute("SET search_path = reviewed_0, pg_catalog")
    try:
        connection.execute("INSERT INTO shipments VALUES (30, 1, 42)")
    except psycopg.errors.ForeignKeyViolation as exc:
        assert exc.sqlstate == "23503"
    else:
        raise AssertionError("Orphan shipment was accepted")
print(json.dumps(answers, ensure_ascii=False, default=str))
"""


def main():
    sources = {}
    for slug in EXAMPLES:
        path = ROOT / "content/stage-11" / slug / "lesson.md"
        blocks = re.findall(r"```sql\n(.*?)```", path.read_text(), re.S)
        assert len(blocks) == 1, (slug, len(blocks))
        sources[slug] = blocks[0]
    with attempt() as (backend, handle):
        result = backend.client.containers.get(handle).exec_run(
            [PYTHON, "-c", VERIFY, json.dumps(sources, ensure_ascii=False)],
            user="postgres", demux=True,
        )
        stdout, stderr = result.output
        assert result.exit_code == 0, stderr.decode() if stderr else result
        actual = json.loads(stdout)
    checked = 0
    for slug, expected in EXAMPLES.items():
        assert len(actual[slug]) == len(expected), (slug, actual[slug])
        for result, wanted in zip(actual[slug], expected, strict=True):
            if wanted in ("plan", "analysis"):
                assert result["types"] == ["text"] and result["rows"], slug
                text = "\n".join(row[0] for row in result["rows"])
                assert "cost=" in text
                if wanted == "analysis":
                    assert "actual rows=" in text or "(actual rows=" in text
                    assert "Buffers:" in text
            else:
                types, rows = wanted
                assert result == {"types": types, "rows": rows}, (slug, result, wanted)
            checked += 1
        print(slug + ": verified")
    print(f"{len(EXAMPLES)} PostgreSQL lesson blocks, {checked} result sets and the real FK error verified.")


if __name__ == "__main__":
    main()
