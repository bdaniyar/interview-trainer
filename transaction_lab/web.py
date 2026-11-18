"""Private single-process controller for the Pythoria web Transaction Lab."""
from contextlib import asynccontextmanager, contextmanager
from dataclasses import dataclass
import logging
import os
from threading import Event, Lock, Thread
from time import monotonic
from typing import Literal
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from starlette.concurrency import run_in_threadpool

from sql_runner.app.config import Settings
from sql_runner.app.docker_backend import SandboxUnavailable
from sql_runner.app.policy import PolicyError
from transaction_lab.control import IMAGE, SCENARIOS, TransactionBackend, attempt, check
from transaction_lab.version import fingerprint
from transaction_lab.wire import ResidentWire

log = logging.getLogger(__name__)


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Scope(Input):
    slug: str = Field(pattern=r"^[a-z0-9-]{1,100}$")
    kind: Literal["dml", "booking", "practice"]


class Command(Scope):
    generation: int = Field(ge=1)
    action: Literal["status", "run", "cancel", "snapshot", "reset", "close"]
    side: Literal["A", "B"] = "A"
    operation: UUID | None = None
    after: int = Field(default=0, ge=0)
    sql: str = Field(default="", max_length=32768)


class Grading(Input):
    kind: Literal["dml", "booking"]
    sql: str = Field(min_length=1, max_length=32768)


class Scenario(Input):
    name: str = Field(max_length=80)


@dataclass
class Workspace:
    sid: UUID
    generation: int
    scope: Scope
    handle: str
    wire: ResidentWire
    deadline: float

    def public(self):
        return {"session_id": str(self.sid), "generation": self.generation,
                "remaining_ms": max(0, round((self.deadline - monotonic()) * 1000))}


class Coordinator:
    def __init__(self, namespace, *, lifetime=60):
        self.settings = Settings(image=IMAGE, namespace=namespace, absolute_seconds=lifetime,
                                 query_seconds=20)
        self.backend = None
        self.workspace = None
        self.sessions = Lock()
        self.mutations = Lock()
        self.grades = Lock()
        self.grade_namespace = f"{namespace}-grade"

    @contextmanager
    def admitted(self, gate):
        if not gate.acquire(blocking=False):
            raise HTTPException(409, "busy")
        try:
            yield
        finally:
            gate.release()

    def get_backend(self):
        if self.backend is None:
            self.backend = TransactionBackend(self.settings)
            self.backend.reap(set())
        return self.backend

    def discard(self):
        old, self.workspace = self.workspace, None
        if old:
            try:
                old.wire.close()
            finally:
                self.backend.remove(old.handle)

    def open(self, scope, *, sid=None, generation=1):
        backend = self.get_backend()
        # Reap a previous controller's containers and any incomplete cleanup.
        backend.reap(set())
        sid = sid or uuid4()
        deadline = monotonic() + self.settings.absolute_seconds
        handle = backend.create(sid.hex, generation, lifetime=self.settings.absolute_seconds)
        try:
            if backend._command(handle, "transaction_lab.version", [], student=True) != {
                "profile": "pg-transaction-v1", "fingerprint": fingerprint()
            }:
                raise SandboxUnavailable("Transaction image mismatch")
            if scope.kind != "practice":
                backend.install_case(handle, scope.kind, "public")
            wire = ResidentWire(backend.client, handle)
        except Exception:
            backend.remove(handle)
            raise
        self.workspace = Workspace(sid, generation, scope, handle, wire, deadline)
        return self.workspace.public()

    def create(self, scope):
        with self.workspace_access():
            if self.workspace and self.workspace.deadline > monotonic():
                raise HTTPException(409, "workspace_active")
            self.discard()
            return self.open(scope)

    @contextmanager
    def workspace_access(self, *, poll=False):
        if poll:
            with self.admitted(self.sessions):
                yield
        else:
            # At most one mutation can wait for an in-flight, bounded wire poll.
            # A status poll must not cause a learner's Run or COMMIT to be dropped.
            with self.admitted(self.mutations), self.sessions:
                yield

    def command(self, sid, payload):
        with self.workspace_access(poll=payload.action == "status"):
            workspace = self.workspace
            if not workspace or workspace.sid != sid:
                raise HTTPException(410, "session_closed")
            if (workspace.scope.slug, workspace.scope.kind, workspace.generation) != (
                payload.slug, payload.kind, payload.generation
            ):
                raise HTTPException(409, "stale_session")
            if workspace.deadline <= monotonic():
                self.discard()
                raise HTTPException(410, "session_closed")
            if payload.action in ("reset", "close"):
                self.discard()
                if payload.action == "close":
                    return {"closed": True}
                return self.open(workspace.scope, sid=sid, generation=workspace.generation + 1)
            operation = uuid4() if payload.action == "run" else payload.operation
            data = payload.model_dump(include={"action", "side", "after", "sql"})
            data["operation"] = str(operation) if operation is not None else None
            if payload.action == "run" and len(payload.sql.encode("utf-8")) > 32768:
                raise HTTPException(422, "policy")
            try:
                result = workspace.wire.request(data)
            except Exception:
                self.discard()
                raise HTTPException(410, "session_closed") from None
            if code := result.get("error"):
                raise HTTPException({"busy": 409, "operation_gone": 409, "policy": 422}.get(code, 503), code)
            return result | workspace.public()

    def expire(self):
        if self.sessions.acquire(blocking=False):
            try:
                if self.workspace and self.workspace.deadline <= monotonic():
                    self.discard()
            finally:
                self.sessions.release()

    def cleanup_startup(self):
        with self.sessions:
            self.get_backend()
        with self.grades:
            orphan_backend = TransactionBackend(Settings(image=IMAGE, namespace=self.grade_namespace))
            try:
                orphan_backend.reap(set())
            finally:
                orphan_backend.close()

    def grade(self, payload):
        with self.admitted(self.grades):
            return check(payload.kind, payload.sql, namespace=self.grade_namespace)

    def scenario(self, name):
        if name not in SCENARIOS:
            raise HTTPException(404, "invalid_scenario")
        with self.admitted(self.grades):
            with attempt(self.grade_namespace) as (backend, handle):
                result = backend.execute(handle, "scenario", {"scenario": name})
                if "error" in result:
                    raise SandboxUnavailable("Controlled scenario failed")
                return result

    def shutdown(self):
        with self.sessions:
            try:
                self.discard()
            finally:
                if self.backend:
                    self.backend.close()


