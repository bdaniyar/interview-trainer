from decimal import Decimal as D

import pytest

from contracts import Estimate, Price, Usage
from main import estimate


def price(unit=1000):
    return Price("v4", unit, D("0.25"), D("0.05"), D("1.10"))


def test_repeated_attempts_and_budget_boundary():
    attempts = [Usage(12, 2, 7), Usage(8, 3, 1)]
    assert estimate(price(), attempts, D("0.0128")) == Estimate("within", D("0.0128"), "v4")
    assert estimate(price(), attempts, D("0.01279")).status == "over"


@pytest.mark.parametrize("unit", [100, 1000000])
def test_units(unit):
    assert estimate(price(unit), [Usage(20, 0, 0)], D("1")).total == D(5) / unit


@pytest.mark.parametrize("attempt", [None, Usage(3, None, 4), Usage(None, 0, 9)], ids=["missing", "cache", "input"])
def test_unknown_does_not_disappear_in_total(attempt):
    assert estimate(price(), [Usage(10, 0, 2), attempt], D("1")) == Estimate("unknown", None, "v4")
    assert estimate(None, [Usage(10, 0, 2)], D("1")) == Estimate("unknown", None, None)


def test_zero_usage_is_known():
    assert estimate(price(), [Usage(0, 0, 0)], D(0)) == Estimate("within", D(0), "v4")
    assert estimate(price(), [], D(0)).total == 0


@pytest.mark.parametrize(("tariff", "measure", "budget"), [
    (price(0), Usage(0, 0, 0), D(0)), (price(), Usage(1, 2, 0), D(1)),
    (price(), Usage(3, 0, -1), D(1)), (price(), Usage(3, 0, 0), D("NaN")),
    (Price("vbad", 100, D("Infinity"), D(0), D(0)), Usage(0, 0, 0), D(1)),
], ids=["unit", "cache-subset", "negative", "not-finite-budget", "not-finite-price"])
def test_invalid_values(tariff, measure, budget):
    with pytest.raises(ValueError):
        estimate(tariff, [measure], budget)
