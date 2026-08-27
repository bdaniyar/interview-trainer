import asyncio
import threading
from main import run_blocking_calls

def test_order_and_thread():
    owner = threading.get_ident()
    def work(value): return value * 2, threading.get_ident() != owner
    result = asyncio.run(run_blocking_calls(work, [3, 1, 2]))
    assert [item[0] for item in result] == [6, 2, 4] and all(item[1] for item in result)
