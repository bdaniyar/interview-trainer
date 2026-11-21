from decimal import Decimal

from contracts import Estimate, demo


def valid_money(value):
    return isinstance(value, Decimal) and value.is_finite() and value >= 0


def estimate(price, attempts, budget) -> Estimate:
    if not valid_money(budget):
        raise ValueError("Некорректный бюджет")
    if price is not None and (type(price.unit) is not int or price.unit <= 0 or
                              not all(valid_money(x) for x in (price.regular, price.cached, price.output))):
        raise ValueError("Некорректный тариф")
    complete = price is not None
    revision = price.revision if price is not None else None
    total = Decimal(0)
    for attempt in attempts:
        if attempt is None:
            complete = False
            continue
        i, c, o = attempt.input_tokens, attempt.cached_tokens, attempt.output_tokens
        values = (i, c, o)
        if any(type(x) is not int or x < 0 for x in values if x is not None):
            raise ValueError("Некорректный счётчик токенов")
        if i is not None and c is not None and c > i:
            raise ValueError("Cached превышает общий вход")
        if price is None or None in values:
            complete = False
            continue
        total += (price.regular * (i - c) + price.cached * c + price.output * o) / price.unit
    if not complete:
        return Estimate("unknown", None, revision)
    return Estimate("within" if total <= budget else "over", total, revision)


if __name__ == "__main__":
    demo(estimate)
