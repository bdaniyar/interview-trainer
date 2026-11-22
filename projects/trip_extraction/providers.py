"""Default offline fixture provider. It does not infer on unseen input."""
import asyncio
from copy import deepcopy
import json
from pathlib import Path

from contracts import FIELDS, PROMPT_DEMO, Prompt, ProviderReply

FIXTURES = Path(__file__).parent / "data" / "provider-fixtures.jsonl"


class ScriptedProvider:
    identity = "scripted-trip-v1"

    def __init__(self, fixture_path: Path = FIXTURES):
        rows = [json.loads(row) for row in fixture_path.read_text(encoding="utf-8").splitlines()]
        self._replies = {row["text"]: (row["kind"], row.get("payload")) for row in rows}
        if len(self._replies) != len(rows):
            raise ValueError("duplicate provider prompt")

    async def extract(self, prompt: Prompt, request_id: str, *, repair: bool) -> ProviderReply:
        await asyncio.sleep(0)
        blank = {"trip": dict.fromkeys(FIELDS)}
        kind, payload = self._replies.get(prompt.text, ("completed", blank))
        if (
            prompt.version == PROMPT_DEMO and kind == "completed" and isinstance(payload, dict)
            and isinstance(payload.get("trip"), dict) and payload["trip"].keys() == set(FIELDS)
        ):
            trip = payload["trip"]
            payload = {"trip": {**trip, "city": trip["city"] if trip["city"] is not None else "Алматы",
                                "guests": trip["guests"] if trip["guests"] is not None else 2}}
        return ProviderReply(kind, deepcopy(payload))
