import asyncio
import pytest
from fixtures import Outcome, Request
from main import recover

class Script:
    def __init__(self,*outcomes):
        self.outcomes=list(outcomes)
        self.calls=[]
    async def __call__(self,request,*,repair):
        self.calls.append((request,repair))
        value=self.outcomes.pop(0)
        if isinstance(value,BaseException): raise value
        return value
def run(*outcomes,allowed=True):
    request=Request("Осло {данные}", "c-202")
    script=Script(*outcomes)
    result=asyncio.run(recover(script,request,allow_repair=allowed))
    assert all(r is request for r,_ in script.calls)
    assert [b for _,b in script.calls]==[False,True][:len(script.calls)]
    assert result.correlation_id==request.correlation_id and result.attempts==len(script.calls)
    return result
@pytest.mark.parametrize("kind",["refusal","permanent","incomplete","malformed","retryable"])
def test_without_authorization(kind):
    assert run(Outcome(kind),allowed=False).status==kind
def test_refusal_and_timeout_are_terminal():
    assert run(Outcome("refusal")).status=="refusal"
    assert run(TimeoutError("private")).status=="timeout"
def test_budget_not_reset():
    assert run(Outcome("incomplete"),Outcome("malformed")).status=="malformed"
    assert run(Outcome("incomplete"),Outcome("incomplete")).attempts==2
def test_unknown_and_invalid():
    trip={"city":"Осло","check_in":None,"check_out":None,"guests":2}
    result=run(Outcome("retryable"),Outcome("completed",trip))
    assert result.status=="needs_clarification" and result.trip==trip
    assert run(Outcome("completed",{**trip,"guests":-7})).status=="invalid_domain"
    assert run(Outcome("completed",{**trip,"check_in":"2028-01-20","check_out":"2028-01-19"})).status=="invalid_domain"
def test_cancel():
    with pytest.raises(asyncio.CancelledError): run(asyncio.CancelledError())
