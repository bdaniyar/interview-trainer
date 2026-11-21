import asyncio
import json

import httpx2
import pytest
from openai import AsyncOpenAI, APITimeoutError, AuthenticationError, RateLimitError

from example import get_response


def client_for(handler):
    return AsyncOpenAI(
        api_key="offline-test", base_url="https://provider.invalid/v1",
        max_retries=0, http_client=httpx2.AsyncClient(transport=httpx2.MockTransport(handler)),
    )


def test_current_sdk_serializes_responses_and_reads_multiple_items():
    requests = []

    def handler(request):
        requests.append(request)
        return httpx2.Response(200, json={
            "id": "resp_sample", "object": "response", "created_at": 42, "model": "test-model",
            "status": "completed", "output": [
                {"id": "r1", "type": "reasoning", "summary": []},
                {"id": "m1", "type": "message", "status": "completed", "role": "assistant",
                 "content": [{"type": "output_text", "text": "сначала", "annotations": []},
                             {"type": "output_text", "text": " каталог", "annotations": []}]},
            ],
            "usage": {"input_tokens": 11, "output_tokens": 7, "total_tokens": 18,
                      "input_tokens_details": {"cached_tokens": 2},
                      "output_tokens_details": {"reasoning_tokens": 0}},
        })

    async def run():
        async with client_for(handler) as client:
            response = await get_response(client, "test-model", "Где описание?")
            assert response.status == "completed"
            assert [item.type for item in response.output] == ["reasoning", "message"]
            assert response.output_text == "сначала каталог"
            assert response.usage.input_tokens_details.cached_tokens == 2
        assert client.is_closed()

    asyncio.run(run())
    assert len(requests) == 1
    request = requests[0]
    assert request.method == "POST" and request.url.path == "/v1/responses"
    body = json.loads(request.content)
    assert body == {
        "model": "test-model", "instructions": "Explain the catalog entry briefly.",
        "input": [{"role": "user", "content": [{"type": "input_text", "text": "Где описание?"}]}],
        "store": False,
    }


def test_incomplete_and_usage_missing():
    result = {"id": "resp_cut", "object": "response", "created_at": 42, "model": "test-model",
              "status": "incomplete", "incomplete_details": {"reason": "max_output_tokens"},
              "output": [], "usage": None}

    async def run():
        async with client_for(lambda request: httpx2.Response(200, json=result)) as client:
            response = await get_response(client, "test-model", "?")
            assert response.output_text == "" and response.usage is None
            assert response.status == "incomplete" and response.incomplete_details.reason == "max_output_tokens"

    asyncio.run(run())


@pytest.mark.parametrize(("status", "error"), [(401, AuthenticationError), (429, RateLimitError), (None, APITimeoutError)])
def test_sdk_errors_and_explicit_retry_budget(status, error):
    requests = []

    def handler(request):
        requests.append(request)
        if status is None:
            raise httpx2.ReadTimeout("test timeout", request=request)
        return httpx2.Response(status, json={"error": {"message": "synthetic failure"}}, headers={"Retry-After": "1"})

    async def run():
        async with client_for(handler) as client:
            with pytest.raises(error) as rejected:
                await get_response(client, "test-model", "x")
            if status == 429:
                assert rejected.value.response.headers["retry-after"] == "1"

    asyncio.run(run())
    assert len(requests) == 1
