"""Author-side OpenAI Responses example for Structured Outputs."""
from openai import AsyncOpenAI
from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr


class WireTrip(BaseModel):
    model_config = ConfigDict(extra="forbid")
    city: StrictStr | None
    check_in: StrictStr | None
    check_out: StrictStr | None
    guests: StrictInt | None


class WireExtraction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    trip: WireTrip


async def parse_trip(client: AsyncOpenAI, model: str, text: str):
    return await client.responses.parse(
        model=model,
        instructions="Extract stated trip fields. Leave unknown values null. Use complete ISO dates.",
        input=[{"role": "user", "content": [{"type": "input_text", "text": text}]}],
        text_format=WireExtraction,
        max_output_tokens=384,
        store=False,
    )
