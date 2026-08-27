import asyncio
import inspect
from main import fetch_name

class Client:
    async def get_user(self, user_id): return {"id": user_id, "name": "Aida"}
def test_coroutine():
    assert inspect.iscoroutinefunction(fetch_name)
    assert asyncio.run(fetch_name(Client(), 7)) == "Aida"
