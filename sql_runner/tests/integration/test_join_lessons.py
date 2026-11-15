from collections import Counter
from pathlib import Path
import re

import pytest


def example(names, types, rows, *, ordered=True):
    return names.split(), types.split(), rows, ordered


USERS_ORDERS = [["1", "10"], ["1", "11"], ["2", "12"], ["2", "13"], ["3", None], ["4", "14"]]
FULL_ROWS = [["1", "local-only", None, None], ["2", "local-match", "2", "remote-match"], [None, None, "3", "remote-only"]]
EXPECTED = {
    "s10-inner-join": [
        example("id name", "int8 text", [["100", "Python Book"], ["101", "Keyboard"], ["102", "SQL Book"]]),
        example("order_id product_id quantity", "int8 int8 int4", [["10", "100", "2"], ["10", "101", "1"], ["12", "101", "2"], ["13", "102", "1"], ["14", "100", "1"]]),
        example("order_id name quantity", "int8 text int4", [["10", "Python Book", "2"], ["10", "Keyboard", "1"], ["12", "Keyboard", "2"], ["13", "SQL Book", "1"], ["14", "Python Book", "1"]]),
        example("name", "text", [["Python Book"], ["Keyboard"], ["Keyboard"], ["SQL Book"], ["Python Book"]]),
        example("name", "text", [["Keyboard"], ["Python Book"], ["SQL Book"]]),
        example("pairs", "int8", [["15"]]),
        example("order_id name quantity", "int8 text int4", []), "42702",
        example("joined_rows orders_with_items", "int8 int8", [["5", "4"]]),
        example("order_id email", "int8 text", [["10", "a@example.com"], ["11", "a@example.com"], ["12", "b@example.com"], ["13", "b@example.com"], ["14", "d@example.com"]], ordered=False),
        example("order_id name quantity", "int8 text int4", [["10", "Python Book", "2"], ["10", "Keyboard", "1"], ["12", "Keyboard", "2"], ["13", "SQL Book", "1"]]),
        example("name units", "text int8", [["Python Book", "3"], ["Keyboard", "3"], ["SQL Book", "1"]]),
    ],
    "s10-left-join": [
        example("user_id order_id", "int8 int8", USERS_ORDERS),
        example("user_id order_id", "int8 int8", [["1", "10"], ["2", "12"], ["2", "13"], ["3", None], ["4", None]]),
        example("user_id order_id", "int8 int8", [["1", "10"], ["2", "12"], ["2", "13"]]),
        example("user_id order_id", "int8 int8", [["1", "10"], ["2", "12"], ["2", "13"], ["3", None]]),
        example("id name", "int8 text", []), example("id name", "int8 text", []),
        example("id joined_rows orders_count", "int8 int8 int8", [["1", "2", "2"], ["2", "2", "2"], ["3", "1", "0"], ["4", "1", "1"]]),
        example("user_id order_id", "int8 int8", [["3", None]]),
        example("id email", "int8 text", [["3", "c@example.com"]], ordered=False),
        example("id email", "int8 text", [["3", "c@example.com"]], ordered=False),
        example("user_id paid_orders_count", "int8 int8", [["1", "1"], ["2", "2"], ["3", "0"], ["4", "0"]]),
    ],
    "s10-right-and-full-outer-join": [
        example("user_id order_id", "int8 int8", USERS_ORDERS),
        example("user_id order_id", "int8 int8", USERS_ORDERS),
        example("left_id left_label right_id right_label", "int4 text int4 text", FULL_ROWS),
        example("id local_label remote_label", "int4 text text", [["1", "local-only", None], ["2", "local-match", "remote-match"], ["3", None, "remote-only"]]),
        example("sql_null text_null zero", "text text int8", [[None, "NULL", "0"]]),
        example("user_id order_id", "int8 int8", USERS_ORDERS), example("id", "int8", []),
        example("id local_label remote_label", "int4 text text", [["1", "local-only", None], ["3", None, "remote-only"]]),
        example("product_id order_id", "int8 int8", [["100", "10"], ["100", "14"], ["101", "10"], ["101", "12"], ["102", "13"]]),
        example("id local_label remote_label", "int4 text text", [["2", "local-match", "remote-match"]]),
        example("product_id positions_count", "int8 int8", [["100", "2"], ["101", "2"], ["102", "1"]]),
    ],
    "s10-self-join": [
        example("id email manager_id", "int8 text int8", [["1", "a@example.com", None], ["2", "b@example.com", "1"], ["3", "c@example.com", "1"], ["4", "d@example.com", "2"]]),
        example("employee_id manager_id matched_manager_id", "int8 int8 int8", [["1", None, None], ["2", "1", "1"], ["3", "1", "1"], ["4", "2", "2"]]),
        example("employee_id manager_id", "int8 int8", [["2", "1"], ["3", "1"], ["4", "2"]]),
        example("manager_id worker_id", "int8 int8", [["1", "2"], ["1", "3"], ["2", "4"], ["3", None], ["4", None]]),
        "42702",
        example("manager_id direct_reports", "int8 int8", [["1", "2"], ["2", "1"], ["3", "0"], ["4", "0"]]),
        example("email manager_email", "text text", [["a@example.com", None], ["b@example.com", "a@example.com"], ["c@example.com", "a@example.com"], ["d@example.com", "b@example.com"]]),
        example("id email", "int8 text", [["1", "a@example.com"]]),
        example("id email", "int8 text", [["2", "b@example.com"], ["3", "c@example.com"]]),
    ],
}


@pytest.mark.parametrize("slug,goldens", EXPECTED.items())
def test_every_join_lesson_sql_block_has_independent_typed_expected_values(manager, session, slug, goldens):
    path = Path(__file__).resolve().parents[3] / "content" / "stage-10" / slug / "lesson.md"
    source = path.read_text()
    blocks = list(re.finditer(r"```sql\n(.*?)```", source, re.S))
    assert len(blocks) == len(goldens)
    for block, golden in zip(blocks, goldens):
        actual = manager.run(session["session_id"], 1, block[1])
        if isinstance(golden, str):
            context = source[max(0, block.start() - 400):block.start()]
            assert "Намеренно ошибочный" in context and golden in context
            assert actual["error"]["sqlstate"] == golden
            continue
        columns, types, rows, ordered = golden
        assert actual["error"] is None and not actual["truncated"], (slug, block[1], actual)
        assert [c["name"] for c in actual["columns"]] == columns, block[1]
        assert [c["pg_type"] for c in actual["columns"]] == types, block[1]
        if ordered:
            assert actual["rows"] == rows, (slug, block[1], actual["rows"], rows)
        else:
            assert Counter(map(tuple, actual["rows"])) == Counter(map(tuple, rows)), (slug, block[1])
    assert len(manager.backend.containers()) == 1  # Only this public Explorer session.
