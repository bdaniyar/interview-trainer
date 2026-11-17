import pytest
from main import backoff

@pytest.mark.parametrize('attempt,base,cap,result',[(1,1,8,1),(2,1,8,2),(4,1,8,8),(8,1,8,8),(3,.25,2,1),(2,5,5,5)], ids=['case-1', 'case-2', 'case-3', 'case-4', 'case-5', 'case-6'])
def test_delays(attempt,base,cap,result):assert backoff(attempt,base,cap)==result

@pytest.mark.parametrize('args',[(0,),(-1,),(True,),(1.5,),(9,),(1,0,8),(1,-1,8),(1,9,8),(1,float('nan'),8),(1,1,float('inf')),(1,False,8)], ids=['case-1', 'case-2', 'case-3', 'case-4', 'case-5', 'case-6', 'case-7', 'case-8', 'case-9', 'case-10', 'case-11'])
def test_invalid(args):
    with pytest.raises(ValueError):backoff(*args)
