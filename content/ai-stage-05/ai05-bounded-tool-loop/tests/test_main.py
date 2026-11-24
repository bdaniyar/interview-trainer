import asyncio

import pytest

from contracts import Budget, Call, Observation, Reply
from main import run_loop


def script(replies, outputs=None, budget=Budget(), **options):
    seen, invoked = [], []
    outputs = {} if outputs is None else outputs

    async def model(history):
        seen.append(history)
        return replies.pop(0)

    async def execute(call):
        invoked.append(call.call_id)
        value = outputs.get(call.call_id, "done")
        if isinstance(value, Exception):
            raise value
        return value

    return asyncio.run(run_loop(model, execute, budget, **options)), seen, invoked


def tools(*ids):
    return Reply("calls", calls=tuple(Call(i, "fixture-tool") for i in ids))


def test_multiple_turns_use_real_correlated_observations():
    final, seen, invoked = script([tools("t-7", "t-2"), tools("t-3"), Reply("final", "done")],
                                  {"t-7": "Ka", "t-2": "Al", "t-3": "Ta"})
    assert final.reason == "completed" and final.text == "done" and final.steps == 3
    assert invoked == ["t-7", "t-2", "t-3"]
    assert seen == [(), (Observation("t-7", "Ka"), Observation("t-2", "Al")), final.observations]


@pytest.mark.parametrize(("reply", "reason"), [
    (Reply("final", "result"), "completed"), (Reply("final", " "), "empty_final"),
    (Reply("refusal", "internal"), "refusal"), (Reply("incomplete"), "incomplete"),
    (Reply("calls"), "invalid_reply"),
])
def test_terminal_without_tool_invocation(reply, reason):
    final, _, invoked = script([reply])
    assert final.reason == reason and invoked == []
    assert final.text == ("result" if reason == "completed" else None)


@pytest.mark.parametrize(("replies", "expected"), [
    ([tools("x", "x")], []), ([tools("x"), tools("x", "y")], ["x"]), ([tools("")], []),
])
def test_duplicate_is_rejected_before_any_later_call(replies, expected):
    final, _, invoked = script(replies)
    assert final.reason == "duplicate_or_missing_id" and invoked == expected


def test_steps_break_repeated_tool_requests():
    final, observations, invoked = script([tools(str(n)) for n in range(10)], budget=Budget(steps=2, calls=10))
    assert final.reason == "step_limit" and len(observations) == 2 and invoked == ["0", "1"]


def test_call_budget_rejects_batch_before_work():
    final, _, invoked = script([tools("one", "two")], budget=Budget(calls=1))
    assert final.reason == "call_limit" and invoked == []


def test_output_budget_counts_utf8_cumulatively():
    final, seen, invoked = script([tools("uno", "dos")], {"uno": "я", "dos": "x"},
                                  budget=Budget(output_bytes=2))
    assert final.reason == "output_limit" and invoked == ["uno"] and len(seen) == 1


def test_tool_error_is_a_safe_observation():
    final, observed, _ = script([tools("x"), Reply("final", "handled")], {"x": RuntimeError("PII")})
    assert observed[-1] == (Observation("x", "tool_error"),)
    assert final.reason == "completed"


def test_provider_error_is_typed():
    async def model(history):
        raise RuntimeError("private")

    result = asyncio.run(run_loop(model, None))
    assert result.reason == "provider_error" and result.text is None


def test_overall_deadline_is_not_reset_after_a_turn():
    times = iter((0.0, .1, .2, .3, .4, .49, .51))
    final, _, _ = script([tools("y"), tools("z"), Reply("final", "too late")],
                         clock=lambda: next(times), budget=Budget(seconds=.5))
    assert final.reason == "timeout" and final.calls <= 1


@pytest.mark.parametrize("cancel", [False, True])
def test_event_timeout_or_cancellation_cleans_up_tool(cancel):
    async def go():
        entered, closed = asyncio.Event(), asyncio.Event()

        async def model(history):
            return tools("t")

        async def execute(call):
            entered.set()
            try:
                await asyncio.Event().wait()
            finally:
                closed.set()

        task = asyncio.create_task(run_loop(model, execute, Budget(seconds=.2, tool_seconds=.02)))
        async with asyncio.timeout(.3):
            await entered.wait()
            if cancel:
                task.cancel()
                with pytest.raises(asyncio.CancelledError):
                    await task
            else:
                assert (await task).reason == "tool_timeout"
        assert closed.is_set()

    asyncio.run(go())
