import asyncio

async def checkpoint(log):
    log.append("before")
    await asyncio.sleep(0)
    log.append("after")
