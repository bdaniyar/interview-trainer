import asyncio
import pytest
from main import AsyncResource

async def scenario(fail=False):
    events = []
    async def open_(): events.append("open"); return 42
    async def close_(value): events.append(("close", value))
    async with AsyncResource(open_, close_) as value:
        assert value == 42
        if fail: raise RuntimeError("boom")
    return events
def test_lifecycle(): assert asyncio.run(scenario()) == ["open", ("close", 42)]
def test_error():
    with pytest.raises(RuntimeError): asyncio.run(scenario(True))
