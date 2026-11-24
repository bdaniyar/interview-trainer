import math

import pytest

from main import cosine, dot, norm, top_k


def test_arithmetic_and_float_tolerance():
    assert dot((2, 3, 1), (1, -2, 4)) == 0
    assert dot((2, 4), (2, -3)) == -8
    assert norm((3, 4)) == 5
    assert cosine((2, 0), (3, 3)) == pytest.approx(math.sqrt(0.5))


@pytest.mark.parametrize("a,b,value", [
    ((3, 4), (6, 8), 1), ((-2, 0), (8, 0), -1), ((2, 1), (-1, 2), 0),
    ((1e300, 1e300), (1e-300, 1e-300), 1),
])
def test_angles(a, b, value):
    assert cosine(a, b) == pytest.approx(value)


@pytest.mark.parametrize("vectors", [
    ((1,), (1, 2)), ((0, 0), (1, 2)), ((1, 2), (0, 0)), ((), (1,)),
    ((float("inf"),), (1,)), ((1,), (float("nan"),)), ((True,), (1,)),
])
def test_validation(vectors):
    with pytest.raises(ValueError):
        cosine(*vectors)


def test_rank_ties_and_negative_scores():
    result = top_k((1, 0), {"z": (1, 1), "a": (1, 1), "q": (0, 1), "n": (-1, 0)}, 17)
    assert [key for key, _ in result] == ["a", "z", "q", "n"]
    assert [value for _, value in result] == pytest.approx([math.sqrt(.5), math.sqrt(.5), 0, -1])


def test_empty_and_zero_k():
    assert top_k((1,), {}, 7) == []
    assert top_k((1,), {"a": (1,)}, 0) == []
    with pytest.raises(ValueError):
        top_k((1,), {"invalid": (0,)}, 0)


@pytest.mark.parametrize("k", [-1, True, 1.2])
def test_invalid_k(k):
    with pytest.raises(ValueError):
        top_k((1,), {}, k)
