from math import inf,log
import pytest
from main import sequence_nll

def test_shift_and_mean():
    assert sequence_nll(["B","x","y"],[{"x":.2,"y":.8},{"x":.3,"y":.7}])==pytest.approx(-log(.14)/2)
def test_masked_excluded():
    assert sequence_nll(["B","x","y"],[{},{"y":.4,"x":.6}],(1,))==pytest.approx(-log(.4))
def test_zero_and_empty():
    assert sequence_nll(["B","x"],[{"y":1}])==inf
    assert sequence_nll(["B","x"],[{"x":0,"y":1}])==inf
    assert sequence_nll(["B"],[]) is None
    assert sequence_nll(["B","x"],[{}],(1,)) is None
@pytest.mark.parametrize("rows,mask", [([{}],[]),([{"x":float("nan")}],[]),([{"x":-1,"z":2}],[]),
                                        ([{"x":.4}],[]),([],[]),([{"x":1}],[0])],
                         ids=["empty","nonfinite","negative","sum","length","badmask"])
def test_invalid(rows,mask):
    with pytest.raises(ValueError):
        sequence_nll(["B","x"],rows,mask)
