import asyncio
import json
from contextlib import asynccontextmanager
from dataclasses import replace
from uuid import UUID

import httpx
import pytest
from fastapi.testclient import TestClient

from assistant import Assistant
from bookings import BookingRepository, Tools
from contracts import Budget, Call, ChatInput, Exchange, Output, ProviderUnavailable, Reply, Turn
from evaluate import DATA, evaluate
from history import InMemoryHistory, POLICY, build_context, exchange_units, units
from main import DEMO_ACTORS, create_app


NORTH = {"X-Demo-Actor": "north-alice"}
SOUTH = {"X-Demo-Actor": "south-alice"}
PRIVATE = "INTERNAL_DEMO_NOTE"


def conversation(client, headers=NORTH):
    response = client.post("/assistant/conversations", headers=headers)
    assert response.status_code == 201
    return response.json()["conversation_id"]


def test_http_list_lookup_proposal_and_redacted_trace():
    repository = BookingRepository()
    snapshot = repository.records.copy()
    with TestClient(create_app(repository=repository)) as client:
        key = conversation(client)
        def chat(text):
            response = client.post("/assistant/chat", headers=NORTH,
                                   json={"conversation_id": key, "text": text})
            assert response.status_code == 200
            body = response.json()
            assert body["reason"] == "completed" and body["conversation_id"] == key
            assert body["usage"]["provider_tokens"] is None
            UUID(body["request_id"])
            trace = json.dumps(body["trace"])
            assert all(event["request_id"] == body["request_id"] for event in body["trace"])
            assert PRIVATE not in json.dumps(body)
            assert all(secret not in trace for secret in ("alice", "north", "demo-booking", text))
            return body
        assert chat("список")["tools"][0]["bookings"] == [
            {"booking_id": 42, "status": "confirmed"}, {"booking_id": 43, "status": "pending"}
        ]
        assert chat("бронь 43")["tools"][0]["bookings"][0]["booking_id"] == 43
        proposal = chat("предложи отмену 42")["proposals"][0]
        assert proposal["status"] == "pending" and proposal["arguments"] == {"booking_id": 42}
        assert proposal["owner_tenant"] == "north" and proposal["owner_subject"] == "alice"
        assert UUID(proposal["proposal_id"]) != UUID(chat("предложи отмену 42")["proposals"][0]["proposal_id"])
    assert repository.reads == [(("north", "alice"), n) for n in (42, 43, 43)]
    assert repository.records == snapshot and not repository.writes


def test_http_conversation_isolation_and_invalid_request_do_not_publish_input():
    history = InMemoryHistory()
    with TestClient(create_app(history=history)) as client:
        key = conversation(client)
        payload = {"conversation_id": key, "text": PRIVATE}
        unauthorized = client.post("/assistant/chat", json=payload)
        another = client.post("/assistant/chat", json=payload, headers=SOUTH)
        missing = client.post("/assistant/chat", json=payload | {"conversation_id": "a" * 32}, headers=SOUTH)
        invalid = client.post("/assistant/chat", json=payload | {"tenant": "north"}, headers=NORTH)
        assert unauthorized.status_code == 401
        assert another.status_code == missing.status_code == 404
        assert another.json() == missing.json() == {"detail": "conversation_unavailable"}
        assert invalid.status_code == 422 and invalid.json() == {"detail": "invalid_input"}
        assert not history.entries[key].turns


@pytest.mark.parametrize("arguments", [
    '{"booking_id":"42"}', '{"booking_id":true}', '{"booking_id":3.5}', '{}', '[]',
    '{"booking_id":42,"booking_id":43}', '{"booking_id":NaN}', '{"booking_id":42,"role":"admin"}',
    '{"booking_id":42,"approved":true}', '{"booking_id":42,"url":"https://example.invalid"}',
])
def test_invalid_arguments_never_invoke_tool(arguments):
    repository = BookingRepository()
    tools = Tools(repository)
    result = asyncio.run(tools.execute(DEMO_ACTORS["north-alice"], "call-1", "get_booking", arguments))
    assert result.outcome == "invalid_arguments"
    assert not tools.invocations and not repository.reads


@pytest.mark.parametrize("actor,tool,id", [
    ("north-alice", "get_booking", 44), ("north-alice", "get_booking", 45),
    ("north-alice", "get_booking", 46), ("north-alice", "get_booking", 999),
    ("north-observer", "list_my_bookings", 0), ("north-bob", "propose_cancel", 44),
    ("south-alice", "get_booking", 42), ("north-alice", "propose_cancel", 45),
])
def test_permission_check_precedes_protected_io(actor, tool, id):
    repository = BookingRepository()
    tools = Tools(repository)
    result = asyncio.run(tools.execute(DEMO_ACTORS[actor], "call-1", tool,
                                       json.dumps({"booking_id": id} if id else {})))
    assert result.outcome == "unavailable"
    assert not result.bookings and result.proposal is None
    assert not repository.reads and not repository.writes


