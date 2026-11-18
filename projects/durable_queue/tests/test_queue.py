from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import multiprocessing
import os
from threading import Barrier, Event, Thread

import httpx
import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from queue_app.store import Store, LostLease
from queue_app.worker import process


def count(admin, table):
    assert table in {"jobs", "outbox", "effects", "external_effects"}
    with admin.connect() as c:
        return c.execute(text("SELECT COUNT(*) FROM " + table)).scalar_one()


def expire(admin, job):
    with admin.begin() as c:
        c.execute(
            text(
                "UPDATE jobs SET lease_until=clock_timestamp()-INTERVAL '1 second' WHERE id=:id"
            ),
            dict(id=job),
        )


def ready(admin, job):
    with admin.begin() as c:
        c.execute(
            text(
                "UPDATE jobs SET available_at=clock_timestamp()-INTERVAL '1 second' WHERE id=:id"
            ),
            dict(id=job),
        )


@pytest.mark.parametrize("jobs", [1, 2])
def test_two_workers_claim_simultaneously_without_duplicate_ownership(env, jobs):
    store, admin = env
    for i in range(jobs):
        store.submit("job" + str(i), {"n": i})
    gate = Barrier(2, timeout=5)

    def claim(worker):
        gate.wait()
        return store.claim(worker)

    with ThreadPoolExecutor(max_workers=2) as pool:
        pending = [pool.submit(claim, str(i)) for i in range(2)]
        leases = [p.result(timeout=5) for p in pending]
    live = [lease for lease in leases if lease]
    assert len(live) == jobs and len({lease.id for lease in live}) == jobs


def _crash_worker(url, channel, during_work):
    store = Store(url)
    lease = store.claim("crashing-worker")
    channel.send(lease)
    if not during_work:
        os._exit(17)

    def work(*_):
        channel.send("working")
        Event().wait(30)
        return {"unused": True}

    process(store, lease, 60, work)


@pytest.mark.parametrize("during_work", [False, True])
def test_real_process_crash_then_recovery_and_stale_generation_rejection(
    env, during_work
):
    store, admin = env
    job, _ = store.submit("crash", {"n": 8})
    ctx = multiprocessing.get_context("spawn")
    parent, child = ctx.Pipe()
    worker = ctx.Process(
        target=_crash_worker,
        args=(
            str(store.engine.url.render_as_string(hide_password=False)),
            child,
            during_work,
        ),
    )
    worker.start()
    try:
        assert parent.poll(8)
        old = parent.recv()
        if during_work:
            assert parent.poll(8) and parent.recv() == "working"
            worker.terminate()
        worker.join(timeout=8)
        assert not worker.is_alive() and worker.exitcode != 0
        assert store.get(job["id"])["state"] == "running"
        expire(admin, job["id"])
        new = store.claim("replacement")
        assert new.generation > old.generation and new.attempts == 2
        with pytest.raises(LostLease):
            store.finish(old, {"stale": True})
        store.finish(new, {"sum_squares": 204})
        assert (
            count(admin, "effects") == 1
            and store.get(job["id"])["state"] == "succeeded"
        )
    finally:
        if worker.is_alive():
            worker.terminate()
            worker.join(timeout=5)
        parent.close()
        child.close()


def test_worker_returns_after_losing_lease_cannot_commit(env):
    store, admin = env
    job, _ = store.submit("late", {"n": 2})
    old = store.claim("old")
    entered = Event()
    release = Event()

    def slow(*_):
        entered.set()
        assert release.wait(5)
        return {"stale": True}

    thread = Thread(target=process, args=(store, old, 60, slow))
    thread.start()
    try:
        assert entered.wait(5)
        expire(admin, job["id"])
        new = store.claim("new")
        store.finish(new, {"winner": True})
    finally:
        release.set()
        thread.join(timeout=5)
    assert not thread.is_alive() and store.get(job["id"])["result"] == {"winner": True}
    assert count(admin, "effects") == 1


def test_delayed_heartbeat_cannot_extend_expired_or_reassigned_lease(env):
    store, admin = env
    job, _ = store.submit("heartbeat", {"n": 1})
    old = store.claim("old")
    assert store.heartbeat(old)
    expire(admin, job["id"])
    assert not store.heartbeat(old)
    new = store.claim("new")
    assert new.generation > old.generation
    assert not store.heartbeat(old) and store.heartbeat(new)


