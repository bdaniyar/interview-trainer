import itertools
import pytest
from main import score

@pytest.mark.parametrize("inputs", list(itertools.product([True, False], repeat=4)), ids=[f"case-{i}" for i in range(16)])
def test_dimensions(inputs):
    a,b,c,d=inputs
    expected="fail" if False in (a,b,c) else "clarify" if d else "pass"
    assert score(*inputs) == expected

def test_strict_signals():
    with pytest.raises(ValueError):
        score(True, True, "False")
