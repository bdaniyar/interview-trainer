from concurrent.futures import ThreadPoolExecutor
from threading import Event

from fastapi.testclient import TestClient
import pytest

from sql_runner.app.config import Settings
from sql_runner.app.docker_backend import QueryDeadline, SandboxUnavailable
from sql_runner.app.executor import empty_result
from sql_runner.app.lifecycle import Manager, SessionError
from sql_runner.app.main import create_app


class FakeBackend:
    def __init__(self, settings=None):
        self.handles = set()
        self.created = 0
        self.fail_create = self.fail_remove = False
        self.failure = None
        self.entered, self.release = Event(), Event()
        self.block = False
        self.executions = []

    def create(self, sid, generation):
        if self.fail_create:
            raise SandboxUnavailable()
        self.created += 1
        handle = f"container-{self.created}"
        self.handles.add(handle)
        return handle

    def remove(self, handle):
        if self.fail_remove:
            raise SandboxUnavailable()
        self.handles.discard(handle)

    def live_count(self):
        return len(self.handles)

    def reap(self, known):
        for handle in self.handles - known:
            self.remove(handle)

    def execute(self, handle, operation, payload):
        self.executions.append((handle, operation, payload))
        if self.block:
            self.entered.set()
            assert self.release.wait(timeout=2)
        if self.failure:
            raise self.failure
        if operation == "catalog":
            return {"tables": [dict(name="users", columns=[], primary_key=["id"], foreign_keys=[])]}
        return empty_result()

    def close(self):
        pass


@pytest.fixture
def manager():
    clock = [100.0]
    backend = FakeBackend()
    instance = Manager(Settings(idle_seconds=10, absolute_seconds=30), backend, clock=lambda: clock[0])
    instance.test_clock = clock
    yield instance
    backend.fail_remove = False
    instance.shutdown()
    assert not backend.handles


def assert_error(code, call):
    with pytest.raises(SessionError) as error:
        call()
    assert error.value.code == code


def test_reset_replaces_sandbox_rotates_handles_and_checks_generation(manager):
    session = manager.create()
    sid = session["session_id"]
    first = manager.sessions[sid].handle
    table = manager.catalog(sid, 1)["tables"][0]["handle"]
    new = manager.reset(sid, 1)
    assert new["generation"] == 2 and first not in manager.backend.handles
    assert_error("stale_generation", lambda: manager.run(sid, 1, "SELECT 1"))
    assert_error("stale_generation", lambda: manager.close_session(sid, 1))
    assert_error("unknown_table", lambda: manager.browse(sid, 2, table))
    manager.close_session(sid, 2)
    manager.close_session(sid, 2)
    assert not manager.backend.handles


def test_forged_cross_session_handles_and_capacity(manager):
    first, second = manager.create(), manager.create()
    sid = first["session_id"]
    handle = manager.catalog(sid, 1)["tables"][0]["handle"]
    assert_error("capacity", manager.create)
    assert_error("unknown_table", lambda: manager.browse(second["session_id"], 1, handle))
    assert_error("unknown_table", lambda: manager.browse(sid, 1, "users; DROP TABLE users"))
    assert_error("unknown_session", lambda: manager.run("forged", 1, "SELECT 1"))


def test_idle_and_absolute_expiry_cleanup_and_bounded_tombstones(manager):
    sid = manager.create()["session_id"]
    manager.test_clock[0] += 11
    assert_error("expired", lambda: manager.run(sid, 1, "SELECT 1"))
    assert not manager.backend.handles
    sid = manager.create()["session_id"]
    for _ in range(3):
        manager.test_clock[0] += 9
        manager.run(sid, 1, "SELECT 1")
    manager.reset(sid, 1)
    manager.test_clock[0] += 4
    manager.reap()
    assert manager.sessions[sid].status == "expired" and not manager.backend.handles
    for _ in range(140):
        session = manager.create()
        manager.close_session(session["session_id"], 1)
    manager.reap()
    assert len(manager.sessions) <= 128


