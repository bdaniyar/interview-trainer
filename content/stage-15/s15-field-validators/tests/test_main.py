import pytest
from pydantic import ValidationError
from main import LoginInput

def test_normalizes(): assert LoginInput(email=" A@Example.COM ").email == "a@example.com"
@pytest.mark.parametrize("value", ["no-at", "@host", "a@", "a@@b"])
def test_invalid(value):
    with pytest.raises(ValidationError): LoginInput(email=value)
