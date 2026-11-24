"""Ranking metrics with explicit undefined values and seen-ID policy."""


def rank_score(ranked, relevant, k):
    if type(k) is not int or k < 1:
        raise ValueError("k must be positive")
    ranked = tuple(dict.fromkeys(ranked))[:k]
    relevant = set(relevant)
    matches = len(set(ranked) & relevant)
    first = next((rank for rank, key in enumerate(ranked, 1) if key in relevant), None)
    return {"hits": matches, "relevant": len(relevant), "returned": len(ranked),
            "recall": matches / len(relevant) if relevant else None,
            "precision": matches / len(ranked) if ranked else None,
            "mrr": (1 / first if first else 0.0) if relevant else None}


def mean_defined(values):
    defined = [value for value in values if value is not None]
    return {"mean": sum(defined) / len(defined) if defined else None, "n": len(defined)}
