import pytest
from main import Transaction

class Resource:
    def __init__(self): self.calls = []
    def commit(self): self.calls.append("commit")
    def rollback(self): self.calls.append("rollback")

def test_commit():
    resource = Resource()
    with Transaction(resource) as value: assert value is resource
    assert resource.calls == ["commit"]
def test_rollback():
    resource = Resource()
    with pytest.raises(RuntimeError):
        with Transaction(resource): raise RuntimeError("boom")
    assert resource.calls == ["rollback"]
