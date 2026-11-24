from copy import deepcopy
import json

from contracts import ToolCall, ToolResult
from fixtures import demo


def reject_constant(value):
    raise ValueError("non-JSON constant")


def read_calls(output: list[dict], allowed: set[str]) -> list[ToolCall]:
    calls = []
    call_ids = set()
    item_ids = set()
    for item in output:
        if item.get("type") != "function_call":
            continue
        item_id, call_id, name = (item.get(key) for key in ("id", "call_id", "name"))
        if not all(isinstance(value, str) and value.strip() for value in (item_id, call_id, name)):
            raise ValueError("missing function call fields")
        if call_id in call_ids or item_id in item_ids or name not in allowed:
            raise ValueError("duplicate id or unknown tool")
        raw = item.get("arguments")
        if not isinstance(raw, str):
            raise ValueError("arguments must be a JSON string")
        arguments = json.loads(raw, parse_constant=reject_constant)
        if not isinstance(arguments, dict):
            raise ValueError("arguments must be an object")
        calls.append(ToolCall(item_id, call_id, name, arguments))
        call_ids.add(call_id)
        item_ids.add(item_id)
    return calls


def continuation(output: list[dict], results: list[ToolResult], allowed: set[str]) -> list[dict]:
    calls = read_calls(output, allowed)
    by_id = {}
    for result in results:
        if result.call_id in by_id or not isinstance(result.output, str):
            raise ValueError("duplicate result or invalid output")
        by_id[result.call_id] = result.output
    if set(by_id) != {call.call_id for call in calls}:
        raise ValueError("results must match calls")
    return deepcopy(output) + [
        {"type": "function_call_output", "call_id": call.call_id, "output": by_id[call.call_id]}
        for call in calls
    ]


if __name__ == "__main__":
    demo(read_calls, continuation)
