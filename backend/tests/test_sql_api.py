import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
import json
from threading import Event

import httpx
import pytest

from backend.app import main as main_module
from backend.app.sql_runner_client import SQLRunnerClient, SqlServiceError

SLUG = "s10-select-aliases-and-expressions"


class RunnerStub:
    def __init__(self):
        self.records = {}
        self.serial = 0
        self.calls = []
        self.started, self.release = Event(), Event()
        self.block = False
        self.fail = None
        self.result_error = None
        self.result_override = {}

    async def __call__(self, request):
        path, method = request.url.path, request.method
        body = json.loads(request.content) if request.content else None
        self.calls.append((method, path, body, dict(request.url.params)))
        if self.fail:
            return httpx.Response(self.fail, json={"detail": "secret admin DSN", "error": {"message": "Docker /private/path"}})
        if path == "/v1/sessions":
            self.serial += 1
            sid = "runner-" + str(self.serial)
            now = datetime.now(timezone.utc)
            info = dict(session_id=sid, generation=1, dataset_id="shop-v1", dataset_checksum="a" * 64,
                        postgres_major=17, created_at=now.isoformat(), expires_at=(now + timedelta(minutes=15)).isoformat(), cold_start_ms=3)
            self.records[sid] = info
            return httpx.Response(201, json=info | {"private_field": "never public"})
        sid = path.split("/")[3]
        info = self.records.get(sid)
        if method == "DELETE":
            self.records.pop(sid, None)
            return httpx.Response(204)
        if not info:
            return httpx.Response(410, json={"error": {"code": "expired"}})
        generation = body["generation"] if body else int(request.url.params["generation"])
        if generation != info["generation"]:
            return httpx.Response(409, json={"error": {"code": "stale_generation"}})
        if path.endswith("/reset"):
            self.records[sid] = info | {"generation": generation + 1}
            return httpx.Response(200, json=self.records[sid])
        if path.endswith("/catalog"):
            return httpx.Response(200, json=dict(session_id=sid, generation=generation, tables=[dict(
                handle=f"users-g{generation}", schema_name="lab", name="users", primary_key=["id"], foreign_keys=[],
                columns=[dict(name="id", pg_type="bigint", nullable=False)])]))
        if "/tables/" in path and path.split("/")[-2] != f"users-g{generation}":
            return httpx.Response(404, json={"error": {"code": "unknown_table"}})
        if self.block and path.endswith("/run"):
            self.started.set()
            while not self.release.is_set():
                await asyncio.sleep(0.01)
        result = dict(session_id=sid, generation=generation, command="SELECT",
                      columns=[dict(name="id", pg_type="int8", type_oid=20)], rows=[["9007199254740993"]],
                      rows_returned=1, has_more=False, truncated=False, duration_ms=2, error=self.result_error)
        return httpx.Response(200, json=result | {"solution_sql": "secret", "hidden_dataset": "secret"} | self.result_override)


@pytest.fixture
def runner(client):
    stub = RunnerStub()
    main_module.app.state.sql_sessions.client = SQLRunnerClient(url="http://runner-test", transport=httpx.MockTransport(stub))
    yield stub
    stub.release.set()
    stub.fail = None


def create(client):
    response = client.post("/api/sql/sessions", json={"lesson_slug": SLUG})
    assert response.status_code == 201, response.text
    return response.json()


def test_public_manifest_has_guided_capability_and_no_answers(client):
    data = client.get(f"/api/sql/lessons/{SLUG}").json()
    assert data["starter_sql"] == "SELECT id, email FROM users;\n" and data["can_check"] is False
    for field in ("solution_sql", "expected_reasoning", "hidden_dataset", "seed", "expected_columns"):
        assert field not in data
    assert client.get(f"/api/lessons/{SLUG}").json()["workspace_kind"] == "sql"
    assert client.get("/api/lessons/is-vs-eq").json()["workspace_kind"] == "python"
    for slug in ("is-vs-eq", "s10-where-and-boolean-logic", "does-not-exist"):
        assert client.get(f"/api/sql/lessons/{slug}").status_code == 404


