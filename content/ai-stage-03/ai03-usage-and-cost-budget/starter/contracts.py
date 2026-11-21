from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Price:
    revision: str
    unit: int
    regular: Decimal
    cached: Decimal
    output: Decimal


@dataclass(frozen=True)
class Usage:
    input_tokens: int | None
    cached_tokens: int | None
    output_tokens: int | None


@dataclass(frozen=True)
class Estimate:
    status: str
    total: Decimal | None
    revision: str | None


def demo(estimate):
    tariff = Price("synthetic-1", 100, Decimal("0.50"), Decimal("0.10"), Decimal("0.80"))
    result = estimate(tariff, [Usage(20, 10, 15)], Decimal("0.18"))
    assert result == Estimate("within", Decimal("0.18"), tariff.revision)
    print(result)
