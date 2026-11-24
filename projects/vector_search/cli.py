import argparse
import json
import os
from dataclasses import asdict
from pathlib import Path

from .benchmark import benchmark
from .fixtures import OWNER, axis, seed
from .store import Store


LOCAL_DSN = "postgresql://vector_app:local_vector_app@127.0.0.1:15437/vector_lab"


def main():
    parser = argparse.ArgumentParser(description="Disposable pgvector teaching project")
    parser.add_argument("command", choices=("seed", "exact", "ann", "benchmark"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    store = Store(os.environ.get("VECTOR_DSN", LOCAL_DSN))
    if args.command == "seed":
        result = {"documents": len(seed(store))}
    elif args.command == "benchmark":
        admin_dsn = os.environ.get("VECTOR_BENCH_ADMIN_DSN")
        if not admin_dsn:
            parser.error("set VECTOR_BENCH_ADMIN_DSN for ANALYZE on a fresh disposable benchmark database")
        result = benchmark(store, Store(admin_dsn))
    else:
        result = [asdict(hit) for hit in store.dense(OWNER, axis(), limit=args.limit, approximate=args.command == "ann")]
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload)
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
