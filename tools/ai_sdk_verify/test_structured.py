import asyncio
import json

import httpx2
import pytest
from pydantic import ValidationError

from structured import WireExtraction, parse_trip
from test_responses import client_for


TRIP = {"city": "Алматы", "check_in": None, "check_out": None, "guests": 3}


def response(status, part=None):
    output = [] if part is None else [{
        "id": "msg_fixture",
        "type": "message",
        "role": "assistant",
        "status": status,
        "content": [part],
    }]
    return {"object": "response", "id": "resp_fixture", "created_at": 0, "model": "fake",
            "status": status, "output": output, "usage": None}


def output_text(text):
    return {"type": "output_text", "text": text, "annotations": []}


def test_structured_wire_request_and_parsed_nested_value():
    requests = []

    def handle(request):
        requests.append(request)
        return httpx2.Response(200, json=response("completed", output_text(json.dumps({"trip": TRIP}))))

    async def run():
        async with client_for(handle) as client:
            parsed = await parse_trip(client, "fake", "Нас трое, Алматы")
            assert isinstance(parsed.output_parsed, WireExtraction)
            assert parsed.output_parsed.trip.model_dump() == TRIP

    asyncio.run(run())
    assert len(requests) == 1 and requests[0].url.path == "/v1/responses"
    body = json.loads(requests[0].content)
    assert body["store"] is False and body["max_output_tokens"] == 384
    assert body["input"][0]["content"][0]["text"] == "Нас трое, Алматы"
    format_ = body["text"]["format"]
    assert format_["type"] == "json_schema" and format_["strict"] is True
    schema = format_["schema"]
    assert schema["required"] == ["trip"] and schema["additionalProperties"] is False
    nested = schema["$defs"]["WireTrip"]
    assert set(nested["required"]) == set(TRIP) and nested["additionalProperties"] is False
    assert {"type": "null"} in nested["properties"]["check_in"]["anyOf"]


@pytest.mark.parametrize(("status", "part"), [
    ("completed", {"type": "refusal", "refusal": "synthetic refusal"}),
    ("incomplete", None),
], ids=["refusal", "incomplete"])
def test_structured_non_success_has_no_parsed_object(status, part):
    async def run():
        async with client_for(lambda _: httpx2.Response(200, json=response(status, part))) as client:
            parsed = await parse_trip(client, "fake", "synthetic")
            assert parsed.status == status and parsed.output_parsed is None
            if part:
                assert parsed.output[0].content[0].type == "refusal"

    asyncio.run(run())


@pytest.mark.parametrize(("status", "payload"), [
    ("completed", '{"trip":'),
    ("completed", '{"trip":{"city":"Костанай"}}'),
    ("incomplete", '{"trip":'),
], ids=["malformed-json", "missing-fields", "truncated-text"])
def test_sdk_can_raise_validation_error_before_returning_response(status, payload):
    async def run():
        async with client_for(lambda _: httpx2.Response(200, json=response(status, output_text(payload)))) as client:
            with pytest.raises(ValidationError):
                await parse_trip(client, "fake", "synthetic")

    asyncio.run(run())
