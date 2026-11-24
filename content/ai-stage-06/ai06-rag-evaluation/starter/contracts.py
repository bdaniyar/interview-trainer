from dataclasses import dataclass


@dataclass(frozen=True)
class Case:
    id: str
    lang: str
    relevant: tuple[str, ...]
    allowed: frozenset[str]
    expected: str
    supported_claims: frozenset[str]


@dataclass(frozen=True)
class Prediction:
    ranked: tuple[str, ...]
    status: str
    citations: tuple[str, ...]
    claims: tuple[str, ...]
