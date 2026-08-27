import asyncio
import threading
from main import call_blocking

def test_arguments_and_thread():
    owner = threading.get_ident()
    def work(a, *, b): return a + b, threading.get_ident() != owner
    assert asyncio.run(call_blocking(work, 2, b=3)) == (5, True)
