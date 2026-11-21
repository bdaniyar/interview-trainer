import asyncio

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from contracts import Generation, ProviderUnavailable
from main import create_app


@pytest.mark.parametrize(("outcome", "http", "status", "usage"), [
    (Generation("completed", "  ", 0), 502, "empty", 0),
    (Generation("refusal", "sensitive partial", 3), 200, "refusal", 3),
    (Generation("incomplete", "sensitive partial"), 200, "incomplete", None),
    (ProviderUnavailable("sensitive diagnostic"), 503, "unavailable", None),
], ids=["empty", "refusal", "incomplete", "unavailable"])
def test_non_success_outcomes_are_redacted(outcome, http, status, usage, caplog):
    class Fake:
        async def generate(self, question):
            if isinstance(outcome, Exception):
                raise outcome
            return outcome

    with TestClient(create_app(Fake(), id_factory=lambda: "req-x")) as client:
        response = client.post("/chat", json={"question": "Проверка?"})
    assert response.status_code == http
    assert response.json() == {"request_id": "req-x", "status": status, "usage": usage, "text": None}
    assert "sensitive" not in response.text + caplog.text


@pytest.mark.parametrize("body", [{"question": " "}, {"question": "a" * 501}, {"question": "x", "api_key": "private"}],
                         ids=["blank", "long", "extra"])
def test_reject_before_provider_without_echo(body):
    class Never:
        async def generate(self, question):
            raise AssertionError("invalid request reached provider")

    with TestClient(create_app(Never())) as client:
        response = client.post("/chat", json=body)
    assert response.status_code == 422 and response.json() == {"status": "invalid_request"}


def test_concurrent_requests_use_distinct_ids_and_text():
    async def scenario():
        class Echo:
            async def generate(self, question):
                await asyncio.sleep(0)
                return Generation("completed", question, len(question))

        app = create_app(Echo())
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://offline") as client:
            replies = await asyncio.gather(*[client.post("/chat", json={"question": text})
                                             for text in ["  первый  ", "второй!"]])
        a, b = [item.json() for item in replies]
        assert a["text"] == "первый" and a["usage"] == 6 and b["text"] == "второй!" and b["usage"] == 7
        assert a["request_id"] != b["request_id"] and a["status"] == b["status"] == "completed"
    asyncio.run(scenario())


@pytest.mark.parametrize("cancel", [False, True])
def test_timeout_or_cancellation_cleans_operation(cancel):
    async def scenario():
        entered, cleaned = asyncio.Event(), asyncio.Event()

        class Blocked:
            async def generate(self, question):
                entered.set()
                try:
                    await asyncio.Event().wait()
                finally:
                    cleaned.set()

        async with AsyncClient(
            transport=ASGITransport(app=create_app(Blocked(), timeout=0.5 if cancel else 0)),
            base_url="http://offline"
        ) as client:
            task = asyncio.create_task(client.post("/chat", json={"question": "Пауза"}))
            await asyncio.wait_for(entered.wait(), 0.3)
            if cancel:
                task.cancel()
                with pytest.raises(asyncio.CancelledError):
                    await task
            else:
                response = await task
                assert response.status_code == 504 and response.json()["status"] == "timeout"
        assert cleaned.is_set()
    asyncio.run(scenario())
