"""Version the index workload contract independently of previous graders."""
from hashlib import sha256
from pathlib import Path
import json

FILES = ("policy.py", "workloads.py", "bootstrap.py", "install.py", "read.py")


def fingerprint():
    root = Path(__file__).parent
    return sha256(b"\0".join(name.encode() + b"\0" + (root / name).read_bytes()
                             for name in FILES)).hexdigest()


if __name__ == "__main__":
    print(json.dumps({"profile": "pg-index-v1", "fingerprint": fingerprint()}))
