from contextlib import asynccontextmanager
from dataclasses import dataclass


@dataclass(frozen=True)
class Outcome:
    status: str
    text: str | None = None


async def demo(open_service):
    class Repo:
        @asynccontextmanager
        async def read(self, actor):
            yield f"Правила {actor}"

    class Client:
        async def generate(self, context, question):
            return f"{context}:{question}"

        async def aclose(self):
            pass

    async with open_service(Client, Repo(), 1) as service:
        result = await service.ask("a", "дедлайн")
        assert result == Outcome("completed", "Правила a:дедлайн")
        assert (await service.ask("b", "дата")).text == "Правила b:дата"
        print(result)