def test_failed_provision_reset_and_cleanup_do_not_resurrect_old_data(manager):
    sid = manager.create()["session_id"]
    manager.backend.fail_create = True
    assert_error("provision_failed", lambda: manager.reset(sid, 1))
    assert not manager.backend.handles
    assert_error("failed", lambda: manager.run(sid, 2, "SELECT 1"))
    assert_error("provision_failed", manager.create)
    manager.backend.fail_create = False
    for _ in range(2):
        manager.create()
    manager.backend.fail_remove = True
    for session in list(manager.sessions.values()):
        manager.close_session(session.id, session.generation)
    assert len(manager.backend.handles) == 2
    # Cleanup failure doesn't release capacity or create more sandboxes.
    with pytest.raises(Exception):
        manager.create()
    manager.backend.fail_remove = False
    manager.reap()
    assert not manager.backend.handles
    manager.create()


@pytest.mark.parametrize("failure", [QueryDeadline(), SandboxUnavailable()])
def test_query_failure_closes_actual_boundary(manager, failure):
    sid = manager.create()["session_id"]
    manager.backend.failure = failure
    if isinstance(failure, QueryDeadline):
        assert manager.run(sid, 1, "SELECT 1")["error"]["code"] == "query_deadline"
    else:
        assert_error("sandbox_unavailable", lambda: manager.run(sid, 1, "SELECT 1"))
    assert not manager.backend.handles and manager.sessions[sid].status == "failed"


def test_run_reset_race_is_rejected_without_destroying_active_container(manager):
    sid = manager.create()["session_id"]
    manager.backend.block = True
    with ThreadPoolExecutor(1) as pool:
        running = pool.submit(manager.run, sid, 1, "SELECT 1")
        assert manager.backend.entered.wait(timeout=1)
        assert_error("busy", lambda: manager.reset(sid, 1))
        assert len(manager.backend.handles) == 1
        manager.backend.release.set()
        assert running.result()["generation"] == 1
    assert manager.reset(sid, 1)["generation"] == 2


def test_startup_orphan_reaper_and_policy_does_not_reach_database(manager):
    manager.backend.handles.add("orphan")
    manager.start()
    assert not manager.backend.handles
    sid = manager.create()["session_id"]
    result = manager.run(sid, 1, "DELETE FROM users")
    assert result["error"]["kind"] == "policy" and not manager.backend.executions


def test_api_typed_contract_and_strict_admission():
    backend = FakeBackend()
    with TestClient(create_app(backend_factory=lambda _: backend)) as api:
        assert api.get("/health").json()["status"] == "ok"
        assert api.post("/v1/sessions", json={"image": "evil"}).status_code == 422
        assert api.post("/v1/sessions", json={"dataset_id": "../../etc"}).status_code == 422
        response = api.post("/v1/sessions", json={})
        assert response.status_code == 201
        session = response.json()
        assert "container" not in str(session)
        sid = session["session_id"]
        base = f"/v1/sessions/{sid}"
        result = api.post(base + "/run", json={"generation": 1, "sql": "SELECT 1"})
        assert result.status_code == 200 and result.json()["generation"] == 1
        cat = api.get(base + "/catalog", params={"generation": 1}).json()
        handle = cat["tables"][0]["handle"]
        assert api.get(base + f"/tables/{handle}/rows", params={"generation": 1}).status_code == 200
        assert backend.executions[-1][2] == {"table": "users", "limit": 50, "offset": 0}
        assert api.get(base + f"/tables/{handle}/rows", params={"generation": 1, "limit": 101}).status_code == 422
        assert api.post(base + "/run", content=b" " * (256 * 1024 + 1)).status_code == 413
        import json
        malformed_unicode = json.dumps({"generation": 1, "sql": "SELECT '\ud800'"}).encode()
        rejected = api.post(base + "/run", content=malformed_unicode,
                            headers={"Content-Type": "application/json"})
        assert rejected.status_code == 422 and rejected.json()["error"]["code"] == "invalid_request"
        assert api.post(base + "/run", json={"generation": 1, "sql": "SELECT '" + "я" * 17000 + "'"}).json()["error"]["code"] == "sql_size"
        assert api.post(base + "/reset", json={"generation": 1}).json()["generation"] == 2
        assert api.delete(base, params={"generation": 2}).status_code == 204
    assert not backend.handles
