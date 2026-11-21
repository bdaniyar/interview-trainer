import asyncio
import json

import pytest
from fastapi.testclient import TestClient
from starlette.requests import ClientDisconnect

from contracts import ProviderEvent, ProviderUnavailable
from main import create_app, stream_frames
from providers import ScriptedProvider


def parse(body):
    parsed = []
    for frame in body.strip().split("\n\n"):
        event, data = frame.splitlines()
        assert event.startswith("event: ") and data.startswith("data: ")
        parsed.append((event[7:], json.loads(data[6:])))
    return parsed


@pytest.mark.parametrize(("event", "expected"), [
    (ProviderEvent("completed"), "completed"), (ProviderEvent("refusal", "private"), "refusal"),
    (ProviderEvent("incomplete"), "incomplete"), (ProviderEvent("failed"), "unavailable"),
    (ProviderUnavailable("internal"), "unavailable"), (None, "incomplete"),
])
def test_http_sse_terminal_and_cleanup(event, expected):
    closed = []

    class Scripted(ScriptedProvider):
        async def stream(self, question):
            try:
                yield ProviderEvent("delta", "")
                yield ProviderEvent("delta", "ёж 🐾")
                if isinstance(event, Exception):
                    raise event
                if event:
                    yield event
                    raise AssertionError("asked for output past terminal")
            finally:
                closed.append(question)

    with TestClient(create_app(Scripted)) as client:
        response = client.post("/chat/stream", json={"question": "Q"})
    assert response.status_code == 200 and response.headers["content-type"].startswith("text/event-stream")
    assert len(closed) == 1
    frames = parse(response.text)
    assert [kind for kind, _ in frames] == ["delta", "terminal"]
    assert frames[0][1]["text"] == "ёж 🐾" and frames[1][1]["status"] == expected
    assert frames[0][1]["request_id"] == frames[1][1]["request_id"]
    assert "internal" not in response.text and "private" not in response.text


def test_sse_timeout_closes_provider():
    closed = []

    class Blocked(ScriptedProvider):
        async def stream(self, question):
            try:
                yield ProviderEvent("delta", "Начало")
                await asyncio.Event().wait()
            finally:
                closed.append(question)

    async def scenario():
        result = [part async for part in stream_frames(Blocked(), "wait", "id", 0.02)]
        assert parse("".join(result))[-1][1]["status"] == "timeout"
    asyncio.run(scenario())
    assert closed == ["wait"]


def test_disconnect_during_asgi_send_closes_upstream():
    async def scenario():
        closed = []

        class Blocked(ScriptedProvider):
            async def stream(self, question):
                try:
                    yield ProviderEvent("delta", "First")
                    await asyncio.Event().wait()
                finally:
                    await asyncio.sleep(0)
                    closed.append(question)

        application = create_app(Blocked)
        sent_start = []
        chunks = []
        body = iter([{"type": "http.request", "body": b'{"question":"q"}', "more_body": False}])
        async def receive():
            return next(body)

        async def send(message):
            if message["type"] == "http.response.start":
                sent_start.append(message["status"])
            else:
                chunks.append(message.get("body", b""))
                raise OSError("synthetic disconnect")

        scope = {"type": "http", "asgi": {"version": "3.0", "spec_version": "2.4"},
                 "scheme": "http", "method": "POST", "path": "/chat/stream", "root_path": "",
                 "headers": [(b"content-type", b"application/json")], "query_string": b"",
                 "server": ("test", 80), "client": ("test", 0), "http_version": "1.1"}
        async with application.router.lifespan_context(application):
            with pytest.raises(ClientDisconnect):
                await application(scope, receive, send)
        assert sent_start == [200] and len(chunks) == 1 and closed == ["q"]
    asyncio.run(scenario())
