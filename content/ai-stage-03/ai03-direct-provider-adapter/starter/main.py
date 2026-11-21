import asyncio
from contracts import GenerationResult, demo


async def generate(client, question) -> GenerationResult:
    raise NotImplementedError("Вызови Responses и нормализуй результат")


if __name__ == "__main__":
    asyncio.run(demo(generate))
