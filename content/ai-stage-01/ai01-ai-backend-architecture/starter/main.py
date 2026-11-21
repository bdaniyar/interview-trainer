import asyncio
from contracts import Generation
from demo import exercise


async def dispatch(provider, question, timeout=0.5) -> Generation:
    raise NotImplementedError("Сохрани общий контракт при разных исходах")


if __name__ == "__main__":
    asyncio.run(exercise(dispatch))
