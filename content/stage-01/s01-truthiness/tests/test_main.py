import pytest
from main import normalize_limit

def test_none_uses_default(): assert normalize_limit(None, 30) == 30
def test_zero_is_not_missing(): assert normalize_limit(0) == 0
def test_boundaries(): assert (normalize_limit(1), normalize_limit(100)) == (1, 100)
@pytest.mark.parametrize("value", [-1, 101, True, "10"])
def test_invalid(value):
    with pytest.raises(ValueError): normalize_limit(value)
