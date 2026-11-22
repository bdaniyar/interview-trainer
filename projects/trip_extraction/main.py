"""Local FastAPI entry point for P2."""
from uuid import uuid4

from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from contracts import ExtractRequest, ExtractResult, PROMPT_V1, Provider
from pipeline import extract_trip
from providers import ScriptedProvider

STATUS_CODES = {"invalid_schema": 502, "invalid_domain": 502, "unavailable": 503, "timeout": 504}


def create_app(provider: Provider | None = None, *, timeout=0.5, allow_repair=False) -> FastAPI:
    adapter = provider if provider is not None else ScriptedProvider()
    app = FastAPI(title="Pythoria P2 — Structured Trip Extraction")

    def get_provider() -> Provider:
        return adapter

    @app.exception_handler(RequestValidationError)
    async def invalid_input(request, exc):
        result = ExtractResult(request_id=str(uuid4()), status="invalid_request", model=adapter.identity,
                               prompt_version=PROMPT_V1, category="invalid_input")
        return JSONResponse(result.model_dump(mode="json"), status_code=422)

    @app.post("/extract-trip", response_model=ExtractResult,
              responses={code: {"model": ExtractResult} for code in (422, 502, 503, 504)})
    async def extract(request: ExtractRequest, client: Provider = Depends(get_provider)):
        result = await extract_trip(client, request, str(uuid4()), timeout=timeout, allow_repair=allow_repair)
        if result.status in STATUS_CODES:
            return JSONResponse(result.model_dump(mode="json"), status_code=STATUS_CODES[result.status])
        return result

    return app


app = create_app()
