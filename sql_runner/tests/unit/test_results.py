from datetime import date, datetime, time, timezone
from decimal import Decimal
from types import SimpleNamespace

import pytest

from sql_runner.app.config import RESULT_BYTES
from sql_runner.app.executor import OutputError, collect, encode, json_bytes


def test_lossless_cells_and_nulls():
    values = [None, "", "NULL", False, 0, 9007199254740993,
              Decimal("12345678901234567890.012300"), date(2026, 1, 1),
              time(12, 30), datetime(2026, 1, 1, tzinfo=timezone.utc)]
    assert [encode(x) for x in values] == [None, "", "NULL", False, "0", "9007199254740993",
        "12345678901234567890.012300", "2026-01-01", "12:30:00", "2026-01-01T00:00:00Z"]


def test_cell_budget_counts_utf8_and_rejects_unsupported_types():
    for value in ["я" * 32769, [1], {"x": 1}, b"bytes"]:
        with pytest.raises(OutputError):
            encode(value)


class Cursor:
    description = [SimpleNamespace(name="x", type_code=25), SimpleNamespace(name="x", type_code=25)]

    def __init__(self, rows):
        self.rows = iter(rows)
        self.reads = 0

    def fetchone(self):
        self.reads += 1
        return next(self.rows, None)


CONNECTION = SimpleNamespace(adapters=SimpleNamespace(types={25: SimpleNamespace(name="text")}))


def test_server_cursor_stops_at_one_lookahead_and_preserves_aliases():
    cur = Cursor(([i, i] for i in range(1000000)))
    result = collect(cur, CONNECTION)
    assert cur.reads == 501
    assert result["rows_returned"] == 500 and result["has_more"] and result["truncated"]
    assert [c["name"] for c in result["columns"]] == ["x", "x"]


def test_byte_budget_is_applied_before_appending_row():
    cur = Cursor((["x" * 60000, "я" * 20000] for _ in range(1000)))
    result = collect(cur, CONNECTION)
    assert 0 < result["rows_returned"] < 500
    assert result["has_more"]
    assert len(json_bytes(result)) < RESULT_BYTES


def test_empty_result_retains_column_metadata():
    result = collect(Cursor([]), CONNECTION)
    assert result["rows"] == [] and len(result["columns"]) == 2 and not result["has_more"]


def test_unregistered_composite_types_and_column_explosion_are_rejected():
    cur = Cursor([])
    cur.description = [SimpleNamespace(name="row", type_code=123456)]
    with pytest.raises(OutputError, match="unsupported PostgreSQL type"):
        collect(cur, CONNECTION)
    cur.description = [SimpleNamespace(name="x", type_code=25)] * 129
    with pytest.raises(OutputError, match="128"):
        collect(cur, CONNECTION)
