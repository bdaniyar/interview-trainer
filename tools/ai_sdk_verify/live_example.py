"""Explicit opt-in developer CLI. Offline verification uses MockTransport."""
import argparse
import asyncio
import os

from openai import APIError, AsyncOpenAI

from example import get_response


async def main(model):
    try:
        async with AsyncOpenAI(max_retries=0, timeout=10) as client:
            response = await get_response(client, model, "Explain what a Python tuple is in one sentence.")
    except APIError as exc:
        raise SystemExit(f"Provider call failed: {type(exc).__name__}") from None
    print(f"Status: {response.status}")
    if response.status == "completed" and response.output_text:
        print(response.output_text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send one explicitly authorized live Responses API request")
    parser.add_argument("--live", action="store_true", help="Enable one potentially billed API call")
    args = parser.parse_args()
    model = os.environ.get("OPENAI_MODEL")
    if not args.live or not model or not os.environ.get("OPENAI_API_KEY"):
        parser.error("requires --live, OPENAI_MODEL and OPENAI_API_KEY")
    asyncio.run(main(model))
