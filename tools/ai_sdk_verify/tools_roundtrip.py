"""One Responses API continuation. Caller supplies the authorized executor and client."""
import json
from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from openai import AsyncOpenAI


def tool_definition(name, description, properties):
    return {
        "type": "function", "name": name, "description": description, "strict": True,
        "parameters": {"type": "object", "properties": properties,
                       "required": list(properties), "additionalProperties": False},
    }


def booking_tools():
    return [
        tool_definition("get_booking", "Read a booking owned by the caller", {"booking_id": {"type": "integer"}}),
        tool_definition("list_my_bookings", "List bookings owned by the caller", {}),
    ]


class ToolProtocolError(ValueError):
    pass


def reject_constant(value):
    raise ToolProtocolError("non-JSON constant")


@dataclass(frozen=True)
class Call:
    item_id: str
    call_id: str
    name: str
    arguments: dict


def extract_calls(items):
    calls = []
    seen_items, seen_calls = set(), set()
    for item in items:
        if item.type != "function_call":
            continue
        item_id, call_id, name, raw = (getattr(item, key, None)
                                       for key in ("id", "call_id", "name", "arguments"))
        if not all(isinstance(value, str) and value.strip() for value in (item_id, call_id, name)):
            raise ToolProtocolError("missing id or name")
        if call_id in seen_calls or item_id in seen_items:
            raise ToolProtocolError("duplicate id")
        try:
            arguments = json.loads(raw, parse_constant=reject_constant)
        except (TypeError, ValueError):
            raise ToolProtocolError("invalid JSON arguments") from None
        if not isinstance(arguments, dict):
            raise ToolProtocolError("expected argument object")
        seen_items.add(item_id)
        seen_calls.add(call_id)
        calls.append(Call(item_id, call_id, name, arguments))
    return calls


async def roundtrip(client: AsyncOpenAI, model: str, question: str,
                    execute: Callable[[Call], Awaitable[str]]):
    """Demonstrate a stateless exchange with no more than two provider requests."""
    original = [{"role": "user", "content": question}]
    tools = booking_tools()
    options = dict(model=model, tools=tools, store=False, max_output_tokens=256,
                   include=["reasoning.encrypted_content"])
    response = await client.responses.create(input=original, **options)
    if response.status != "completed":
        return response
    calls = extract_calls(response.output)
    if not calls:
        return response
    if len(calls) > 2 or any(call.name not in {tool["name"] for tool in tools} for call in calls):
        raise ToolProtocolError("tool outside this example's allowlist or budget")
    results = [
        {"type": "function_call_output", "call_id": call.call_id, "output": await execute(call)}
        for call in calls
    ]
    previous = [item.model_dump(mode="json", exclude_unset=True) for item in response.output]
    final = await client.responses.create(input=original + previous + results, **(options | {"tool_choice": "none"}))
    if extract_calls(final.output):
        raise ToolProtocolError("unexpected additional tool turn")
    return final
