import asyncio

async def call_blocking(function, *args, **kwargs):
    return await asyncio.to_thread(function, *args, **kwargs)
