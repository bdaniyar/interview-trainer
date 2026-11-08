import asyncio
import pytest
from main import load_profile

class Client:
    def __init__(self, roles):
        self.user = {"id": 4, "name": "Aida", "roles": ["old"]}
        self.roles = roles
        self.calls = []
    async def get_user(self, user_id):
        self.calls.append(("user", user_id))
        return self.user
    async def get_roles(self, user_id):
        self.calls.append(("roles", user_id))
        return self.roles

@pytest.mark.parametrize("roles", [[], ["reader"]])
def test_profile(roles):
    client = Client(roles)
    assert asyncio.run(load_profile(client, 4)) == {"id": 4, "name": "Aida", "roles": roles}
    assert client.user["roles"] == ["old"]
    assert sorted(client.calls) == [("roles", 4), ("user", 4)]

def test_failure():
    class Broken(Client):
        async def get_roles(self, user_id):
            raise LookupError("no roles")
    with pytest.raises(LookupError, match="no roles"):
        asyncio.run(load_profile(Broken([]), 4))
