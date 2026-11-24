from dataclasses import dataclass
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class BookingArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    booking_id: Annotated[int, Field(strict=True, gt=0)]


@dataclass(frozen=True)
class Principal:
    tenant: str
    subject: str
    scopes: frozenset[str]


@dataclass(frozen=True)
class Policy:
    tenant: str
    owner: str
    revoked: bool = False


@dataclass(frozen=True)
class Outcome:
    status: str
    booking: dict | None = None
