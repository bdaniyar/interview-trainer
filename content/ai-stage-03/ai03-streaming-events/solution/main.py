import asyncio
from contracts import AppEvent, StreamFailed, demo


async def normalize_events(source):
    terminal = AppEvent("incomplete")
    try:
        async for event in source:
            if event.kind == "text_delta":
                if event.text:
                    yield AppEvent("delta", event.text)
            elif event.kind == "done":
                terminal = AppEvent("completed", usage=event.usage)
                break
            elif event.kind == "incomplete":
                terminal = AppEvent("incomplete", usage=event.usage)
                break
            elif event.kind == "failure":
                terminal = AppEvent("failed")
                break
    except StreamFailed:
        terminal = AppEvent("failed")
    finally:
        await source.aclose()
    yield terminal


if __name__ == "__main__":
    asyncio.run(demo(normalize_events))
