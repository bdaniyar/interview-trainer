"""Verified Responses API calls. The caller owns the configured async client."""
from openai import AsyncOpenAI


async def get_response(client: AsyncOpenAI, model: str, question: str):
    return await client.responses.create(
        model=model,
        instructions="Explain the catalog entry briefly.",
        input=[{"role": "user", "content": [{"type": "input_text", "text": question}]}],
        store=False,
    )


async def open_stream(client: AsyncOpenAI, model: str, question: str):
    return await client.responses.create(model=model, input=question, store=False, stream=True)
