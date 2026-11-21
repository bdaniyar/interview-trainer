from math import exp, fsum, isclose, isfinite
from random import Random


def candidates(logits, temperature, top_p):
    if not logits or not all(isfinite(value) for value in logits):
        raise ValueError("Нужны конечные logits")
    if not isfinite(temperature) or temperature < 0 or not 0 < top_p <= 1:
        raise ValueError("Некорректные параметры sampling")
    ranked = sorted(enumerate(logits), key=lambda item: -item[1])
    if temperature == 0:
        return [(ranked[0][0], 1)]
    largest = ranked[0][1]
    weights = [(index, exp((value - largest) / temperature)) for index, value in ranked]
    threshold = top_p * fsum(weight for _, weight in weights)
    leading = []
    total = 0.0
    for index, weight in weights:
        leading.append((index, weight))
        total += weight
        if top_p < 1 and (total >= threshold or isclose(total, threshold, rel_tol=0, abs_tol=1e-12)):
            break
    return [(index, weight / total) for index, weight in leading]


def sample(logits, temperature, top_p, rng):
    distribution = candidates(logits, temperature, top_p)
    if temperature == 0:
        return distribution[0][0]
    value = rng.random()
    cumulative = 0
    for index, weight in distribution:
        cumulative += weight
        if value < cumulative:
            return index
    return distribution[-1][0]


if __name__ == "__main__":
    assert candidates([1, 1], 1, 0.5) == [(0, 1)]
    print(sample([1, 1], 1, 1, Random(4)))
