import math
import pytest
from main import dot, norm, matvec

def test_rectangular_values():
    assert matvec([[1,2,3],[-2,0,5]], [2,0,-1]) == [-1,-9]
    assert dot([-4, 3, 7],[2,-2,0]) == -14
def test_empty_and_zero():
    assert dot([],[]) == norm([]) == norm([0,0]) == 0
    assert matvec([[],[]],[]) == [0,0]
    assert matvec([], [5,6]) == []
def test_float_arithmetic():
    assert dot([0.2, 0.1],[0.3, 0.3]) == pytest.approx(0.09)
    assert norm([1e100,-1e100]) == pytest.approx(math.sqrt(2)*1e100)
@pytest.mark.parametrize("bad", [math.nan, math.inf, True, "4"], ids=["nan","inf","bool","str"])
def test_invalid_coordinates(bad):
    for call in (lambda:dot([bad],[0]),lambda:norm([bad]),lambda:matvec([[bad]],[3])):
        with pytest.raises(ValueError): call()
@pytest.mark.parametrize("call", [lambda:dot([1],[2,3]),lambda:matvec([[1,2],[3]],[4,5]),
                                  lambda:matvec([[1,2,3]],[1,2])], ids=["dot","ragged","cols"])
def test_shape(call):
    with pytest.raises(ValueError): call()
