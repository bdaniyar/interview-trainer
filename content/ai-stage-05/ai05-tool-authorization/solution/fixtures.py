import asyncio

from contracts import Policy, Principal


class Store:
    def __init__(self, policies=None, rows=None):
        self.policies = policies if policies is not None else {42: Policy("training", "ada")}
        self.rows = rows if rows is not None else {42: {"city": "Бишкек", "private_note": "synthetic secret"}}
        self.policy_ids = []
        self.protected_reads = []
        self.writes = []

    async def policy(self, booking_id):
        self.policy_ids.append(booking_id)
        return self.policies.get(booking_id)

    async def read(self, booking_id):
        self.protected_reads.append(booking_id)
        return self.rows.get(booking_id)


def demo(get_my_booking):
    async def run():
        store = Store()
        for user in ("ada", "sam"):
            actor = Principal("training", user, frozenset({"booking:read"}))
            print(await get_my_booking({"booking_id": 42}, actor, store))
        print("protected reads:", store.protected_reads)

    asyncio.run(run())
