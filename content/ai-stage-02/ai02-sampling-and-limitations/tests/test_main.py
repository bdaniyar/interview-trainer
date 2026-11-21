from math import log
from random import Random

import pytest

from main import candidates, sample


def test_probabilities_and_top_p():
    logits = [log(2), log(5), log(3)]
    result = candidates(logits, 1, 0.8)
    assert [i for i, _ in result] == [1, 2]
    assert [p for _, p in result] == pytest.approx([0.625, 0.375])
    assert len(candidates(logits, 1, 0.80001)) == 3
    assert candidates([10000, -10000], 1, 1) == [(0, 1), (1, 0)]


def test_greedy_and_injected_rng():
    assert sample([1, 3, 3], 0, 0.3, None) == 1
    class Boundary:
        calls = 0

        def random(self):
            self.calls += 1
            return 0.5

    rng = Boundary()
    assert sample([3, 3], 1, 1, rng) == 1
    assert rng.calls == 1


def test_seeded_sequence():
    rng = Random(2)
    assert [sample([0, 0, 0], 4, 1, rng) for _ in range(4)] == [2, 2, 0, 0]


@pytest.mark.parametrize(("logits", "temperature", "top_p"), [
    ([], 1, 1), ([0, float("nan")], 1, 1), ([0], -1, 1),
    ([0], float("inf"), 1), ([0], 1, 0), ([0], 1, 1.1),
])
def test_invalid_input(logits, temperature, top_p):
    with pytest.raises(ValueError):
        candidates(logits, temperature, top_p)
