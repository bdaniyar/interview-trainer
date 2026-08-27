import asyncio
import pytest
from main import await_with_timeout

def test_result(): assert asyncio.run(await_with_timeout(asyncio.sleep(0, result="ok"), 1)) == "ok"
def test_timeout():
    with pytest.raises(TimeoutError): asyncio.run(await_with_timeout(asyncio.sleep(0.05), 0.001))
