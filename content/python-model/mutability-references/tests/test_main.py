from main import append_marker


def test_mutates_original():
    items = [1, 2]
    append_marker(items, 3)
    assert items == [1, 2, 3]


def test_returns_same_object():
    items = []
    result = append_marker(items, "x")
    assert result is items


def test_accepts_any_marker():
    marker = {"ready": True}
    items = []
    assert append_marker(items, marker) == [marker]
