import asyncio

async def load_profile(client, user_id):
    user, roles = await asyncio.gather(client.get_user(user_id), client.get_roles(user_id))
    return {**user, "roles": roles}
