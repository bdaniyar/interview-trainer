import asyncio

import pytest

from contracts import Generation, ProviderUnavailable
from main import dispatch


@pytest.mark.parametrize(("result", "expected"), [
    (Generation("completed", "карта", 14), Generation("completed", "карта", 14)),
    (Generation("completed", " ", 0), Generation("incomplete", None, 0)),
    (Generation("completed", None, None), Generation("incomplete", None, None)),
    (Generation("incomplete", "обрезано", 12), Generation("incomplete", None, 12)),
    (Generation("unavailable", "provider-detail", None), Generation("unavailable", None, None)),
])
def test_typed_outcomes(result, expected):
    class Substitute:
        async def generate(self, question):
            assert question == "маршрут"
            return result

    assert asyncio.run(dispatch(Substitute(), "маршрут")) == expected


def test_transport_failure():
    class Offline:
        async def generate(self, question):
            raise ProviderUnavailable("private transport diagnostic")

    assert asyncio.run(dispatch(Offline(), "поиск")) == Generation("unavailable", None, None)


def test_timeout_with_cleanup():
    cleaned = []

    class Blocked:
        async def generate(self, question):
            try:
                await asyncio.Event().wait()
            finally:
                cleaned.append(question)

    assert asyncio.run(dispatch(Blocked(), "?", timeout=0)) == Generation("timeout", None, None)
    assert cleaned == ["?"]


def test_concurrent_adapter_replacement():
    class Echo:
        async def generate(self, question):
            await asyncio.sleep(0)
            return Generation("completed", question[::-1], len(question))

    async def scenario():
        provider = Echo()
        return await asyncio.gather(dispatch(provider, "абв"), dispatch(provider, "аб"))
    assert asyncio.run(scenario()) == [Generation("completed", "вба", 3), Generation("completed", "ба", 2)]


def test_unexpected_error_is_not_unavailable():
    class Broken:
        async def generate(self, question):
            raise ValueError("bad fixtures")

    with pytest.raises(ValueError):
        asyncio.run(dispatch(Broken(), "проверка"))
