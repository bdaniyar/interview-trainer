import asyncio
import threading
from main import call_blocking

def test_arguments_and_thread():
    owner = threading.get_ident()
    def work(a, *, b): return a + b, threading.get_ident() != owner
    assert asyncio.run(call_blocking(work, 2, b=3)) == (5, True)

import pytest

def test_no_args_and_error():
    assert asyncio.run(call_blocking(lambda: "ok")) == "ok"
    def broken():
        raise ValueError("original")
    with pytest.raises(ValueError, match="original"):
        asyncio.run(call_blocking(broken))
