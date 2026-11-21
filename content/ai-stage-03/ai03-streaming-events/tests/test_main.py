import asyncio

import pytest

from contracts import AppEvent, StreamFailed, WireEvent
from main import normalize_events


@pytest.mark.parametrize(("end", "expected"), [
    (WireEvent("done", usage=5), AppEvent("completed", usage=5)),
    (WireEvent("incomplete", "partial", 0), AppEvent("incomplete", usage=0)),
    (WireEvent("failure", "private"), AppEvent("failed")),
    (StreamFailed("private"), AppEvent("failed")),
    (None, AppEvent("incomplete")),
], ids=["complete", "incomplete", "failure", "exception", "eof"])
def test_delta_and_single_terminal(end, expected):
    closed = []
    async def source():
        try:
            yield WireEvent("text_delta", "")
            yield WireEvent("metadata", "do not send")
            yield WireEvent("text_delta", "ёж 🫖")
            if isinstance(end, Exception):
                raise end
            if end is not None:
                yield end
                raise AssertionError("read past terminal")
        finally:
            closed.append("done")

    async def scenario():
        async for event in normalize_events(source()):
            if event.kind != "delta":
                assert closed == ["done"]
            yield event

    async def collect():
        return [event async for event in scenario()]
    assert asyncio.run(collect()) == [AppEvent("delta", "ёж 🫖"), expected]


def test_consumer_closes_source_after_first_chunk():
    closed = []
    async def source():
        try:
            yield WireEvent("text_delta", "alpha")
            raise AssertionError("early consumer pulled twice")
        finally:
            closed.append(True)

    async def scenario():
        stream = normalize_events(source())
        assert await anext(stream) == AppEvent("delta", "alpha")
        await stream.aclose()
    asyncio.run(scenario())
    assert closed == [True]


def test_cancellation_propagates_and_closes():
    async def scenario():
        started, closed = asyncio.Event(), asyncio.Event()
        async def source():
            try:
                started.set()
                await asyncio.Event().wait()
                yield WireEvent("done")
            finally:
                closed.set()

        stream = normalize_events(source())
        task = asyncio.create_task(anext(stream))
        await asyncio.wait_for(started.wait(), 0.5)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert closed.is_set()
    asyncio.run(scenario())
