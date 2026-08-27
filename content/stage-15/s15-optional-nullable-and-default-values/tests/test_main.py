import pytest
from pydantic import ValidationError
from main import UserPatch

def test_missing(): assert UserPatch().model_dump(exclude_unset=True) == {}
def test_explicit_null(): assert UserPatch(display_name=None).model_dump(exclude_unset=True) == {"display_name": None}
def test_extra():
    with pytest.raises(ValidationError): UserPatch(role="admin")
