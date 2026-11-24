"""Frozen retrieval/answer evaluation. Run dev before opening holdout results."""
import argparse
import json
import os
import statistics
import time
from collections import Counter
from hashlib import sha256
from pathlib import Path

from .citations import verdict
from .corpus_data import ACTORS, DATA, HERE, SPACE, cases, catalog, seed
from .metrics import mean_defined, rank_score
from .pipeline import Claim, Draft, context_for
from .retrieval import RetrievalStore, retrieve
from .scripted import embed, generate, lexical_query, rerank_script


LOCAL_DSN = "postgresql://vector_app:local_vector_app@127.0.0.1:15438/vector_lab"
METHODS = ("fts", "dense", "hybrid", "rerank")
K, WINDOW = 6, 4
EXPECTED_FILES = ("catalog.json", "questions.jsonl")


def freeze_fingerprint():
    digest = sha256()
    files = [DATA / name for name in EXPECTED_FILES] + sorted((HERE / "corpus").glob("*.md"))
    for file in files:
        digest.update(str(file.relative_to(HERE)).encode() + b"\0" + file.read_bytes() + b"\0")
    return digest.hexdigest()


def access_oracle(actor, rows):
    latest = {}
    for row in rows:
        key = row["tenant"], row["id"]
        if key not in latest or latest[key]["version"] < row["version"]:
            latest[key] = row
    active, allowed = set(), set()
    for (tenant, doc), row in latest.items():
        if row["deleted"] or tenant != actor.tenant:
            continue
        key = (doc, row["version"])
        active.add(key)
        if actor.subject == row["owner"] or actor.subject in set(row["grants"]) - set(row["revoke"]):
            allowed.add(key)
    return active, allowed


def metrics_for(rows):
    return {method: {m: mean_defined(row["retrieval"][method]["metrics"][m] for row in rows)
                     for m in ("recall", "precision", "mrr")} for method in METHODS}


def answer_metrics(rows):
    result = {}
    for key in ("answer_correct", "citation_valid", "claim_supported", "correct_abstention", "correct_conflict",
                "rejects_unsupported_control"):
        result[key] = mean_defined(row["answer"][key] for row in rows)
    result["error_buckets"] = dict(sorted(Counter(row["answer"]["bucket"] for row in rows).items()))
    return result


def validate_corpus(records, questions):
    counts = Counter((c["lang"], c["split"]) for c in questions)
    expected = {(lang, split): n for lang in ("ru", "kk", "en") for split, n in (("dev", 6), ("holdout", 4))}
    if counts != expected or len({c["id"] for c in questions}) != 30:
        raise ValueError("invalid frozen split")
    groups = {}
    for case in questions:
        prior = groups.setdefault(case["group"], case["split"])
        if prior != case["split"]:
            raise ValueError("similar cases cross split")
        actor = ACTORS[case["actor"]]
        _, allowed = access_oracle(actor, records)
        if not set(map(tuple, case["qrels"])) <= allowed:
            raise ValueError("qrels include an inaccessible source")
    if len({(row["tenant"], row["id"]) for row in records}) < 20 or len({row["tenant"] for row in records}) < 2:
        raise ValueError("corpus too small")


def retrieval_suite(store, split):
    docs, all_cases = catalog(), cases()
    validate_corpus(docs, all_cases)
    evidence_by_case = {}
    results = []
    timings = {method: [] for method in METHODS}
    for case in all_cases:
        if case["split"] != split:
            continue
        actor = ACTORS[case["actor"]]
        active, allowed = access_oracle(actor, docs)
        question = case["question"]
        retrieval = {}
        for method in METHODS:
            started = time.perf_counter()
            evidence = retrieve(store, actor, question, SPACE, method=method, k=K, embed=embed,
                                scorer=rerank_script, window=WINDOW, lexical_text=lexical_query(question))
            timings[method].append((time.perf_counter() - started) * 1000)
            evidence_by_case[(case["id"], method)] = evidence
            ranked = list(dict.fromkeys((item.source.document_id, item.source.version) for item in evidence))
            stale = sum(pair not in active for pair in ranked)
            forbidden = sum(pair not in allowed for pair in ranked)
            retrieval[method] = {"ranked": ranked, "metrics": rank_score(ranked, map(tuple, case["qrels"]), K),
                                 "stale": stale, "forbidden": forbidden}
        results.append({"id": case["id"], "lang": case["lang"], "split": split,
                        "qrels": case["qrels"], "retrieval": retrieval})
    latency = {method: {"n": len(samples), "p50": statistics.median(samples),
                        "p95": statistics.quantiles(samples, n=20, method="inclusive")[18]}
               for method, samples in timings.items()}
    return results, evidence_by_case, latency


