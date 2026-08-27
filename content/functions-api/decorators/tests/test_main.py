from dataclasses import dataclass
import pytest
from main import require_role

@dataclass
class User: roles: set[str]

@require_role("admin")
def delete(user, item_id): return item_id

def test_allows(): assert delete(User({"admin"}), 7) == 7
def test_denies():
    with pytest.raises(PermissionError): delete(User({"reader"}), 7)
def test_metadata(): assert delete.__name__ == "delete"
