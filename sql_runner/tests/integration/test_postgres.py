"""Real PostgreSQL/Docker assertions, deliberately separate from default pytest."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import json
from pathlib import Path
from time import monotonic, sleep

from fastapi.testclient import TestClient
import pytest

from sql_runner.app.config import RESULT_BYTES
from sql_runner.app.docker_backend import DockerBackend
from sql_runner.app.executor import json_bytes
from sql_runner.app.lifecycle import Manager, SessionError
from sql_runner.app.main import create_app
from sql_runner.tests.unit.test_policy import BANNED

ROOT = Path(__file__).resolve().parents[3]
# A target-list SRF streams without FunctionScan's materialized tuplestore.
# Its billion-row aggregate hits statement_timeout before temp_file_limit.
SLOW_SQL = "SELECT sum(g) FROM (SELECT generate_series(1,1000000000) AS g) s"


def run(manager, session, query):
    return manager.run(session["session_id"], session["generation"], query)


def container(manager, session):
    return manager.backend.client.containers.get(manager.sessions[session["session_id"]].handle)


def psql(box, query, user="student"):
    args = ["psql", "-X", "-A", "-t", "-v", "ON_ERROR_STOP=1", "-v", "VERBOSITY=verbose", "-U", user, "-d", "lab"]
    if user == "student":
        # Separate transactions deliberately disable the read-only default to
        # prove GRANT/REVOKE is an independent protection, bypassing our AST.
        args += ["-c", "SET default_transaction_read_only=off"]
    return box.exec_run(args + ["-c", query], user="65532:65532" if user == "student" else "postgres")


def test_real_select_join_catalog_and_browsing(manager, session):
    sid = session["session_id"]
    result = run(manager, session, "SELECT id, email FROM users ORDER BY id")
    assert result["error"] is None
    assert result["rows"] == [["1", "a@example.com"], ["2", "b@example.com"],
                              ["3", "c@example.com"], ["4", "d@example.com"]]
    assert result["columns"][0]["pg_type"] == "int8"
    joined = run(manager, session, "SELECT u.email, o.total FROM users u JOIN orders o ON u.id=o.user_id WHERE o.status='paid' ORDER BY o.total DESC LIMIT 2")
    assert joined["rows"] == [["b@example.com", "200.00"], ["a@example.com", "100.00"]]
    catalog = manager.catalog(sid, 1)
    tables = {t["name"]: t for t in catalog["tables"]}
    assert set(tables) == {"users", "orders", "products", "order_items"}
    assert tables["order_items"]["primary_key"] == ["order_id", "product_id"]
    assert tables["users"]["foreign_keys"][0]["referenced_table"] == "users"
    orders = tables["orders"]
    assert orders["foreign_keys"][0]["columns"] == ["user_id"]
    assert orders["foreign_keys"][0]["referenced_columns"] == ["id"]
    total = next(c for c in orders["columns"] if c["name"] == "total")
    assert total["pg_type"] == "numeric(12,2)" and not total["nullable"]
    country = next(c for c in tables["users"]["columns"] if c["name"] == "country")
    assert country["nullable"]
    page = manager.browse(sid, 1, tables["order_items"]["handle"], 2, 1)
    assert page["rows"] == [["10", "101", "1"], ["12", "101", "2"]]
    assert page["has_more"]
    assert len(manager.browse(sid, 1, orders["handle"])["rows"]) == 5


def test_entire_existing_reference_corpus_on_restricted_role(manager, session):
    tasks = json.loads((ROOT / "content/practice_banks.json").read_text())["sql"]
    for task in tasks:
        if task["solution_sql"]:
            result = run(manager, session, task["solution_sql"])
            assert result["error"] is None, (task["id"], result)
            assert [c["name"] for c in result["columns"]] == task["expected_columns"]


def test_typed_values_empty_rows_duplicates_and_postgres_errors(manager, session):
    result = run(manager, session, "SELECT NULL AS x, '' AS x, true, 9007199254740993::bigint, 12345678901234567890.012300::numeric, '2026-01-02'::date, '12:34:56'::time, '2026-01-02 03:00:00+03'::timestamptz")
    assert result["error"] is None, result
    assert result["rows"] == [[None, "", True, "9007199254740993", "12345678901234567890.012300",
                               "2026-01-02", "12:34:56", "2026-01-02T00:00:00Z"]]
    assert [c["name"] for c in result["columns"]][:2] == ["x", "x"]
    empty = run(manager, session, "SELECT id, email FROM users WHERE false")
    assert empty["rows"] == [] and len(empty["columns"]) == 2
    division = run(manager, session, "SELECT 1/0")
    assert division["error"]["sqlstate"] == "22012"
    unknown = "SELECT 'я', missing FROM users"
    error = run(manager, session, unknown)["error"]
    assert error["sqlstate"] == "42703" and error["position"] == unknown.index("missing") + 1
    syntax = "SELECT 'я', FROM users"
    error = run(manager, session, syntax)["error"]
    assert error["sqlstate"] == "42601" and error["position"] == syntax.index("FROM") + 1
    assert run(manager, session, "SELECT count(*) FROM users")["rows"] == [["4"]]
    assert run(manager, session, "SELECT users FROM users")["error"]["code"] == "output_limit"


def test_banned_queries_leave_all_seed_rows_unchanged(manager, session):
    before = run(manager, session, "SELECT id,email,country,active,manager_id,created_at FROM users ORDER BY id")["rows"]
    for query in BANNED:
        result = run(manager, session, query)
        assert result["error"]["kind"] == "policy", (query, result)
    after = run(manager, session, "SELECT id,email,country,active,manager_id,created_at FROM users ORDER BY id")["rows"]
    assert after == before
    for table, count in [("orders", 5), ("products", 3), ("order_items", 5)]:
        assert run(manager, session, f"SELECT count(*) FROM {table}")["rows"] == [[str(count)]]


def test_privileges_peer_auth_and_functions_independently_of_ast(manager, session):
    box = container(manager, session)
    for query in ["UPDATE users SET active=false", "INSERT INTO products VALUES (9,'x','x',1)",
                  "DELETE FROM order_items", "CREATE TABLE lab.bad(x int)",
                  "CREATE TEMP TABLE bad(x int)", "SELECT * FROM pg_catalog.pg_authid",
                  "SELECT * FROM pg_catalog.pg_stat_activity", "SELECT * FROM pg_catalog.pg_settings",
                  "SELECT pg_read_file('/etc/passwd')", "SELECT pg_sleep(1)",
                  "SELECT set_config('statement_timeout','0',false)",
                  "SELECT pg_advisory_lock(1)", "SET ROLE postgres", "COPY users TO PROGRAM 'id'"]:
        response = psql(box, query)
        assert response.exit_code != 0, (query, response.output)
        assert b"42501" in response.output, (query, response.output)
    impersonation = box.exec_run(["psql", "-X", "-U", "postgres", "-d", "lab", "-c", "SELECT 1"], user="65532:65532")
    assert impersonation.exit_code != 0 and b"Peer authentication failed" in impersonation.output
    flags = psql(box, "SELECT rolsuper,rolcreatedb,rolcreaterole,rolreplication,rolbypassrls FROM pg_roles WHERE rolname='student'", user="postgres")
    assert flags.exit_code == 0 and flags.output.strip() == b"f|f|f|f|f"
    memberships = psql(box, "SELECT count(*) FROM pg_auth_members WHERE member=(SELECT oid FROM pg_roles WHERE rolname='student')", user="postgres")
    assert memberships.exit_code == 0 and memberships.output.strip() == b"0"
    assert run(manager, session, "SELECT active FROM users WHERE id=1")["rows"] == [[True]]


def test_container_isolation_budgets_and_cold_start_measurement(manager, session):
    box = container(manager, session)
    box.reload()
    config, host = box.attrs["Config"], box.attrs["HostConfig"]
    assert config["User"] == "postgres"
    assert config["NetworkDisabled"] and host["NetworkMode"] == "none"
    assert host["ReadonlyRootfs"] and host["Binds"] in (None, [])
    assert host["Memory"] == host["MemorySwap"] == 512 * 1024**2
    assert host["NanoCpus"] == 1_000_000_000 and host["PidsLimit"] == 128
    assert host["CapDrop"] == ["ALL"]
    assert "no-new-privileges:true" in host["SecurityOpt"]
    assert not host["PortBindings"]
    assert set(host["Tmpfs"]) == {"/pgdata", "/var/run/postgresql", "/tmp", "/var/lib/postgresql/data"}
    assert all(m["Type"] == "tmpfs" for m in box.attrs["Mounts"])
    assert not config.get("Env") or not any("DATABASE_URL" in e or "TOKEN=" in e for e in config["Env"])
    stats = box.stats(stream=False)
    print("SQL_BENCHMARK", json.dumps({"cold_start_ms": session["cold_start_ms"],
          "memory_usage_bytes": stats["memory_stats"].get("usage"), "image": manager.settings.image,
          "anonymous_memory_bytes": stats["memory_stats"].get("stats", {}).get("anon"),
          "cpu_limit": 1, "memory_limit_bytes": host["Memory"]}))
    assert session["cold_start_ms"] < 30000


def test_reset_baseline_two_session_isolation_composite_fk_and_stale_handles(manager, session):
    sid = session["session_id"]
    old_box = container(manager, session)
    other = manager.create()
    old_catalog = manager.catalog(sid, 1)
    assert psql(old_box, "UPDATE lab.users SET email='changed@example.com' WHERE id=1", user="postgres").exit_code == 0
    assert run(manager, other, "SELECT email FROM users WHERE id=1")["rows"] == [["a@example.com"]]
    assert run(manager, session, "SELECT email FROM users WHERE id=1")["rows"] == [["changed@example.com"]]
    changes = """ALTER TABLE lab.orders ADD UNIQUE(id,user_id);
        ALTER TABLE lab.order_items ADD COLUMN user_id bigint;
        UPDATE lab.order_items i SET user_id=o.user_id FROM lab.orders o WHERE o.id=i.order_id;
        ALTER TABLE lab.order_items ADD CONSTRAINT pair_fk FOREIGN KEY(order_id,user_id) REFERENCES lab.orders(id,user_id);"""
    assert psql(old_box, changes, user="postgres").exit_code == 0
    items = next(t for t in manager.catalog(sid, 1)["tables"] if t["name"] == "order_items")
    pair = next(f for f in items["foreign_keys"] if f["name"] == "pair_fk")
    assert pair["columns"] == ["order_id", "user_id"] and pair["referenced_columns"] == ["id", "user_id"]
    new = manager.reset(sid, 1)
    assert new["generation"] == 2
    with pytest.raises(SessionError, match="generation"):
        manager.run(sid, 1, "SELECT 1")
    with pytest.raises(SessionError):
        manager.browse(sid, 2, old_catalog["tables"][0]["handle"])
    assert run(manager, new, "SELECT email FROM users WHERE id=1")["rows"] == [["a@example.com"]]
    assert len(manager.backend.containers()) == 2
    manager.close_session(sid, 2)
    manager.close_session(other["session_id"], 1)
    assert not manager.backend.containers()
    assert manager.create()["session_id"] != sid


def test_row_byte_and_single_cell_limits(manager, session):
    result = run(manager, session, "SELECT g FROM generate_series(1,1000000) g")
    assert result["error"] is None and result["rows_returned"] == 500 and result["has_more"]
    result = run(manager, session, "SELECT repeat('x',60000) FROM generate_series(1,1000)")
    assert result["error"] is None and 0 < result["rows_returned"] < 500 and result["truncated"]
    assert len(json_bytes(result)) < RESULT_BYTES
    result = run(manager, session, "SELECT repeat('я',40000)")
    assert result["error"]["code"] == "output_limit"
    assert run(manager, session, "SELECT 1")["rows"] == [["1"]]


def test_server_temp_file_budget_destroys_resource_exhausted_session(manager, session):
    # FunctionScan materializes this set; it exceeds the independently enforced
    # 32 MiB temp-file budget before it can return the first aggregate row.
    result = run(manager, session, "SELECT sum(g) FROM generate_series(1,100000000) g")
    assert result["error"]["sqlstate"] == "53400", result
    assert not manager.backend.containers()


def test_statement_timeout_destroys_session_and_run_reset_race(manager, session):
    sid = session["session_id"]
    started = monotonic()
    with ThreadPoolExecutor(1) as pool:
        future = pool.submit(run, manager, session, SLOW_SQL)
        sleep(0.3)
        with pytest.raises(SessionError) as conflict:
            manager.reset(sid, 1)
        assert conflict.value.code == "busy"
        result = future.result(timeout=10)
    assert result["error"]["sqlstate"] == "57014", result
    assert monotonic() - started < 10 and not manager.backend.containers()
    with pytest.raises(SessionError) as failed:
        run(manager, session, "SELECT 1")
    assert failed.value.status == 410


def test_external_deadline_kills_executor_and_container(settings):
    settings = replace(settings, query_seconds=0.05)
    manager = Manager(settings, DockerBackend(settings))
    try:
        manager.start()
        session = manager.create()
        result = run(manager, session, SLOW_SQL)
        assert result["error"]["code"] == "query_deadline"
        assert not manager.backend.containers()
    finally:
        manager.shutdown()


def test_provisioning_failure_removes_partial_container(settings):
    settings = replace(settings, provision_seconds=0.001)
    backend = DockerBackend(settings)
    manager = Manager(settings, backend)
    try:
        manager.start()
        with pytest.raises(SessionError) as failure:
            manager.create()
        assert failure.value.code == "provision_failed"
        assert not backend.containers()
    finally:
        manager.shutdown()


def test_lock_and_idle_transaction_limits_independent_of_ast(manager, session):
    box = container(manager, session)
    # Bootstrap owner holds a lock; the student query must hit lock_timeout first.
    with ThreadPoolExecutor(1) as pool:
        locker = pool.submit(psql, box, "BEGIN; LOCK lab.users IN ACCESS EXCLUSIVE MODE; SELECT pg_sleep(1.5); ROLLBACK", "postgres")
        sleep(0.3)
        result = run(manager, session, "SELECT * FROM users")
        assert result["error"]["sqlstate"] == "55P03", result
        assert locker.result(timeout=5).exit_code == 0
    # A test-only driver bypass proves the server closes idle transactions too.
    code = "import psycopg,time; c=psycopg.connect(host='/var/run/postgresql',user='student',dbname='lab'); c.execute('SELECT 1'); time.sleep(2.3); c.execute('SELECT 1')"
    response = box.exec_run(["/opt/sql-venv/bin/python", "-c", code], user="65532:65532")
    assert response.exit_code != 0 and b"idle-in-transaction timeout" in response.output


def test_crashed_container_during_run_is_cleaned_up(manager, session):
    box = container(manager, session)
    with ThreadPoolExecutor(1) as pool:
        running = pool.submit(run, manager, session, SLOW_SQL)
        sleep(0.25)
        box.kill()
        try:
            result = running.result(timeout=10)
            assert result["error"] is not None
        except SessionError as error:
            assert error.code == "sandbox_unavailable"
    assert not manager.backend.containers()


def test_ttl_startup_reaper_and_independent_container_watchdog(settings):
    backend = DockerBackend(settings)
    clock = [100.0]
    manager = Manager(replace(settings, idle_seconds=1), backend, clock=lambda: clock[0])
    try:
        manager.start()
        session = manager.create()
        clock[0] += 2
        manager.reap()
        assert not backend.containers()
        orphan = backend.create("orphan", 1)
        # A restarted controller has no leases and removes its labeled orphans.
        backend.reap(set())
        assert not backend.containers()
        watchdog = DockerBackend(replace(settings, absolute_seconds=4))
        try:
            handle = watchdog.create("watchdog", 1)
            deadline = monotonic() + 8
            while watchdog.containers() and monotonic() < deadline:
                sleep(0.2)
            assert not watchdog.containers(), "PID1 did not enforce its independent lifetime"
        finally:
            watchdog.reap(set())
            watchdog.close()
    finally:
        manager.shutdown()


def test_real_api_without_backend_or_application_database(settings):
    with TestClient(create_app(settings)) as api:
        response = api.post("/v1/sessions", json={"dataset_id": "shop-v1"})
        assert response.status_code == 201, response.text
        session = response.json()
        base = "/v1/sessions/" + session["session_id"]
        response = api.post(base + "/run", json={"generation": 1, "sql": "SELECT id,email FROM users ORDER BY id"})
        assert response.status_code == 200 and len(response.json()["rows"]) == 4
        cat = api.get(base + "/catalog", params={"generation": 1})
        assert cat.status_code == 200 and len(cat.json()["tables"]) == 4
        assert api.post(base + "/reset", json={"generation": 1}).json()["generation"] == 2
        assert api.delete(base, params={"generation": 2}).status_code == 204


def test_reaper_does_not_touch_another_controller_namespace(manager, session, settings):
    foreign_settings = replace(settings, namespace=settings.namespace + "-other")
    other = Manager(foreign_settings, DockerBackend(foreign_settings))
    try:
        other.start()
        foreign_session = other.create()
        manager.backend.reap(set())
        assert not manager.backend.containers()
        assert run(other, foreign_session, "SELECT count(*) FROM users")["rows"] == [["4"]]
    finally:
        other.shutdown()


def test_controller_crash_during_query_and_restart_reaps_orphan(settings):
    backend = DockerBackend(settings)
    client = backend.client
    controller = None

    def call(path, data=None):
        # Only this test controller mounts Docker's socket, as Compose does.
        # PostgreSQL sandboxes are independently inspected to have no bind mounts.
        code = ("import json,urllib.request; "
                f"r=urllib.request.Request('http://127.0.0.1:8002{path}', "
                f"data={json.dumps(data).encode()!r} if {data is not None!r} else None, "
                "headers={'Content-Type':'application/json'}); "
                "print(urllib.request.urlopen(r,timeout=25).read().decode())")
        response = controller.exec_run(["python", "-c", code])
        assert response.exit_code == 0, response.output
        return json.loads(response.output)

    def ready():
        deadline = monotonic() + 15
        while monotonic() < deadline:
            try:
                if call("/health")["status"] == "ok":
                    return
            except (AssertionError, ValueError):
                sleep(0.1)
        pytest.fail("Test SQL controller did not become ready")

    try:
        controller = client.containers.run(
            "pythoria-sql-runner:phase1", detach=True, network_mode="none",
            volumes={"/var/run/docker.sock": {"bind": "/var/run/docker.sock", "mode": "rw"}},
            environment={"SQL_RUNNER_NAMESPACE": settings.namespace,
                         "SQL_SANDBOX_IMAGE": settings.image},
        )
        ready()
        session = call("/v1/sessions", {})
        path = f"/v1/sessions/{session['session_id']}/run"
        with ThreadPoolExecutor(1) as pool:
            running = pool.submit(call, path, dict(sql=SLOW_SQL, generation=1))
            sleep(0.4)
            assert not running.done()
            controller.kill(signal="SIGKILL")
            with pytest.raises(Exception):
                running.result(timeout=10)
        assert backend.containers(), "Crash scenario did not leave a lease to reap"
        controller.start()
        ready()
        assert not backend.containers(), "Startup failed to reap interrupted lease"
    finally:
        if controller:
            controller.remove(force=True, v=True)
        backend.reap(set())
        backend.close()


def test_existing_python_docker_run_check_and_terminal():
    from runner.app.main import ExecutionRequest, execute_docker
    for mode, files, tests, command in [
        ("run", {"main.py": "print('python still works')"}, {}, ["python", "main.py"]),
        ("terminal", {}, {}, ["python", "--version"]),
        ("check", {"main.py": "answer=42"}, {"tests/test_main.py": "from main import answer\ndef test_answer(): assert answer==42\n"},
         ["pytest", "-v", "--tb=short", "-p", "no:cacheprovider", "tests"]),
    ]:
        result = execute_docker(ExecutionRequest(mode=mode, files=files, tests=tests, command=command))
        assert result["exit_code"] == 0, result
        if mode == "check":
            assert result["tests_passed"] == result["tests_total"] == 1
