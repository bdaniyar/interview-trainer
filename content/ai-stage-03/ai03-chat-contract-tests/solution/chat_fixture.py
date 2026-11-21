"""Alternate synthetic service behind the contract-testing harness."""
import asyncio
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from chat_types import ProviderUnavailable


def create_app(provider, timeout):
    app = FastAPI()

    def response(http, state, answer=None):
        return JSONResponse(
            {"status": state, "text": answer, "request_id": uuid4().hex},
            status_code=http,
        )

    @app.post("/probe/message")
    async def send(request: Request):
        data = await request.json()
        message = data.get("text")
        if not isinstance(message, str) or not message.strip():
            return response(422, "invalid_request")
        if len(message) > 200:
            return response(422, "invalid_request")
        try:
            async with asyncio.timeout(timeout):
                outcome = await provider.generate(message.strip())
        except TimeoutError:
            return response(504, "timeout")
        except ProviderUnavailable:
            return response(503, "unavailable")
        if outcome.status == "completed":
            if outcome.text:
                return response(200, "completed", outcome.text)
            return response(502, "empty")
        return response(200, outcome.status)

    return app
