from contracts import Context, Message
from fixtures import demo


def validate_unit(unit):
    if not unit:
        raise ValueError("empty exchange")
    first, *rest = unit
    if len(unit) == 1 and first.role in {"user", "assistant"} and not first.call_ids and first.call_id is None:
        return
    if first.role != "assistant" or first.call_id is not None or not first.call_ids:
        raise ValueError("exchange must start with tool calls")
    if any(message.role != "tool" or message.call_ids or not message.call_id for message in rest):
        raise ValueError("invalid tool result")
    ids = set(first.call_ids)
    if "" in ids or len(ids) != len(first.call_ids) or len(ids) != len(rest):
        raise ValueError("unexpected number of results")
    if ids != {message.call_id for message in rest}:
        raise ValueError("results must match calls")


def build_context(history, conversation_id, principal, policy, current, *, capacity, reserve, count) -> Context:
    conversation = history.get(conversation_id)
    if conversation is None or conversation.owner != principal:
        raise PermissionError("conversation unavailable")
    if capacity < 0 or reserve < 0:
        raise ValueError("invalid budget")
    for unit in conversation.units:
        validate_unit(unit)

    first, last = Message("system", policy), Message("user", current)
    total = count(first) + count(last)
    if total + reserve > capacity:
        raise ValueError("mandatory context exceeds budget")
    recent = []
    for unit in reversed(conversation.units):
        size = sum(count(message) for message in unit)
        if total + size + reserve > capacity:
            break
        total += size
        recent.append(unit)
    messages = (first,) + tuple(message for unit in reversed(recent) for message in unit) + (last,)
    return Context(messages, total, reserve)


if __name__ == "__main__":
    demo(build_context)
