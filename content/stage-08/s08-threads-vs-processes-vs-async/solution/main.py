import asyncio

async def map_limited(function, values, limit):
    if limit <= 0:
        raise ValueError("limit must be positive")
    semaphore = asyncio.Semaphore(limit)
    async def run(value):
        async with semaphore:
            return await function(value)
    return await asyncio.gather(*(run(value) for value in values))
