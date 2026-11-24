from dataclasses import dataclass


@dataclass(frozen=True)
class Actor:
    tenant: str
    subject: str
    scopes: frozenset[str]


@dataclass(frozen=True)
class Chunk:
    index: int
    text: str


@dataclass(frozen=True)
class Document:
    owner: str
    version: int
    digest: str
    chunks: tuple[Chunk, ...]
    epoch: int
    readers: frozenset[str] = frozenset()
    deleted: bool = False


@dataclass(frozen=True)
class Ref:
    tenant: str
    key: str
    version: int
    epoch: int
    index: int


@dataclass(frozen=True)
class Answer:
    status: str
    text: str | None = None
    ref: Ref | None = None