@pytest.mark.parametrize("kind,status,reason", [
    ("refusal", 200, "refusal"), ("incomplete", 200, "incomplete"),
    ("unavailable", 503, "provider_unavailable"), ("invalid", 502, "invalid_provider"),
    ("unexpected", 502, "invalid_provider"), ("deadline", 504, "deadline"), ("steps", 429, "step_budget"), ("context", 422, "context_budget"),
])
def test_http_terminal_mapping_and_lifespan(kind, status, reason):
    events = []
    class Provider:
        async def reply(self, context, exchanges):
            if kind == "unavailable":
                raise ProviderUnavailable(PRIVATE)
            if kind == "unexpected":
                raise RuntimeError(PRIVATE)
            if kind == "deadline":
                await asyncio.Event().wait()
            if kind == "steps":
                return Reply("tools", calls=(Call("a", "list_my_bookings", "{}"),))
            if kind == "invalid":
                return Reply("final", " ")
            return Reply(kind, PRIVATE)
    @asynccontextmanager
    async def start():
        events.append("started")
        yield Provider()
        events.append("closed")
    budget = replace(Budget(), steps=1, deadline=0.03, context_units=1 if kind == "context" else 6000)
    with TestClient(create_app(budget=budget, provider_context=start)) as client:
        key = conversation(client)
        response = client.post("/assistant/chat", headers=NORTH, json={"conversation_id": key, "text": "list"})
        assert response.status_code == status and response.json()["reason"] == reason
        assert response.json()["trace"][-1]["outcome"] == reason
        assert PRIVATE not in response.text
    assert events == ["started", "closed"]


def test_atomic_trim_uses_current_exchange_and_reserved_output():
    calls = (Call("a", "get_booking", "{}"), Call("b", "get_booking", "{}"))
    exchange = Exchange(calls, (Output("a", '{"id":42}'), Output("b", '{"id":43}')))
    old, new = Turn("old", (exchange,), "done"), Turn("new", (exchange,), "done")
    mandatory = units(POLICY) + units("input") + 30 + exchange_units(exchange)
    limit = mandatory + units("newdone") + exchange_units(exchange)
    budget = replace(Budget(), context_units=limit, reserved_units=30)
    context, used = build_context((old, new), "input", (exchange,), budget)
    assert used == limit and context.history == (new,)
    context, used = build_context((old, new), "input", (exchange,), replace(budget, context_units=limit - 1))
    assert context.history == () and used == mandatory


def test_concurrent_turn_rejected_and_cancel_releases_claim():
    async def scenario():
        entered, release = asyncio.Event(), asyncio.Event()
        class Provider:
            async def reply(self, context, exchanges):
                entered.set()
                await release.wait()
                return Reply("final", "ready")
        history = InMemoryHistory()
        @asynccontextmanager
        async def provider():
            yield Provider()
        app = create_app(history=history, provider_context=provider)
        async with app.router.lifespan_context(app), httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app), base_url="http://local.test", headers=NORTH) as client:
            key = (await client.post("/assistant/conversations")).json()["conversation_id"]
            payload = {"conversation_id": key, "text": "one"}
            active = asyncio.create_task(client.post("/assistant/chat", json=payload))
            async with asyncio.timeout(1):
                await entered.wait()
                blocked = await client.post("/assistant/chat", json=payload)
                assert blocked.status_code == 409 and blocked.json()["detail"] == "conversation_busy"
                active.cancel()
                with pytest.raises(asyncio.CancelledError):
                    await active
                assert not history.entries[key].turns
                release.set()
                assert (await client.post("/assistant/chat", json=payload)).status_code == 200
                assert len(history.entries[key].turns) == 1
    asyncio.run(scenario())


def test_deadline_cancels_in_progress_tools_and_releases_claim():
    class BlockedRepository(BookingRepository):
        cleaned = False
        async def read(self, principal, number):
            try:
                await asyncio.Event().wait()
            finally:
                self.cleaned = True
    class Provider:
        async def reply(self, context, exchanges):
            return Reply("tools", calls=(Call("first", "get_booking", '{"booking_id":42}'),))
    async def scenario():
        repository, history = BlockedRepository(), InMemoryHistory()
        principal = DEMO_ACTORS["north-alice"]
        key = history.create(principal)
        service = Assistant(Provider(), Tools(repository), history, replace(Budget(), deadline=0.03))
        result = await service.chat(principal, ChatInput(conversation_id=key, text="one"))
        assert result.reason == "deadline" and repository.cleaned
        assert not history.entries[key].busy and not history.entries[key].turns
    asyncio.run(scenario())


def test_frozen_evaluation_matches_byte_for_byte():
    report = asyncio.run(evaluate())
    assert report["workflows"] == report["totals"]["matched"]
    assert json.dumps(report, ensure_ascii=False, indent=2) + "\n" == (DATA / "evaluation.json").read_text()


def test_evaluation_rejects_missing_auth_and_write_capability():
    class MissingAuthorization(Tools):
        def allowed(self, principal, number, scope):
            return number in self.repository.records

    class WritesOnProposal(Tools):
        async def execute(self, principal, alias, name, raw):
            result = await super().execute(principal, alias, name, raw)
            if result.proposal:
                self.repository.writes.append(result.proposal.arguments["booking_id"])
            return result

    first = asyncio.run(evaluate(MissingAuthorization))
    second = asyncio.run(evaluate(WritesOnProposal))
    assert first["totals"]["authorization_violations"] > 0
    assert first["totals"]["unauthorized_protected_reads"] > 0
    assert second["totals"]["booking_writes"] > 0
    assert first["totals"]["matched"] < first["workflows"]
    assert second["totals"]["matched"] < second["workflows"]
