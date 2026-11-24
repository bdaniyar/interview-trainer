"""Application contracts independent of any provider SDK."""
from dataclasses import dataclass
from typing import Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)


@dataclass(frozen=True)
class Principal:
    tenant: str
    subject: str
    scopes: frozenset[str]

    @property
    def owner(self) -> tuple[str, str]:
        return self.tenant, self.subject


class BookingSummary(StrictModel):
    booking_id: int
    status: Literal["confirmed", "pending"]


class Proposal(StrictModel):
    proposal_id: str
    owner_tenant: str
    owner_subject: str
    action: Literal["cancel_booking"] = "cancel_booking"
    arguments: dict[str, int]
    status: Literal["pending"] = "pending"
    explanation: str = "Cancellation has been proposed. The booking is unchanged."


Outcome = Literal["ok", "unavailable", "invalid_arguments", "unknown_tool",
                  "tool_error", "tool_timeout", "result_too_large"]


class ToolResult(StrictModel):
    call: str
    tool: Literal["get_booking", "list_my_bookings", "propose_cancel", "unknown"]
    outcome: Outcome
    bookings: tuple[BookingSummary, ...] = ()
    proposal: Proposal | None = None

    def observation(self) -> str:
        # Ownership remains available to the client through the typed proposal.
        return self.model_dump_json(exclude={
            "call": True, "tool": True,
            "proposal": {"owner_tenant", "owner_subject"},
        }, exclude_none=True)


class ChatInput(StrictModel):
    conversation_id: str = Field(pattern=r"^[0-9a-f]{32}$")
    text: str = Field(min_length=1, max_length=750, pattern=r"\S")

    @field_validator("text")
    @classmethod
    def unicode_text(cls, text: str) -> str:
        text.encode()
        return text


@dataclass(frozen=True)
class Call:
    id: str
    name: str
    arguments_json: str


@dataclass(frozen=True)
class Output:
    call_id: str
    body: str


@dataclass(frozen=True)
class Exchange:
    calls: tuple[Call, ...]
    outputs: tuple[Output, ...]


@dataclass(frozen=True)
class Turn:
    user: str
    exchanges: tuple[Exchange, ...]
    answer: str


@dataclass(frozen=True)
class Context:
    policy: str
    history: tuple[Turn, ...]
    user: str


@dataclass(frozen=True)
class Reply:
    kind: Literal["tools", "final", "refusal", "incomplete"]
    text: str = ""
    calls: tuple[Call, ...] = ()


class Provider(Protocol):
    async def reply(self, context: Context, exchanges: tuple[Exchange, ...]) -> Reply: ...


class ProviderUnavailable(Exception):
    pass


Reason = Literal["completed", "refusal", "incomplete", "invalid_provider", "provider_unavailable",
                 "deadline", "step_budget", "call_budget", "output_budget", "context_budget"]


@dataclass(frozen=True)
class Budget:
    steps: int = 3
    calls: int = 5
    output_bytes: int = 3500
    result_bytes: int = 1500
    context_units: int = 6000
    reserved_units: int = 512
    deadline: float = 1.5
    tool_timeout: float = 0.25


class Usage(StrictModel):
    steps: int
    calls: int
    output_bytes: int
    context_units: int
    provider_tokens: None = None


class TraceEvent(StrictModel):
    request_id: str
    step: int
    event: Literal["model", "tool", "terminal"]
    tool: str | None = None
    call_id: str | None = None
    outcome: str
    calls: int
    output_bytes: int
    elapsed_ms: int


class ChatResult(StrictModel):
    request_id: str
    conversation_id: str
    status: Literal["completed", "refused", "incomplete", "failed"]
    reason: Reason
    text: str | None
    tools: tuple[ToolResult, ...]
    proposals: tuple[Proposal, ...]
    usage: Usage
    limits: Budget
    trace: tuple[TraceEvent, ...]
