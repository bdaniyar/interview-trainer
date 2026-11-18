from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
from uuid import uuid4
from threading import Barrier, Event, Thread
from time import monotonic

import httpx
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import OperationalError

from architecture.orders import BookingService, LocalNotificationAdapter, OutboxAdapter
from architecture.notifications import NotificationStore
from architecture.relay import Relay


def count(engine, table):
    assert table in {"bookings", "outbox", "notifications", "inbox"}
    with engine.connect() as conn:
        return conn.execute(text("SELECT count(*) FROM " + table)).scalar_one()


def first_event(db):
    with db.connect() as conn:
        return conn.execute(text("SELECT payload FROM outbox")).scalar_one()


def ready(db):
    with db.begin() as conn:
        conn.execute(
            text(
                "UPDATE outbox SET available_at=clock_timestamp()-INTERVAL '1 second' WHERE state='pending'"
            )
        )


def place(client, key="one", room=1):
    return client.post(
        "/bookings",
        json=dict(room_id=room),
        headers={"Idempotency-Key": key, "X-Correlation-ID": "workflow-test"},
    )


@pytest.mark.parametrize("mode", ["orders", "monolith"])
def test_actual_http_two_requests_do_not_double_book_and_replay_is_stable(
    clients, databases, mode
):
    gate = Barrier(2, timeout=5)

    def send(key):
        gate.wait()
        return key, place(clients[mode], key)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(send, ["a", "b"]))
    assert sorted(r.status_code for _, r in results) == [201, 409]
    key, success = next(pair for pair in results if pair[1].status_code == 201)
    assert place(clients[mode], key).json()["id"] == success.json()["id"]
    assert place(clients[mode], key, 2).status_code == 409
    db = databases["mono" if mode == "monolith" else "orders"]
    assert count(db, "bookings") == 1
    with db.connect() as c:
        assert (
            c.execute(text("SELECT available FROM inventory WHERE id=1")).scalar_one()
            == 0
        )


def test_monolith_notification_shares_one_transaction_and_rollback(clients, databases):
    result = place(clients["monolith"])
    assert result.status_code == 201
    assert (
        count(databases["mono"], "bookings")
        == count(databases["mono"], "notifications")
        == 1
    )
    service = BookingService(
        os.environ["MONO_DATABASE_URL"], LocalNotificationAdapter()
    )

    def fail(_):
        raise RuntimeError("injected before COMMIT")

    try:
        with pytest.raises(RuntimeError):
            service.place("rollback", 2, "rollback", after_record=fail)
    finally:
        service.engine.dispose()
    assert (
        count(databases["mono"], "bookings")
        == count(databases["mono"], "notifications")
        == 1
    )


def test_distributed_transaction_does_not_automatically_deliver_and_read_is_stale(
    clients, databases
):
    result = place(clients["orders"])
    assert result.status_code == 201
    booking = result.json()["id"]
    assert clients["orders"].get("/bookings/" + booking).status_code == 200
    assert clients["notifications"].get("/notifications/" + booking).status_code == 404
    assert (
        count(databases["orders"], "outbox") == 1
        and count(databases["notify"], "inbox") == 0
    )
    relay = Relay(os.environ["ORDERS_DATABASE_URL"])
    try:
        assert relay.once("http://notifications:8000/events")
    finally:
        relay.engine.dispose()
    assert (
        clients["notifications"]
        .get("/notifications/" + booking)
        .json()["correlation_id"]
        == "workflow-test"
    )


def test_unavailable_service_does_not_rollback_committed_booking(clients, databases):
    assert place(clients["orders"]).status_code == 201
    relay = Relay(os.environ["ORDERS_DATABASE_URL"])
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    try:
        assert not relay.once(f"http://127.0.0.1:{port}/events", timeout=0.2)
        assert (
            count(databases["orders"], "bookings") == 1
            and count(databases["notify"], "notifications") == 0
        )
        ready(databases["orders"])
        assert relay.once("http://notifications:8000/events")
    finally:
        relay.engine.dispose()
    assert count(databases["notify"], "notifications") == 1


