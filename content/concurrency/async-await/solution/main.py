async def load_profile(client, user_id):
    user = await client.get_user(user_id)
    roles = await client.get_roles(user_id)
    return {**user, "roles": roles}
