import pytest

from main import recall_at_k, summarize


@pytest.mark.parametrize("exact,approx,k,score", [
    (("a", "b"), ("a", "z"), 2, .5), (("x", "x", "y"), ("y", "y", "x"), 2, 1.),
    ((), ("a",), 2, None), (("last",), (), 2, 0.),
    (("a", "b"), ("d", "a"), 1, 0.), (("a",), ("a", "b", "c"), 3, 1.),
])
def test_recall_at_k(exact, approx, k, score):
    assert recall_at_k(exact, approx, k) == score


def test_separate_denominators_and_nearest_rank():
    cases = {"hit": (("x",), ("x",), 11), "miss": (("z",), (), 1), "empty": ((), (), 4)}
    assert summarize(cases, 3) == {"recall": {"hit": 1., "miss": 0., "empty": None}, "recall_mean": .5,
                                    "recall_n": 2, "latency_n": 3, "p50": 4, "p95": 11}


def test_empty_measurements():
    result = summarize({}, 3)
    assert result == {"recall": {}, "recall_mean": None, "recall_n": 0, "latency_n": 0, "p50": None, "p95": None}


@pytest.mark.parametrize("elapsed", [-.5, float("inf"), float("nan"), True])
def test_bad_timing(elapsed):
    with pytest.raises(ValueError):
        summarize({"x": (("x",), (), elapsed)}, 1)


@pytest.mark.parametrize("k", [True, 0, -2, 2.2])
def test_invalid_k(k):
    with pytest.raises(ValueError):
        recall_at_k(("a",), ("a",), k)
