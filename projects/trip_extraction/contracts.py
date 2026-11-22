"""Wire types, domain validation, and the local extraction contract."""
import re
from dataclasses import dataclass
from datetime import date
from typing import Annotated, Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, field_validator, model_validator


PROMPT_V1 = "trip.prompt.v1"
PROMPT_DEMO = "trip.prompt.v2-regression"
SCHEMA_VERSION = "trip.schema.v1"
FIELDS = ("city", "check_in", "check_out", "guests")


class ExtractRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    text: Annotated[str, Field(strict=True, min_length=1, max_length=500)]
    note: Annotated[str, Field(strict=True, max_length=400)] | None = None

    @field_validator("text")
    @classmethod
    def meaningful_text(cls, value: str):
        if not value.strip():
            raise ValueError("empty text")
        return value


class WireTrip(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    city: StrictStr | None
    check_in: StrictStr | None
    check_out: StrictStr | None
    guests: StrictInt | None


class Envelope(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    trip: WireTrip


class TripRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)
    city: Annotated[str, Field(strict=True, min_length=1, max_length=120)] | None
    check_in: date | None
    check_out: date | None
    guests: Annotated[int, Field(strict=True, gt=0)] | None

    @field_validator("check_in", "check_out", mode="before")
    @classmethod
    def full_date(cls, raw):
        if raw is None:
            return None
        if isinstance(raw, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", raw):
            return date.fromisoformat(raw)
        raise ValueError("expected a complete ISO date")

    @model_validator(mode="after")
    def dates_are_ordered(self):
        if self.check_in is not None and self.check_out is not None and self.check_in >= self.check_out:
            raise ValueError("departure must follow arrival")
        return self


@dataclass(frozen=True)
class Prompt:
    version: str
    instructions: str
    examples: tuple[tuple[str, str], ...]
    text: str
    note: str | None


@dataclass(frozen=True)
class ProviderReply:
    kind: Literal["completed", "refusal", "incomplete", "malformed", "retryable", "unavailable"]
    payload: object = None


class Provider(Protocol):
    identity: str

    async def extract(self, prompt: Prompt, request_id: str, *, repair: bool) -> ProviderReply: ...


class ExtractResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    request_id: str
    status: Literal["completed", "needs_clarification", "refusal", "incomplete",
                    "invalid_schema", "invalid_domain", "timeout", "unavailable", "invalid_request"]
    model: str
    prompt_version: str
    schema_version: str = SCHEMA_VERSION
    category: Literal["missing_facts", "provider_refusal", "provider_incomplete", "invalid_wire",
                      "invalid_trip", "deadline", "provider_unavailable", "invalid_input"] | None = None
    trip: TripRequest | None = None
    attempts: int = 0
    schema_valid: bool | None = None
    domain_valid: bool | None = None
