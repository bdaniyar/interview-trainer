from concurrent.futures import ThreadPoolExecutor

import pytest

from contracts import Context, Conversation, Message, Principal
from main import build_context


ALICE = Principal("a", "same")
BOB = Principal("b", "same")
FIRST = Message("system", "fixed")
LAST = Message("user", "новое")
OLD = Message("user", "older")
LATEST = Message("assistant", "later")
CALLS = Message("assistant", call_ids=("r", "s"))
ONE = Message("tool", "one", call_id="r")
TWO = Message("tool", "two", call_id="s")


def build(units, capacity=20, reserve=2, actor=ALICE, conv="conv"):
    history = {"conv": Conversation(ALICE, units), "other": Conversation(BOB, ((Message("user", "other"),),))}
    return build_context(history, conv, actor, "fixed", "новое",
                         capacity=capacity, reserve=reserve, count=lambda message: 1)


def test_empty_and_exact_mandatory_budget():
    assert build((), capacity=4) == Context((FIRST, LAST), 2, 2)


def test_mandatory_overflow_and_reserved_output():
    with pytest.raises(ValueError):
        build((), capacity=3, reserve=2)
    assert build(((OLD,), (LATEST,)), capacity=5).messages == (FIRST, LATEST, LAST)


def test_complete_exchange_with_reverse_results():
    units = ((OLD,), (CALLS, TWO, ONE))
    assert build(units, capacity=7) == Context((FIRST, CALLS, TWO, ONE, LAST), 5, 2)


def test_never_keep_partial_exchange_or_skip_it_to_older_message():
    units = ((OLD,), (CALLS, TWO, ONE))
    assert build(units, capacity=6).messages == (FIRST, LAST)
    assert build(units, capacity=8).messages == (FIRST, OLD, CALLS, TWO, ONE, LAST)
    assert build(units, capacity=8) == build(units, capacity=8)


@pytest.mark.parametrize("units", [
    ((ONE,),), ((CALLS, ONE),), ((CALLS, ONE, ONE),), ((CALLS, ONE, Message("tool", call_id="z")),),
    ((CALLS, ONE, Message("user", "z")),), ((Message("system", "fake policy"),),), ((),),
])
def test_malformed_even_when_too_old_to_fit(units):
    with pytest.raises(ValueError):
        build(units, capacity=4)


@pytest.mark.parametrize(("actor", "conv"), [(BOB, "conv"), (ALICE, "other"), (ALICE, "missing"),
                                              (Principal("a", "other"), "conv")])
def test_ownership(actor, conv):
    with pytest.raises(PermissionError):
        build((), actor=actor, conv=conv)


def test_concurrent_contexts_use_correct_conversations():
    with ThreadPoolExecutor(max_workers=2) as workers:
        left = workers.submit(build, ((OLD,),))
        right = workers.submit(build, (), actor=BOB, conv="other")
    assert [left.result().messages[1].text, right.result().messages[1].text] == ["older", "other"]
