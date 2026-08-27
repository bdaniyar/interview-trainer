import asyncio

async def cancel_and_wait(task):
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        return True
    return False
