import asyncio
from email.utils import parsedate_to_datetime
from math import isfinite
import re

from contracts import HTTPFailure, RetryExhausted, demo


def server_delay(header, now_utc):
    if not isinstance(header, str):
        return 0
    value = header.strip()
    if re.fullmatch(r"[0-9]+", value):
        try:
            return int(value)
        except ValueError:
            return 0
    if now_utc is None:
        return 0
    try:
        retry_at = parsedate_to_datetime(value)
        return max(0, (retry_at - now_utc()).total_seconds())
    except (TypeError, ValueError, OverflowError):
        return 0


async def call_with_retry(send, *, clock, sleep, rng, max_attempts, budget, base=1, cap=8, now_utc=None):
    if type(max_attempts) is not int or max_attempts <= 0 or not all(
        isinstance(value, (int, float)) and isfinite(value) and value >= 0 for value in (budget, base, cap)
    ):
        raise ValueError("Некорректные пределы")
    deadline = clock() + budget
    limit = min(base, cap)
    last_failure = None
    for attempt in range(max_attempts):
        remaining = deadline - clock()
        if remaining <= 0:
            break
        timer = asyncio.timeout(remaining)
        try:
            async with timer:
                result = await send()
        except TimeoutError:
            if not timer.expired():
                raise
            break
        except HTTPFailure as exc:
            if exc.status not in {429, 503}:
                raise
            last_failure = exc
            if attempt + 1 >= max_attempts:
                break
            delay = max(limit * rng(), server_delay(exc.retry_after, now_utc))
            if delay >= deadline - clock():
                break
            wait_timer = asyncio.timeout(deadline - clock())
            try:
                async with wait_timer:
                    await sleep(delay)
            except TimeoutError:
                if not wait_timer.expired():
                    raise
                break
            limit = min(cap, 2 * limit)
        else:
            if clock() < deadline:
                return result
            break
    raise RetryExhausted("Бюджет попыток исчерпан") from last_failure


if __name__ == "__main__":
    asyncio.run(demo(call_with_retry))
