import asyncio
from main import fetch_many

async def fetch(value):
    await asyncio.sleep((4 - value) * 0.001)
    return value * 10
def test_order(): assert asyncio.run(fetch_many(fetch, [1, 3, 2])) == [10, 30, 20]
def test_empty(): assert asyncio.run(fetch_many(fetch, [])) == []
