import pytest
from fixtures import Block
from main import select_context


def test_budget_group_and_atomic_pairs():
    first = Block("x", ("summary",), 4, priority=1)
    policy = Block(None, ("policy",), 2, True)
    pair = Block("x", ("call", "result"), 7, priority=9)
    recent = Block("x", ("recent",), 4, priority=1)
    foreign = Block("y", ("private",), 0, True)
    blocks = [first, policy, pair, recent, foreign]
    assert select_context(blocks, "x", 10, 3, 1) == [policy, recent]
    assert select_context(blocks, "x", 12, 2, 1) == [policy, pair]
    assert select_context(blocks, "y", 3, 1) == [policy, foreign]


def test_preserve_order_within_budget():
    early = Block("x", ("one",), 2)
    late = Block("x", ("two",), 1, priority=100)
    assert select_context([early, late], "x", 5, 2) == [early, late]


def test_empty_and_invalid_budget():
    assert select_context([], "x", 10, 10) == []
    for options in [(10, 11, 0), (10, 0, -1)]:
        with pytest.raises(ValueError):
            select_context([], "x", *options)
    with pytest.raises(ValueError):
        select_context([Block(None, ("policy",), 8, True)], "x", 10, 3)
