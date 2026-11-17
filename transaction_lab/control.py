"""Local trusted coordinator; only this process may contact Docker."""

from contextlib import contextmanager
import json
import docker
from collections import Counter
from time import monotonic
from threading import Event
from uuid import uuid4

from sql_runner.app.config import Settings, PYTHON
from sql_runner.app.comparator import compare
from sql_runner.app.docker_backend import DockerBackend, SandboxUnavailable
from transaction_lab.fixtures import DML_CASES, BOOK_CASES
from transaction_lab.policy import validate_script
from transaction_lab.version import fingerprint

IMAGE = "pythoria-transaction-sandbox:phase8b"
SCENARIOS = {
    "read-committed",
    "repeatable-read",
    "mvcc",
    "rollback-savepoint",
    "nowait",
    "skip-locked",
    "blocking-update",
    "deadlock",
    "serializable",
    "lost-update",
    "indexes",
    "exclusion",
}
DML_REFERENCE = "UPDATE orders SET status='paid' WHERE id=10 RETURNING id,status;"
BOOKING_REFERENCE = """BEGIN;
WITH claimed AS (
 UPDATE inventory SET available=available-1 WHERE id=1 AND available>0 RETURNING id
)
INSERT INTO reservations(request_key,room_id)
SELECT 'REQUEST_KEY',id FROM claimed RETURNING request_key,room_id;
COMMIT;"""


class TransactionBackend(DockerBackend):
    def __init__(self, settings):
        super().__init__(settings, client=docker.from_env(timeout=25))

    def create(self, *args, **kwargs):
        handle = super().create(*args, **kwargs)
        try:
            deadline = monotonic() + 5
            while monotonic() < deadline:
                response = self.client.containers.get(handle).exec_run(
                    ["test", "-f", "/pgdata/tx-ready"], user="postgres"
                )
                if response.exit_code == 0:
                    return handle
                Event().wait(0.03)
            raise SandboxUnavailable("Transaction bootstrap unavailable")
        except Exception:
            self.remove(handle)
            raise

    def execute(self, handle, operation, payload):
        if operation not in {"script", "booking", "scenario"}:
            raise ValueError("Unknown transaction operation")
        if operation == "scenario":
            if payload.get("scenario") not in SCENARIOS:
                raise ValueError("Unknown controlled scenario")
        else:
            validate_script(payload["sql"])
        return self._command(
            handle,
            "transaction_lab.execute",
            [json.dumps(payload | {"operation": operation})],
            student=True,
        )

    def install_case(self, handle, kind, case):
        if kind not in {"dml", "booking"} or case not in (
            DML_CASES if kind == "dml" else BOOK_CASES
        ):
            raise ValueError("Unknown trusted fixture")
        return self._command(
            handle, "transaction_lab.fixtures", [kind, case], student=False
        )

    def _command(self, handle, module, args, *, student):
        def work():
            response = self.client.containers.get(handle).exec_run(
                [PYTHON, "-m", module, *args],
                user="65532:65532" if student else "postgres",
                demux=True,
            )
            stdout, _ = response.output
            if response.exit_code != 0 or not stdout or len(stdout) > 1024 * 1024:
                raise SandboxUnavailable("Transaction execution failed")
            return json.loads(stdout)

        return self._bounded(work, handle)


@contextmanager
def attempt(namespace=None):
    backend = TransactionBackend(
        Settings(
            image=IMAGE,
            namespace=namespace or "tx-" + uuid4().hex[:12],
            absolute_seconds=60,
            query_seconds=20,
        )
    )
    handle = None
    try:
        handle = backend.create("attempt", 1, lifetime=60)
        version = backend._command(handle, "transaction_lab.version", [], student=True)
        if version != {"profile": "pg-transaction-v1", "fingerprint": fingerprint()}:
            raise SandboxUnavailable(
                "Rebuild the transaction image: profile fingerprint differs"
            )
        yield backend, handle
    finally:
        try:
            if handle:
                backend.remove(handle)
            backend.reap(set())
        finally:
            backend.close()


def outputs(trace):
    return [e["result"] for e in trace if e.get("result", {}).get("columns")]


