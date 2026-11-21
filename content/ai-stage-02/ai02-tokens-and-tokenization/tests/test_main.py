import pytest
from main import decode, encode, fits_budget


@pytest.mark.parametrize(("version", "expected"), [("A", [4, 0x1f642 + 100, 2]), ("B", [14, 132, 0x1f642 + 100, 11, 12])])
def test_versions_and_unicode(version, expected):
    value = "def 🙂привет"
    assert encode(value, version) == expected
    assert decode([0, *expected, 1], version) == value
    assert fits_budget(value, version, len(expected) + 2)
    assert not fits_budget(value, version, len(expected) + 1)


def test_empty_input():
    assert encode("", "B") == []
    assert decode([0, 1], "B") == ""
    assert fits_budget("", "B", 2)
    assert not fits_budget("", "B", 1)


@pytest.mark.parametrize("ids", [[0], [2, 1], [0, 1, 1], [99], [0x110000 + 100]])
def test_invalid_ids(ids):
    with pytest.raises(ValueError):
        decode(ids, "A")


def test_unknown_version_and_negative_budget():
    with pytest.raises(ValueError):
        encode("", "C")
    with pytest.raises(ValueError):
        fits_budget("", "A", -1)
