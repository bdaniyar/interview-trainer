"""A resource boundary that belongs to the synthetic testing fixture."""
from contextlib import aclosing, asynccontextmanager


@asynccontextmanager
async def open_feed(source):
    async with aclosing(source):
        yield source
