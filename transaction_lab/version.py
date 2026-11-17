"""Bind the local coordinator to the exact built profile, not a stale image tag."""

from hashlib import sha256
import json
from pathlib import Path


def fingerprint():
    root = Path(__file__).parent
    return sha256(
        b"\0".join(
            name.encode() + b"\0" + (root / name).read_bytes()
            for name in ["bootstrap.py", "execute.py", "policy.py", "fixtures.py"]
        )
    ).hexdigest()


if __name__ == "__main__":
    print(json.dumps({"profile": "pg-transaction-v1", "fingerprint": fingerprint()}))
