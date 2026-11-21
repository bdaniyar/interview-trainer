import asyncio
from contracts import demo


async def call_with_retry(send, *, clock, sleep, rng, max_attempts, budget, base=1, cap=8, now_utc=None):
    raise NotImplementedError("Ограничь попытки, задержку и общее ожидание")


if __name__ == "__main__":
    asyncio.run(demo(call_with_retry))