@pytest.mark.parametrize("crash", [False, True])
def test_retry_budget_exhaustion_is_terminal(env, crash):
    store, admin = env
    job, _ = store.submit("retry", {"n": 1, "fail_until": 7}, max_attempts=2)
    for _ in range(2):
        lease = store.claim("worker")
        assert lease
        if crash:
            expire(admin, job["id"])
        else:
            process(store, lease)
            ready(admin, job["id"])
    assert store.claim("replacement") is None
    result = store.get(job["id"])
    assert result["state"] == "failed" and result["attempts"] == 2
    assert count(admin, "effects") == 0


def test_recoverable_failures_eventually_succeed_with_one_effect(env):
    store, admin = env
    job, _ = store.submit("transient-retry", {"n": 10, "fail_until": 2}, max_attempts=3)
    for attempt in range(1, 4):
        lease = store.claim("retry-worker")
        assert lease and lease.attempts == attempt
        process(store, lease)
        current = store.get(job["id"])
        if attempt < 3:
            assert current["state"] == "queued" and count(admin, "effects") == 0
            # Advance the persisted retry schedule, without relying on wall-clock sleeps.
            ready(admin, job["id"])
        else:
            assert current["state"] == "succeeded"
            assert current["result"] == {"sum_squares": 385}
    assert store.claim("another-worker") is None
    assert count(admin, "effects") == 1


def test_cancellation_races_with_completion_with_one_valid_terminal_result(env):
    store, admin = env
    job, _ = store.submit("cancel", {"n": 1})
    lease = store.claim("worker")
    gate = Barrier(2, timeout=5)

    def finish():
        gate.wait()
        try:
            store.finish(lease, {"done": True})
            return True
        except LostLease:
            return False

    def cancel():
        gate.wait()
        return store.cancel(job["id"])

    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(finish)
        second = pool.submit(cancel)
        completed, cancelled = first.result(timeout=5), second.result(timeout=5)
    assert completed != cancelled
    result = store.get(job["id"])
    assert result["state"] == ("succeeded" if completed else "cancelled")
    assert count(admin, "effects") == int(completed)
    with pytest.raises(LostLease):
        store.finish(lease, {"late": True})


def test_duplicate_message_delivery_cannot_duplicate_database_effect(env):
    store, admin = env
    store.submit("delivery", {"n": 3})
    lease = store.claim("worker")
    store.finish(lease, {"value": 14})
    with pytest.raises(LostLease):
        store.finish(lease, {"value": 14})
    assert store.claim("another") is None and count(admin, "effects") == 1


def test_actual_api_idempotency_contract_under_concurrent_duplicate_requests(api, env):
    store, admin = env
    gate = Barrier(2, timeout=5)
    payload = {"payload": {"n": 4}, "max_attempts": 3}

    def submit():
        gate.wait()
        return api.post("/jobs", json=payload, headers={"Idempotency-Key": "same-key"})

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(submit) for _ in range(2)]
        responses = [f.result(timeout=8) for f in futures]
    assert sorted(r.status_code for r in responses) == [200, 201]
    assert len({r.json()["id"] for r in responses}) == 1
    assert count(admin, "jobs") == count(admin, "outbox") == 1
    assert (
        api.post(
            "/jobs", json={"payload": {"n": 5}}, headers={"Idempotency-Key": "same-key"}
        ).status_code
        == 409
    )
    assert api.get("/jobs/" + responses[0].json()["id"]).status_code == 200


def test_job_and_outbox_are_atomic_even_if_producer_crashes_before_publish(env):
    store, admin = env

    def broken(_):
        raise RuntimeError("injected before outbox")

    with pytest.raises(RuntimeError):
        store.submit("rollback", {"n": 1}, after_insert=broken)
    assert count(admin, "jobs") == count(admin, "outbox") == 0
    job, _ = store.submit("committed", {"n": 1})
    assert count(admin, "jobs") == count(admin, "outbox") == 1
    event = store.claim_event()
    assert event["payload"]["job_id"] == str(job["id"])
    # Producer/relay dies without acknowledgement; expiry permits redelivery.
    with admin.begin() as c:
        c.execute(
            text("UPDATE outbox SET lease_until=clock_timestamp()-INTERVAL '1 second'")
        )
    replacement = store.claim_event()
    assert (
        replacement["id"] == event["id"]
        and replacement["generation"] > event["generation"]
    )
    assert not store.ack_event(event) and store.ack_event(replacement)
    assert store.claim_event() is None


