from dataclasses import dataclass


@dataclass(frozen=True)
class Space:
    model: str
    revision: str
    dimension: int
    normalized: bool


@dataclass(frozen=True)
class Item:
    id: str
    text: str


@dataclass(frozen=True)
class Embedding:
    id: str
    space: Space
    vector: tuple[float, ...]


@dataclass(frozen=True)
class Cached:
    space: Space
    digest: str
    vector: tuple[float, ...]


@dataclass(frozen=True)
class Outcome:
    id: str
    digest: str
    status: str
    vector: tuple[float, ...] | None = None
