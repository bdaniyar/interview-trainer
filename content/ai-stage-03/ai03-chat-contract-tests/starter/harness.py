import asyncio
from dataclasses import dataclass, field
import io
import logging
import socket
from unittest.mock import patch

from httpx import ASGITransport, AsyncClient

from chat_fixture import create_app
from chat_types import Generation, ProviderUnavailable
from stream_fixture import open_feed


CASES = ("success", "empty", "refusal", "incomplete", "unavailable", "timeout",
         "invalid", "cancellation", "isolation", "stream_cleanup", "offline")


@dataclass
class Observation:
    http: int | None = None
    body: dict = field(default_factory=dict)
    second: dict = field(default_factory=dict)
    calls: int = 0
    cancelled: bool = False
    cleaned: bool = False
    socket_calls: int = 0
    secret_seen: bool = False
    deltas: tuple[str, ...] = ()
    expected_text: str = ""
    expected_second: str = ""


class Probe:
    def __init__(self, first="Курс", second="Модуль", broken=False):
        self.first, self.second, self.broken = first, second, broken

    async def __call__(self, case):
        if case not in CASES:
            raise ValueError("unknown scenario")
        if case == "stream_cleanup":
            closed = False

            async def source():
                nonlocal closed
                try:
                    yield self.first
                    raise AssertionError("unexpected pull")
                finally:
                    closed = True

            async with open_feed(source()) as stream:
                delta = await anext(stream)
            return Observation(deltas=(delta,), cleaned=closed, expected_text=self.first)

        entered, ended = asyncio.Event(), asyncio.Event()
        calls = []
        secret = "synthetic-provider-secret"
        outcomes = {
            "empty": Generation("completed", ""),
            "refusal": Generation("refusal", "private refusal"),
            "incomplete": Generation("incomplete", "partial"),
        }
        if self.broken:
            outcomes["refusal"] = Generation("completed", "private refusal")

        class Scripted:
            async def generate(self, value):
                calls.append(value)
                if case in {"unavailable", "offline"}:
                    raise ProviderUnavailable(secret)
                if case in {"timeout", "cancellation"}:
                    entered.set()
                    try:
                        await asyncio.Event().wait()
                    finally:
                        ended.set()
                return outcomes.get(case, Generation("completed", value))

        app = create_app(Scripted(), timeout=0 if case == "timeout" else 0.5)
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            async def request(value):
                return await client.post("/probe/message", json={"text": value})

            if case == "isolation":
                first, second = await asyncio.gather(request(self.first), request(self.second))
                return Observation(first.status_code, first.json(), second.json(), len(calls),
                                   expected_text=self.first, expected_second=self.second)
            if case == "cancellation":
                task = asyncio.create_task(request(self.first))
                await asyncio.wait_for(entered.wait(), 0.3)
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    return Observation(calls=len(calls), cancelled=True, cleaned=ended.is_set())
                return Observation(calls=len(calls), cleaned=ended.is_set())

            if case == "offline":
                sockets = 0

                def reject(*args, **kwargs):
                    nonlocal sockets
                    sockets += 1
                    raise AssertionError("network attempted")
                output = io.StringIO()
                handler = logging.StreamHandler(output)
                logger = logging.getLogger()
                logger.addHandler(handler)
                try:
                    with patch.object(socket.socket, "connect", reject), patch.object(socket, "getaddrinfo", reject):
                        response = await request(self.first)
                finally:
                    logger.removeHandler(handler)
                return Observation(response.status_code, response.json(), calls=len(calls), socket_calls=sockets,
                                   secret_seen=secret in (output.getvalue() + response.text))

            result = await request(" " if case == "invalid" else self.first)
            return Observation(result.status_code, result.json(), calls=len(calls),
                               cleaned=ended.is_set(), expected_text=self.first)


async def demo(verify):
    await verify(Probe())
    try:
        await verify(Probe(broken=True))
    except AssertionError:
        print("Контракт выявил сломанный отказ")
    else:
        raise AssertionError("Сломанный адаптер прошёл проверку")
