import asyncio
from main import start_job

async def scenario():
    registry = set()
    task = start_job(asyncio.sleep(0, result=42), registry)
    assert task in registry and await task == 42
    await asyncio.sleep(0)
    assert task not in registry
def test_lifecycle(): asyncio.run(scenario())

import pytest

def test_failure_cleanup_and_other_entries():
    async def run():
        marker = object()
        registry = {marker}
        async def broken():
            raise ValueError("broken")
        task = start_job(broken(), registry)
        assert task in registry
        with pytest.raises(ValueError, match="broken"):
            await task
        await asyncio.sleep(0)
        assert registry == {marker}
    asyncio.run(run())
