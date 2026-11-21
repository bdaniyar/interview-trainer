import asyncio

import pytest
from httpx import ASGITransport, AsyncClient
from fastapi.testclient import TestClient

from main import create_app


class Spy:
    def __init__(self):
        self.calls = []

    async def generate(self, text, conversation_id):
        self.calls.append((text, conversation_id))
        await asyncio.sleep(0)
        return f"{conversation_id}:{text}"


@pytest.mark.parametrize(("body", "status"), [
    ({"question": "?", "conversation_id": 5}, 404),
    ({"question": "?", "conversation_id": 40}, 404),
    ({"question": " ", "conversation_id": 4}, 422),
    ({"question": "?" * 241, "conversation_id": 4}, 422),
    ({"question": "?", "conversation_id": 5, "owner": "other"}, 422),
])
def test_reject_before_provider(body, status):
    spy = Spy()
    with TestClient(create_app("author", {4: "author", 5: "other"}, spy)) as client:
        assert client.post("/chat", json=body).status_code == status
    assert not spy.calls


def test_concurrent_requests():
    async def run():
        spy = Spy()
        transport = ASGITransport(app=create_app("a", {4: "a", 6: "a"}, spy))
        async with AsyncClient(transport=transport, base_url="http://offline") as client:
            replies = await asyncio.gather(*[
                client.post("/chat", json={"question": f"  {value} ", "conversation_id": number})
                for value, number in [("один", 6), ("два", 4)]
            ])
        assert [r.json() for r in replies] == [
            {"conversation_id": 6, "text": "6:один"}, {"conversation_id": 4, "text": "4:два"},
        ]
        assert set(spy.calls) == {("один", 6), ("два", 4)}
    asyncio.run(run())


@pytest.mark.parametrize("cancel", [False, True])
def test_wait_has_cleanup(cancel):
    async def run():
        started, cleaned = asyncio.Event(), asyncio.Event()

        class Delayed:
            async def generate(self, question, conversation_id):
                started.set()
                try:
                    await asyncio.Event().wait()
                finally:
                    cleaned.set()

        app = create_app("a", {7: "a"}, Delayed(), timeout=1 if cancel else 0)
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://offline") as client:
            task = asyncio.create_task(client.post("/chat", json={"question": "вопрос", "conversation_id": 7}))
            await asyncio.wait_for(started.wait(), 0.5)
            if cancel:
                task.cancel()
                with pytest.raises(asyncio.CancelledError):
                    await task
            else:
                assert (await task).status_code == 504
        assert cleaned.is_set()
    asyncio.run(run())
