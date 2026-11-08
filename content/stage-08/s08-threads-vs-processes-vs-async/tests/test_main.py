import asyncio
import pytest
from main import map_limited

async def scenario():
    active = peak = 0
    async def work(value):
        nonlocal active, peak
        active += 1; peak = max(peak, active)
        await asyncio.sleep(0)
        active -= 1
        return value * 2
    return await map_limited(work, [3, 1, 2, 4], 2), peak
def test_limit_order(): assert asyncio.run(scenario()) == ([6, 2, 4, 8], 2)
def test_invalid():
    async def noop(value): return value
    with pytest.raises(ValueError): asyncio.run(map_limited(noop, [1], 0))

def test_empty_negative_and_error():
    async def run():
        async def work(value):
            return value
        assert await map_limited(work, [], 1) == []
        for limit in (0, -1):
            with pytest.raises(ValueError):
                await map_limited(work, [], limit)
        async def broken(value):
            raise ValueError("original")
        with pytest.raises(ValueError, match="original"):
            await map_limited(broken, [1], 1)
    asyncio.run(run())
