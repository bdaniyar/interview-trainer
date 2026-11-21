import asyncio
from contracts import demo


def open_service(make_client, repository, timeout):
    raise NotImplementedError("Задай жизненный цикл async-клиента")


if __name__ == "__main__":
    asyncio.run(demo(open_service))
