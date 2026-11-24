import asyncio
import json

import httpx2
import pytest
from openai import APITimeoutError, InternalServerError

from test_responses import client_for
from tools_roundtrip import Call, ToolProtocolError, roundtrip


def payload(output, *, status="completed"):
    return {"id": "resp_fixture", "object": "response", "created_at": 42, "model": "fixture",
            "status": status, "output": output, "usage": None}


def call():
    return {"type": "function_call", "id": "fc_1", "call_id": "call_get",
            "name": "get_booking", "arguments": '{"booking_id":17}'}


def test_real_sdk_roundtrip_with_two_calls_and_opaque_reasoning_item():
    requests, invoked = [], []
    output = [
        {"type": "reasoning", "id": "rs_1", "summary": [], "encrypted_content": "opaque-fixture"},
        call(), call() | {"id": "fc_2", "call_id": "call_list", "name": "list_my_bookings", "arguments": "{}"},
    ]

    def handle(request):
        assert request.url.path == "/v1/responses" and request.method == "POST"
        requests.append(json.loads(request.content))
        if len(requests) == 1:
            return httpx2.Response(200, json=payload(output))
        return httpx2.Response(200, json=payload([{
            "type": "message", "id": "msg_fin", "status": "completed", "role": "assistant",
            "content": [{"type": "output_text", "text": "Две проверки выполнены", "annotations": []}],
        }]))

    async def execute(proposal):
        invoked.append(proposal)
        return "Алматы" if proposal.name == "get_booking" else "2"

    async def run():
        async with client_for(handle) as client:
            response = await roundtrip(client, "fixture", "Проверь брони", execute)
            assert response.output_text == "Две проверки выполнены"
        assert client.is_closed()

    asyncio.run(run())
    assert invoked == [Call("fc_1", "call_get", "get_booking", {"booking_id": 17}),
                       Call("fc_2", "call_list", "list_my_bookings", {})]
    assert len(requests) == 2
    initial, continuation = requests
    assert initial["store"] is False and initial["include"] == ["reasoning.encrypted_content"]
    assert [tool["name"] for tool in initial["tools"]] == ["get_booking", "list_my_bookings"]
    assert initial["tools"][0]["strict"] is True
    assert initial["tools"][0]["parameters"]["required"] == ["booking_id"]
    assert all(tool["parameters"]["additionalProperties"] is False for tool in initial["tools"])
    assert continuation["tool_choice"] == "none" and "previous_response_id" not in continuation
    assert continuation["input"] == initial["input"] + output + [
        {"type": "function_call_output", "call_id": "call_get", "output": "Алматы"},
        {"type": "function_call_output", "call_id": "call_list", "output": "2"},
    ]


@pytest.mark.parametrize("defect", ["missing_id", "missing_call_id", "json", "array", "duplicate", "outside"])
def test_malformed_call_is_rejected_before_any_tool_runs(defect):
    item = call()
    if defect == "missing_id":
        item.pop("id")
    elif defect == "missing_call_id":
        item.pop("call_id")
    elif defect == "json":
        item["arguments"] = "{"
    elif defect == "array":
        item["arguments"] = "[17]"
    elif defect == "outside":
        item["name"] = "outside"
    output = [item, call() | {"id": "fc_2"}] if defect == "duplicate" else [item]
    requests = []

    def handle(request):
        requests.append(request)
        return httpx2.Response(200, json=payload(output))

    async def execute(proposal):
        pytest.fail("an invalid turn cannot run a tool")

    async def run():
        async with client_for(handle) as client:
            with pytest.raises(ToolProtocolError):
                await roundtrip(client, "fixture", "sample", execute)

    asyncio.run(run())
    assert len(requests) == 1


@pytest.mark.parametrize(("status", "error"), [(None, APITimeoutError), (503, InternalServerError)])
def test_no_retries_after_failed_continuation(status, error):
    requests = []

    def handle(request):
        requests.append(request)
        if len(requests) == 1:
            return httpx2.Response(200, json=payload([call()]))
        if status is None:
            raise httpx2.ReadTimeout("fixture timeout", request=request)
        return httpx2.Response(status, json={"error": {"message": "fixture failure"}})

    async def run():
        async def execute(proposal):
            return "read result"
        async with client_for(handle) as client:
            with pytest.raises(error):
                await roundtrip(client, "fixture", "sample", execute)

    asyncio.run(run())
    assert len(requests) == 2


def test_incomplete_initial_turn_does_not_execute_partial_call():
    async def run():
        async def execute(proposal):
            pytest.fail("incomplete turn must not run a tool")
        async with client_for(lambda _: httpx2.Response(200, json=payload([call()], status="incomplete"))) as client:
            assert (await roundtrip(client, "fixture", "sample", execute)).status == "incomplete"

    asyncio.run(run())
