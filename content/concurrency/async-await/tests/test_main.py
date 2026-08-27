import asyncio
from main import load_profile

class Client:
    def __init__(self): self.active = self.peak = 0
    async def call(self, value):
        self.active += 1; self.peak = max(self.peak, self.active)
        await asyncio.sleep(0)
        self.active -= 1
        return value
    async def get_user(self, user_id): return await self.call({"id": user_id})
    async def get_roles(self, user_id): return await self.call(["reader"])
def test_concurrent():
    client = Client()
    assert asyncio.run(load_profile(client, 4)) == {"id": 4, "roles": ["reader"]}
    assert client.peak == 2
