import asyncio
from harness import demo


async def verify_contract(probe):
    raise NotImplementedError("Проверь наблюдения всех сценариев")


if __name__ == "__main__":
    asyncio.run(demo(verify_contract))
