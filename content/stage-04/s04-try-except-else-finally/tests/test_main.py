import pytest
from main import parse_optional_int

@pytest.mark.parametrize(("value", "expected"), [(None, None), ("", None), ("42", 42), (-3, -3)])
def test_values(value, expected): assert parse_optional_int(value) == expected
@pytest.mark.parametrize("value", [True, "4.2", object()])
def test_invalid(value):
    with pytest.raises(ValueError): parse_optional_int(value)