def valid_dml(result):
    if result.get("error"):
        return False
    before = result["before"]
    after = result["after"]
    if any(
        v["truncated"] or v["has_more"]
        for state in [before, after]
        for v in state.values()
    ):
        return False
    expected = [list(row) for row in before["orders"]["rows"]]
    returned = []
    for row in expected:
        if row[0] == "10":
            row[2] = "paid"
            returned.append([row[0], row[2]])
    for table in before:
        if after[table]["columns"] != before[table]["columns"]:
            return False
        if after[table]["rows"] != (
            expected if table == "orders" else before[table]["rows"]
        ):
            return False
    values = outputs(result["timeline"])
    expected_result = dict(
        columns=[before["orders"]["columns"][0], before["orders"]["columns"][2]],
        rows=returned,
        rows_returned=len(returned),
        error=None,
        truncated=False,
        has_more=False,
    )
    return (
        bool(values)
        and compare(expected_result, values[-1], numeric_compatible=True) == "passed"
        and not any("sqlstate" in e or "cleanup" in e for e in result["timeline"])
    )


def valid_booking(result):
    if result.get("error"):
        return False
    before = result["before"]
    after = result["after"]
    if any(
        v["truncated"] or v["has_more"]
        for state in [before, after]
        for v in state.values()
    ):
        return False
    for table in ["users", "orders", "products", "order_items", "slots"]:
        if before[table]["rows"] != after[table]["rows"]:
            return False
    old_inventory = {row[0]: row[1] for row in before["inventory"]["rows"]}
    new_inventory = {row[0]: row[1] for row in after["inventory"]["rows"]}
    new_rows = [
        row
        for row in after["reservations"]["rows"]
        if row not in before["reservations"]["rows"]
    ]
    expected_count = min(1, int(old_inventory.get("1", "0")))
    if len(new_rows) != expected_count or any(
        row[0] not in {"request-A", "request-B"} or row[1:] != ["1", True]
        for row in new_rows
    ):
        return False
    if any(
        row not in after["reservations"]["rows"]
        for row in before["reservations"]["rows"]
    ):
        return False
    expected_inventory = dict(old_inventory)
    if "1" in expected_inventory:
        expected_inventory["1"] = str(int(expected_inventory["1"]) - expected_count)
    if new_inventory != expected_inventory:
        return False
    returned = []
    for trace in result["requests"]:
        for entry in trace:
            if "cleanup" in entry:
                return False
            if entry.get("sqlstate") not in (None, "23505", "40001", "55P03"):
                return False
        values = outputs(trace)
        if not values:
            if not any(
                entry.get("sqlstate") in {"23505", "40001", "55P03"} for entry in trace
            ):
                return False
            continue
        last = values[-1]
        if (
            [c["name"] for c in last["columns"]] != ["request_key", "room_id"]
            or last["columns"][0]["pg_type"] not in {"text", "varchar", "bpchar"}
            or last["columns"][1]["pg_type"] not in {"int2", "int4", "int8"}
        ):
            return False
        returned.extend(last["rows"])
    return Counter(tuple(row) for row in returned) == Counter(
        tuple(row[:2]) for row in new_rows
    )


def check(kind, source):
    if kind not in {"dml", "booking"}:
        raise ValueError("Unknown exercise")
    validate_script(source)  # Fail before provisioning on policy errors.
    cases = DML_CASES if kind == "dml" else BOOK_CASES
    count = 0
    for case in cases:
        with attempt() as (backend, handle):
            backend.install_case(handle, kind, case)
            result = backend.execute(
                handle, "script" if kind == "dml" else "booking", {"sql": source}
            )
            if result.get("error") in {
                "OperationalError",
                "InterfaceError",
                "RuntimeError",
            } or str(result.get("sqlstate") or "").startswith(("08", "58", "57P")):
                raise SandboxUnavailable(
                    "Transaction infrastructure failed; retry later"
                )
            count += bool((valid_dml if kind == "dml" else valid_booking)(result))
    return dict(
        profile="pg-transaction-v1",
        task_id=(
            "pg.write.10.25.status-v1" if kind == "dml" else "pg.tx.11.17.booking-v1"
        ),
        revision=1,
        passed=count == len(cases),
        tests_passed=count,
        tests_total=len(cases),
        feedback=(
            "Проверьте возвращённые строки, итог всех таблиц и границы транзакции."
            if count < len(cases)
            else "Все проверки пройдены."
        ),
        xp_awarded=0,
    )