def test_postgresql_connection_interruption_rolls_back_partial_submission(env):
    store, admin = env

    def disconnect(conn):
        pid = conn.execute(text("SELECT pg_backend_pid()")).scalar_one()
        with admin.connect().execution_options(isolation_level="AUTOCOMMIT") as control:
            assert control.execute(
                text("SELECT pg_terminate_backend(:pid)"), dict(pid=pid)
            ).scalar_one()

    with pytest.raises(SQLAlchemyError):
        store.submit("disconnect", {"n": 2}, after_insert=disconnect)
    assert count(admin, "jobs") == count(admin, "outbox") == 0
    job, created = store.submit("disconnect", {"n": 2})
    assert created and store.get(job["id"])
    assert count(admin, "jobs") == count(admin, "outbox") == 1


def test_real_http_timeout_after_external_commit_requires_receiver_idempotency(env):
    store, admin = env
    committed = Event()
    release = Event()
    first = Event()

    class Receiver(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def do_POST(self):
            payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            value = store.receive_effect(self.headers["Idempotency-Key"], payload)
            if not first.is_set():
                first.set()
                committed.set()
                release.wait(5)
            body = json.dumps(value).encode()
            try:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(body)
            except BrokenPipeError:
                pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Receiver)
    thread = Thread(target=server.serve_forever)
    thread.start()
    try:
        url = f"http://127.0.0.1:{server.server_port}/effect"
        headers = {"Idempotency-Key": "event-1"}
        with ThreadPoolExecutor(max_workers=1) as pool:
            pending = pool.submit(
                httpx.post, url, json={"value": 42}, headers=headers, timeout=1
            )
            assert committed.wait(5)
            with pytest.raises(httpx.TimeoutException):
                pending.result(timeout=4)
        assert count(admin, "external_effects") == 1
        assert httpx.post(
            url, json={"value": 42}, headers=headers, timeout=3
        ).json() == {"value": 42}
        assert count(admin, "external_effects") == 1
    finally:
        release.set()
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_actual_worker_heartbeat_renews_while_processing(env):
    from time import monotonic

    store, admin = env
    job, _ = store.submit("pulse", {"n": 1})
    lease = store.claim("pulsing", 2)
    first = store.get(job["id"])["lease_until"]
    entered = Event()
    release = Event()

    def work(*_):
        entered.set()
        assert release.wait(5)
        return {"done": True}

    thread = Thread(target=process, args=(store, lease, 2, work))
    thread.start()
    try:
        assert entered.wait(3)
        end = monotonic() + 4
        while store.get(job["id"])["lease_until"] <= first:
            assert monotonic() < end
            Event().wait(0.02)
    finally:
        release.set()
        thread.join(timeout=5)
    assert store.get(job["id"])["state"] == "succeeded" and count(admin, "effects") == 1


def test_duplicate_periodic_schedulers_use_one_durable_business_key(env):
    from queue_app.periodic import enqueue_periodic

    store, admin = env
    first, created = enqueue_periodic(store, "training", 61, 60, {"n": 2})
    second, repeated = enqueue_periodic(store, "training", 119, 60, {"n": 2})
    assert created and not repeated and first["id"] == second["id"]
    assert count(admin, "jobs") == 1


