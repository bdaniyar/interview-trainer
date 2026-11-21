import asyncio

from harness import demo


async def verify_contract(probe):
    success = await probe("success")
    assert success.http == 200 and success.body["status"] == "completed"
    assert success.calls == 1 and success.body["text"] == success.expected_text

    for case, http in [
        ("empty", 502), ("refusal", 200), ("incomplete", 200),
        ("unavailable", 503), ("timeout", 504),
    ]:
        result = await probe(case)
        assert result.http == http and result.body["status"] == case
        assert result.body["text"] is None and result.calls == 1
        if case == "timeout":
            assert result.cleaned

    invalid = await probe("invalid")
    assert invalid.http == 422 and invalid.body["status"] == "invalid_request" and invalid.calls == 0

    cancelled = await probe("cancellation")
    assert cancelled.cancelled and cancelled.cleaned

    isolated = await probe("isolation")
    assert isolated.http == 200 and isolated.calls == 2
    assert isolated.body["status"] == isolated.second["status"] == "completed"
    assert isolated.body["request_id"] != isolated.second["request_id"]
    assert isolated.body["text"] == isolated.expected_text
    assert isolated.second["text"] == isolated.expected_second

    flow = await probe("stream_cleanup")
    assert flow.cleaned and flow.deltas == (flow.expected_text,) and bool(flow.expected_text)

    offline = await probe("offline")
    assert offline.http == 503 and offline.body["status"] == "unavailable"
    assert offline.socket_calls == 0 and not offline.secret_seen


if __name__ == "__main__":
    asyncio.run(demo(verify_contract))