def evaluate_answers(store, results, selected, cases_by_id, evidence_by_case):
    for row in results:
        case = cases_by_id[row["id"]]
        actor = ACTORS[case["actor"]]
        question = case["question"]
        context = context_for(question, evidence_by_case[(row["id"], selected)])
        draft = generate(context)
        active = store.scoped_sources(actor, tuple(item.source for item in context.evidence), SPACE)
        status = verdict(draft, context.evidence, frozenset(active), question=question)
        claims = [c.text for c in draft.claims] if status == "answered" else []
        qrels = set(map(tuple, case["qrels"]))
        emitted = {(s.document_id, s.version) for c in draft.claims for s in c.sources} if claims else set()
        # The generator only sees context. Gold labels are used below for offline scoring.
        correctness = status == case["expected"] and claims == case["claims"]
        supported = set(claims) <= set(case["claims"]) if claims else None
        valid = emitted <= qrels if emitted else None
        controls = case["unsupported_claims"]
        negative = None
        if controls and active and any((item.document_id, item.version) in qrels for item in active):
            bad = Draft("answer", (Claim(controls[0], (next(item for item in active
                       if (item.document_id, item.version) in qrels),)),))
            negative = verdict(bad, context.evidence, frozenset(active), question=question) == "unsupported"
        if correctness:
            bucket = "ok"
        elif case["expected"] == "answered" and not row["retrieval"][selected]["metrics"]["hits"]:
            bucket = "retrieval_miss"
        else:
            bucket = "answer_mismatch"
        row["answer"] = {"status": status, "expected": case["expected"], "claims": claims,
                         "answer_correct": correctness, "citation_valid": valid, "claim_supported": supported,
                         "correct_abstention": correctness if case["expected"] == "insufficient_evidence" else None,
                         "correct_conflict": correctness if case["expected"] == "conflict" else None,
                         "rejects_unsupported_control": negative, "bucket": bucket}


def report(store, split, selection=None):
    results, evidence, latency = retrieval_suite(store, split)
    summary = metrics_for(results)
    if split == "dev":
        selected = max(METHODS, key=lambda m: (summary[m]["recall"]["mean"], summary[m]["mrr"]["mean"]))
        selection = dict(method=selected, k=K, rerank_window=WINDOW, fixture_sha256=freeze_fingerprint(),
                         criterion="dev recall, then dev MRR, then order fts/dense/hybrid/rerank")
    elif (selection is None or selection.get("fixture_sha256") != freeze_fingerprint()
          or selection.get("k") != K or selection.get("rerank_window") != WINDOW
          or selection.get("method") not in METHODS):
        raise ValueError("holdout requires matching dev selection")
    evaluate_answers(store, results, selection["method"], {c["id"]: c for c in cases()}, evidence)
    groups = {}
    for lang in ("ru", "kk", "en"):
        rows = [row for row in results if row["lang"] == lang]
        groups[lang] = {"n": len(rows), "retrieval": metrics_for(rows), "answer": answer_metrics(rows)}
    forbidden = sum(result["forbidden"] for row in results for result in row["retrieval"].values())
    stale = sum(result["stale"] for row in results for result in row["retrieval"].values())
    unsupported_control_failures = sum(row["answer"]["rejects_unsupported_control"] is False for row in results)
    summary = {"split": split, "n": len(results), "configuration": selection, "retrieval": summary,
               "answer": answer_metrics(results), "languages": groups,
               "security": {"forbidden": forbidden, "stale": stale,
                            "unsupported_control_failures": unsupported_control_failures},
               "cases": results}
    return summary, latency, selection


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("seed", "dev", "holdout"))
    parser.add_argument("--output-dir", type=Path, default=DATA)
    args = parser.parse_args()
    store = RetrievalStore(os.environ.get("VECTOR_DSN", LOCAL_DSN))
    if args.command == "seed":
        seed(store)
        return 0
    args.output_dir.mkdir(parents=True, exist_ok=True)
    selection_file = args.output_dir / "selection.json"
    selection = json.loads(selection_file.read_text()) if args.command == "holdout" else None
    summary, latency, selection = report(store, args.command, selection)
    if args.command == "dev":
        write(selection_file, selection)
    write(args.output_dir / f"{args.command}-report.json", summary)
    write(args.output_dir / f"{args.command}-timings.json",
          {"p50_p95": latency, "clock": "client monotonic; POSIX loopback, no cold-cache guarantee"})
    return int(any(summary["security"].values()))


if __name__ == "__main__":
    raise SystemExit(main())
