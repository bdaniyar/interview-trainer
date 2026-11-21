import asyncio
from contextlib import asynccontextmanager

import pytest

from contracts import Outcome
from main import open_service


class Repo:
    active = 0

    @asynccontextmanager
    async def read(self, actor):
        self.active += 1
        try:
            yield f"scope-{actor}"
        finally:
            self.active -= 1


def test_shared_client_isolates_concurrent_calls():
    async def scenario():
        repo = Repo()
        events = []

        class Provider:
            def __init__(self):
                events.append("open")

            async def generate(self, context, question):
                assert repo.active == 0
                await asyncio.sleep(0)
                return f"{context}:{question}"

            async def aclose(self):
                events.append("close")

        async with open_service(Provider, repo, 1) as service:
            output = await asyncio.gather(service.ask("a", "X"), service.ask("b", "Y"))
            assert events == ["open"]
        assert events == ["open", "close"]
        assert output == [Outcome("completed", "scope-a:X"), Outcome("completed", "scope-b:Y")]
    asyncio.run(scenario())


@pytest.mark.parametrize("cancel", [True, False])
def test_cleanup_with_no_open_transaction(cancel):
    async def scenario():
        started, cleaned = asyncio.Event(), asyncio.Event()
        repo = Repo()
        closed = []

        class Provider:
            async def generate(self, context, question):
                assert repo.active == 0 and context == "scope-user"
                started.set()
                try:
                    await asyncio.Event().wait()
                finally:
                    cleaned.set()

            async def aclose(self):
                closed.append(True)

        async with open_service(Provider, repo, 1 if cancel else 0) as service:
            task = asyncio.create_task(service.ask("user", "wait"))
            await asyncio.wait_for(started.wait(), 0.5)
            if cancel:
                task.cancel()
                with pytest.raises(asyncio.CancelledError):
                    await task
            else:
                assert await task == Outcome("timeout")
            assert cleaned.is_set() and not closed
        assert closed == [True]
    asyncio.run(scenario())


def test_lifespan_exception_still_closes():
    async def scenario():
        closed = []

        class Provider:
            async def aclose(self):
                closed.append(True)

        with pytest.raises(RuntimeError):
            async with open_service(Provider, Repo(), 0):
                raise RuntimeError("failed application setup")
        assert closed == [True]
    asyncio.run(scenario())
