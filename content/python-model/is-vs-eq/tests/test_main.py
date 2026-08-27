from main import compare_objects


def test_same_object():
    value = [1]
    assert compare_objects(value, value) == {"same_identity": True, "same_value": True}


def test_equal_distinct_objects():
    assert compare_objects([1], [1]) == {"same_identity": False, "same_value": True}


def test_different_values():
    assert compare_objects([1], [2]) == {"same_identity": False, "same_value": False}
