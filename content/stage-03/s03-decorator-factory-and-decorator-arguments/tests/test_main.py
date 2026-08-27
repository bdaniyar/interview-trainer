import pytest
from main import retry

def test_retry_then_success():
    retries = []
    @retry(3, (ValueError,), retries.append)
    def work():
        if len(retries) < 2: raise ValueError("temporary")
        return "ok"
    assert work() == "ok" and retries == [1, 2]
def test_last_error():
    @retry(2, (ValueError,))
    def work(): raise ValueError("boom")
    with pytest.raises(ValueError, match="boom"): work()
def test_permanent_not_retried():
    @retry(3, (ValueError,))
    def work(): raise TypeError("bad")
    with pytest.raises(TypeError): work()
