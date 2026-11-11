from fastapi import APIRouter, Depends, Query, Request, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .sql_content import public_lesson
from .database import get_db
from .sql_progress import completed
from .sql_schemas import SqlCatalog, SqlCheck, SqlCheckResult, SqlCreate, SqlGeneration, SqlLesson, SqlResult, SqlRun, SqlSession

router = APIRouter(prefix="/api/sql", tags=["SQL Lab"])


class SQLBodyLimit:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or not scope["path"].startswith("/api/sql/"):
            return await self.app(scope, receive, send)
        parts, size = [], 0
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            size += len(message.get("body", b""))
            if size > 256 * 1024:
                return await JSONResponse({"error": {"code": "request_size", "message": "SQL-запрос слишком большой."}},
                                          status_code=413)(scope, receive, send)
            parts.append(message.get("body", b""))
            if not message.get("more_body", False):
                break
        consumed = False

        async def replay():
            nonlocal consumed
            if not consumed:
                consumed = True
                return {"type": "http.request", "body": b"".join(parts), "more_body": False}
            return await receive()

        await self.app(scope, replay, send)


def sessions(request):
    return request.app.state.sql_sessions


@router.get("/lessons/{slug}", response_model=SqlLesson)
def lesson(slug: str, db: Session = Depends(get_db)):
    manifest = public_lesson(slug)
    manifest.completed = completed(db, manifest.task_id)
    return manifest


@router.post("/lessons/{slug}/tasks/{task_id}/check", response_model=SqlCheckResult)
async def check(slug: str, task_id: str, payload: SqlCheck, request: Request):
    return await request.app.state.sql_checks.check(slug, task_id, payload)


@router.post("/sessions", response_model=SqlSession, status_code=201)
async def create(payload: SqlCreate, request: Request):
    return await sessions(request).create(payload.lesson_slug)


@router.post("/sessions/{sid}/run", response_model=SqlResult)
async def run(sid: str, payload: SqlRun, request: Request):
    return await sessions(request).run(sid, payload.generation, payload.sql)


@router.get("/sessions/{sid}/catalog", response_model=SqlCatalog)
async def catalog(sid: str, request: Request, generation: int = Query(ge=1)):
    return await sessions(request).catalog(sid, generation)


@router.get("/sessions/{sid}/tables/{handle}/rows", response_model=SqlResult)
async def browse(sid: str, handle: str, request: Request, generation: int = Query(ge=1),
                 limit: int = Query(default=50, ge=1, le=100), offset: int = Query(default=0, ge=0, le=10000)):
    return await sessions(request).browse(sid, generation, handle, limit, offset)


@router.post("/sessions/{sid}/reset", response_model=SqlSession)
async def reset(sid: str, payload: SqlGeneration, request: Request):
    return await sessions(request).reset(sid, payload.generation)


@router.delete("/sessions/{sid}", status_code=204)
async def close(sid: str, request: Request, generation: int = Query(ge=1)):
    await sessions(request).close(sid, generation)
    return Response(status_code=204)
