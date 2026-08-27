import asyncio

async def fetch_many(fetch, ids):
    return await asyncio.gather(*(fetch(value) for value in ids))