def test_real_outbox_http_delivery_ack_and_receiver_idempotency(api, env):
    from queue_app.outbox import deliver_once

    store, admin = env
    store.submit("relay-http", {"n": 3})
    keys = []

    def send(key, payload):
        keys.append(key)
        response = api.post(
            "/demo-effects", json=payload, headers={"Idempotency-Key": key}
        )
        response.raise_for_status()
        assert (
            api.post(
                "/demo-effects", json=payload, headers={"Idempotency-Key": key}
            ).json()
            == response.json()
        )
        assert (
            api.post(
                "/demo-effects",
                json={"different": True},
                headers={"Idempotency-Key": key},
            ).status_code
            == 409
        )

    assert deliver_once(store, send)
    assert not deliver_once(store, send)
    assert len(keys) == 1 and count(admin, "external_effects") == 1
    with admin.connect() as conn:
        assert conn.execute(text("SELECT delivered FROM outbox")).scalar_one() is True


@pytest.mark.parametrize(
    "columns",
    [
        "state='queued',worker_id='stray'",
        "state='queued',lease_until=clock_timestamp()",
        "state='running',worker_id='owner',lease_until=NULL",
    ],
)
def test_database_rejects_incomplete_ownership_state(env, columns):
    from sqlalchemy.exc import IntegrityError

    store, _ = env
    job, _ = store.submit("invalid-owner", {"n": 1})
    with pytest.raises(IntegrityError):
        with store.engine.begin() as conn:
            conn.execute(
                text("UPDATE jobs SET " + columns + " WHERE id=:id"), dict(id=job["id"])
            )
    assert store.get(job["id"])["state"] == "queued"


def test_application_database_role_cannot_create_or_access_other_database(env):
    from sqlalchemy.exc import DBAPIError
    from sqlalchemy import create_engine
    from sqlalchemy.engine import make_url

    store, _ = env
    with pytest.raises(DBAPIError):
        with store.engine.begin() as conn:
            conn.execute(text("CREATE TEMP TABLE unexpected(id integer)"))
    engine = create_engine(
        make_url(os.environ["DATABASE_URL"]).set(database="postgres")
    )
    try:
        with pytest.raises(DBAPIError):
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
    finally:
        engine.dispose()


def graceful_worker(url, entered, release, stopped_seen):
    import signal
    from queue_app.worker import run, calculate

    store = Store(url)
    stopped = Event()

    def stop(*_):
        stopped.set()
        stopped_seen.set()

    signal.signal(signal.SIGTERM, stop)

    def work(payload, attempt):
        entered.set()
        assert release.wait(6)
        return calculate(payload, attempt)

    try:
        run(store, "graceful-test", stopped, 5, work)
    finally:
        store.engine.dispose()


def test_real_sigterm_finishes_current_job_without_claiming_the_next(env):
    import signal

    store, admin = env
    first, _ = store.submit("first-graceful", {"n": 3})
    second, _ = store.submit("second-graceful", {"n": 4})
    context = multiprocessing.get_context("spawn")
    entered = context.Event()
    release = context.Event()
    stopped_seen = context.Event()
    child = context.Process(
        target=graceful_worker,
        args=(os.environ["DATABASE_URL"], entered, release, stopped_seen),
    )
    child.start()
    try:
        assert entered.wait(5)
        os.kill(child.pid, signal.SIGTERM)
        assert stopped_seen.wait(5)
        release.set()
        child.join(timeout=6)
        assert child.exitcode == 0
        assert store.get(first["id"])["state"] == "succeeded"
        assert store.get(second["id"])["state"] == "queued"
        assert count(admin, "effects") == 1
    finally:
        release.set()
        if child.is_alive():
            child.kill()
            child.join(3)
        child.close()


def test_api_keys_cannot_collide_with_periodic_scheduler_namespace(api, env):
    from queue_app.periodic import enqueue_periodic, periodic_key

    store, _ = env
    key = periodic_key("training", 0, 60)
    response = api.post(
        "/jobs", json={"payload": {"n": 1}}, headers={"Idempotency-Key": key}
    )
    assert response.status_code == 201
    scheduled, created = enqueue_periodic(store, "training", 0, 60, {"n": 2})
    assert created and str(scheduled["id"]) != response.json()["id"]
    assert (
        api.post(
            "/jobs", json={"payload": {"n": 3}}, headers={"Idempotency-Key": "x" * 128}
        ).status_code
        == 201
    )
    assert (
        api.post(
            "/jobs", json={"payload": {"n": 3}}, headers={"Idempotency-Key": "x" * 129}
        ).status_code
        == 422
    )
