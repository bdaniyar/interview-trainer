from dataclasses import dataclass


@dataclass(frozen=True)
class Caller:
    tenant: str
    subject: str


@dataclass(frozen=True)
class Ref:
    id: str
    version: int


@dataclass(frozen=True)
class Source:
    id: str
    version: int
    tenant: str
    owner: str
    deleted: bool = False


@dataclass(frozen=True)
class Claim:
    text: str
    refs: tuple[Ref, ...]


@dataclass(frozen=True)
class Draft:
    claims: tuple[Claim, ...]
