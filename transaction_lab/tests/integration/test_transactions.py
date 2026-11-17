import json
import os

import pytest

from transaction_lab.control import (
    attempt,
    outputs,
    SCENARIOS,
    DML_REFERENCE,
    BOOKING_REFERENCE,
    check,
)
from sql_runner.app.config import PYTHON

pytestmark = pytest.mark.skipif(
    os.getenv("SQL_DOCKER_TESTS") != "1",
    reason="Opt into disposable Docker transaction tests",
)


@pytest.mark.parametrize("scenario", sorted(SCENARIOS))
def test_real_independent_session_timeline(scenario):
    with attempt() as (backend, handle):
        result = backend.execute(handle, "scenario", {"scenario": scenario})
        assert not result.get("error"), result
        assert result["connections"] == 2
        if scenario == "read-committed":
            assert result["first"] == [["1"]] and result["second"] == [["0"]]
        if scenario in {"repeatable-read", "mvcc"}:
            assert result["first"] == result["second"] == [["1"]] and result[
                "current"
            ] == [["0"]]
        if scenario == "nowait":
            assert result["sqlstate"] == "55P03"
        if scenario == "skip-locked":
            assert result["claimed"] == [["2"]]
        if scenario == "blocking-update":
            assert result["blocked_observed"] and result["resumed"] == [["1"]]
        if scenario == "deadlock":
            assert result["states"].count("40P01") == 1
        if scenario == "serializable":
            assert (
                "40001" in result["states"]
                and sum(int(r[1]) for r in result["after"]) == 1
            )
        if scenario == "lost-update":
            assert result["after"] == [["2"]] and result["serial_expected"] == "3"
        if scenario == "rollback-savepoint":
            assert result["inside"] == [["1", "0"], ["2", "1"]]
            assert result["outside"] == result["after"] == [["1", "1"], ["2", "1"]]
        if scenario == "exclusion":
            assert (
                result["blocked_observed"]
                and result["sqlstate"] == "23P01"
                and result["after"] == [["1", "1", "3"]]
            )
        if scenario == "indexes":
            assert result["plan"] and any("orders" in r[0] for r in result["plan"])


@pytest.mark.parametrize(
    "kind,source,passed",
    [
        ("dml", DML_REFERENCE, True),
        ("dml", "UPDATE orders SET status='paid' RETURNING id,status", False),
        ("dml", "SELECT 10::bigint AS id,'paid' AS status", False),
        (
            "dml",
            "BEGIN; UPDATE orders SET status='paid' WHERE id=10 RETURNING id,status; ROLLBACK;",
            False,
        ),
        (
            "dml",
            "WITH changed AS (UPDATE orders SET status='paid' WHERE id=10 RETURNING id,status) SELECT id,status FROM changed",
            True,
        ),
        ("booking", BOOKING_REFERENCE, True),
        (
            "booking",
            BOOKING_REFERENCE.replace(
                "BEGIN;", "BEGIN; SELECT id FROM inventory WHERE id=1 FOR UPDATE;", 1
            ),
            True,
        ),
        (
            "booking",
            BOOKING_REFERENCE.replace(
                "BEGIN;", "BEGIN ISOLATION LEVEL SERIALIZABLE;", 1
            ),
            True,
        ),
        ("booking", "SELECT 'request-A' AS request_key,1::bigint AS room_id", False),
        (
            "booking",
            "BEGIN; UPDATE inventory SET available=0; INSERT INTO reservations VALUES ('REQUEST_KEY',1,true) RETURNING request_key,room_id; COMMIT;",
            False,
        ),
    ],
)
def test_returned_rows_and_whole_database_state_across_six_cases(kind, source, passed):
    result = check(kind, source)
    assert result["passed"] == passed and result["tests_total"] == 6
    assert (result["tests_passed"] == 6) == passed
    assert result["xp_awarded"] == 0
    assert not any(
        x in json.dumps(result)
        for x in [
            "before",
            "after",
            "request-A",
            "request-B",
            "existing",
            "sqlstate",
            "seed",
            "orders",
        ]
    )


@pytest.mark.parametrize(
    "source,state",
    [
        ("INSERT INTO orders VALUES (20,999,'new',1,'2026-01-01')", "23503"),
        ("INSERT INTO orders VALUES (10,1,'new',1,'2026-01-01')", "23505"),
        ("UPDATE inventory SET available=-1 WHERE id=1", "23514"),
    ],
)
def test_actual_constraints_and_rollback(source, state):
    with attempt() as (backend, handle):
        backend.install_case(handle, "dml", "public")
        result = backend.execute(
            handle, "script", {"sql": "BEGIN; " + source + "; ROLLBACK;"}
        )
        assert any(e.get("sqlstate") == state for e in result["timeline"])
        assert result["before"] == result["after"]


