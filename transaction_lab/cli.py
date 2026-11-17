"""Local Run/Check and controlled transaction timelines (not a network service)."""

import argparse
import json
from pathlib import Path
from transaction_lab.control import SCENARIOS, attempt, check
from transaction_lab.policy import validate_script
from sql_runner.app.policy import PolicyError
from sql_runner.app.docker_backend import SandboxUnavailable


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for command in ["run", "check"]:
        cmd = sub.add_parser(command)
        cmd.add_argument("--exercise", choices=["dml", "booking"], default="dml")
        cmd.add_argument("--file", type=Path, required=True)
    cmd = sub.add_parser("scenario")
    cmd.add_argument("name", choices=sorted(SCENARIOS))
    args = parser.parse_args()
    try:
        result = execute(args)
    except (PolicyError, SandboxUnavailable, OSError, UnicodeError) as error:
        parser.exit(2, "Transaction Lab: " + str(error) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get("error") or result.get("passed") is False:
        raise SystemExit(1)


def execute(args):
    if args.command == "scenario":
        with attempt() as (backend, handle):
            result = backend.execute(handle, "scenario", {"scenario": args.name})
    else:
        with args.file.open("rb") as stream:
            data = stream.read(32769)
        if len(data) > 32768:
            raise PolicyError("SQL file exceeds 32768 bytes")
        source = data.decode("utf-8")
        validate_script(source)
        if args.command == "check":
            result = check(args.exercise, source)
        else:
            with attempt() as (backend, handle):
                backend.install_case(handle, args.exercise, "public")
                result = backend.execute(
                    handle,
                    "script" if args.exercise == "dml" else "booking",
                    {"sql": source},
                )
    return result


if __name__ == "__main__":
    main()
