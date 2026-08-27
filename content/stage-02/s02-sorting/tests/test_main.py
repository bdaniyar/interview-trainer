from main import sort_events

def test_descending_and_stable():
    rows = [
        {"id": "a", "created_at": 2}, {"id": "b", "created_at": 3},
        {"id": "c", "created_at": 3}, {"id": "d", "created_at": 1},
    ]
    result = sort_events(rows)
    assert [row["id"] for row in result] == ["b", "c", "a", "d"]
    assert result is not rows and [row["id"] for row in rows] == ["a", "b", "c", "d"]
