from copy import deepcopy
import pytest
from main import step, train

def test_simultaneous_update():
    assert step([(2,5),(0,1)],1,0,0.25)==dict(predictions=[2,0],loss=5,dw=-6,db=-4,w=2.5,b=1)
def test_finite_difference():
    rows=[(-2,1),(1,-3),(3,5),(4,5)]
    w,b=0.7,-0.6
    def baseline(weight,bias):
        return sum((weight*x+bias-y)**2 for x,y in rows)/len(rows)
    e=1e-5
    out=step(rows,w,b,0.04)
    assert out["dw"]==pytest.approx((baseline(w+e,b)-baseline(w-e,b))/(2*e))
    assert out["db"]==pytest.approx((baseline(w,b+e)-baseline(w,b-e))/(2*e))
def test_training():
    rows=[[-1,-1],[0,2],[1,5],[2,8]]
    before=deepcopy(rows)
    assert train(rows,-1,0,0.1,0)==(-1,0)
    w,b=train(rows,-1,0,0.1,20)
    assert step(rows,w,b,0.1)["loss"]<0.05
    assert rows==before
@pytest.mark.parametrize("rows,rate", [([],0.1), ([(1,float("nan"))],0.1), ([(1,2)],0), ([(1,2)],-0.1)],
                        ids=["empty","nan","zero","negative"])
def test_invalid(rows,rate):
    with pytest.raises(ValueError): step(rows,0,0,rate)
def test_invalid_steps():
    with pytest.raises(ValueError): train([(0,0)],0,0,1,-1)
