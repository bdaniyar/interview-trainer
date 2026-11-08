import asyncio
from main import fetch_many

async def fetch(value):
    await asyncio.sleep((4 - value) * 0.001)
    return value * 10
def test_order(): assert asyncio.run(fetch_many(fetch, [1, 3, 2])) == [10, 30, 20]
def test_empty(): assert asyncio.run(fetch_many(fetch, [])) == []

import pytest

def test_overlap_duplicates_and_failure():
    async def run():
        entered = []
        all_started = asyncio.Event()
        async def work(value):
            entered.append(value)
            if len(entered) == 3:
                all_started.set()
            await all_started.wait()
            return value * 2
        assert await asyncio.wait_for(fetch_many(work, [2, 2, 1]), 1) == [4, 4, 2]
        async def broken(value):
            raise ValueError("broken")
        with pytest.raises(ValueError, match="broken"):
            await fetch_many(broken, [1])
    asyncio.run(run())
