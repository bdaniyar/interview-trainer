class HTTPFailure(Exception):
    def __init__(self, status, retry_after=None):
        self.status = status
        self.retry_after = retry_after
        super().__init__(f"HTTP {status}")


class RetryExhausted(Exception):
    pass


async def demo(retry):
    events = iter([HTTPFailure(429), HTTPFailure(503), "готово"])
    now = 0

    async def send():
        event = next(events)
        if isinstance(event, Exception):
            raise event
        return event

    async def sleep(seconds):
        nonlocal now
        now += seconds

    result = await retry(send, clock=lambda: now, sleep=sleep, rng=lambda: 0.5, max_attempts=3, budget=4)
    assert result == "готово" and now == 1.5
    print(result, now)
