import pytest
from main import compare

def test_detects_regression_and_undefined():
    report=compare({"metrics":{"x":{"rate":0.5},"y":{"rate":None}},"errors":{"a":[],"b":["old"]}},
                   {"metrics":{"x":{"rate":0.25},"y":{"rate":0.8}},"errors":{"a":["city"],"b":["new detail"]}})
    assert report=={"delta":{"x":-0.25,"y":None},"new_errors":["a"]}

@pytest.mark.parametrize("after", [{"metrics":{},"errors":{"b":[]}},{"metrics":{"new":{"rate":0}},"errors":{"a":[]}}],
                         ids=["different-cases","different-metrics"])
def test_rejects_different_partitions(after):
    with pytest.raises(ValueError):
        compare({"metrics":{},"errors":{"a":[]}},after)
