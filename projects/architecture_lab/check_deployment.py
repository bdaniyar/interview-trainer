"""Trusted host check of both dev deployments on fresh isolated resources."""

import json
from pathlib import Path
import socket
import subprocess
import tempfile
from threading import Event
from time import monotonic
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from uuid import UUID, uuid4


def main():
    source = Path(__file__).with_name("compose.yml")
    project = "pythoria-architecture-smoke-" + uuid4().hex[:10]
    volume = project + "_architecture_data"
    assert (
        volume.startswith("pythoria-architecture-smoke-")
        and volume != "pythoria_pythoria_data"
    )
    model = json.loads(
        subprocess.check_output(
            ["docker", "compose", "-f", str(source), "config", "--format", "json"],
            text=True,
        )
    )
    model["name"] = project
    model["volumes"]["architecture_data"]["name"] = volume
    for key, value in model["networks"].items():
        value["name"] = project + "_" + key
    reserved = []
    try:
        for service in ["monolith", "orders", "notifications"]:
            sock = socket.socket()
            sock.bind(("127.0.0.1", 0))
            reserved.append(sock)
            for port in model["services"][service]["ports"]:
                port["published"] = str(sock.getsockname()[1])
                port["host_ip"] = "127.0.0.1"
    finally:
        for sock in reserved:
            sock.close()
    with tempfile.TemporaryDirectory(
        prefix="pythoria-architecture-smoke-"
    ) as temporary:
        path = Path(temporary) / "compose.json"
        path.write_text(json.dumps(model))
        argv = ["docker", "compose", "-p", project, "-f", str(path)]

        def compose(*args):
            return subprocess.check_output(
                argv + list(args), text=True, stderr=subprocess.STDOUT
            )

        def endpoint(service):
            address = compose("port", service, "8000").strip()
            assert address.startswith("127.0.0.1:"), address
            return "http://" + address

        def call(base, path, body=None, key="deployment-key"):
            request = Request(
                base + path,
                data=json.dumps(body).encode() if body is not None else None,
                headers={
                    "Content-Type": "application/json",
                    "Idempotency-Key": key,
                    "X-Correlation-ID": "deployment-test",
                },
            )
            try:
                with urlopen(request, timeout=5) as response:
                    return response.status, json.load(response)
            except HTTPError as response:
                return response.code, json.load(response)

        def ready(service):
            base = endpoint(service)
            end = monotonic() + 20
            while True:
                try:
                    if call(base, "/health")[0] == 200:
                        return base
                except OSError:
                    pass
                assert monotonic() < end, "API readiness deadline"
                Event().wait(0.05)

        def delivered(base, booking):
            end = monotonic() + 25
            while True:
                status, row = call(base, "/notifications/" + booking)
                if status == 200:
                    return row
                assert status == 404 and monotonic() < end, "Delivery deadline"
                Event().wait(0.05)

        try:
            compose("build", "orders")
            compose("up", "-d", "--wait", "db", "monolith", "orders", "notifications")
            mono = ready("monolith")
            orders = ready("orders")
            notifications = ready("notifications")
            status, local = call(mono, "/bookings", {"room_id": 1}, "mono-first")
            assert status == 201
            local_id = str(UUID(local["id"]))
            assert call(mono, "/notifications/" + local_id)[0] == 200
            status, booking = call(orders, "/bookings", {"room_id": 1}, "service-first")
            assert status == 201
            booking_id = str(UUID(booking["id"]))
            assert call(notifications, "/notifications/" + booking_id)[0] == 404
            compose("up", "-d", "--wait", "relay")
            row = delivered(notifications, booking_id)
            assert row["correlation_id"] == "deployment-test"
            query = (
                "SELECT payload FROM outbox WHERE (payload->>'order_id')='"
                + booking_id
                + "'"
            )
            event = json.loads(
                compose(
                    "exec",
                    "-T",
                    "db",
                    "psql",
                    "-U",
                    "postgres",
                    "-d",
                    "arch_orders",
                    "-tAc",
                    query,
                )
            )
            assert call(notifications, "/events", event)[1] == {"created": False}
            original_orders = compose("ps", "-q", "orders").strip()
            compose(
                "up", "-d", "--wait", "--no-deps", "--force-recreate", "notifications"
            )
            notifications = ready("notifications")
            assert compose("ps", "-q", "orders").strip() == original_orders
            assert call(orders, "/bookings/" + booking_id)[0] == 200
            assert call(notifications, "/events", event)[1] == {"created": False}
            compose("down", "--remove-orphans")
            compose("up", "-d", "--wait", "db", "monolith", "orders", "notifications")
            mono = ready("monolith")
            orders = ready("orders")
            notifications = ready("notifications")
            assert call(mono, "/notifications/" + local_id)[0] == 200
            status, replay = call(orders, "/bookings", {"room_id": 1}, "service-first")
            assert status == 200 and replay["id"] == booking_id
            assert call(notifications, "/events", event)[1] == {"created": False}
            assert call(orders, "/bookings", {"room_id": 1}, "another-key")[0] == 409
            print(
                json.dumps(
                    dict(
                        monolithAtomic=True,
                        distributedEventuallyDelivered=True,
                        consumerRecreated=True,
                        ordersUnaffected=True,
                        persistentRestart=True,
                        eventReplayIdempotent=True,
                    )
                )
            )
        finally:
            compose("down", "--remove-orphans")
            result = subprocess.run(
                ["docker", "volume", "rm", volume], text=True, capture_output=True
            )
            if result.returncode and "no such volume" not in result.stderr.lower():
                raise RuntimeError("Fresh architecture test volume cleanup failed")


if __name__ == "__main__":
    main()
