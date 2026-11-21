from dataclasses import dataclass
from typing import AsyncGenerator, Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Question(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    question: str = Field(min_length=1, max_length=500)


class Usage(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    input_tokens: int = Field(ge=0, strict=True)
    output_tokens: int = Field(ge=0, strict=True)
    cached_tokens: int | None = Field(default=None, ge=0, strict=True)

    @model_validator(mode="after")
    def cached_is_part_of_input(self):
        if self.cached_tokens is not None and self.cached_tokens > self.input_tokens:
            raise ValueError("cached tokens cannot exceed input tokens")
        return self


@dataclass(frozen=True)
class Generation:
    status: Literal["completed", "refusal", "incomplete"]
    text: str | None = None
    usage: Usage | None = None


@dataclass(frozen=True)
class ProviderEvent:
    kind: Literal["delta", "completed", "refusal", "incomplete", "failed"]
    text: str | None = None
    usage: Usage | None = None


class ProviderUnavailable(Exception):
    pass


class ProviderBusy(ProviderUnavailable):
    """A documented rejection before any generation began."""

    def __init__(self, retry_after: float = 0):
        self.retry_after = retry_after


class Provider(Protocol):
    async def generate(self, question: str) -> Generation: ...
    def stream(self, question: str) -> AsyncGenerator[ProviderEvent, None]: ...
    async def aclose(self) -> None: ...
