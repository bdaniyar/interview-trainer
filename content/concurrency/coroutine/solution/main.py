async def fetch_name(client, user_id):
    user = await client.get_user(user_id)
    return user["name"]
