from math import ceil, isfinite


def top(ids, k):
    if any(type(value) is not str or not value for value in ids):
        raise ValueError("invalid ID")
    return tuple(dict.fromkeys(ids))[:k]


def recall_at_k(exact, approximate, k):
    if type(k) is not int or k < 1:
        raise ValueError("k must be positive")
    reference = set(top(exact, k))
    found = set(top(approximate, k))
    return len(reference & found) / len(reference) if reference else None


def summarize(cases, k):
    """cases maps ID to (exact IDs, approximate IDs, measured milliseconds)."""
    if type(k) is not int or k < 1:
        raise ValueError("k must be positive")
    recalls, timings = {}, []
    for key, (exact, approximate, elapsed) in cases.items():
        if type(elapsed) not in (float, int) or not isfinite(elapsed) or elapsed < 0:
            raise ValueError("invalid latency")
        recalls[key] = recall_at_k(exact, approximate, k)
        timings.append(elapsed)
    defined = [score for score in recalls.values() if score is not None]
    timings.sort()
    n = len(timings)
    return {"recall": recalls, "recall_mean": sum(defined) / len(defined) if defined else None,
            "recall_n": len(defined), "latency_n": n,
            "p50": timings[ceil(n * .50) - 1] if n else None,
            "p95": timings[ceil(n * .95) - 1] if n else None}


if __name__ == "__main__":
    print(summarize({"x": (("a", "b"), ("b", "c"), 3.5)}, 2))
