from dataclasses import dataclass


@dataclass(frozen=True)
class Scope:
    tenant: str
    subject: str
    space: str
    may_read: bool = True


@dataclass(frozen=True)
class Row:
    tenant: str
    owner: str
    readers: frozenset[str]
    document: str
    version: int
    active_version: int
    deleted: bool
    space: str
    chunk_id: str
    embedding: tuple[float, ...]
