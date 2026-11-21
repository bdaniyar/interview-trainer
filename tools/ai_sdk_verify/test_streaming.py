import asyncio
import json

import httpx2

from example import open_stream
from test_responses import client_for


def test_stream_events_and_client_cleanup():
    opens = []

    class Bytes(httpx2.AsyncByteStream):
        async def __aiter__(self):
            completed = {"id": "resp_test", "object": "response", "status": "completed",
                         "model": "fixture", "created_at": 10, "output": []}
            for event in [
                {"type": "response.output_text.delta", "delta": "ё", "item_id": "m1",
                 "output_index": 0, "content_index": 0, "sequence_number": 1, "logprobs": []},
                {"type": "response.completed", "response": completed, "sequence_number": 2},
            ]:
                yield f"event: {event['type']}\ndata: {json.dumps(event, ensure_ascii=False)}\n\n".encode()

        async def aclose(self):
            opens.append("closed")

    def handler(request):
        assert request.url.path == "/v1/responses"
        assert json.loads(request.content) == {
            "model": "fixture", "input": "?", "stream": True, "store": False,
        }
        return httpx2.Response(200, headers={"content-type": "text/event-stream"}, stream=Bytes())

    async def run():
        async with client_for(handler) as client:
            async with await open_stream(client, "fixture", "?") as stream:
                events = [event async for event in stream]
            assert len(events) == 2 and events[0].delta == "ё"
            assert events[-1].type == "response.completed"
            assert events[-1].response.status == "completed"

    asyncio.run(run())
    assert opens == ["closed"]
