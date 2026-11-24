import asyncio

from contracts import Principal, Provider, Repository, Result
from fixtures import DemoProvider, DemoRepository


async def run_assistant(prompt: str, principal: Principal, provider: Provider,
                        repository: Repository) -> Result:
    """Выполните начальный шаг и при необходимости единственное продолжение."""
    return Result("incomplete")


async def main():
    result = await run_assistant("Покажи мою бронь", Principal("north", "alice"),
                                 DemoProvider(), DemoRepository())
    print(result.reason, result.text)


if __name__ == "__main__":
    asyncio.run(main())
