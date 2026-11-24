import math

import pytest

from main import bm25, rerank, rrf


def test_bm25_numeric():
    corpus = {"short": ("tea",), "long": ("tea", "tea", "one", "two"), "absent": ("milk",)}
    idf = math.log(1 + 1.5 / 2.5)
    actual = dict(bm25(("tea", "tea"), corpus))
    assert set(actual) == {"short", "long"}
    assert actual["short"] == pytest.approx(idf * 2.2 / (1 + 1.2 * (.25 + .75 / 2)))
    assert actual["long"] == pytest.approx(idf * 4.4 / (2 + 1.2 * (.25 + 1.5)))


@pytest.mark.parametrize("query,corpus", [((), {"a": ("p",)}), (("q",), {}), (("q",), {"a": ()}), (("q",), {"a": ("x",)})])
def test_bm25_empty(query, corpus):
    assert bm25(query, corpus) == []


def test_bm25_scores_tie_by_string_id():
    assert [key for key, _ in bm25(("t",), {"z": ("t",), "h": ("t",)})] == ["h", "z"]


def test_rrf_deduplicates_with_1_based_rank_and_numeric_verification():
    result = rrf((("t2", "t2", "t1"), ("t1",), ()), rank_constant=4, limit=2)
    assert [x for x, _ in result] == ["t1", "t2"]
    assert dict(result)["t1"] == pytest.approx(1 / 6 + 1 / 5)
    assert rrf((("z",), ("a",)), limit=1)[0][0] == "a"
    assert rrf((), limit=2) == []


def test_rerank_checks_acl_before_bounded_call():
    calls = []
    def scorer(keys):
        calls.append(keys)
        return [("y", 2), ("x", 2)]
    result = rerank(("foreign", "y", "x", "y", "z"), {"x", "y", "z"}, 2, scorer)
    assert result == ("x", "y", "z") and calls == [("y", "x")]


@pytest.mark.parametrize("output", [
    [("b", 1)], [("a", 0), ("a", 1)], [("a", 1), ("other", 0)],
    [("a", 1), ("b", float("nan"))], [("a", 1), ("b", True)],
])
def test_rerank_validates_full_batch(output):
    with pytest.raises(ValueError):
        rerank(("a", "b", "c"), {"a", "b", "c"}, 2, lambda _: output)


def test_rerank_empty_window_does_not_call():
    assert rerank(("x",), {"x"}, 0, lambda _: pytest.fail("called")) == ("x",)
    assert rerank(("x",), set(), 8, lambda _: pytest.fail("called")) == ()
