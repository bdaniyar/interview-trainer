import pytest
from fixtures import Embedding as E
from main import normalize,cosine,rank

def test_cosine_and_normalization():
    a,b=E("m@7",3,(3,4,0)),E("m@7",3,(0,2,0))
    assert normalize(a)==pytest.approx((.6,.8,0))
    assert cosine(a,b)==pytest.approx(.8)
    assert cosine(a,E("m@7",3,(-6,-8,0)))==pytest.approx(-1)
def test_stable_ranking():
    q=E("v",2,(1,0))
    assert rank(q,{"z":q,"b":E("v",2,(0,2)),"a":q})==[("a",1),("z",1),("b",0)]
    assert rank(q,{})==[]
@pytest.mark.parametrize("data",[E("m",2,(0,0)),E("m",2,(1,)),E("m",2,(1,float("inf"))),E("m",1,(True,))],
                         ids=["zero","wrong-dims","nonfinite","bool"])
def test_invalid(data):
    with pytest.raises(ValueError): normalize(data)
def test_different_model_and_width():
    for data in [E("b",2,(1,4)),E("a",3,(1,0,0))]:
        with pytest.raises(ValueError): cosine(E("a",2,(1,4)),data)
