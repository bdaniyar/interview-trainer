from dataclasses import dataclass
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class Args(BaseModel):
    model_config = ConfigDict(extra="forbid")
    booking_id: Annotated[int, Field(strict=True, gt=0)]


@dataclass(frozen=True)
class Principal:
    tenant: str
    subject: str
    scopes: frozenset[str]


@dataclass(frozen=True)
class Proposal:
    proposal_id: str
    tenant: str
    subject: str
    action: str
    booking_id: int
    arguments: tuple[tuple[str, int], ...]
    status: str
    explanation: str


@dataclass(frozen=True)
class Outcome:
    status: str
    booking: dict | None = None
    proposal: Proposal | None = None
