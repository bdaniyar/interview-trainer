import pytest
from main import User

def test_subclass_and_normalization():
    class Admin(User): pass
    value = Admin.from_mapping({"id": 7, "email": " A@Example.COM "})
    assert isinstance(value, Admin) and (value.user_id, value.email) == (7, "a@example.com")
def test_invalid():
    with pytest.raises(ValueError): User.from_mapping({"id": 0, "email": "a@x.io"})
