from copy import deepcopy

import pytest

from main import split_bookings


def row(identifier, owner, time):
    return {"id": identifier, "user_id": owner, "booked_at": time,
            "features": {"now": (identifier, time), "future": (42, time + 1)}, "label": 0}


def test_no_group_leak_no_lost_ids_and_stable_order():
    entries = [row(9, "d", 20), row(5, "b", 3), row(6, "b", 10), row(2, "a", 0),
                row(1, "a", 0), row(8, "c", 11)]
    before = deepcopy(entries)
    result = split_bookings(entries, 10, 20)
    assert {k: [r["id"] for r in v] for k, v in result.items()} == {
        "train": [1, 2], "validation": [8], "test": [9], "quarantine": [5, 6],
    }
    assert entries == before
    assert result == split_bookings(reversed(entries), 10, 20)
    assert all(r["features"] == {"now": (r["id"], r["booked_at"])}
               for group in result.values() for r in group)


def test_empty_split():
    assert all(not group for group in split_bookings([], 0, 1).values())


@pytest.mark.parametrize(("rows", "first", "second"), [
    ([row(1, "x", 0), row(1, "y", 12)], 10, 20), ([], 12, 12), ([], 30, 10),
])
def test_invalid_data(rows, first, second):
    with pytest.raises(ValueError):
        split_bookings(rows, first, second)
