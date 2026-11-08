import asyncio
from main import checkpoint

async def scenario():
    log = []
    task = asyncio.create_task(checkpoint(log))
    await asyncio.sleep(0)
    assert log == ["before"]
    await task
    return log
def test_checkpoint(): assert asyncio.run(scenario()) == ["before", "after"]

def test_existing_log():
    log = ["existing"]
    assert asyncio.run(checkpoint(log)) is None
    assert log == ["existing", "before", "after"]
