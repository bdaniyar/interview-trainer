import asyncio
import json

import pytest

from contracts import BookingArgs, BookingView, Principal, Tool, ToolCall
from main import execute_tool


def run(read, arguments='{"booking_id":91}', name="lookup"):
    who = Principal("tenant-green", "guest-6")
    result = asyncio.run(execute_tool(ToolCall("in-18", name, arguments), who,
                                     {"lookup": Tool(BookingArgs, BookingView, read)}))
    assert result.call_id == "in-18"
    return result


def test_calls_real_function_and_returns_its_output():
    seen = []

    async def read(principal, args):
        seen.append((principal, args.booking_id))
        return {"city": "Костанай"}

    result = run(read)
    assert seen == [(Principal("tenant-green", "guest-6"), 91)]
    assert result.status == "ok" and json.loads(result.output) == {"city": "Костанай"}


@pytest.mark.parametrize("arguments", [
    '{"booking_id":"91"}', '{"booking_id":true}', '{"booking_id":0}',
    '{"booking_id":-7}', '{"booking_id":1,"tenant":"other"}', '{"booking_id":',
    '[]', '{"booking_id":1}' + ' ' * 512,
])
def test_bad_arguments_never_call_service(arguments):
    calls = []

    async def read(*args):
        calls.append(args)
        return {"city": "sentinel"}

    result = run(read, arguments)
    assert result.status == "invalid_arguments" and result.output is None
    assert calls == []


def test_unknown_tool_never_calls_service():
    async def read(*args):
        pytest.fail("unknown tool invoked the service")
    assert run(read, name="unknown").status == "unknown_tool"


@pytest.mark.parametrize(("data", "status"), [
    (None, "not_found"), ({"city": "city", "secret": "CANARY"}, "tool_error"),
    ({"city": 18}, "tool_error"), ({"city": "Я" * 300}, "output_limit"),
])
def test_safe_output(data, status):
    async def read(*args):
        return data

    result = run(read)
    assert result.status == status and result.output is None


def test_exception_redacted():
    async def read(*args):
        raise RuntimeError("internal SECRET-2026")
    assert run(read).status == "tool_error" and run(read).output is None


def test_cancellation_propagates_and_cleans_up():
    async def scenario():
        entered = asyncio.Event()
        stopped = asyncio.Event()

        async def read(*args):
            entered.set()
            try:
                await asyncio.Event().wait()
            finally:
                stopped.set()

        pending = asyncio.create_task(execute_tool(ToolCall("id", "lookup", '{"booking_id":13}'),
                            Principal("org", "user"), {"lookup": Tool(BookingArgs, BookingView, read)}))
        async with asyncio.timeout(0.3):
            await entered.wait()
            pending.cancel()
            with pytest.raises(asyncio.CancelledError):
                await pending
        assert stopped.is_set()

    asyncio.run(scenario())
