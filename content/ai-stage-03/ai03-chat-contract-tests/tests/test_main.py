import asyncio
from dataclasses import replace

import pytest

from harness import CASES, Probe
from main import verify_contract


def test_healthy_contract_with_independently_selected_prompts():
    seen = []
    real = Probe("ночной режим 🚀", "временной пояс")

    async def observe(case):
        seen.append(case)
        return await real(case)

    asyncio.run(verify_contract(observe))
    assert set(seen) == set(CASES)


@pytest.fixture(scope="module")
def observations():
    # Capture real ASGI observations once. Each mutant changes exactly one property.
    baseline = Probe("отложенный вызов", "инструкция к тесту")

    async def capture():
        return {case: await baseline(case) for case in CASES}

    return asyncio.run(capture())


@pytest.mark.parametrize(("bad_case", "corruption"), [
    ("success", lambda o: replace(o, body={**o.body, "text": "same for everyone"})),
    ("empty", lambda o: replace(o, http=200)),
    ("refusal", lambda o: replace(o, body={**o.body, "text": "private"})),
    ("incomplete", lambda o: replace(o, body={**o.body, "status": "completed"})),
    ("unavailable", lambda o: replace(o, http=500)),
    ("timeout", lambda o: replace(o, cleaned=False)),
    ("cancellation", lambda o: replace(o, cancelled=False)),
    ("invalid", lambda o: replace(o, calls=1)),
    ("isolation", lambda o: replace(o, second={**o.second, "request_id": o.body["request_id"]})),
    ("stream_cleanup", lambda o: replace(o, cleaned=False)),
    ("offline", lambda o: replace(o, socket_calls=1)),
    ("offline", lambda o: replace(o, secret_seen=True)),
], ids=["constant", "empty-code", "refusal-text", "incomplete-outcome", "upstream", "timeout-cleanup",
        "cancellation", "validation-order", "request-id", "stream-cleanup", "network", "secret"])
def test_test_suite_catches_each_defect(bad_case, corruption, observations):
    async def inject(case):
        actual = observations[case]
        return corruption(actual) if case == bad_case else actual

    with pytest.raises(AssertionError):
        asyncio.run(verify_contract(inject))


def test_real_broken_adapter_fails():
    with pytest.raises(AssertionError):
        asyncio.run(verify_contract(Probe("проверка", "сверка", broken=True)))
