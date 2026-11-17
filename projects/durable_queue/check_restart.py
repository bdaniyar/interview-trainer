"""Trusted host smoke: restart a fresh dev-volume project, never Pythoria data."""

import json
from pathlib import Path
import subprocess
import socket
import tempfile
from threading import Event
from time import monotonic
from urllib.request import Request, urlopen
from uuid import UUID, uuid4


def main():
    original = Path(__file__).with_name("compose.yml")
    project = "pythoria-queue-restart-" + uuid4().hex[:10]
    volume = project + "_queue_data"
    assert (
        volume.startswith("pythoria-queue-restart-")
        and volume != "pythoria_pythoria_data"
    )
    config = json.loads(
        subprocess.check_output(
            ["docker", "compose", "-f", str(original), "config", "--format", "json"],
            text=True,
        )
    )
    config["name"] = project
    for key, network in config.get("networks", {}).items():
        network["name"] = project + "_" + key
    config["volumes"]["queue_data"]["name"] = volume
    with socket.socket() as reserved:
        reserved.bind(("127.0.0.1", 0))
        published = reserved.getsockname()[1]
    for port in config["services"]["api"]["ports"]:
        port["published"] = str(published)
        port["host_ip"] = "127.0.0.1"
    with tempfile.TemporaryDirectory(prefix="pythoria-queue-restart-") as temporary:
        path = Path(temporary) / "compose.json"
        path.write_text(json.dumps(config))
        command = ["docker", "compose", "-p", project, "-f", str(path)]

        def compose(*args):
            return subprocess.check_output(
                command + list(args), text=True, stderr=subprocess.STDOUT
            )

        def url():
            address = compose("port", "api", "8000").strip()
            assert address.startswith("127.0.0.1:"), repr(address)
            return "http://" + address

        def call(base, route, body=None):
            request = Request(
                base + route,
                data=json.dumps(body).encode() if body is not None else None,
                headers={
                    "Content-Type": "application/json",
                    "Idempotency-Key": "durable-volume-check",
                },
            )
            with urlopen(request, timeout=5) as response:
                return response.status, json.load(response)

        def available():
            end = monotonic() + 20
            while True:
                base = url()
                try:
                    if call(base, "/health")[0] == 200:
                        return base
                except OSError:
                    pass
                assert monotonic() < end, "API startup deadline"
                Event().wait(0.05)

        try:
            compose("build", "api")
            compose("up", "-d", "--wait", "db", "api")
            base = available()
            body = {"payload": {"n": 5}}
            status, job = call(base, "/jobs", body)
            assert status == 201 and job["state"] == "queued"
            job_id = str(UUID(job["id"]))
            compose("down", "--remove-orphans")  # Keep only this fresh volume.
            compose("up", "-d", "--wait", "db", "api")
            base = available()
            assert call(base, "/jobs/" + job_id)[1]["state"] == "queued"
            status, replay = call(base, "/jobs", body)
            assert status == 200 and replay["id"] == job_id
            compose("up", "-d", "--scale", "worker=2", "worker", "relay")
            end = monotonic() + 25
            while True:
                result = call(base, "/jobs/" + job_id)[1]
                if result["state"] == "succeeded":
                    break
                assert monotonic() < end, "Worker completion deadline"
                Event().wait(0.05)
            assert result["result"] == {"sum_squares": 55}
            query = (
                "SELECT (SELECT count(*) FROM effects WHERE job_id='"
                + job_id
                + "'),(SELECT count(*) FROM outbox WHERE job_id='"
                + job_id
                + "' AND delivered)"
            )
            while True:
                observed = compose(
                    "exec",
                    "-T",
                    "db",
                    "psql",
                    "-U",
                    "postgres",
                    "-d",
                    "queue_lab",
                    "-tAc",
                    query,
                ).strip()
                if observed == "1|1":
                    break
                assert monotonic() < end, "Outbox delivery deadline"
                Event().wait(0.05)
            assert call(base, "/jobs", body)[0] == 200
            print(
                json.dumps(
                    dict(
                        persistentRestart=True,
                        idempotentReplay=True,
                        workers=2,
                        result=55,
                        effects=1,
                        outboxDelivered=1,
                    )
                )
            )
        finally:
            compose("down", "--remove-orphans")
            result = subprocess.run(
                ["docker", "volume", "rm", volume], capture_output=True, text=True
            )
            if result.returncode and "no such volume" not in result.stderr.lower():
                raise RuntimeError("Fresh restart-test volume cleanup failed")


if __name__ == "__main__":
    main()
