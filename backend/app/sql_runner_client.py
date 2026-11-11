"""Internal HTTP only; student SQL never connects to a database in the backend."""
import json
import os

import httpx
from pydantic import ValidationError

from .sql_schemas import RunnerGrade, RunnerSession, SqlCatalog, SqlResult


class SqlServiceError(RuntimeError):
    def __init__(self, status, code, message):
        self.status, self.code = status, code
        super().__init__(message)


MESSAGES = {
    404: ("unknown_session", "SQL-сессия не найдена. Создайте новую."),
    410: ("expired", "SQL-сессия завершена. Запрос сохранён в браузере."),
    409: ("busy", "SQL-сессия занята. Повторите действие после завершения запроса."),
    429: ("capacity", "Достигнут лимит SQL-сессий. Закройте SQL Lab в другой вкладке или дождитесь истечения сессии."),
    422: ("invalid_request", "SQL Runner отклонил параметры запроса."),
    413: ("request_size", "SQL-запрос слишком большой."),
}


class SQLRunnerClient:
    def __init__(self, url=None, transport=None):
        self.url = (url or os.getenv("SQL_RUNNER_URL", "http://sql-runner:8002")).rstrip("/")
        self.transport = transport

    async def request(self, method, path, model=None, *, body=None, params=None, cold=False, grading=False):
        timeout = httpx.Timeout(95 if grading else 35 if cold else 15, connect=3)
        try:
            async with httpx.AsyncClient(timeout=timeout, transport=self.transport, trust_env=False) as client:
                async with client.stream(method, self.url + path, json=body, params=params) as response:
                    wire = bytearray()
                    async for chunk in response.aiter_bytes():
                        if len(wire) + len(chunk) > 1024 * 1024 + 4096:
                            raise ValueError("Runner response budget")
                        wire.extend(chunk)
                    if response.status_code >= 400:
                        status = response.status_code if response.status_code in MESSAGES else 503
                        code, message = MESSAGES.get(status, ("runner_unavailable", "SQL Runner недоступен. Проверьте запуск сервисов и повторите."))
                        if status in (404, 409):
                            try:
                                runner_code = json.loads(wire).get("error", {}).get("code")
                                if status == 409 and runner_code == "stale_generation":
                                    code, message = "stale_generation", "SQL-сессия была сброшена. Создайте новую сессию."
                                if status == 404 and runner_code == "unknown_table":
                                    code, message = "unknown_table", "Таблица не найдена. Обновите схему базы."
                            except (ValueError, AttributeError):
                                pass
                        raise SqlServiceError(status, code, message)
                    if model is None:
                        if response.status_code != 204:
                            raise ValueError("Expected empty close response")
                        return None
                    return model.model_validate_json(wire)
        except SqlServiceError:
            raise
        except (httpx.HTTPError, ValueError, ValidationError):
            # Never relay internal tracebacks, Docker paths or arbitrary HTTP errors.
            raise SqlServiceError(503, "runner_unavailable", "SQL Runner недоступен. Проверьте запуск сервисов и повторите.") from None

    async def create(self):
        return await self.request("POST", "/v1/sessions", RunnerSession, body={"dataset_id": "shop-v1"}, cold=True)

    async def run(self, sid, generation, query):
        return await self.request("POST", f"/v1/sessions/{sid}/run", SqlResult,
                                  body={"generation": generation, "sql": query})

    async def catalog(self, sid, generation):
        return await self.request("GET", f"/v1/sessions/{sid}/catalog", SqlCatalog, params={"generation": generation})

    async def browse(self, sid, generation, handle, limit, offset):
        return await self.request("GET", f"/v1/sessions/{sid}/tables/{handle}/rows", SqlResult,
                                  params={"generation": generation, "limit": limit, "offset": offset})

    async def reset(self, sid, generation):
        return await self.request("POST", f"/v1/sessions/{sid}/reset", RunnerSession,
                                  body={"generation": generation}, cold=True)

    async def close(self, sid, generation):
        await self.request("DELETE", f"/v1/sessions/{sid}", params={"generation": generation})

    async def check(self, task, query):
        return await self.request("POST", "/v1/check", RunnerGrade, grading=True, body={
            "task_id": task["id"], "task_revision": task["revision"], "grader_revision": task["grader_revision"], "sql": query})
