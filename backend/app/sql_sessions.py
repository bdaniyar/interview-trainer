"""Ephemeral bindings for one server-owned local principal, without SQLite writes."""
import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
import logging
import re
from uuid import uuid4

from .sql_content import public_lesson
from .sql_runner_client import SQLRunnerClient, SqlServiceError
from .sql_schemas import RunnerSession, SqlSession

log = logging.getLogger(__name__)
LOCAL_PRINCIPAL = "local"
OPAQUE_HANDLE = re.compile(r"^[A-Za-z0-9_-]{1,128}$")


@dataclass
class Binding:
    public_id: str
    lesson_id: str
    lesson_slug: str
    info: RunnerSession
    owner: str = LOCAL_PRINCIPAL
    lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    closing: bool = False

    def public(self):
        return SqlSession(**(self.info.model_dump() | {"session_id": self.public_id}),
                          lesson_id=self.lesson_id, lesson_slug=self.lesson_slug,
                          task_id=public_lesson(self.lesson_slug).task_id)


class SQLSessions:
    def __init__(self, client=None):
        self.client = client or SQLRunnerClient()
        self.bindings = {}
        self.creation_lock = asyncio.Lock()
        self.reaper = None

    def start(self):
        self.reaper = asyncio.create_task(self._reap_loop())

    async def _delete(self, binding):
        binding.closing = True
        try:
            await self.client.close(binding.info.session_id, binding.info.generation)
        except SqlServiceError as error:
            if error.status not in (404, 410):
                raise
        self.bindings.pop(binding.public_id, None)

    async def reap(self):
        now = datetime.now(timezone.utc)
        for binding in list(self.bindings.values()):
            if not binding.lock.locked() and (binding.closing or binding.info.expires_at <= now):
                async with binding.lock:
                    try:
                        await self._delete(binding)
                    except SqlServiceError:
                        log.warning("SQL lease cleanup will be retried")

    async def _reap_loop(self):
        while True:
            await asyncio.sleep(30)
            await self.reap()

    async def shutdown(self):
        if self.reaper:
            self.reaper.cancel()
            try:
                await self.reaper
            except asyncio.CancelledError:
                pass
        for binding in list(self.bindings.values()):
            async with binding.lock:
                try:
                    await self._delete(binding)
                except SqlServiceError:
                    log.warning("SQL lease cleanup deferred to runner TTL")

    async def create(self, slug):
        lesson = public_lesson(slug)
        if self.creation_lock.locked():
            raise SqlServiceError(409, "busy", "Создание SQL-сессии уже выполняется.")
        async with self.creation_lock:
            await self.reap()
            if len(self.bindings) >= 2:
                raise SqlServiceError(429, "capacity", "Закройте SQL Lab в другой вкладке или дождитесь завершения сессии.")
            info = await self.client.create()
            if not OPAQUE_HANDLE.fullmatch(info.session_id):
                raise SqlServiceError(503, "runner_protocol", "SQL Runner вернул некорректную сессию.")
            binding = Binding(uuid4().hex, lesson.lesson_id, lesson.lesson_slug, info)
            self.bindings[binding.public_id] = binding
            return binding.public()

    @asynccontextmanager
    async def lease(self, sid, generation):
        binding = self.bindings.get(sid)
        if binding is None or binding.owner != LOCAL_PRINCIPAL:
            raise SqlServiceError(404, "unknown_session", "SQL-сессия не найдена. Создайте новую.")
        if binding.lock.locked():
            raise SqlServiceError(409, "busy", "SQL-сессия занята. Дождитесь завершения операции.")
        async with binding.lock:
            if binding.closing:
                raise SqlServiceError(410, "expired", "SQL-сессия завершена. Создайте новую.")
            if binding.info.generation != generation:
                raise SqlServiceError(409, "stale_generation", "SQL-сессия была сброшена. Обновите её состояние.")
            public_lesson(binding.lesson_slug)  # still enabled and bound on the server
            if binding.info.expires_at <= datetime.now(timezone.utc):
                try:
                    await self._delete(binding)
                except SqlServiceError:
                    pass
                raise SqlServiceError(410, "expired", "SQL-сессия истекла. Запрос остался в браузере.")
            try:
                yield binding
            except SqlServiceError as error:
                if error.status == 410 or (error.status == 404 and error.code != "unknown_table"):
                    self.bindings.pop(sid, None)
                raise
            else:
                # Phase 1 has a fixed 15 min idle / 30 min absolute profile.
                binding.info.expires_at = min(datetime.now(timezone.utc) + timedelta(minutes=15),
                                               binding.info.created_at + timedelta(minutes=30))

    def public_output(self, binding, result):
        if result.session_id != binding.info.session_id or result.generation != binding.info.generation:
            raise SqlServiceError(503, "runner_protocol", "Ответ SQL Runner относится к другой сессии.")
        result.session_id = binding.public_id
        return result

    async def run(self, sid, generation, query):
        async with self.lease(sid, generation) as binding:
            result = self.public_output(binding, await self.client.run(binding.info.session_id, generation, query))
            result.session_closed = False  # public lifecycle state is derived here
            if result.error:
                code = result.error.sqlstate or ""
                if (code.startswith(("53", "57", "58", "08")) or code == "25P04"
                        or result.error.kind == "infrastructure" or result.error.code == "query_deadline"):
                    result.session_closed = True
                    self.bindings.pop(sid, None)
            return result

    async def catalog(self, sid, generation):
        async with self.lease(sid, generation) as binding:
            return self.public_output(binding, await self.client.catalog(binding.info.session_id, generation))

    async def browse(self, sid, generation, handle, limit, offset):
        if not OPAQUE_HANDLE.fullmatch(handle):
            raise SqlServiceError(404, "unknown_table", "Неизвестная таблица SQL-сессии.")
        async with self.lease(sid, generation) as binding:
            return self.public_output(binding, await self.client.browse(binding.info.session_id, generation, handle, limit, offset))

    async def reset(self, sid, generation):
        async with self.lease(sid, generation) as binding:
            try:
                info = await self.client.reset(binding.info.session_id, generation)
            except SqlServiceError as error:
                if error.status != 409:
                    self.bindings.pop(sid, None)
                raise
            if info.session_id != binding.info.session_id or info.generation != generation + 1:
                raise SqlServiceError(503, "runner_protocol", "Некорректное поколение SQL-сессии.")
            binding.info = info
            return binding.public()

    async def close(self, sid, generation):
        binding = self.bindings.get(sid)
        if binding is None or binding.owner != LOCAL_PRINCIPAL:
            return
        if binding.lock.locked():
            raise SqlServiceError(409, "busy", "SQL-сессия занята.")
        async with binding.lock:
            if binding.info.generation != generation:
                raise SqlServiceError(409, "stale_generation", "SQL-сессия была сброшена.")
            await self._delete(binding)
