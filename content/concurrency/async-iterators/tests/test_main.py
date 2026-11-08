import asyncio
from main import AsyncRange

async def collect(value): return [item async for item in value]
def test_values(): assert asyncio.run(collect(AsyncRange(2, 5))) == [2, 3, 4]
def test_empty(): assert asyncio.run(collect(AsyncRange(3, 3))) == []

def test_exhausted_and_reversed():
    async def run():
        source = AsyncRange(1, 2)
        assert await collect(source) == [1]
        assert await collect(source) == []
        assert await collect(AsyncRange(5, 2)) == []
    asyncio.run(run())
