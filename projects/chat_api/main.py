import asyncio
import json
from contextlib import asynccontextmanager
from decimal import Decimal
from math import isfinite
from typing import Literal
from uuid import uuid4

import anyio
from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel

from contracts import Provider, ProviderBusy, ProviderUnavailable, Question, Usage
from providers import ScriptedProvider


class Reply(BaseModel):
    request_id: str
    status: Literal["completed", "refusal", "incomplete", "empty", "unavailable", "timeout"]
    text: str | None = None
    usage: Usage | None = None
    estimated_usd: str | None = None
    price_revision: str | None = None


def reply(request_id: str, status, text=None, usage=None) -> Reply:
    # Per 1,000 tokens. A synthetic tariff for the exercise, with separate cached input.
    if usage is None or usage.cached_tokens is None:
        return Reply(request_id=request_id, status=status, text=text, usage=usage)
    cached = usage.cached_tokens
    price = (Decimal("0.50") * (usage.input_tokens - cached)
             + Decimal("0.10") * cached + Decimal("1.00") * usage.output_tokens) / 1000
    return Reply(request_id=request_id, status=status, text=text, usage=usage,
                 estimated_usd=str(price), price_revision="synthetic-v1")


async def generate(provider, question, timeout, pause):
    # Only one retry after a documented rejection before dispatch.
    # Timeout or generic unavailability can have an unknown effect.
    loop = asyncio.get_running_loop()
    end = loop.time() + timeout
    async with asyncio.timeout_at(end):
        try:
            return await provider.generate(question)
        except ProviderBusy as exc:
            if not isfinite(exc.retry_after) or exc.retry_after < 0:
                raise ProviderUnavailable() from None
            delay = max(0.05, exc.retry_after)
            if loop.time() + delay >= end:
                raise
            await pause(delay)
            return await provider.generate(question)


def frame(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


async def stream_frames(provider, question, request_id, timeout):
    source = None
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout
    terminal = reply(request_id, "incomplete")
    try:
        source = provider.stream(question)
        while True:
            remaining = deadline - loop.time()
            if remaining <= 0:
                terminal = reply(request_id, "timeout")
                break
            event = await asyncio.wait_for(anext(source), remaining)
            if event.kind == "delta":
                if event.text:
                    yield frame("delta", {"request_id": request_id, "text": event.text})
                continue
            status = "unavailable" if event.kind == "failed" else event.kind
            terminal = reply(request_id, status, usage=event.usage)
            break
    except StopAsyncIteration:
        pass
    except ProviderUnavailable:
        terminal = reply(request_id, "unavailable")
    except TimeoutError:
        terminal = reply(request_id, "timeout")
    finally:
        if source is not None:
            with anyio.CancelScope(shield=True):
                await source.aclose()
    yield frame("terminal", terminal.model_dump(mode="json"))


class ChatStream(StreamingResponse):
    async def stream_response(self, send):
        try:
            await super().stream_response(send)
        finally:
            # The socket can close while ASGI is sending a yielded frame.
            with anyio.CancelScope(shield=True):
                await self.body_iterator.aclose()


def create_app(make_provider=ScriptedProvider, *, timeout=0.5, pause=asyncio.sleep) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app):
        app.state.provider = make_provider()
        try:
            yield
        finally:
            await app.state.provider.aclose()

    app = FastAPI(title="Pythoria P1 · LLM Chat API", lifespan=lifespan)

    @app.exception_handler(RequestValidationError)
    async def invalid_input(request, exc):
        return JSONResponse({"request_id": str(uuid4()), "status": "invalid_request"}, status_code=422)

    def get_provider() -> Provider:
        return app.state.provider

    @app.post("/chat", response_model=Reply,
              responses={502: {"model": Reply}, 503: {"model": Reply}, 504: {"model": Reply}})
    async def chat(question: Question, provider: Provider = Depends(get_provider)):
        request_id = str(uuid4())
        try:
            outcome = await generate(provider, question.question, timeout, pause)
        except TimeoutError:
            return JSONResponse(reply(request_id, "timeout").model_dump(), status_code=504)
        except ProviderUnavailable:
            return JSONResponse(reply(request_id, "unavailable").model_dump(), status_code=503)
        if outcome.status == "completed":
            if not outcome.text or not outcome.text.strip():
                empty = reply(request_id, "empty", usage=outcome.usage)
                return JSONResponse(empty.model_dump(), status_code=502)
            return reply(request_id, "completed", outcome.text, outcome.usage)
        return reply(request_id, outcome.status, usage=outcome.usage)

    @app.post("/chat/stream", response_class=ChatStream)
    async def chat_stream(question: Question, provider: Provider = Depends(get_provider)):
        return ChatStream(
            stream_frames(provider, question.question, str(uuid4()), timeout),
            media_type="text/event-stream", headers={"Cache-Control": "no-cache"},
        )

    return app


app = create_app()
