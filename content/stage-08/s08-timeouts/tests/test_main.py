import asyncio
import pytest
from main import await_with_timeout

def test_result(): assert asyncio.run(await_with_timeout(asyncio.sleep(0, result="ok"), 1)) == "ok"
def test_timeout():
    with pytest.raises(TimeoutError): asyncio.run(await_with_timeout(asyncio.sleep(0.05), 0.001))

def test_cleanup_and_unrelated_error():
    async def run():
        closed = []
        async def pending():
            try:
                await asyncio.Event().wait()
            finally:
                closed.append(True)
        with pytest.raises(TimeoutError):
            await await_with_timeout(pending(), 0)
        assert closed == [True]
        async def broken():
            raise ValueError("original")
        with pytest.raises(ValueError, match="original"):
            await await_with_timeout(broken(), 1)
    asyncio.run(run())
