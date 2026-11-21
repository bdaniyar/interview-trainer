from dataclasses import dataclass


@dataclass(frozen=True)
class WireEvent:
    kind: str
    text: str | None = None
    usage: int | None = None


@dataclass(frozen=True)
class AppEvent:
    kind: str
    text: str | None = None
    usage: int | None = None


class StreamFailed(Exception):
    pass


async def demo(normalize):
    async def source():
        yield WireEvent("text_delta", "утро")
        yield WireEvent("done", usage=3)

    events = [event async for event in normalize(source())]
    assert events == [AppEvent("delta", "утро"), AppEvent("completed", usage=3)]
    print(events)
