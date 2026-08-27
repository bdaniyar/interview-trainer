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
