import pytest
from main import can_commit

@pytest.mark.parametrize('args,expected',[(('running',2,2,10,9),True),(('running',2,1,10,9),False),(('running',2,3,10,9),False),(('running',2,2,10,10),False),(('running',2,2,10,11),False),(('cancelled',2,2,10,9),False),(('succeeded',2,2,10,9),False),(('queued',0,0,10,9),False)], ids=['case-1', 'case-2', 'case-3', 'case-4', 'case-5', 'case-6', 'case-7', 'case-8'])
def test_ownership(args,expected):assert can_commit(*args) is expected

@pytest.mark.parametrize('args',[({},1,1,10,9),('other',1,1,10,9),('running',True,1,10,9),('running',1,-1,10,9),('running',1,1,float('inf'),9),('running',1,1,10,True)], ids=['case-1', 'case-2', 'case-3', 'case-4', 'case-5', 'case-6'])
def test_invalid(args):
    with pytest.raises(ValueError):can_commit(*args)