def controller():
    return Coordinator(os.getenv("TX_RUNNER_NAMESPACE", "pythoria-tx-local"))


@asynccontextmanager
async def lifespan(app):
    app.state.tx = coordinator = controller()
    stop = Event()

    def reaper():
        try:
            coordinator.cleanup_startup()
        except Exception:
            # Docker may start after the HTTP service. Create retries discovery,
            # and old containers keep their independent watchdogs.
            pass
        while not stop.wait(1):
            try:
                coordinator.expire()
            except Exception:
                # The independent container watchdog still removes abandoned state.
                continue

    worker = Thread(target=reaper, daemon=True)
    worker.start()
    try:
        yield
    finally:
        stop.set()
        await run_in_threadpool(coordinator.shutdown)


app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)


@app.get("/health")
def health():
    return {"status": "ok", "profile": "pg-transaction-v1"}


def safe(call, *args):
    try:
        return call(*args)
    except PolicyError:
        raise HTTPException(422, "policy") from None
    except HTTPException:
        raise
    except Exception as error:
        cause = error
        chain = []
        while cause is not None and len(chain) < 5:
            chain.append(type(cause).__name__)
            cause = cause.__cause__
        description = str(error) if isinstance(error, SandboxUnavailable) else ""
        log.warning("Transaction %s failed (%s): %s", call.__name__, "/".join(chain), description)
        raise HTTPException(503, "runner_unavailable") from None


@app.post("/sessions", status_code=201)
def create(payload: Scope):
    return safe(app.state.tx.create, payload)


@app.post("/sessions/{sid}")
def command(sid: UUID, payload: Command):
    return safe(app.state.tx.command, sid, payload)


@app.post("/grade")
def grade(payload: Grading):
    return safe(app.state.tx.grade, payload)


@app.post("/scenario")
def scenario(payload: Scenario):
    return safe(app.state.tx.scenario, payload.name)
