from dataclasses import replace

import pytest

from contracts import Case, Prediction
from main import score_case, summarize


CASE = Case("x", "ru", ("a-v2", "b-v1"), frozenset({"a-v2", "b-v1", "noise"}), "answered", frozenset({"x"}))


def test_dedup_rank_recall_precision_mrr_and_exact_answer():
    row = score_case(CASE, Prediction(("noise", "noise", "b-v1", "a-v2"), "answered", ("b-v1",), ("x",)), 2)
    assert row == {"recall": .5, "precision": .5, "mrr": .5, "citation_valid": True,
                   "claim_support": 1., "correct": True, "abstention": None, "forbidden": 0, "bucket": "ok"}


def test_precision_for_short_list_uses_returned_count():
    row = score_case(CASE, Prediction(("b-v1",), "answered", ("b-v1",), ("x",)), 10)
    assert row["recall"] == .5 and row["precision"] == 1.0


def test_empty_relevant_and_empty_retrieval_have_independent_denominators():
    row = score_case(replace(CASE, relevant=(), expected="abstain"),
                     Prediction((), "abstain", (), ()), 4)
    assert all(row[key] is None for key in ("recall", "mrr", "precision", "citation_valid", "claim_support"))
    assert row["abstention"] is True


def test_answer_miss_distinguished_from_bad_claim_and_citation():
    missing = score_case(CASE, Prediction(("noise",), "abstain", (), ()), 4)
    wrong = score_case(CASE, Prediction(("a-v2",), "answered", ("a-v2",), ("x", "unproven")), 4)
    unsupplied = score_case(CASE, Prediction(("a-v2",), "answered", ("b-v1",), ("x",)), 4)
    assert missing["bucket"] == "retrieval_miss" and missing["mrr"] == 0
    assert wrong["bucket"] == "answer_error" and wrong["claim_support"] == .5
    assert unsupplied["citation_valid"] is False and unsupplied["correct"] is False


def test_forbidden_not_hidden_outside_top_k():
    row = score_case(CASE, Prediction(("a-v2", "private", "a-v1"), "answered", ("a-v2", "private"), ("x",)), 1)
    assert row["bucket"] == "forbidden" and row["forbidden"] == 2


def test_summary_reports_counts_even_if_all_undefined():
    passed = score_case(CASE, Prediction(("b-v1",), "answered", ("b-v1",), ("x",)), 4)
    empty = score_case(replace(CASE, relevant=(), expected="abstain"), Prediction((), "abstain", (), ()), 4)
    summary = summarize([passed, empty])
    assert summary["recall"] == {"mean": .5, "n": 1}
    assert summary["abstention"] == {"mean": 1., "n": 1}
    assert summary["correct"] == {"mean": 1., "n": 2}
    assert summarize([])["mrr"] == {"mean": None, "n": 0}


@pytest.mark.parametrize("k", [True, 0, -1, 2.5])
def test_invalid_k(k):
    with pytest.raises(ValueError):
        score_case(CASE, Prediction((), "abstain", (), ()), k)
