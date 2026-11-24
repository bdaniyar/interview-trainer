"""Measure natural and diagnostic plans on the same eligible PG17 rows."""
import json
import platform
import random
import statistics
import time

from .contracts import ChunkInput, Space, vector_param
from .fixtures import OWNER, READER, SOUTH, unit
from .store import ANN, EXACT


SEED, DIMENSION, CORPUS_PER_DOC, K, N = 1305, 16, 768, 8, 18


def seed_benchmark(store, maintenance, rng):
    for i, actor in enumerate((OWNER, OWNER, OWNER, READER, SOUTH)):
        inputs = []
        lines = []
        offset = 0
        for index in range(CORPUS_PER_DOC):
            text = f"fixture benchmark {i:02d}/{index:04d}\n"
            vector = unit(tuple(rng.uniform(-1, 1) for _ in range(DIMENSION)))
            inputs.append(ChunkInput(f"{index:04d}", "Benchmark", offset, text, vector))
            lines.append(text)
            offset += len(text)
        store.ingest(actor, f"bench-{i}", 1, "".join(lines), Space(), tuple(inputs), expected_count=len(inputs))
    # Reproducible statistics on the disposable benchmark database.
    with maintenance.connect() as db:
        db.execute("ANALYZE chunks_v1")
        db.execute("ANALYZE documents")


def keys(rows):
    return {(row[0], row[1], row[3]) for row in rows}


def index_uses(plan):
    names = []
    if "Index Name" in plan:
        names.append(plan["Index Name"])
    for child in plan.get("Plans", ()):
        names.extend(index_uses(child))
    return names


def benchmark(store, maintenance):
    rng = random.Random(SEED)
    seed_benchmark(store, maintenance, rng)
    queries = [unit(tuple(rng.uniform(-1, 1) for _ in range(DIMENSION))) for _ in range(N)]
    settings = [("exact", None, False)]
    settings += [(f"natural-{ef}", ef, False) for ef in (16, 48, 128)]
    settings += [(f"forced-{ef}", ef, True) for ef in (16, 48, 128)]
    report = {"seed": SEED, "query_count": N, "dimensions": DIMENSION, "k": K,
              "corpus": CORPUS_PER_DOC * 5, "eligible": CORPUS_PER_DOC * 3,
              "filters": "north/alice, allowed active version, fixture-v1",
              "host": platform.platform(), "architecture": platform.machine(),
              "method": "Warm PostgreSQL buffers after two unmeasured queries per setting. No cold-cache claim.",
              "hnsw_build": {"m": 16, "ef_construction": 64}, "settings": {}}
    exact_ids = []
    with store.connect() as db:
        report["postgres"] = db.execute("SHOW server_version").fetchone()[0]
        report["pgvector"] = db.execute("SELECT extversion FROM pg_extension WHERE extname='vector'").fetchone()[0]
        report["hnsw_bytes"] = db.execute("SELECT pg_relation_size('chunks_v1_hnsw')").fetchone()[0]
        report["chunk_partition_bytes"] = db.execute("SELECT pg_relation_size('chunks_v1')").fetchone()[0]
        report["shared_buffers"] = db.execute("SHOW shared_buffers").fetchone()[0]
        for name, ef, force in settings:
            query = ANN if ef is not None else EXACT
            db.execute("SELECT set_config('enable_seqscan', %s, true)", ("off" if force else "on",))
            if ef is not None:
                db.execute("SELECT set_config('hnsw.ef_search', %s, true)", (str(ef),))
            params = [
                dict(tenant=OWNER.tenant, subject=OWNER.subject, space=Space().id, limit=K,
                     vector=vector_param(vector, Space()))
                for vector in queries
            ]
            for value in params[:2]:
                db.execute(query, value).fetchall()
            times, recalls, counts = [], [], []
            for index, value in enumerate(params):
                started = time.perf_counter()
                rows = db.execute(query, value).fetchall()
                times.append((time.perf_counter() - started) * 1000)
                ids = keys(rows)
                if ef is None:
                    exact_ids.append(ids)
                counts.append(len(ids))
                recalls.append(len(exact_ids[index] & ids) / len(exact_ids[index]))
            plan = db.execute("EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) " + query, params[0]).fetchone()[0][0]
            indexes = index_uses(plan["Plan"])
            if ef is None and any("hnsw" in name for name in indexes):
                raise RuntimeError("the exact oracle unexpectedly used HNSW")
            report["settings"][name] = {
                "ef_search": ef, "disable_seqscan_diagnostic": force,
                "recall_at_k": statistics.mean(recalls), "minimum_returned": min(counts),
                "latency_ms": {"p50": statistics.median(times), "p95": statistics.quantiles(times, n=20, method="inclusive")[18]},
                "indexes": indexes, "explain_analyze": plan,
            }
    return report
