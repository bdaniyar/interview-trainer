import asyncio
from main import AsyncRange

async def collect(value): return [item async for item in value]
def test_values(): assert asyncio.run(collect(AsyncRange(2, 5))) == [2, 3, 4]
def test_empty(): assert asyncio.run(collect(AsyncRange(3, 3))) == []