def test_duplicate_message_and_conflicting_payload_actual_http(clients, databases):
    assert place(clients["orders"]).status_code == 201
    event = first_event(databases["orders"])
    first = clients["notifications"].post("/events", json=event)
    second = clients["notifications"].post("/events", json=event)
    assert first.json() == {"created": True} and second.json() == {"created": False}
    duplicate_business = dict(event, event_id=str(uuid4()))
    assert (
        clients["notifications"].post("/events", json=duplicate_business).status_code
        == 409
    )
    event["correlation_id"] = "different"
    assert clients["notifications"].post("/events", json=event).status_code == 409
    assert (
        count(databases["notify"], "inbox")
        == count(databases["notify"], "notifications")
        == 1
    )


def test_unknown_timeout_after_receiver_commit_then_retry_one_effect(
    clients, databases
):
    assert place(clients["orders"]).status_code == 201
    store = NotificationStore(os.environ["NOTIFICATIONS_DATABASE_URL"])
    relay = Relay(os.environ["ORDERS_DATABASE_URL"])
    committed = Event()
    release = Event()

    class Receiver(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def do_POST(self):
            payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            store.receive(payload)
            committed.set()
            release.wait(5)
            try:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"{}")
            except BrokenPipeError:
                pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Receiver)
    thread = Thread(target=server.serve_forever)
    thread.start()
    try:
        with ThreadPoolExecutor(max_workers=1) as pool:
            future = pool.submit(
                relay.once, f"http://127.0.0.1:{server.server_port}/events", timeout=0.8
            )
            assert committed.wait(5)
            assert future.result(timeout=4) is False
        assert count(databases["notify"], "notifications") == 1
        ready(databases["orders"])
        assert relay.once("http://notifications:8000/events")
        assert count(databases["notify"], "notifications") == 1
    finally:
        release.set()
        server.shutdown()
        server.server_close()
        thread.join(2)
        store.engine.dispose()
        relay.engine.dispose()


def test_real_producer_process_crash_after_commit_recovers_outbox(clients, databases):
    env = {
        "PATH": os.environ["PATH"],
        "PYTHONPATH": str(Path.cwd()),
        "ORDERS_DATABASE_URL": os.environ["ORDERS_DATABASE_URL"],
    }
    script = "from architecture.orders import BookingService,OutboxAdapter;import os;s=BookingService(os.environ['ORDERS_DATABASE_URL'],OutboxAdapter());s.place('crashed',1,'producer-crash');os._exit(23)"
    child = subprocess.run([sys.executable, "-c", script], env=env, timeout=10)
    assert (
        child.returncode == 23
        and count(databases["orders"], "bookings")
        == count(databases["orders"], "outbox")
        == 1
    )
    relay = Relay(os.environ["ORDERS_DATABASE_URL"])
    try:
        assert relay.once("http://notifications:8000/events")
    finally:
        relay.engine.dispose()
    assert count(databases["notify"], "notifications") == 1


@contextmanager
def restarted_consumer(factory="architecture.api:notifications_app", settings=None):
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    env = {
        "PATH": os.environ["PATH"],
        "PYTHONPATH": str(Path.cwd()),
        "NOTIFICATIONS_DATABASE_URL": os.environ["NOTIFICATIONS_DATABASE_URL"],
    }

    def start():
        proc = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                factory,
                "--factory",
                "--host",
                "127.0.0.1",
                "--port",
                str(port),
            ],
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        end = monotonic() + 10
        with httpx.Client(timeout=0.2) as client:
            while True:
                try:
                    if client.get(f"http://127.0.0.1:{port}/health").status_code == 200:
                        return proc
                except httpx.HTTPError:
                    pass
                if proc.poll() is not None:
                    raise AssertionError(proc.stderr.read().decode())
                assert monotonic() < end, "Consumer startup deadline"
                Event().wait(0.02)

    if settings is not None:
        env = {"PATH": os.environ["PATH"], "PYTHONPATH": str(Path.cwd()), **settings}
    proc = start()
    try:
        yield f"http://127.0.0.1:{port}", lambda: (
            proc.terminate(),
            proc.wait(timeout=5),
        )
    finally:
        if proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=5)
        proc.stderr.close()


