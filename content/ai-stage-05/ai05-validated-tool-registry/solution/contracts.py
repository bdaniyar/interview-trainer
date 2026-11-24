from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StrictStr


class BookingArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    booking_id: Annotated[int, Field(strict=True, gt=0)]


class BookingView(BaseModel):
    model_config = ConfigDict(extra="forbid")
    city: StrictStr


@dataclass(frozen=True)
class Principal:
    tenant: str
    subject: str


@dataclass(frozen=True)
class ToolCall:
    call_id: str
    name: str
    arguments: str


@dataclass(frozen=True)
class Tool:
    arguments: type[BaseModel]
    output: type[BaseModel]
    read: Callable[[Principal, BaseModel], Awaitable[dict | None]]


@dataclass(frozen=True)
class ToolResult:
    call_id: str
    status: str
    output: str | None = None
