import json
import os
from pathlib import Path
import re
import pytest
from transaction_lab.control import attempt, outputs, DML_REFERENCE, BOOKING_REFERENCE

pytestmark = pytest.mark.skipif(
    os.getenv("SQL_DOCKER_TESTS") != "1", reason="Real disposable PostgreSQL required"
)
# Independent expected names, PG types and rows for the reviewed examples.
EXPECTED = json.loads(Path(__file__).with_name('lesson_expected.json').read_text())


@pytest.mark.parametrize("slug,golden", EXPECTED.items())
def test_every_transaction_lesson_sql_block_has_typed_expected_output(slug, golden):
    # Read the actual committed curated lesson.
    root = Path(__file__).resolve().parents[3] / 'content'
    path = next(root.glob("*/" + slug + "/lesson.md"))
    source = path.read_text()
    blocks = re.findall(r"```sql\n(.*?)```", source, re.S)
    assert len(blocks) == (
        2 if slug in {"s10-data-modification", "s11-booking-concurrency"} else 1
    )
    for i, block in enumerate(blocks):
        if i == 0:
            assert block.strip() == golden["query"]
        else:
            assert block.strip() == (
                DML_REFERENCE if slug == "s10-data-modification" else BOOKING_REFERENCE
            )
        with attempt() as (backend, handle):
            backend.install_case(handle, "dml", "public")
            result = backend.execute(handle, "script", {"sql": block})
            assert not result.get("error"), result
            if golden["error"]:
                assert any(
                    e.get("sqlstate") == golden["error"] for e in result["timeline"]
                )
                assert result["before"] == result["after"]
            else:
                actual = outputs(result["timeline"])[-1]
                names, types, rows = golden["names"], golden["types"], golden["rows"]
                if i:
                    names, types, rows = (
                        (["id", "status"], ["int8", "text"], [["10", "paid"]])
                        if slug == "s10-data-modification"
                        else (
                            ["request_key", "room_id"],
                            ["text", "int8"],
                            [["REQUEST_KEY", "1"]],
                        )
                    )
                assert [c["name"] for c in actual["columns"]] == names
                assert [c["pg_type"] for c in actual["columns"]] == types
                assert actual["rows"] == rows
