"""Translate provider outcomes and enforce application-owned rules."""
import asyncio
import re

from pydantic import ValidationError

from contracts import Envelope, ExtractRequest, ExtractResult, PROMPT_V1, Provider, ProviderReply, TripRequest
from prompt import build_prompt


FAILURES = {
    "refusal": ("refusal", "provider_refusal"),
    "incomplete": ("incomplete", "provider_incomplete"),
    "malformed": ("invalid_schema", "invalid_wire"),
    "retryable": ("unavailable", "provider_unavailable"),
    "unavailable": ("unavailable", "provider_unavailable"),
}


def interpret(reply: ProviderReply, *, request: ExtractRequest, **origin) -> ExtractResult:
    if not isinstance(reply, ProviderReply) or not isinstance(reply.kind, str) or reply.kind not in {*FAILURES, "completed"}:
        return ExtractResult(**origin, status="invalid_schema", category="invalid_wire", schema_valid=False)
    if reply.kind != "completed":
        status, category = FAILURES[reply.kind]
        return ExtractResult(**origin, status=status, category=category,
                             schema_valid=False if reply.kind == "malformed" else None)
    try:
        if isinstance(reply.payload, (str, bytes)):
            wire = Envelope.model_validate_json(reply.payload)
        else:
            wire = Envelope.model_validate(reply.payload)
    except ValidationError:
        return ExtractResult(**origin, status="invalid_schema", category="invalid_wire", schema_valid=False)
    try:
        trip = TripRequest.model_validate(wire.trip.model_dump())
    except ValidationError:
        return ExtractResult(**origin, status="invalid_domain", category="invalid_trip",
                             schema_valid=True, domain_valid=False)

    # Accept only full date literals grounded in the user's input.
    # A year in a booking identifier or the untrusted note never suffices.
    literals = set(re.findall(r"(?<!\d)[0-9]{4}-[0-9]{2}-[0-9]{2}(?!\d)", request.text))
    unsupported = {
        name: None
        for name in ("check_in", "check_out")
        if (value := getattr(trip, name)) is not None and value.isoformat() not in literals
    }
    if unsupported:
        trip = trip.model_copy(update=unsupported)
    missing = any(value is None for value in trip.model_dump().values())
    return ExtractResult(**origin, status="needs_clarification" if missing else "completed",
                         category="missing_facts" if missing else None,
                         trip=trip, schema_valid=True, domain_valid=True)


async def extract_trip(provider: Provider, request: ExtractRequest, request_id: str, *,
                       prompt_version: str = PROMPT_V1, timeout: float = 0.5,
                       allow_repair: bool = False) -> ExtractResult:
    prompt = build_prompt(request, prompt_version)
    origin = {"request_id": request_id, "model": provider.identity, "prompt_version": prompt.version}
    attempts = 0
    try:
        async with asyncio.timeout(timeout):
            for attempt in (1, 2):
                attempts = attempt
                try:
                    outcome = await provider.extract(prompt, request_id, repair=attempt == 2)
                except TimeoutError:
                    raise
                except Exception:
                    # The provider boundary may hold credentials or user text.
                    # Keep raw exceptions out of the HTTP response and server logs.
                    outcome = ProviderReply("unavailable")
                result = interpret(outcome, request=request, attempts=attempt, **origin)
                may_repair = (
                    allow_repair and attempt == 1 and (
                        result.status in {"incomplete", "invalid_schema"}
                        or isinstance(outcome, ProviderReply) and outcome.kind == "retryable"
                    )
                )
                if not may_repair:
                    return result
    except TimeoutError:
        return ExtractResult(**origin, status="timeout", category="deadline", attempts=attempts)
    raise AssertionError("bounded extraction must yield an outcome")