def test_savepoint_error_recovery_and_open_transaction_cleanup():
    with attempt() as (backend, handle):
        source = "BEGIN; SAVEPOINT s; UPDATE inventory SET available=-1 WHERE id=1; ROLLBACK TO SAVEPOINT s; UPDATE inventory SET available=0 WHERE id=1; COMMIT; SELECT id,available FROM inventory ORDER BY id"
        result = backend.execute(handle, "script", {"sql": source})
        assert any(e.get("sqlstate") == "23514" for e in result["timeline"])
        assert result["after"]["inventory"]["rows"] == [["1", "0"], ["2", "1"]]
        result = backend.execute(
            handle,
            "script",
            {"sql": "BEGIN; UPDATE inventory SET available=0 WHERE id=2;"},
        )
        assert result["before"] == result["after"] and result["timeline"][-1]["cleanup"]


def test_security_process_network_mounts_roles_and_direct_permission_boundary():
    with attempt() as (backend, handle):
        box = backend.client.containers.get(handle)
        box.reload()
        host = box.attrs["HostConfig"]
        assert host["NetworkMode"] == "none" and host["ReadonlyRootfs"]
        assert not host.get("Binds") and all(
            m["Type"] == "tmpfs" for m in box.attrs["Mounts"]
        )
        assert (
            host["Memory"] == 512 * 1024 * 1024
            and host["PidsLimit"] == 128
            and host["NanoCpus"] == 1000000000
        )
        assert host["CapDrop"] == ["ALL"] and any(
            "no-new-privileges" in v for v in host["SecurityOpt"]
        )
        code = """import psycopg,json
from transaction_lab.execute import connect
out=[]
for query in ['CREATE TABLE lab.evil(id integer)','SET ROLE postgres',\"SELECT pg_read_file('/etc/passwd')\",'UPDATE users SET active=false']:
 try:
  with connect() as c:c.execute(query)
  out.append('unexpected success')
 except psycopg.Error as e:out.append(e.sqlstate)
try:
 psycopg.connect(host='/var/run/postgresql',user='postgres',dbname='lab')
 out.append('unexpected owner login')
except psycopg.Error:out.append('owner denied')
print(json.dumps(out))
"""
        response = box.exec_run([PYTHON, "-c", code], user="65532:65532")
        assert json.loads(response.output) == ["42501"] * 4 + ["owner denied"]


def test_cancellation_and_controller_exception_remove_the_actual_container():
    handle = None
    with pytest.raises(RuntimeError, match="injected"):
        with attempt() as (backend, handle):
            assert backend.containers()
            raise RuntimeError("injected controller failure")
    import docker

    fresh = docker.from_env()
    try:
        assert not fresh.containers.list(all=True, filters={"id": handle})
    finally:
        fresh.close()


def test_external_cancellation_kills_the_process_boundary():
    from dataclasses import replace
    from sql_runner.app.docker_backend import QueryDeadline

    with attempt() as (backend, handle):
        backend.settings = replace(backend.settings, query_seconds=0.2)
        with pytest.raises(QueryDeadline):
            backend.execute(
                handle,
                "script",
                {"sql": "SELECT SUM(g) FROM generate_series(1,1000000000) g"},
            )
        assert not backend.containers()


def test_profile_watchdog_removes_an_orphan_without_controller_cleanup():
    from threading import Event
    from time import monotonic
    from uuid import uuid4
    from transaction_lab.control import TransactionBackend, IMAGE
    from sql_runner.app.config import Settings

    backend = TransactionBackend(
        Settings(image=IMAGE, namespace="tx-ttl-" + uuid4().hex[:8], absolute_seconds=6)
    )
    handle = None
    try:
        handle = backend.create("ttl", 1, lifetime=6)
        end = monotonic() + 9
        while backend.containers() and monotonic() < end:
            Event().wait(0.05)
        assert not backend.containers()
    finally:
        if handle:
            backend.remove(handle)
        backend.close()


@pytest.mark.parametrize(
    "source,rows",
    [
        (
            "INSERT INTO orders(id,user_id,status,total,created_at) VALUES(20,1,'new',25,'2026-01-01') RETURNING id,status",
            [["20", "new"]],
        ),
        (
            "UPDATE orders SET status='queued' WHERE id=11 RETURNING id,status",
            [["11", "queued"]],
        ),
        ("DELETE FROM orders WHERE id=11 RETURNING id,status", [["11", "cancelled"]]),
        (
            "INSERT INTO orders(id,user_id,status,total,created_at) VALUES(10,1,'review',25,'2026-01-01') ON CONFLICT(id) DO UPDATE SET status=excluded.status RETURNING id,status",
            [["10", "review"]],
        ),
    ],
)
def test_insert_update_delete_and_upsert_return_actual_modified_values(source, rows):
    with attempt() as (backend, handle):
        backend.install_case(handle, "dml", "public")
        result = backend.execute(handle, "script", {"sql": source})
        assert outputs(result["timeline"])[-1]["rows"] == rows
        assert not any(e.get("sqlstate") for e in result["timeline"])
        assert result["before"]["users"] == result["after"]["users"]
