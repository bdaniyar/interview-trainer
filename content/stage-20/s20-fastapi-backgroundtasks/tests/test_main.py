import asyncio
import json
import pytest
from fastapi.testclient import TestClient
from main import make_app

def test_real_asgi_response_precedes_background_effect():
    events=[]
    app=make_app(lambda value: events.append(('sink',value)))
    body=json.dumps({'value':'audit'}).encode()
    async def run():
        sent=False
        async def receive():
            nonlocal sent
            if not sent:sent=True;return {'type':'http.request','body':body,'more_body':False}
            return {'type':'http.disconnect'}
        async def send(message):
            if message['type']=='http.response.start':events.append(('status',message['status']))
            if message['type']=='http.response.body' and not message.get('more_body'):events.append(('body',True))
        await app({'type':'http','asgi':{'version':'3.0','spec_version':'2.3'},'http_version':'1.1','method':'POST','scheme':'http','path':'/events','raw_path':b'/events','query_string':b'','headers':[(b'content-type',b'application/json')],'server':('test',80),'client':('test',123),'root_path':''},receive,send)
    asyncio.run(run())
    assert ('status',202) in events and events.count(('sink','audit'))==1
    assert events.index(('body',True))<events.index(('sink','audit'))

@pytest.mark.parametrize('value',['x','unicode-Я'], ids=['case-1', 'case-2'])
def test_accepts_one_event(value):
    seen=[]
    with TestClient(make_app(seen.append)) as client:
        response=client.post('/events',json={'value':value})
        assert response.status_code==202 and response.json()=={'accepted':True}
    assert seen==[value]

@pytest.mark.parametrize('payload',[{}, {'value':''},{'value':5},{'value':'x'*21}], ids=['case-1', 'case-2', 'case-3', 'case-4'])
def test_invalid_input_has_no_effect(payload):
    seen=[]
    with TestClient(make_app(seen.append)) as client:assert client.post('/events',json=payload).status_code==422
    assert seen==[]
