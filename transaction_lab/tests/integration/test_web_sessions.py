"""Real PostgreSQL and Docker exec-stream coverage for the web coordinator."""
from time import monotonic, sleep
import os
from uuid import UUID, uuid4

from fastapi import HTTPException
import pytest

from transaction_lab.web import Command, Coordinator, Scope

pytestmark = pytest.mark.skipif(
    os.getenv("SQL_DOCKER_TESTS") != "1", reason="Opt into disposable Docker transaction tests"
)


@pytest.fixture
def web():
    coordinator = Coordinator("tx-web-test-" + uuid4().hex[:12])
    scope = Scope(slug="s11-booking-concurrency", kind="booking")
    try:
        session = coordinator.create(scope)

        def command(action, **kwargs):
            return coordinator.command(UUID(session["session_id"]), Command(
                **scope.model_dump(), generation=session["generation"], action=action, **kwargs
            ))

        yield coordinator, session, command
    finally:
        backend = coordinator.backend
        if backend:
            coordinator.discard()
            assert not backend.containers()
        coordinator.shutdown()


def await_status(command, predicate, *, timeout=3):
    deadline = monotonic() + timeout
    while monotonic() < deadline:
        state = command("status")
        if predicate(state):
            return state
        sleep(.015)
    pytest.fail("Timed out awaiting a PostgreSQL-observed state")


def run_and_wait(command, side, source):
    op = command("run", side=side, sql=source)["operation"]
    return await_status(command, lambda state: side not in state["pending"] and any(
        event.get("operation") == op for event in state["timeline"]))


@pytest.mark.parametrize("end,expected", [("COMMIT", "0"), ("ROLLBACK", "1")])
def test_observed_blocker_release_and_transaction_state(web, end, expected):
    _, _, command = web
    a = run_and_wait(command, "A", "BEGIN; UPDATE inventory SET available=0 WHERE id=1")
    assert a["states"]["A"] == "transaction" and a["states"]["B"] == "ready"
    op = command("run", side="B", sql="SELECT available FROM inventory WHERE id=1 FOR UPDATE")["operation"]
    await_status(command, lambda value: value["pending"].get("B", {}).get("blockers") == ["A"])
    with pytest.raises(HTTPException, match="busy"):
        command("run", side="B", sql="SELECT 1")
    command("run", side="A", sql=end)
    status = await_status(command, lambda value: not value["pending"])
    events = [event for event in status["timeline"] if event.get("operation") == op]
    assert [event["phase"] for event in events] == ["running", "blocked", "released", "result"]
    assert events[-1]["result"]["rows"] == [[expected]]
    assert status["states"] == {"A": "ready", "B": "ready"}


def test_nowait_failed_transaction_rollback_and_cancel(web):
    _, _, command = web
    run_and_wait(command, "A", "BEGIN; SELECT id FROM inventory WHERE id=1 FOR UPDATE")
    command("run", side="B", sql="BEGIN; SELECT id FROM inventory WHERE id=1 FOR UPDATE NOWAIT")
    state = await_status(command, lambda value: value["states"]["B"] == "failed")
    assert any(event.get("sqlstate") == "55P03" for event in state["timeline"])
    command("run", side="B", sql="ROLLBACK")
    await_status(command, lambda value: value["states"]["B"] == "ready")
    op = command("run", side="B", sql="SELECT id FROM inventory WHERE id=1 FOR UPDATE")["operation"]
    await_status(command, lambda value: value["pending"].get("B", {}).get("blockers") == ["A"])
    command("cancel", side="B", operation=op)
    completed = await_status(command, lambda value: "B" not in value["pending"])
    assert completed["states"]["A"] == "transaction"
    # Use an incremental cursor because the timeline is paginated.
    page = command("status", after=completed["timeline"][-1]["sequence"])
    all_events = completed["timeline"] + page["timeline"]
    assert any(event.get("sqlstate") == "57014" and event.get("operation") == op for event in all_events)


def test_reset_kills_pending_and_invalidates_generation(web):
    coordinator, session, command = web
    old = coordinator.workspace.handle
    run_and_wait(command, "A", "BEGIN; SELECT id FROM inventory WHERE id=1 FOR UPDATE")
    command("run", side="B", sql="SELECT id FROM inventory WHERE id=1 FOR UPDATE")
    await_status(command, lambda value: value["pending"].get("B", {}).get("blockers") == ["A"])
    new = command("reset")
    assert new["session_id"] == session["session_id"] and new["generation"] == 2
    assert old not in {container.id for container in coordinator.backend.containers()}
    with pytest.raises(HTTPException, match="stale_session"):
        command("status")
    with pytest.raises(HTTPException, match="stale_session"):
        coordinator.command(UUID(session["session_id"]), Command(
            slug="s10-data-modification", kind="dml", generation=2, action="status"))
    coordinator.workspace.deadline = monotonic() - 1
    coordinator.expire()
    assert not coordinator.backend.containers()


def test_crash_and_policy_leave_no_handle_or_internal_details(web):
    coordinator, session, command = web
    with pytest.raises(HTTPException, match="policy"):
        command("run", sql="CREATE TABLE example(id integer)")
    with pytest.raises(HTTPException, match="policy"):
        command("run", sql="SELECT pg_catalog.pg_blocking_pids(1)")
    coordinator.backend.client.containers.get(coordinator.workspace.handle).kill()
    with pytest.raises(HTTPException, match="session_closed"):
        command("status")
    assert not coordinator.backend.containers()
    assert set(session) == {"session_id", "generation", "remaining_ms"}


def test_unresponsive_exec_deadline_removes_workspace(web):
    coordinator, _, command = web
    container = coordinator.backend.client.containers.get(coordinator.workspace.handle)
    container.pause()
    try:
        started = monotonic()
        with pytest.raises(HTTPException, match="session_closed"):
            command("status")
        assert monotonic() - started < 6
    finally:
        # Cleanup a failed assertion without keeping a frozen PostgreSQL process.
        for orphan in coordinator.backend.containers():
            orphan.reload()
            if orphan.status == "paused":
                orphan.unpause()
            coordinator.backend.remove(orphan.id)
    assert not coordinator.backend.containers()


def test_startup_reaps_orphan_in_own_namespace_only():
    namespace = "tx-orphan-test-" + uuid4().hex[:10]
    first = Coordinator(namespace)
    second = Coordinator(namespace)
    try:
        first.create(Scope(slug="s11-locks", kind="practice"))
        assert len(first.backend.containers()) == 1
        second.cleanup_startup()
        assert not second.backend.containers()
    finally:
        first.shutdown()
        second.shutdown()


def test_idle_transaction_expiry_is_visible_and_rolls_back(web):
    _, _, command = web
    run_and_wait(command, "A", "BEGIN; UPDATE inventory SET available=0 WHERE id=1")
    state = await_status(command, lambda value: value["states"]["A"] == "disconnected", timeout=8)
    assert state["states"]["B"] == "ready"
    recovered = run_and_wait(command, "A", "SELECT available FROM inventory WHERE id=1")
    assert recovered["states"]["A"] == "ready"
    assert recovered["timeline"][-1]["result"]["rows"] == [["1"]]
