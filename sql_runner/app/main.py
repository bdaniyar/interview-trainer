from contextlib import asynccontextmanager

from fastapi import FastAPI, Query, Request, Response
from fastapi.responses import JSONResponse

from .config import Settings
from .docker_backend import DockerBackend
from .lifecycle import Manager, SessionError
from .schemas import Catalog, CreateSession, Generation, Result, Run, SessionInfo


class BodyLimit:
    """Bound request memory even for chunked JSON before Pydantic parses it."""
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        parts, size = [], 0
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            size += len(message.get("body", b""))
            if size > 256 * 1024:  # accommodates escaped Unicode; SQL itself <=32KiB
                response = JSONResponse({"error": {"code": "request_size", "message": "Request body too large"}}, status_code=413)
                return await response(scope, receive, send)
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


def create_app(settings=None, backend_factory=DockerBackend):
    settings = settings or Settings.from_env()

    @asynccontextmanager
    async def lifespan(app):
        manager = Manager(settings, backend_factory(settings))
        try:
            manager.start()
            app.state.manager = manager
            yield
        finally:
            manager.shutdown()

    app = FastAPI(title="Pythoria SQL Runner", version="1.0", lifespan=lifespan)
    app.add_middleware(BodyLimit)

    @app.exception_handler(SessionError)
    async def session_error(request, exc):
        return JSONResponse({"error": {"code": exc.code, "message": str(exc)}}, status_code=exc.status)

    # Pydantic's default error includes the entire rejected input. Keep it bounded
    # and avoid echoing untrusted SQL or payloads in validation diagnostics.
    from fastapi.exceptions import RequestValidationError

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, exc):
        return JSONResponse({"error": {"code": "invalid_request", "message": "Invalid SQL runner request"}}, status_code=422)

    @app.get("/health")
    def health():
        return {"status": "ok", "postgres_major": 17, "dataset_id": "shop-v1"}

    def manager(request: Request):
        return request.app.state.manager

    @app.post("/v1/sessions", response_model=SessionInfo, status_code=201)
    def create(payload: CreateSession, request: Request):
        return manager(request).create()

    @app.post("/v1/sessions/{sid}/run", response_model=Result)
    def run(sid: str, payload: Run, request: Request):
        return manager(request).run(sid, payload.generation, payload.sql)

    @app.get("/v1/sessions/{sid}/catalog", response_model=Catalog)
    def catalog(sid: str, request: Request, generation: int = Query(ge=1)):
        return manager(request).catalog(sid, generation)

    @app.get("/v1/sessions/{sid}/tables/{handle}/rows", response_model=Result)
    def rows(sid: str, handle: str, request: Request, generation: int = Query(ge=1),
             limit: int = Query(default=50, ge=1, le=100), offset: int = Query(default=0, ge=0, le=10000)):
        return manager(request).browse(sid, generation, handle, limit, offset)

    @app.post("/v1/sessions/{sid}/reset", response_model=SessionInfo)
    def reset(sid: str, payload: Generation, request: Request):
        return manager(request).reset(sid, payload.generation)

    @app.delete("/v1/sessions/{sid}", status_code=204)
    def close(sid: str, request: Request, generation: int = Query(ge=1)):
        manager(request).close_session(sid, generation)
        return Response(status_code=204)

    return app


app = create_app()
