from dataclasses import dataclass

PROMPT_VERSION="lab.prompt.v1"
SCHEMA_VERSION="lab.schema.v1"

@dataclass(frozen=True)
class Raw:
    status:str
    data:dict|None=None

class ProviderFailure(Exception):
    pass

def demo(make_app):
    from fastapi.testclient import TestClient
    class Local:
        identity="demo-extractor"
        async def extract(self,text):
            return Raw("completed",{"city":"Рига","check_in":None,"check_out":None,"guests":None})
    with TestClient(make_app(Local())) as client:
        response=client.post("/extract-trip",json={"text":"Хочу в Ригу"})
    assert response.status_code==200 and response.json()["status"]=="needs_clarification"
    print(response.json())
