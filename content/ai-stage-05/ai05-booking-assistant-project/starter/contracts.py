from dataclasses import dataclass
from typing import Literal, Protocol


@dataclass(frozen=True)
class Principal:
    tenant: str
    subject: str


@dataclass(frozen=True)
class Call:
    id: str
    name: str
    arguments: dict


@dataclass(frozen=True)
class Booking:
    id: int
    status: str
    private_note: str


@dataclass(frozen=True)
class Observation:
    call_id: str
    outcome: Literal["ok", "unavailable", "invalid_arguments", "unknown_tool", "tool_error"]
    bookings: tuple[tuple[int, str], ...] = ()


@dataclass(frozen=True)
class Reply:
    kind: Literal["tools", "final", "refusal", "incomplete"]
    text: str = ""
    calls: tuple[Call, ...] = ()


@dataclass(frozen=True)
class Trace:
    step: int
    tool: str
    alias: str
    outcome: str


@dataclass(frozen=True)
class Result:
    reason: Literal["completed", "refusal", "incomplete", "invalid_provider",
                    "provider_error", "step_budget", "call_budget"]
    text: str | None = None
    trace: tuple[Trace, ...] = ()


class Provider(Protocol):
    async def reply(self, prompt: str, observations: tuple[Observation, ...]) -> Reply: ...


class Repository(Protocol):
    def owned_ids(self, principal: Principal) -> tuple[int, ...]: ...
    def owner_of(self, booking_id: int) -> Principal | None: ...
    async def read(self, booking_id: int) -> Booking: ...
