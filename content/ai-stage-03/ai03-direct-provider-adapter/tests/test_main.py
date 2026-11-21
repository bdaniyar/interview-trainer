import asyncio

import pytest

from contracts import GenerationResult, Object, Scripted, WireError
from main import generate


def message(*parts):
    return Object(type="message", content=parts)


def text(value):
    return Object(type="output_text", text=value)


def scenario(status, output, usage=None):
    client = Scripted(Object(status=status, output=output, usage=usage))
    result = asyncio.run(generate(client, "Проверка 🚪"))
    assert client.calls == [{"model": "fixture-model", "input": "Проверка 🚪"}]
    return result


def test_multiple_items_and_text_order():
    assert scenario("completed", [Object(type="reasoning"), message(text("a"), text("β")), message(text("🚪"))],
                    Object(input_tokens=4, output_tokens=0)) == GenerationResult("completed", "aβ🚪", (4, 0))


@pytest.mark.parametrize("usage", [None, Object(input_tokens=3), Object(input_tokens=None, output_tokens=1)])
def test_optional_usage(usage):
    assert scenario("completed", [message(text("ок"))], usage) == GenerationResult("completed", "ок")


@pytest.mark.parametrize(("status", "output", "expected"), [
    ("completed", [], "empty"), ("completed", [message(text("  "))], "empty"),
    ("completed", [message(text("partial"), Object(type="refusal", refusal="private"))], "refusal"),
    ("incomplete", [message(text("partial"))], "incomplete"),
    ("failed", [message(text("must not send"))], "unavailable"),
])
def test_outcome_and_partial_text(status, output, expected):
    result = scenario(status, output, Object(input_tokens=1, output_tokens=2))
    assert result == GenerationResult(expected, usage=(1, 2))


def test_wire_error_is_redacted_and_not_retried():
    spy = Scripted(WireError("internal secret"))
    assert asyncio.run(generate(spy, "x")) == GenerationResult("unavailable")
    assert len(spy.calls) == 1


def test_unexpected_error_is_propagated():
    error = RuntimeError("unexpected")
    client = Scripted(error)
    with pytest.raises(RuntimeError) as failure:
        asyncio.run(generate(client, "x"))
    assert failure.value is error and len(client.calls) == 1
