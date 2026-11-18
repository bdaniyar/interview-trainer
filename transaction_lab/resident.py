"""Two student connections owned by a networkless sandbox process."""
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from threading import Event, Lock, Thread
from time import monotonic
import json
from select import select
import sys

import psycopg
from pglast.stream import RawStream

from sql_runner.app.executor import OutputError, json_bytes
from sql_runner.app.policy import PolicyError
from transaction_lab.execute import connect, snapshot, sql
from transaction_lab.policy import validate_script

# Public teaching output. The CLI retains its existing grading result budget.
EVENT_LIMIT = 96
EVENT_BYTES = 64 * 1024
# JSON can encode one ASCII control byte as a six-character unicode escape.
MESSAGE_BYTES = 6 * 32768 + 4096
WIRE_BYTES = 2 * 1024 * 1024


def student_statements(source):
    return [RawStream()(item.stmt) for item in validate_script(source)]


class Resident:
    def __init__(self):
        self.started = monotonic()
        self.lock = Lock()
        self.stop = Event()
        self.pool = ThreadPoolExecutor(max_workers=2)
        self.connections = {}
        self.states = {side: "ready" for side in "AB"}
        self.active = {}
        self.timeline = deque(maxlen=EVENT_LIMIT)
        self.sequence = 0
        self.visible = {}
        self.snapshot_requested = Event()

    def emit(self, side, phase, **fields):
        # All mutations, including increment of the sequence, hold self.lock.
        self.sequence += 1
        self.timeline.append(dict(sequence=self.sequence, ms=round(
            (monotonic() - self.started) * 1000), side=side, phase=phase, **fields))

    @staticmethod
    def state(conn):
        if conn.closed or conn.broken:
            return "disconnected"
        return {"IDLE": "ready", "INTRANS": "transaction",
                "INERROR": "failed"}.get(conn.info.transaction_status.name, "disconnected")

    def idle_state(self, conn):
        # PostgreSQL may close an idle transaction without a new client query.
        # Consume any pending server message only when this connection has no Run.
        if not conn.closed and not conn.broken and select([conn.fileno()], [], [], 0)[0]:
            try:
                conn.pgconn.consume_input()
            except psycopg.Error:
                conn.close()
        return self.state(conn)

    def observe(self):
        # The observer never shares a student connection with an executing query.
        # Only trusted PIDs from the resident connections reach pg_blocking_pids.
        try:
            with connect() as observer:
                while not self.stop.wait(0.05):
                    with self.lock:
                        pending = [(side, record["id"], record["pid"])
                                   for side, record in self.active.items()]
                        sides = {conn.info.backend_pid: side for side, conn in
                                 self.connections.items() if not conn.closed}
                    for side, op, pid in pending:
                        owners = observer.execute(
                            "SELECT pg_catalog.pg_blocking_pids(%s)", (pid,)
                        ).fetchone()[0]
                        blockers = sorted({sides[owner] for owner in owners if owner in sides})
                        with self.lock:
                            active = self.active.get(side)
                            if active and active["id"] == op and blockers != active["blockers"]:
                                active["blockers"] = blockers
                                phase = "blocked" if blockers else "released"
                                self.emit(side, phase, operation=op, blockers=blockers)
                    if self.snapshot_requested.is_set():
                        self.snapshot_requested.clear()
                        view = snapshot(observer)
                        with self.lock:
                            self.visible = {name: value for name, value in view.items()
                                            if len(json_bytes(value)) <= EVENT_BYTES}
                            self.emit("observer", "snapshot")
        except (psycopg.Error, OutputError):
            with self.lock:
                self.emit("observer", "error", code="observation_unavailable")

    def run(self, side, op, statements):
        with self.lock:
            record = self.active[side]
            conn = self.connections[side]
        try:
            if self.state(conn) == "disconnected":
                # Reconnect only between operations. Never silently retry a failed
                # statement or continue after PostgreSQL has rolled back a transaction.
                conn.close()
                conn = connect()
                with self.lock:
                    self.connections[side] = conn
                    record["pid"] = conn.info.backend_pid
                    self.emit(side, "reconnected", operation=op)
            for statement in statements:
                if record["cancelled"]:
                    break
                started = monotonic()
                with self.lock:
                    self.emit(side, "running", operation=op, statement=statement)
                try:
                    result = sql(conn, statement)
                    result["duration_ms"] = round((monotonic() - started) * 1000)
                    if len(json_bytes(result)) > EVENT_BYTES:
                        raise OutputError("Web output budget")
                    fields = {"result": result}
                    phase = "result"
                except OutputError:
                    fields, phase = {"code": "result_limit"}, "error"
                except psycopg.Error as exc:
                    state = exc.sqlstate
                    fields = {"code": "postgres", "sqlstate": state}
                    phase = "error"
                with self.lock:
                    self.states[side] = self.state(conn)
                    if record["blockers"]:
                        self.emit(side, "released", operation=op, blockers=[])
                        record["blockers"] = []
                    self.emit(side, phase, operation=op, state=self.states[side], **fields)
                # Separate Run is required for ROLLBACK after a failed batch.
                if phase == "error":
                    break
        except psycopg.Error:
            with self.lock:
                self.emit(side, "error", operation=op, code="connection_closed")
        finally:
            with self.lock:
                self.states[side] = self.state(conn)
                if record["cancelled"]:
                    self.emit(side, "cancelled", operation=op, state=self.states[side])
                self.active.pop(side)

    def request(self, item):
        action = item["action"]
        if action == "status":
            with self.lock:
                for side in "AB":
                    if side not in self.active:
                        self.states[side] = self.idle_state(self.connections[side])
                events = [event for event in self.timeline if event["sequence"] > item["after"]][:12]
                return dict(states=self.states.copy(), pending={
                    side: {"operation": record["id"], "blockers": record["blockers"],
                           "cancelled": record["cancelled"]}
                    for side, record in self.active.items()
                }, timeline=events, tables=self.visible, sequence=self.sequence)
        if action == "snapshot":
            self.snapshot_requested.set()
            return {"accepted": True}
        side, op = item["side"], item["operation"]
        if side not in ("A", "B"):
            return {"error": "invalid"}
        if action == "run":
            try:
                statements = student_statements(item["sql"])
            except (PolicyError, ValueError):
                return {"error": "policy"}
            if sum(len(statement.encode()) for statement in statements) > 32768:
                return {"error": "policy"}
            with self.lock:
                if side in self.active:
                    return {"error": "busy"}
                conn = self.connections[side]
                self.active[side] = {"id": op, "pid": conn.info.backend_pid if not conn.closed else 0,
                                     "blockers": [], "cancelled": False}
                self.pool.submit(self.run, side, op, statements)
            return {"operation": op}
        if action == "cancel":
            with self.lock:
                record = self.active.get(side)
                if not record or record["id"] != op:
                    return {"error": "operation_gone"}
                record["cancelled"] = True
                conn = self.connections[side]
                # Holding the admission lock prevents cancellation of a later Run.
                try:
                    conn.cancel_safe(timeout=0.4)
                except psycopg.Error:
                    pass  # PostgreSQL's statement deadline still bounds the command.
            return {"accepted": True}
        return {"error": "invalid"}

    def serve(self, inbox, outbox):
        try:
            for side in "AB":
                self.connections[side] = connect()
            if len({conn.info.backend_pid for conn in self.connections.values()}) != 2:
                raise RuntimeError("Expected two independent backends")
            observer = Thread(target=self.observe, daemon=True)
            observer.start()
            outbox.write(b'{"ready":true}\n')
            outbox.flush()
            while line := inbox.readline(MESSAGE_BYTES + 1):
                if len(line) > MESSAGE_BYTES or not line.endswith(b"\n"):
                    break
                response = json_bytes(self.request(json.loads(line)))
                if len(response) > WIRE_BYTES:
                    response = b'{"error":"result_limit"}'
                outbox.write(response + b"\n")
                outbox.flush()
        finally:
            self.stop.set()
            self.pool.shutdown(wait=True, cancel_futures=True)
            for conn in self.connections.values():
                conn.close()


if __name__ == "__main__":
    Resident().serve(sys.stdin.buffer, sys.stdout.buffer)
