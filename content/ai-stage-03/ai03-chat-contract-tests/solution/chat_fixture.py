import asyncio
from typing import Literal
from uuid import uuid4

from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

from chat_types import ProviderUnavailable


class Question(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    question: str = Field(min_length=1, max_length=500)


class Reply(BaseModel):
    request_id: str
    status: Literal["completed", "empty", "refusal", "incomplete", "unavailable", "timeout"]
    text: str | None = None
    usage: int | None = Field(default=None, ge=0, strict=True)


def create_app(provider, *, timeout=0.5, id_factory=uuid4):
    app = FastAPI()

    def get_provider():
        return provider

    @app.exception_handler(RequestValidationError)
    async def invalid(request, exc):
        return JSONResponse({"status": "invalid_request"}, status_code=422)

    @app.post("/chat", response_model=Reply,
              responses={502: {"model": Reply}, 503: {"model": Reply}, 504: {"model": Reply}})
    async def chat(query: Question, client=Depends(get_provider)):
        request_id = str(id_factory())
        try:
            async with asyncio.timeout(timeout):
                answer = await client.generate(query.question)
        except ProviderUnavailable:
            return JSONResponse(Reply(request_id=request_id, status="unavailable").model_dump(), status_code=503)
        except TimeoutError:
            return JSONResponse(Reply(request_id=request_id, status="timeout").model_dump(), status_code=504)
        if answer.status == "completed":
            if answer.text and answer.text.strip():
                return Reply(request_id=request_id, status="completed", text=answer.text, usage=answer.usage)
            return JSONResponse(
                Reply(request_id=request_id, status="empty", usage=answer.usage).model_dump(), status_code=502)
        return Reply(request_id=request_id, status=answer.status, usage=answer.usage)

    return app
