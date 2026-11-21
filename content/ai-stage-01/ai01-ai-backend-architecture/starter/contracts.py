from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class Generation:
    status: Literal["completed", "incomplete", "unavailable", "timeout"]
    text: str | None
    usage: int | None


class ProviderUnavailable(Exception):
    pass
