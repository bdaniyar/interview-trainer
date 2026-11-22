"""Evaluate fixed synthetic dev and holdout separately without contacting a provider."""
import argparse
import asyncio
from hashlib import sha256
import json
from pathlib import Path

from contracts import ExtractRequest, PROMPT_DEMO, PROMPT_V1, SCHEMA_VERSION
from metrics import score
from pipeline import extract_trip
from providers import FIXTURES, ScriptedProvider

DATA = Path(__file__).parent / "data" / "cases.jsonl"


async def evaluate():
    cases = [json.loads(row) for row in DATA.read_text(encoding="utf-8").splitlines()]
    provider = ScriptedProvider()
    report = {
        "dataset_sha256": sha256(DATA.read_bytes()).hexdigest(),
        "fixture_sha256": sha256(FIXTURES.read_bytes()).hexdigest(),
        "model": provider.identity,
        "schema_version": SCHEMA_VERSION,
        "versions": {},
    }
    for version in (PROMPT_V1, PROMPT_DEMO):
        outputs = {}
        for case in cases:
            result = await extract_trip(provider, ExtractRequest(text=case["text"]), case["id"],
                                        prompt_version=version)
            outputs[case["id"]] = result.model_dump(mode="json")
        report["versions"][version] = {
            partition: score([case for case in cases if case["partition"] == partition], outputs)
            for partition in ("dev", "holdout")
        }
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write the reproducible JSON report here")
    args = parser.parse_args()
    report = json.dumps(asyncio.run(evaluate()), ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if args.output:
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report, end="")


if __name__ == "__main__":
    main()
