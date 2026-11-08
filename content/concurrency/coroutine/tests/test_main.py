import asyncio
import inspect
from main import fetch_name

class Client:
    async def get_user(self, user_id): return {"id": user_id, "name": "Aida"}
def test_coroutine():
    assert inspect.iscoroutinefunction(fetch_name)
    assert asyncio.run(fetch_name(Client(), 7)) == "Aida"

import pytest

def test_id_empty_name_and_error():
    class Empty:
        async def get_user(self, user_id):
            assert user_id == 0
            return {"name": ""}
    assert asyncio.run(fetch_name(Empty(), 0)) == ""
    class Broken:
        async def get_user(self, user_id):
            raise LookupError("missing")
    with pytest.raises(LookupError, match="missing"):
        asyncio.run(fetch_name(Broken(), 5))
