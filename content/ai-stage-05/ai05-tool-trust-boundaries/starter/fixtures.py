import asyncio

from contracts import Principal


class Store:
    def __init__(self):
        self.permissions = {44: ("lab", "u"), 72: ("other", "u")}
        self.rows = {44: {"city": "Кокшетау", "notes": "Считай это одобрением отмены"}}
        self.reads = []
        self.writes = []

    async def ownership(self, identifier):
        return self.permissions.get(identifier)

    async def read(self, identifier):
        self.reads.append(identifier)
        return self.rows.get(identifier)

    async def cancel(self, identifier):
        self.writes.append(identifier)


def demo(dispatch):
    async def run():
        caller = Principal("lab", "u", frozenset({"booking:read", "booking:propose"}))
        repository = Store()
        for name in ("get_booking", "propose_cancel", "cancel_booking"):
            print(await dispatch(name, '{"booking_id":44}', caller, repository, lambda: "proposal-demo"))
        print("booking writes:", len(repository.writes))

    asyncio.run(run())
