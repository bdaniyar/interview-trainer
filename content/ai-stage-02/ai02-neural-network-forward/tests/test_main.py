from copy import deepcopy
import pytest
from main import forward,sensitivity

def inputs():
    return ([2,-1], [[1,2],[-1,1]], [1,2], [[-3,4],[7,2]], [-2,1])

def test_shapes_values_no_mutation():
    args=inputs()
    before=deepcopy(args)
    assert forward(*args)==[-5,8] and args==before

def test_central_difference():
    args=inputs()
    e=1e-5
    for out,h,j in ((0,0,1),(1,0,0),(0,1,0)):
        hi,lo=deepcopy(args),deepcopy(args)
        hi[1][h][j]+=e
        lo[1][h][j]-=e
        assert sensitivity(*args,out,h,j)==pytest.approx((forward(*hi)[out]-forward(*lo)[out])/(2*e), abs=1e-8)
def test_kink_and_indices():
    with pytest.raises(ValueError):
        sensitivity([1],[[1]],[-1],[[1]],[0],0,0,0)
    with pytest.raises(ValueError):
        sensitivity(*inputs(),0,-1,0)

@pytest.mark.parametrize("i,value",[(0,[]),(1,[[1],[2,3]]),(2,[0]),(3,[[float("inf"),1]]),(4,[0,0,1])],
                         ids=["empty","ragged","bias1","nonfinite","bias2"])
def test_bad_layers(i,value):
    args=list(inputs())
    args[i]=value
    with pytest.raises(ValueError):
        forward(*args)
