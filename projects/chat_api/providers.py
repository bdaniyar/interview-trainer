import asyncio

from contracts import Generation, ProviderEvent, Usage


class ScriptedProvider:
    """Local default. Each call constructs its own text and event sequence."""

    async def generate(self, question: str) -> Generation:
        await asyncio.sleep(0)
        return Generation("completed", f"Учебный ответ на вопрос «{question}».",
                          Usage(input_tokens=8, output_tokens=12, cached_tokens=2))

    async def stream(self, question: str):
        yield ProviderEvent("delta", "Учебный ответ: ")
        await asyncio.sleep(0)
        yield ProviderEvent("delta", question)
        yield ProviderEvent("completed", usage=Usage(input_tokens=8, output_tokens=12, cached_tokens=2))

    async def aclose(self):
        pass
