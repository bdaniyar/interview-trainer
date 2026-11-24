from dataclasses import dataclass


@dataclass(frozen=True)
class Call:
    call_id: str
    name: str


@dataclass(frozen=True)
class Reply:
    kind: str
    text: str | None = None
    calls: tuple[Call, ...] = ()


@dataclass(frozen=True)
class Observation:
    call_id: str
    output: str


@dataclass(frozen=True)
class Budget:
    steps: int = 3
    calls: int = 4
    output_bytes: int = 256
    seconds: float = 0.5
    tool_seconds: float = 0.1


@dataclass(frozen=True)
class Outcome:
    reason: str
    text: str | None
    steps: int
    calls: int
    observations: tuple[Observation, ...]
