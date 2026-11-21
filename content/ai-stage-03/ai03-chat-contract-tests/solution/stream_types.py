from dataclasses import dataclass


@dataclass(frozen=True)
class WireEvent:
    kind: str
    text: str | None = None
    usage: int | None = None


@dataclass(frozen=True)
class AppEvent:
    kind: str
    text: str | None = None
    usage: int | None = None


class StreamFailed(Exception):
    pass
