from dataclasses import dataclass
from hashlib import sha256
from math import hypot, isfinite


DIMENSIONS = 16


class InvalidVector(ValueError):
    pass


class AccessDenied(Exception):
    pass


class VersionConflict(Exception):
    pass


@dataclass(frozen=True)
class Actor:
    tenant: str
    subject: str
    scopes: frozenset[str]

    def require(self, scope: str):
        if scope not in self.scopes:
            raise AccessDenied(scope)


@dataclass(frozen=True)
class Space:
    id: str = "fixture-v1"
    model: str = "synthetic"
    revision: str = "1"
    dimension: int = DIMENSIONS
    normalized: bool = True


@dataclass(frozen=True)
class ChunkInput:
    chunk_id: str
    section: str
    start: int
    text: str
    vector: tuple[float, ...]


@dataclass(frozen=True)
class Source:
    document_id: str
    version: int
    space_id: str
    chunk_id: str
    section: str
    start: int
    end: int
    epoch: int

    @property
    def key(self):
        return self.document_id, self.version, self.chunk_id


@dataclass(frozen=True)
class Hit:
    source: Source
    score: float


def digest(text: str) -> str:
    return sha256(text.encode()).hexdigest()


def vector_param(vector: tuple[float, ...], space: Space) -> str:
    if (len(vector) != space.dimension or not all(type(item) in (float, int)
            and isfinite(item) for item in vector) or abs(hypot(*vector) - 1) > 1e-6):
        raise InvalidVector("expected a finite unit vector with the declared dimension")
    return "[" + ",".join(str(value) for value in vector) + "]"
