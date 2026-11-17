import pytest
from main import periodic_key

@pytest.mark.parametrize('epoch,period,bucket',[(0,60,0),(59,60,0),(60,60,1),(119,60,1),(120,60,2),(9007199254740993,1,9007199254740993)], ids=['case-1', 'case-2', 'case-3', 'case-4', 'case-5', 'case-6'])
def test_stable_windows(epoch,period,bucket):assert periodic_key('training',epoch,period)==f'periodic:training:{bucket}'

def test_different_schedules():assert periodic_key('a',1,60)!=periodic_key('b',1,60)

@pytest.mark.parametrize('args',[('',1,60),('x'*65,1,60),('x',-1,60),('x',True,60),('x',1,False),('x',1,0),('x',1.5,2)], ids=['case-1', 'case-2', 'case-3', 'case-4', 'case-5', 'case-6', 'case-7'])
def test_invalid(args):
    with pytest.raises(ValueError):periodic_key(*args)
