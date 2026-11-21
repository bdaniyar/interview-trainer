import asyncio
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from contracts import Generation, ProviderBusy, ProviderUnavailable, Usage
from main import app, create_app
from providers import ScriptedProvider


@pytest.fixture
def make():
    def configured(*outcomes, **settings):
        class Scripted(ScriptedProvider):
            questions = []
            closed = False

            async def generate(self, question):
                self.questions.append(question)
                actual = outcomes[min(len(self.questions) - 1, len(outcomes) - 1)]
                if isinstance(actual, Exception):
                    raise actual
                return actual

            async def aclose(self):
                self.closed = True

        provider = Scripted()
        return create_app(lambda: provider, **settings), provider
    return configured


def test_default_app_http_and_versioned_estimate():
    with TestClient(app) as client:
        response = client.post("/chat", json={"question": "  Где конспект?  "})
    body = response.json()
    assert response.status_code == 200 and body["status"] == "completed"
    assert body["text"] == "Учебный ответ на вопрос «Где конспект?»."
    assert UUID(body["request_id"]).version == 4
    assert body["usage"] == {"cached_tokens": 2, "input_tokens": 8, "output_tokens": 12}
    assert body["estimated_usd"] == "0.0152" and body["price_revision"] == "synthetic-v1"


@pytest.mark.parametrize(("outcome", "http", "status"), [
    (Generation("completed", "   "), 502, "empty"),
    (Generation("refusal", "must not be public"), 200, "refusal"),
    (Generation("incomplete", "must not be public"), 200, "incomplete"),
    (ProviderUnavailable("confidential provider input"), 503, "unavailable"),
])
def test_typed_outcomes_make_no_text(outcome, http, status, make, caplog):
    configured, provider = make(outcome)
    with TestClient(configured) as client:
        response = client.post("/chat", json={"question": "Help"})
    assert response.status_code == http and response.json()["status"] == status
    assert response.json()["text"] is None and "confidential" not in response.text + caplog.text
    assert provider.questions == ["Help"] and provider.closed


@pytest.mark.parametrize("value", [None, " " * 3, "x" * 501, {"nested": "value"}])
def test_validation_before_provider(value, make):
    configured, provider = make(Generation("completed", "answer"))
    with TestClient(configured) as client:
        response = client.post("/chat", json={"question": value, "api_key": "omitted"})
        assert response.status_code == 422 and response.json()["status"] == "invalid_request"
        assert "api_key" not in response.text and "omitted" not in response.text
    assert not provider.questions


def test_invalid_billing_metadata_cannot_cross_typed_boundary():
    with pytest.raises(ValueError):
        Usage(input_tokens=2, output_tokens=1, cached_tokens=3)


def test_reported_usage_without_cache_is_not_quoted(make):
    configured, _ = make(Generation("completed", "answer", Usage(input_tokens=5, output_tokens=3)))
    with TestClient(configured) as client:
        body = client.post("/chat", json={"question": "?"}).json()
    assert body["usage"]["input_tokens"] == 5
    assert body["estimated_usd"] is None and body["price_revision"] is None


@pytest.mark.parametrize("status_style", [429, 503])
def test_one_retry_for_explicit_pre_generation_rejection(status_style, make):
    delays = []

    async def pause(delay):
        delays.append(delay)

    issue = ProviderBusy(status_style, 0.1 if status_style == 429 else 0.2)
    configured, provider = make(issue, Generation("completed", "second"), pause=pause)
    with TestClient(configured) as client:
        response = client.post("/chat", json={"question": "retry"})
    assert response.json()["text"] == "second"
    assert delays == [issue.retry_after] and provider.questions == ["retry", "retry"]


def test_unexpected_http_code_is_not_retried(make):
    configured, provider = make(ProviderBusy(401), Generation("completed", "unexpected"))
    with TestClient(configured) as client:
        assert client.post("/chat", json={"question": "?"}).status_code == 503
    assert provider.questions == ["?"]


def test_retry_after_cannot_extend_deadline(make):
    configured, provider = make(ProviderBusy(429, 5), Generation("completed", "late"), timeout=0.3)
    with TestClient(configured) as client:
        assert client.post("/chat", json={"question": "?"}).status_code == 503
    assert provider.questions == ["?"]


@pytest.mark.parametrize("cancel", [False, True])
def test_timeout_and_external_cancellation_cleanup(cancel):
    async def scenario():
        started, cleaned = asyncio.Event(), asyncio.Event()

        class Delayed(ScriptedProvider):
            async def generate(self, question):
                started.set()
                try:
                    await asyncio.Event().wait()
                finally:
                    cleaned.set()

        configured = create_app(Delayed, timeout=0.5 if cancel else 0)
        async with configured.router.lifespan_context(configured):
            async with AsyncClient(transport=ASGITransport(app=configured), base_url="http://offline") as client:
                task = asyncio.create_task(client.post("/chat", json={"question": "?"}))
                await asyncio.wait_for(started.wait(), 0.3)
                if cancel:
                    task.cancel()
                    with pytest.raises(asyncio.CancelledError):
                        await task
                else:
                    failing = await task
                    assert failing.status_code == 504 and failing.json()["status"] == "timeout"
        assert cleaned.is_set()
    asyncio.run(scenario())


def test_concurrent_requests_remain_isolated():
    async def scenario():
        async with app.router.lifespan_context(app):
            async with AsyncClient(transport=ASGITransport(app=app), base_url="http://offline") as client:
                replies = await asyncio.gather(*[client.post("/chat", json={"question": f"q{i}"}) for i in range(12)])
        bodies = [reply.json() for reply in replies]
        assert len({body["request_id"] for body in bodies}) == 12
        assert [body["text"] for body in bodies] == [f"Учебный ответ на вопрос «q{i}»." for i in range(12)]
    asyncio.run(scenario())
