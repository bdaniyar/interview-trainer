from dataclasses import replace

import pytest

from contracts import Row, Scope
from main import exact


ACTOR = Scope("east", "ana", "a")
OWN = Row("east", "ana", frozenset(), "real", 8, 8, False, "a", "b", (1, 0))


@pytest.mark.parametrize("patch", [
    {"tenant": "west"}, {"owner": "other"}, {"space": "a-migration"},
    {"version": 7}, {"deleted": True},
])
def test_ineligible_row_is_filtered_before_reading_embedding(patch):
    denied = replace(OWN, embedding=(), **patch)
    assert exact(ACTOR, (1, 2), (denied,), 3) == []


def test_owner_and_authorized_reader_tie_order():
    rows = (OWN, replace(OWN, document="a", chunk_id="q", owner="bob", readers=frozenset({"ana"})),
            replace(OWN, embedding=(0, 1), document="side"))
    result = exact(ACTOR, (1, 0), rows, 9)
    assert result == [("a", 8, "q", 0), ("real", 8, "b", 0), ("side", 8, "b", 1)]
    assert exact(ACTOR, (1, 0), rows, 1) == result[:1]


def test_no_read_scope():
    with pytest.raises(PermissionError):
        exact(replace(ACTOR, may_read=False), (1, 0), (), 3)


@pytest.mark.parametrize("embedding", [(0, 0), (1,), (True, 0), (float("nan"), 1)])
def test_embedding_errors(embedding):
    with pytest.raises(ValueError):
        exact(ACTOR, (1, 0), (replace(OWN, embedding=embedding),), 3)


def test_empty_limit_invalid_limit_and_cosine_distance():
    assert exact(ACTOR, (-1, 0), (OWN,), 5)[0][-1] == 2
    assert exact(ACTOR, (1, 0), (OWN,), 0) == []
    with pytest.raises(ValueError):
        exact(ACTOR, (1, 0), (OWN,), True)
