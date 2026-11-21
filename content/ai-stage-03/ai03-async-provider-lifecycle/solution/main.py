import asyncio
from contextlib import asynccontextmanager

from contracts import Outcome, demo


class Service:
    def __init__(self, client, repository, timeout):
        self.client = client
        self.repository = repository
        self.timeout = timeout

    async def ask(self, actor, question):
        async with self.repository.read(actor) as context:
            snapshot = context
        try:
            async with asyncio.timeout(self.timeout):
                text = await self.client.generate(snapshot, question)
        except TimeoutError:
            return Outcome("timeout")
        return Outcome("completed", text)


@asynccontextmanager
async def open_service(make_client, repository, timeout):
    client = make_client()
    try:
        yield Service(client, repository, timeout)
    finally:
        await client.aclose()


if __name__ == "__main__":
    asyncio.run(demo(open_service))
