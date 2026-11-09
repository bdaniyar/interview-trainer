"""Bounded, in-memory leases for one trusted local principal/controller."""
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
import logging
import secrets
from threading import Event, Lock, RLock, Thread
from time import monotonic
from uuid import uuid4

from .config import Settings
from .datasets import TABLES, load_dataset
from .docker_backend import QueryDeadline, SandboxUnavailable
from .executor import error_result
from .policy import PolicyError, validate

log = logging.getLogger(__name__)


class SessionError(RuntimeError):
    def __init__(self, status, code, message):
        super().__init__(message)
        self.status, self.code = status, code


@dataclass
class Session:
    id: str
    born: float
    touched: float
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    generation: int = 1
    handle: str | None = None
    status: str = "creating"
    cold_start_ms: int = 0
    tables: dict = field(default_factory=dict)
    lock: Lock = field(default_factory=Lock)


class Manager:
    def __init__(self, settings: Settings, backend, clock=monotonic):
        self.settings, self.backend, self.clock = settings, backend, clock
        self.dataset = load_dataset()
        self.sessions = {}
        self.registry = RLock()
        self.operation = Lock()
        self.stop_event = Event()
        self.thread = None

    def start(self):
        # In-memory leases cannot survive a controller restart. Only this
        # controller namespace is reaped; unrelated Docker resources are untouched.
        self.backend.reap(set())
        self.thread = Thread(target=self._reap_loop, name="sql-reaper", daemon=True)
        self.thread.start()

    def _reap_loop(self):
        while not self.stop_event.wait(self.settings.reap_seconds):
            try:
                self.reap()
            except Exception:
                log.warning("SQL reaper retry scheduled")

    def expiry(self, session):
        return min(session.touched + self.settings.idle_seconds,
                   session.born + self.settings.absolute_seconds)

    def info(self, session):
        return dict(session_id=session.id, generation=session.generation,
                    dataset_id=self.dataset.id, dataset_checksum=self.dataset.checksum,
                    postgres_major=17, created_at=session.created_at,
                    expires_at=datetime.now(timezone.utc) + timedelta(seconds=max(0, self.expiry(session) - self.clock())),
                    cold_start_ms=session.cold_start_ms)

    @contextmanager
    def admission(self):
        if self.stop_event.is_set():
            raise SessionError(503, "stopping", "SQL runner is stopping")
        if not self.operation.acquire(blocking=False):
            raise SessionError(409, "busy", "Another SQL operation is running; retry later")
        try:
            yield
        finally:
            self.operation.release()

    def _dispose(self, session, status):
        session.status = status
        session.tables.clear()
        if session.handle:
            try:
                self.backend.remove(session.handle)
                session.handle = None
            except Exception:
                # Retain the handle and capacity reservation until cleanup works.
                log.warning("SQL sandbox cleanup pending")

    def _provision(self, session):
        started = self.clock()
        try:
            session.handle = self.backend.create(session.id, session.generation)
            session.status = "active"
            session.touched = self.clock()
            session.tables = {secrets.token_urlsafe(24): table for table in TABLES}
            session.cold_start_ms = round((self.clock() - started) * 1000)
        except Exception:
            self._dispose(session, "failed")
            raise SessionError(503, "provision_failed", "Unable to initialize SQL sandbox") from None

    def create(self):
        with self.admission(), self.registry:
            try:
                self._reap_locked()
            except Exception:
                raise SessionError(503, "cleanup_pending", "SQL cleanup is pending; retry later") from None
            active = sum(s.status in {"creating", "active"} or s.handle is not None for s in self.sessions.values())
            try:
                live = self.backend.live_count()
            except Exception:
                raise SessionError(503, "docker_unavailable", "Docker is unavailable") from None
            if max(active, live) >= self.settings.max_sessions:
                raise SessionError(429, "capacity", "SQL session capacity reached; close an existing session")
            now = self.clock()
            session = Session(uuid4().hex, now, now)
            self.sessions[session.id] = session
            self._provision(session)
            return self.info(session)

    @contextmanager
    def lease(self, session_id, generation):
        with self.admission():
            with self.registry:
                session = self.sessions.get(session_id)
            if session is None:
                raise SessionError(404, "unknown_session", "Unknown SQL session")
            with session.lock:
                if session.status != "active":
                    raise SessionError(410, session.status, "SQL session is no longer available")
                if self.clock() >= self.expiry(session):
                    self._dispose(session, "expired")
                    raise SessionError(410, "expired", "SQL session expired; create another session")
                if session.generation != generation:
                    raise SessionError(409, "stale_generation", "Session was reset; refresh its generation")
                session.touched = self.clock()
                yield session
                if session.status == "active":
                    session.touched = self.clock()

    def _execute(self, session, operation, payload):
        try:
            result = self.backend.execute(session.handle, operation, payload)
        except QueryDeadline:
            self._dispose(session, "failed")
            result = error_result("resource", "query_deadline", "External query deadline exceeded; session closed")
        except Exception:
            self._dispose(session, "failed")
            raise SessionError(503, "sandbox_unavailable", "SQL sandbox failed; create another session") from None
        error = result.get("error")
        if error:
            code = error.get("sqlstate") or ""
            if code.startswith(("53", "57", "58", "08")) or code == "25P04" or error["kind"] == "infrastructure":
                self._dispose(session, "failed")
        return result

    def run(self, session_id, generation, query):
        with self.lease(session_id, generation) as session:
            try:
                validate(query)
            except PolicyError as exc:
                result = error_result("policy", exc.code, str(exc), sqlstate=exc.sqlstate, position=exc.position)
            else:
                result = self._execute(session, "run", {"sql": query})
            return dict(result, session_id=session.id, generation=session.generation)

    def catalog(self, session_id, generation):
        with self.lease(session_id, generation) as session:
            result = self._execute(session, "catalog", {})
            if result.get("error"):
                raise SessionError(503, "catalog_unavailable", "Catalog could not be read")
            reverse = {name: handle for handle, name in session.tables.items()}
            return dict(session_id=session.id, generation=session.generation,
                        tables=[dict(table, handle=reverse[table["name"]]) for table in result["tables"]])

    def browse(self, session_id, generation, handle, limit=50, offset=0):
        if not 1 <= limit <= 100 or not 0 <= offset <= 10000:
            raise SessionError(422, "browse_budget", "Browse limit must be 1–100 and offset 0–10000")
        with self.lease(session_id, generation) as session:
            if handle not in session.tables:
                raise SessionError(404, "unknown_table", "Unknown table handle for this session generation")
            result = self._execute(session, "browse", dict(table=session.tables[handle], limit=limit, offset=offset))
            return dict(result, session_id=session.id, generation=session.generation)

    def reset(self, session_id, generation):
        with self.lease(session_id, generation) as session:
            self._dispose(session, "resetting")
            if session.handle:
                raise SessionError(503, "cleanup_pending", "Old sandbox cleanup is pending")
            session.generation += 1
            # Reset replaces data but does not extend the absolute session lifetime.
            self._provision(session)
            return self.info(session)

    def close_session(self, session_id, generation):
        with self.admission(), self.registry:
            session = self.sessions.get(session_id)
            if session is None or (session.status == "closed" and session.handle is None):
                return
            if session.generation != generation:
                raise SessionError(409, "stale_generation", "Session was reset")
            self._dispose(session, "closed")

    def _reap_locked(self):
        for session in list(self.sessions.values()):
            if session.status == "active" and self.clock() >= self.expiry(session):
                self._dispose(session, "expired")
            elif session.status not in {"active", "creating"} and session.handle:
                self._dispose(session, session.status)
        known = {s.handle for s in self.sessions.values() if s.handle}
        self.backend.reap(known)
        # Bounded tombstones preserve useful 410 errors without a registry leak.
        terminal = [s.id for s in self.sessions.values() if s.handle is None and s.status != "creating"]
        for sid in terminal[:-128]:
            self.sessions.pop(sid, None)

    def reap(self):
        if self.operation.acquire(blocking=False):
            try:
                with self.registry:
                    self._reap_locked()
            finally:
                self.operation.release()

    def shutdown(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join(timeout=1)
        # API operations have bounded deadlines; the service lifespan waits for
        # them before closing. Each sandbox also has an independent PID1 TTL.
        with self.operation, self.registry:
            for session in self.sessions.values():
                self._dispose(session, "closed")
            self.backend.close()
