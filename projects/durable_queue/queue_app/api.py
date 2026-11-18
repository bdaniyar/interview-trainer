import os
from uuid import UUID

from fastapi import FastAPI, Header, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, StrictInt
from sqlalchemy.exc import OperationalError

from .store import Store, IdempotencyConflict


class Payload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    n: StrictInt = Field(ge=0, le=100000)
    fail_until: StrictInt = Field(default=0, ge=0, le=7)


class JobRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    payload: Payload
    max_attempts: StrictInt = Field(default=3, ge=1, le=8)


def create_app(url=None):
    store = Store(url or os.environ["DATABASE_URL"])
    app = FastAPI(title="Durable Training Queue")
    app.state.store = store

    @app.exception_handler(OperationalError)
    async def database_failure(_request, _error):
        return JSONResponse(
            status_code=503,
            content={
                "detail": "Database unavailable; retry idempotent requests with the same key"
            },
        )

    @app.post("/demo-effects")
    def demo_effect(
        payload: dict,
        idempotency_key: str = Header(
            alias="Idempotency-Key", min_length=1, max_length=128
        ),
    ):
        try:
            return store.receive_effect(idempotency_key, payload)
        except IdempotencyConflict:
            raise HTTPException(
                409, "Effect key already names another payload"
            ) from None

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.post("/jobs")
    def submit(
        body: JobRequest,
        response: Response,
        idempotency_key: str = Header(
            alias="Idempotency-Key", min_length=1, max_length=128
        ),
    ):
        try:
            job, created = store.submit(
                "api:" + idempotency_key, body.payload.model_dump(), body.max_attempts
            )
        except (IdempotencyConflict, ValueError) as exc:
            raise HTTPException(409, str(exc)) from None
        except OperationalError:
            raise HTTPException(
                503, "Database unavailable; retry with the same idempotency key"
            ) from None
        response.status_code = 201 if created else 200
        return job

    @app.get("/jobs/{job_id}")
    def get(job_id: UUID):
        row = store.get(job_id)
        if not row:
            raise HTTPException(404, "Unknown job")
        return row

    @app.post("/jobs/{job_id}/cancel")
    def cancel(job_id: UUID):
        if not store.cancel(job_id):
            raise HTTPException(409, "Job is terminal or unknown")
        return store.get(job_id)

    return app
