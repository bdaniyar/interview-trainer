"""Optional two-request SDK demo for a single frozen synthetic booking case."""
import argparse
import asyncio
import json
import os
import sys
from decimal import Decimal
from pathlib import Path

from bookings import BookingRepository, Tools
from contracts import Principal


def parse():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--send-one-case", action="store_true")
    parser.add_argument("--model", required=True, help="An explicit Responses-compatible model version.")
    parser.add_argument("--case", choices=("list", "lookup"), default="lookup")
    parser.add_argument("--context-tokens", type=int, required=True)
    parser.add_argument("--input-usd-per-million", type=Decimal, required=True)
    parser.add_argument("--output-usd-per-million", type=Decimal, required=True)
    parser.add_argument("--max-usd", type=Decimal, required=True)
    args = parser.parse_args()
    if not args.send_one_case:
        parser.error("explicit --send-one-case is required")
    rates = (args.input_usd_per_million, args.output_usd_per_million, args.max_usd)
    if args.context_tokens <= 0 or any(not rate.is_finite() or rate <= 0 for rate in rates):
        parser.error("use positive context and verified prices")
    ceiling = 2 * (args.context_tokens * rates[0] + 256 * rates[1]) / 1_000_000
    if ceiling > args.max_usd:
        parser.error(f"estimated upper bound {ceiling} USD exceeds budget")
    if not os.environ.get("OPENAI_API_KEY"):
        parser.error("OPENAI_API_KEY is required")
    return args


async def run(args):
    from openai import APIError, AsyncOpenAI

    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools" / "ai_sdk_verify"))
    from tools_roundtrip import ToolProtocolError, roundtrip

    prompts = {
        "list": "Use list_my_bookings for this synthetic demo and summarize the result.",
        "lookup": "Use get_booking to read synthetic booking 42 and summarize the result.",
    }
    tools = Tools(BookingRepository())
    principal = Principal("north", "alice", frozenset({"booking:read"}))
    count = 0

    async def execute(call):
        nonlocal count
        count += 1
        payload = json.dumps(call.arguments, allow_nan=False)
        result = await tools.execute(principal, f"call-{count}", call.name, payload)
        return result.observation()

    try:
        async with asyncio.timeout(12), AsyncOpenAI(
            base_url="https://api.openai.com/v1", timeout=5, max_retries=0,
        ) as client:
            response = await roundtrip(client, args.model, prompts[args.case], execute)
    except TimeoutError:
        return {"mode": "live", "case": args.case, "status": "deadline"}
    except APIError:
        return {"mode": "live", "case": args.case, "status": "provider_error"}
    except (ToolProtocolError, ValueError):
        return {"mode": "live", "case": args.case, "status": "protocol_error"}
    return {"mode": "live", "case": args.case, "status": response.status,
            "tool_calls": count, "final_has_text": bool(response.output_text)}


if __name__ == "__main__":
    print(json.dumps(asyncio.run(run(parse())), ensure_ascii=False))
