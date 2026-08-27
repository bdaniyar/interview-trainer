import asyncio

async def await_with_timeout(awaitable, seconds):
    async with asyncio.timeout(seconds):
        return await awaitable
