import asyncio
from main import start_job

async def scenario():
    registry = set()
    task = start_job(asyncio.sleep(0, result=42), registry)
    assert task in registry and await task == 42
    await asyncio.sleep(0)
    assert task not in registry
def test_lifecycle(): asyncio.run(scenario())
