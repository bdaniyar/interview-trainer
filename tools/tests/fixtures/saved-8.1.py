import asyncio

async def run_blocking_calls(function, values):
    return await asyncio.gather(*(asyncio.to_thread(function, value) for value in values))