def test_sql_lifecycle_never_changes_python_files_progress_or_xp(client, runner):
    files = {"main.py": "VALUE = 42\n", "extra.py": "SAVED = True\n"}
    client.put(f"/api/lessons/{SLUG}/files", json={"files": files})
    before = client.get(f"/api/lessons/{SLUG}").json()
    course_before = client.get("/api/course").json()["summary"]
    session = create(client)
    assert session["session_id"] != next(iter(runner.records))
    assert "private_field" not in session
    path = "/api/sql/sessions/" + session["session_id"]
    result = client.post(path + "/run", json={"generation": 1, "sql": "SELECT id FROM users"}).json()
    assert result["rows"] == [["9007199254740993"]] and result["session_id"] == session["session_id"]
    assert "solution_sql" not in result and "hidden_dataset" not in result
    cat = client.get(path + "/catalog", params={"generation": 1}).json()
    handle = cat["tables"][0]["handle"]
    assert client.get(path + f"/tables/{handle}/rows", params={"generation": 1}).status_code == 200
    assert runner.calls[-1][-1] == {"generation": "1", "limit": "50", "offset": "0"}
    assert client.post(path + "/reset", json={"generation": 1}).json()["generation"] == 2
    assert client.post(path + "/run", json={"generation": 1, "sql": "SELECT 1"}).status_code == 409
    assert client.delete(path, params={"generation": 2}).status_code == 204
    assert client.delete(path, params={"generation": 2}).status_code == 204
    assert not runner.records
    after = client.get(f"/api/lessons/{SLUG}").json()
    assert after["files"] == before["files"] == files and after["progress"] == before["progress"]
    assert client.get("/api/course").json()["summary"] == course_before


