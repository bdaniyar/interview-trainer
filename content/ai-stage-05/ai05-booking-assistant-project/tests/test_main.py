import asyncio

import pytest

from contracts import Booking, Call, Observation, Principal, Reply, Trace
from fixtures import DemoRepository
from main import run_assistant


class Provider:
    def __init__(self, *replies):
        self.replies = list(replies)
        self.seen = []

    async def reply(self, prompt, observations):
        self.seen.append((prompt, observations))
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        if callable(reply):
            return reply(observations)
        return reply


OWNER = Principal("east", "mila")


def repo():
    repository = DemoRepository()
    repository.owners = {13: OWNER, 81: OWNER, 7: Principal("east", "alex"), 22: Principal("west", "mila")}
    repository.rows = {number: Booking(number, status, "REDACT_THIS_NOTE")
                       for number, status in ((13, "pending"), (81, "confirmed"), (7, "confirmed"), (22, "pending"))}
    return repository


def tool(number, id="provider-key"):
    return Call(id, "get_booking", {"booking_id": number})


def run(provider, repository, owner=OWNER):
    return asyncio.run(run_assistant("private prompt", owner, provider, repository))


@pytest.mark.parametrize("number,status", [(13, "pending"), (81, "confirmed")])
def test_actual_read_controls_final_answer(number, status):
    repository = repo()
    provider = Provider(Reply("tools", calls=(tool(number),)),
                        lambda outputs: Reply("final", repr(outputs[0].bookings)))
    result = run(provider, repository)
    assert repository.reads == [number], "Вызовите внедрённое чтение после проверки владельца"
    assert provider.seen == [("private prompt", ()), ("private prompt", (Observation("provider-key", "ok", ((number, status),)),))]
    assert result.reason == "completed" and result.text == repr(((number, status),))
    assert result.trace == (Trace(1, "get_booking", "call-1", "ok"),)
    assert "REDACT_THIS_NOTE" not in repr((result, provider.seen))


@pytest.mark.parametrize("number", [7, 22, 999])
def test_owner_tenant_or_missing_results_in_no_read(number):
    repository = repo()
    provider = Provider(Reply("tools", calls=(tool(number),)), Reply("final", "Недоступно"))
    result = run(provider, repository)
    assert not repository.reads, "Проверяйте пару tenant/subject до чтения payload"
    assert provider.seen[-1][1] == (Observation("provider-key", "unavailable"),)
    assert result.trace[0].outcome == "unavailable"


def test_reverse_completions_use_wire_call_ids():
    class ReverseRepository(DemoRepository):
        async def read(self, number):
            if number == 13:
                await ready.wait()
            data = await super().read(number)
            if number == 81:
                ready.set()
            return data
    async def scenario():
        nonlocal ready
        ready = asyncio.Event()
        repository = ReverseRepository()
        example = repo()
        repository.owners, repository.rows = example.owners, example.rows
        calls = tool(13, "different-b"), tool(81, "different-a")
        provider = Provider(Reply("tools", calls=calls), Reply("final", "Список"))
        async with asyncio.timeout(0.20):
            result = await run_assistant("read", OWNER, provider, repository)
        assert repository.reads == [81, 13], "Независимые чтения должны завершаться в любом порядке"
        assert provider.seen[-1][1] == (Observation("different-b", "ok", ((13, "pending"),)),
                                         Observation("different-a", "ok", ((81, "confirmed"),)))
        assert result.reason == "completed"
    ready = None
    asyncio.run(scenario())


def test_list_invokes_only_owned_reads():
    repository = repo()
    provider = Provider(Reply("tools", calls=(Call("list", "list_my_bookings", {}),)), Reply("final", "done"))
    run(provider, repository)
    assert repository.reads == [13, 81]
    assert provider.seen[-1][1][0].bookings == ((13, "pending"), (81, "confirmed"))


@pytest.mark.parametrize("arguments", [{"booking_id": True}, {"booking_id": 13, "tenant": "west"}, {"booking_id": "13"}])
def test_invalid_dto_works_without_read(arguments):
    repository = repo()
    provider = Provider(Reply("tools", calls=(Call("a", "get_booking", arguments),)), Reply("final", "done"))
    run(provider, repository)
    assert not repository.reads and provider.seen[-1][1][0].outcome == "invalid_arguments"


def test_no_tool_or_provider_identifier_leaks_via_trace():
    repository = repo()
    provider = Provider(Reply("tools", calls=(Call("REDACT_ID", "REDACT_TOOL", {}),)), Reply("final", "done"))
    result = run(provider, repository)
    assert result.trace == (Trace(1, "unknown", "call-1", "unknown_tool"),)
    assert not repository.reads
    assert provider.seen[-1][1][0].call_id == "REDACT_ID"


def test_internal_error_is_a_safe_observation():
    class BadRepository(DemoRepository):
        async def read(self, number):
            raise OSError("REDACT_CONNECTION")
    repository = BadRepository()
    repository.owners[13] = OWNER
    provider = Provider(Reply("tools", calls=(tool(13),)), Reply("final", "done"))
    result = run(provider, repository)
    assert provider.seen[-1][1] == (Observation("provider-key", "tool_error"),)
    assert "REDACT_CONNECTION" not in repr(result)


@pytest.mark.parametrize("calls,reason", [
    ((tool(13, "a"), tool(81, "a")), "invalid_provider"),
    ((tool(13, ""),), "invalid_provider"),
    (tuple(tool(13, str(i)) for i in range(4)), "call_budget"),
])
def test_invalid_packet_does_not_start_reads(calls, reason):
    repository = repo()
    assert run(Provider(Reply("tools", calls=calls)), repository).reason == reason
    assert not repository.reads


def test_second_round_tools_are_not_executed():
    repository = repo()
    provider = Provider(Reply("tools", calls=(tool(81),)), Reply("tools", calls=(tool(13, "new"),)))
    assert run(provider, repository).reason == "step_budget"
    assert repository.reads == [81]


@pytest.mark.parametrize("second,reason", [
    (Reply("refusal", "private"), "refusal"), (Reply("incomplete"), "incomplete"),
    (RuntimeError("secret"), "provider_error"), (Reply("final", " "), "invalid_provider"),
])
def test_terminal_mapping(second, reason):
    provider = Provider(Reply("tools", calls=(tool(81),)), second)
    result = run(provider, repo())
    assert result.reason == reason and result.text is None and result.trace[0].outcome == "ok"


def test_final_without_tools():
    repository = repo()
    result = run(Provider(Reply("final", "Здравствуйте")), repository)
    assert result.reason == "completed" and result.text == "Здравствуйте" and not repository.reads


def test_cancel_turn_also_cancels_protected_reads():
    async def scenario():
        began, cleaned = asyncio.Event(), asyncio.Event()
        class BlockingRepository(DemoRepository):
            async def read(self, number):
                began.set()
                try:
                    await asyncio.Event().wait()
                finally:
                    cleaned.set()
        repository = BlockingRepository()
        repository.owners[13] = OWNER
        provider = Provider(Reply("tools", calls=(tool(13),)))
        task = asyncio.create_task(run_assistant("demo", OWNER, provider, repository))
        async with asyncio.timeout(0.20):
            await began.wait()
            task.cancel()
            with pytest.raises(asyncio.CancelledError):
                await task
            await cleaned.wait()
        assert len(provider.seen) == 1
    asyncio.run(scenario())
