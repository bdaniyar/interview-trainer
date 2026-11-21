import asyncio
from contracts import Generation, ProviderUnavailable
from demo import exercise


async def dispatch(provider, question, timeout=0.5) -> Generation:
    try:
        async with asyncio.timeout(timeout):
            result = await provider.generate(question)
    except TimeoutError:
        return Generation("timeout", None, None)
    except ProviderUnavailable:
        return Generation("unavailable", None, None)
    if result.status == "completed" and result.text and result.text.strip():
        return result
    if result.status in {"completed", "incomplete"}:
        return Generation("incomplete", None, result.usage)
    return Generation(result.status, None, result.usage)


if __name__ == "__main__":
    asyncio.run(exercise(dispatch))
