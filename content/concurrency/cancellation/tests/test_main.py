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
