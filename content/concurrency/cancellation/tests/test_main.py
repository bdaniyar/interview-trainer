import asyncio
from main import cancel_and_wait

async def scenario():
    cleaned = []
    async def work():
        try: await asyncio.sleep(10)
        finally: cleaned.append(True)
    task = asyncio.create_task(work())
    await asyncio.sleep(0)
    assert await cancel_and_wait(task) is True
    assert task.cancelled() and cleaned == [True]
def test_cancel(): asyncio.run(scenario())

import pytest

def test_done_and_failed():
    async def run():
        task = asyncio.create_task(asyncio.sleep(0, result=42))
        await task
        assert await cancel_and_wait(task) is False
        async def broken():
            raise ValueError("original")
        task = asyncio.create_task(broken())
        with pytest.raises(ValueError):
            await task
        with pytest.raises(ValueError, match="original"):
            await cancel_and_wait(task)
    asyncio.run(run())
