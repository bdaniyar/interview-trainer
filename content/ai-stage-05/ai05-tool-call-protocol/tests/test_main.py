from copy import deepcopy

import pytest

from contracts import ToolCall, ToolResult
from main import continuation, read_calls


def call(item_id="item-11", call_id="request-8", name="inspect", arguments='{"ref":87}'):
    return dict(type="function_call", id=item_id, call_id=call_id, name=name, arguments=arguments)


def test_reverse_results_and_output_preserved():
    left, right = call(), call("item-5", "request-2", "list", "{}")
    output = [{"type": "reasoning", "id": "rs", "encrypted_content": "opaque"},
              left, {"type": "message", "id": "m"}, right]
    original = deepcopy(output)
    allowed = {"inspect", "list"}
    assert read_calls(output, allowed) == [
        ToolCall("item-11", "request-8", "inspect", {"ref": 87}),
        ToolCall("item-5", "request-2", "list", {}),
    ]
    next_input = continuation(output, [ToolResult("request-2", "second"), ToolResult("request-8", "first")], allowed)
    assert next_input == original + [
        {"type": "function_call_output", "call_id": "request-8", "output": "first"},
        {"type": "function_call_output", "call_id": "request-2", "output": "second"},
    ]
    next_input[0]["id"] = "changed"
    assert output == original


@pytest.mark.parametrize("key", ["id", "call_id", "name", "arguments"])
def test_missing_fields(key):
    item = call()
    del item[key]
    with pytest.raises(ValueError):
        read_calls([item], {"inspect"})


@pytest.mark.parametrize("patch", [
    {"call_id": "request-8"}, {"id": "item-11"}, {"name": "other"},
    {"arguments": '{"ref":'}, {"arguments": '[{"ref":42}]'}, {"arguments": {"ref": 42}},
    {"arguments": '{"ref":NaN}'}, {"call_id": " "},
])
def test_malformed_and_duplicate_calls(patch):
    with pytest.raises(ValueError):
        read_calls([call(), call("other-item", "other-call") | patch], {"inspect"})


@pytest.mark.parametrize("results", [[], [ToolResult("item-11", "wrong id")],
    [ToolResult("request-8", "a"), ToolResult("request-8", "b")], [ToolResult("request-8", 1)]])
def test_result_sets_must_match(results):
    with pytest.raises(ValueError):
        continuation([call()], results, {"inspect"})


def test_final_item_without_calls_can_be_preserved():
    final = [{"type": "message", "id": "final"}]
    assert read_calls(final, set()) == []
    assert continuation(final, [], set()) == final
