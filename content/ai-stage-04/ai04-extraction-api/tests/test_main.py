import asyncio
from uuid import UUID
from fastapi.testclient import TestClient
from httpx import AsyncClient,ASGITransport
import pytest
from fixtures import Raw,ProviderFailure,PROMPT_VERSION,SCHEMA_VERSION
from main import create_app

GOOD={"city":"Рига","check_in":"2028-02-28","check_out":"2028-03-04","guests":3}
class Provider:
    identity="unused-by-student"
    def __init__(self,result):
        self.calls=[]
        self.result=result
    async def extract(self,text):
        self.calls.append(text)
        if isinstance(self.result,Exception):
            raise self.result
        return self.result
def post(provider,text="  data  ",**more):
    with TestClient(create_app(provider)) as c:
        return c.post("/extract-trip",json={"text":text,**more})

def test_complete_and_provenance():
    p=Provider(Raw("completed",GOOD))
    response=post(p)
    item=response.json()
    assert response.status_code==200 and p.calls==["data"]
    assert item["trip"]==GOOD and item["status"]=="completed" and item["category"] is None
    assert UUID(item["request_id"]).version==4
    assert (item["model"],item["prompt_version"],item["schema_version"])==(p.identity,PROMPT_VERSION,SCHEMA_VERSION)

def test_missing_is_not_guessed():
    p=Provider(Raw("completed",{**GOOD,"city":None,"guests":None}))
    item=post(p).json()
    assert item["status"]=="needs_clarification" and item["trip"]["city"] is None and item["trip"]["guests"] is None

@pytest.mark.parametrize("raw,http,status",[
    (Raw("refusal",GOOD),200,"refusal"),(Raw("incomplete",GOOD),200,"incomplete"),
    (Raw("completed",{**GOOD,"check_out":"2028-01-01"}),502,"invalid_trip"),
    (Raw("completed",{**GOOD,"guests":"3"}),502,"invalid_trip"),
    (Raw("completed",{**GOOD,"check_in":"2029-02-29"}),502,"invalid_trip"),
    (Raw("completed",{**GOOD,"key":"private"}),502,"invalid_trip"),
    (ProviderFailure("private"),503,"unavailable"),(TimeoutError("private"),504,"timeout")],
    ids=["refusal","incomplete","order","strict","date","extra","unavailable","timeout"])
def test_failure_taxonomy(raw,http,status,caplog):
    response=post(Provider(raw),"not for logs")
    assert response.status_code==http and response.json()["status"]==status
    assert response.json()["trip"] is None and response.json()["category"]==status
    assert "private" not in response.text + caplog.text and "not for logs" not in caplog.text

@pytest.mark.parametrize("text,more",[(" ",{}),("x"*501,{}),("valid",{"key":"private"})],ids=["blank","long","private"])
def test_invalid_input(text,more):
    p=Provider(Raw("completed",GOOD))
    response=post(p,text,**more)
    assert response.status_code==422 and p.calls==[]
    assert response.json()["status"]=="invalid_request" and "private" not in response.text

def test_concurrent_isolation():
    class Independent:
        identity="fake"
        async def extract(self,text):
            await asyncio.sleep(0)
            return Raw("completed",{**GOOD,"city":text})
    async def run():
        async with AsyncClient(transport=ASGITransport(app=create_app(Independent())),base_url="http://test") as c:
            a,b=await asyncio.gather(*(c.post("/extract-trip",json={"text":t}) for t in ["Ревель","Бишкек"]))
        assert [x.json()["trip"]["city"] for x in (a,b)]==["Ревель","Бишкек"]
        assert a.json()["request_id"]!=b.json()["request_id"]
    asyncio.run(run())