def test_binding_and_budget_checks_happen_before_runner_calls(client, runner):
    session = create(client)
    path = "/api/sql/sessions/" + session["session_id"]
    calls = len(runner.calls)
    for payload in [{"lesson_slug": SLUG, "dataset_id": "evil"}, {"lesson_slug": "is-vs-eq"},
                    {"lesson_slug": SLUG, "owner": "other"}]:
        assert client.post("/api/sql/sessions", json=payload).status_code in (404, 422)
    assert client.post("/api/sql/sessions/runner-1/run", json={"generation": 1, "sql": "SELECT 1"}).status_code == 404
    assert client.post(path + "/run", json={"generation": 1, "sql": "я" * 17000}).status_code == 422
    assert client.post(path + "/run", json={"generation": 1, "sql": "SELECT 1", "passed": True}).status_code == 422
    assert client.get(path + "/tables/any/rows", params={"generation": 1, "limit": 101}).status_code == 422
    response = client.post(path + "/run", content=b" " * (256 * 1024 + 1), headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 413 and response.headers["access-control-allow-origin"] == "http://localhost:3000"
    assert len(runner.calls) == calls


def test_wrong_table_handle_does_not_forget_valid_session(client, runner):
    session = create(client)
    path = "/api/sql/sessions/" + session["session_id"]
    response = client.get(path + "/tables/forged/rows", params={"generation": 1})
    assert response.status_code == 404 and response.json()["error"]["code"] == "unknown_table"
    assert client.post(path + "/run", json={"generation": 1, "sql": "SELECT 1"}).status_code == 200


def test_bindings_cannot_be_retargeted_to_other_principals_or_lessons(client, runner):
    session = create(client)
    path = "/api/sql/sessions/" + session["session_id"]
    calls = len(runner.calls)
    assert client.post(path + "/run", json={"generation": 1, "sql": "SELECT 1", "lesson_slug": "is-vs-eq"}).status_code == 422
    main_module.app.state.sql_sessions.bindings[session["session_id"]].owner = "other-principal"
    assert client.post(path + "/run", json={"generation": 1, "sql": "SELECT 1"}).status_code == 404
    assert client.delete(path, params={"generation": 1}).status_code == 204
    assert len(runner.calls) == calls


def test_foreign_or_stale_result_is_not_exposed_to_the_browser(client, runner):
    session = create(client)
    path = "/api/sql/sessions/" + session["session_id"]
    for override in [{"session_id": "foreign-runner"}, {"generation": 99}]:
        runner.result_override = override
        response = client.post(path + "/run", json={"generation": 1, "sql": "SELECT 1"})
        assert response.status_code == 503 and "9007199254740993" not in response.text


def test_failed_close_keeps_capacity_until_reaper_retries(client, runner):
    first = create(client)
    create(client)
    runner.fail = 503
    assert client.delete(f"/api/sql/sessions/{first['session_id']}", params={"generation": 1}).status_code == 503
    service = main_module.app.state.sql_sessions
    assert first["session_id"] in service.bindings
    assert client.post("/api/sql/sessions", json={"lesson_slug": SLUG}).status_code == 429
    runner.fail = None
    create(client)  # admission retries pending cleanup before reserving capacity
    assert first["session_id"] not in service.bindings and len(service.bindings) == 2


def test_capacity_expiry_failures_and_bounded_diagnostics(client, runner):
    first = create(client)
    create(client)
    assert client.post("/api/sql/sessions", json={"lesson_slug": SLUG}).status_code == 429
    path = "/api/sql/sessions/" + first["session_id"]
    binding = main_module.app.state.sql_sessions.bindings[first["session_id"]]
    binding.info.expires_at = datetime.now(timezone.utc) - timedelta(seconds=1)
    assert client.post(path + "/run", json={"generation": 1, "sql": "SELECT 1"}).status_code == 410
    renewed = create(client)
    runner.fail = 503
    response = client.post(f"/api/sql/sessions/{renewed['session_id']}/run", json={"generation": 1, "sql": "SELECT 1"})
    assert response.status_code == 503 and "secret" not in response.text and "/private" not in response.text


def test_run_reset_race_fails_fast_without_losing_generation(client, runner):
    session = create(client)
    path = "/api/sql/sessions/" + session["session_id"]
    runner.block = True
    with ThreadPoolExecutor(1) as pool:
        running = pool.submit(client.post, path + "/run", json={"generation": 1, "sql": "SELECT 1"})
        assert runner.started.wait(2)
        try:
            assert client.post(path + "/reset", json={"generation": 1}).status_code == 409
        finally:
            runner.release.set()
        assert running.result(timeout=3).status_code == 200
    assert client.post(path + "/reset", json={"generation": 1}).json()["generation"] == 2


def test_query_timeout_marks_session_closed_without_awarding_progress(client, runner):
    session = create(client)
    runner.result_error = dict(kind="postgres", code="query_error", message="statement timeout", sqlstate="57014", position=None, hint=None)
    path = "/api/sql/sessions/" + session["session_id"]
    response = client.post(path + "/run", json={"generation": 1, "sql": "SELECT 1"}).json()
    assert response["error"]["sqlstate"] == "57014" and response["session_closed"]
    assert session["session_id"] not in main_module.app.state.sql_sessions.bindings


@pytest.mark.parametrize("response", [httpx.Response(200, json={"admin_dsn": "secret"}),
    httpx.Response(200, content=b"x" * (1024 * 1024 + 4097)), httpx.Response(500, content=b"secret traceback")])
def test_runner_client_rejects_bad_or_oversized_protocol(response):
    async def check():
        client = SQLRunnerClient(transport=httpx.MockTransport(lambda _: response))
        with pytest.raises(SqlServiceError) as error:
            await client.create()
        assert error.value.status == 503 and "secret" not in str(error.value)
    asyncio.run(check())