def test_consumer_process_restart_preserves_deduplication(clients, databases):
    assert place(clients["orders"]).status_code == 201
    event = first_event(databases["orders"])
    with restarted_consumer() as (url, stop):
        assert httpx.post(url + "/events", json=event).json() == {"created": True}
        stop()
    with restarted_consumer() as (url, _):
        assert httpx.post(url + "/events", json=event).json() == {"created": False}
    assert count(databases["notify"], "notifications") == 1


def test_database_ownership_prevents_cross_service_access(databases):
    for variable, foreign in [
        ("ORDERS_DATABASE_URL", "arch_notify"),
        ("NOTIFICATIONS_DATABASE_URL", "arch_orders"),
    ]:
        engine = create_engine(make_url(os.environ[variable]).set(database=foreign))
        try:
            with pytest.raises(OperationalError):
                with engine.connect() as conn:
                    conn.execute(text("SELECT 1"))
        finally:
            engine.dispose()


def test_old_relay_generation_cannot_ack_new_owner(clients, databases):
    assert place(clients["orders"]).status_code == 201
    relay = Relay(os.environ["ORDERS_DATABASE_URL"])
    try:
        old = relay.claim()
        with databases["orders"].begin() as c:
            c.execute(
                text(
                    "UPDATE outbox SET lease_until=clock_timestamp()-INTERVAL '1 second'"
                )
            )
        new = relay.claim()
        assert old["id"] == new["id"] and new["generation"] > old["generation"]
        assert not relay.finish(old, delivered=True) and relay.finish(
            new, delivered=True
        )
    finally:
        relay.engine.dispose()


def test_retry_budget_is_bounded_and_bad_contract_is_rejected(clients, databases):
    assert place(clients["orders"]).status_code == 201
    relay = Relay(os.environ["ORDERS_DATABASE_URL"])
    try:
        for _ in range(5):
            event = relay.claim()
            assert event
            assert relay.finish(event, delivered=False)
            ready(databases["orders"])
        assert relay.claim() is None
    finally:
        relay.engine.dispose()
    with databases["orders"].connect() as c:
        assert c.execute(text("SELECT state FROM outbox")).scalar_one() == "failed"
    assert (
        clients["notifications"].post("/events", json={"event_id": "bad"}).status_code
        == 422
    )


def test_distributed_producer_rollback_removes_booking_and_intent(databases):
    service = BookingService(os.environ["ORDERS_DATABASE_URL"], OutboxAdapter())

    def fail(_):
        raise RuntimeError("injected before commit")

    try:
        with pytest.raises(RuntimeError):
            service.place("rollback", 1, "rollback", after_record=fail)
    finally:
        service.engine.dispose()
    assert (
        count(databases["orders"], "bookings")
        == count(databases["orders"], "outbox")
        == 0
    )
    with databases["orders"].connect() as c:
        assert (
            c.execute(text("SELECT available FROM inventory WHERE id=1")).scalar_one()
            == 1
        )


def test_stateless_two_independent_api_processes_share_idempotency_and_reads(databases):
    settings = {"ORDERS_DATABASE_URL": os.environ["ORDERS_DATABASE_URL"]}
    with restarted_consumer("architecture.api:orders_app", settings) as (
        left,
        _,
    ), restarted_consumer("architecture.api:orders_app", settings) as (right, _):
        gate = Barrier(2, timeout=5)

        def send(url):
            gate.wait()
            with httpx.Client(base_url=url, timeout=5) as client:
                return place(client, "replica-key")

        with ThreadPoolExecutor(max_workers=2) as pool:
            responses = list(pool.map(send, [left, right]))
        assert sorted(r.status_code for r in responses) == [200, 201]
        booking = responses[0].json()["id"]
        assert responses[1].json()["id"] == booking
        for url in [left, right]:
            assert httpx.get(url + "/bookings/" + booking).json()["id"] == booking
    assert count(databases["orders"], "bookings") == 1


@pytest.mark.parametrize("mode", ["orders", "monolith"])
def test_unknown_inventory_and_malformed_body_have_no_effect(clients, databases, mode):
    assert place(clients[mode], "unknown", 999).status_code == 409
    assert place(clients[mode], "boolean", True).status_code == 422
    assert place(clients[mode], "overflow", 9223372036854775808).status_code == 422
    db = databases["orders" if mode == "orders" else "mono"]
    assert count(db, "bookings") == count(db, "outbox") == 0
