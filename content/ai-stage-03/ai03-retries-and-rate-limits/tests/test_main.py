import asyncio
from datetime import datetime, timezone

import pytest

from contracts import HTTPFailure, RetryExhausted
from main import call_with_retry


class Simulation:
    def __init__(self, outcomes):
        self.outcomes = iter(outcomes)
        self.now = 0
        self.delays = []
        self.calls = 0

    async def send(self):
        self.calls += 1
        outcome = next(self.outcomes)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome

    async def sleep(self, delay):
        self.delays.append(delay)
        self.now += delay

    def run(self, **options):
        kwargs = {"clock": lambda: self.now, "sleep": self.sleep, "rng": lambda: 0.25,
                  "max_attempts": 3, "budget": 12, **options}
        return asyncio.run(call_with_retry(self.send, **kwargs))


def test_retryable_sequence_and_fallback_header():
    scenario = Simulation([HTTPFailure(429, "garbage"), HTTPFailure(503, " 2 "), "ok"])
    assert scenario.run() == "ok"
    assert scenario.calls == 3
    assert scenario.delays == [0.25, 2]


def test_retry_date_utc():
    scenario = Simulation([HTTPFailure(429, "Wed, 21 Oct 2015 07:28:00 GMT"), 23])
    assert scenario.run(now_utc=lambda: datetime(2015, 10, 21, 7, 27, 57, tzinfo=timezone.utc)) == 23
    assert scenario.delays == [3]


@pytest.mark.parametrize("failure", [HTTPFailure(401, "1"), TimeoutError("unknown"), asyncio.CancelledError()])
def test_no_retry_for_unknown_permanent_or_cancel(failure):
    scenario = Simulation([failure])
    with pytest.raises(type(failure)):
        scenario.run()
    assert scenario.calls == 1 and scenario.delays == []


def test_retry_after_does_not_fit_deadline():
    error = HTTPFailure(429, "4")
    scenario = Simulation([error])
    with pytest.raises(RetryExhausted) as result:
        scenario.run(budget=4)
    assert result.value.__cause__ is error and scenario.calls == 1 and scenario.delays == []


def test_preserve_exhausted_cause_and_cap():
    reason = HTTPFailure(503)
    scenario = Simulation([HTTPFailure(429), HTTPFailure(503), reason])
    with pytest.raises(RetryExhausted) as result:
        scenario.run(base=4, cap=1)
    assert result.value.__cause__ is reason
    assert scenario.calls == 3 and scenario.delays == [0.25, 0.25]


def test_deadline_includes_transport_latency():
    scenario = Simulation([])
    async def late():
        scenario.now += 5
        return "too late"
    with pytest.raises(RetryExhausted):
        asyncio.run(call_with_retry(late, clock=lambda: scenario.now, sleep=scenario.sleep,
                                    rng=lambda: 0.5, max_attempts=2, budget=4))
    assert scenario.delays == []


def test_zero_budget_has_zero_calls():
    scenario = Simulation([])
    with pytest.raises(RetryExhausted):
        scenario.run(budget=0)
    assert not scenario.calls
