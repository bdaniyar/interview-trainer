import asyncio
from contracts import GenerationResult, WireError, demo


async def generate(client, question) -> GenerationResult:
    try:
        response = await client.responses.create(model="fixture-model", input=question)
    except WireError:
        return GenerationResult("unavailable")
    usage = getattr(response, "usage", None)
    counts = (getattr(usage, "input_tokens", None), getattr(usage, "output_tokens", None))
    reported = counts if None not in counts else None
    if response.status != "completed":
        outcome = "incomplete" if response.status == "incomplete" else "unavailable"
        return GenerationResult(outcome, usage=reported)
    parts = [part for item in response.output if item.type == "message" for part in item.content]
    if any(part.type == "refusal" for part in parts):
        return GenerationResult("refusal", usage=reported)
    text = "".join(part.text for part in parts if part.type == "output_text")
    return GenerationResult("completed", text, reported) if text.strip() else GenerationResult("empty", usage=reported)


if __name__ == "__main__":
    asyncio.run(demo(generate))
