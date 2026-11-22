from math import exp,sqrt
import pytest
from main import attention,softmax

def test_stable_normalization():
    assert softmax([10000,10001,10002])==pytest.approx(softmax([-2,-1,0]))
    assert sum(softmax([3000,3000]))==pytest.approx(1)
def test_scale_rectangular_values_and_mask():
    q=[[2,0],[2,0],[0,1]]
    k=[[0,0],[1,0],[10,0]]
    v=[[1,2],[3,5],[900,900]]
    result, w=attention(q,k,v)
    p=exp(sqrt(2))/(1+exp(sqrt(2)))
    assert w[0]==[1,0,0] and w[1]==pytest.approx([1-p,p,0])
    assert result[1]==pytest.approx([1+2*p,2+3*p])
    assert len(result)==3 and all(len(row)==2 for row in result)
    assert all(sum(row)==pytest.approx(1) for row in w)
    assert attention(q,k,[*v[:2],[-900,-900]])[0][:2]==result[:2]
def test_full_mode():
    result,rows=attention([[0],[0]], [[11],[9]], [[8],[-4]], False)
    assert rows==[[0.5,0.5],[0.5,0.5]] and result==[[2],[2]]
@pytest.mark.parametrize("data", [([],[],[]), ([[1]],[[1,2]],[[1]]), ([[1],[2,3]],[[1],[2]],[[0],[0]]),
                                  ([[1]],[[1]],[[0],[1]]), ([[1]],[[float("inf")]],[[0]])],
                         ids=["empty","width","ragged","count","nonfinite"])
def test_invalid(data):
    with pytest.raises(ValueError): attention(*data)
