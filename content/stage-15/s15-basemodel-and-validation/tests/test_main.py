import pytest
from pydantic import ValidationError
from main import UserCreate

def test_valid(): assert UserCreate(username="aida", age=18).model_dump() == {"username": "aida", "age": 18}
@pytest.mark.parametrize("data", [{"username": "ab", "age": 18}, {"username": "aida", "age": 13}])
def test_invalid(data):
    with pytest.raises(ValidationError): UserCreate(**data)
