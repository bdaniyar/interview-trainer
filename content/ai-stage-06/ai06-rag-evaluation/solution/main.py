from contracts import Case, Prediction


def score_case(case, prediction, k):
    if type(k) is not int or k < 1:
        raise ValueError("k must be positive")
    ranked = tuple(dict.fromkeys(prediction.ranked))[:k]
    relevant = set(case.relevant)
    retrieved = set(ranked)
    hits = len(retrieved & relevant)
    first = next((i for i, key in enumerate(ranked, 1) if key in relevant), None)
    citations = set(prediction.citations)
    claims = set(prediction.claims)
    forbidden = len((set(prediction.ranked) | citations) - case.allowed)
    citation_valid = bool(citations and citations <= relevant and citations <= retrieved) if claims else None
    claim_support = len(claims & case.supported_claims) / len(claims) if claims else None
    correct = (prediction.status == case.expected and
               (case.supported_claims == claims and citation_valid if case.expected == "answered" else not claims and not citations))
    if forbidden:
        bucket = "forbidden"
    elif correct:
        bucket = "ok"
    elif relevant and not hits:
        bucket = "retrieval_miss"
    else:
        bucket = "answer_error"
    return {"recall": hits / len(relevant) if relevant else None,
            "precision": hits / len(ranked) if ranked else None,
            "mrr": (1 / first if first else 0.0) if relevant else None,
            "citation_valid": citation_valid, "claim_support": claim_support,
            "correct": bool(correct), "abstention": bool(correct) if case.expected == "abstain" else None,
            "forbidden": forbidden, "bucket": bucket}


def summarize(rows):
    return {key: {"mean": sum(values) / len(values) if values else None, "n": len(values)}
            for key in ("recall", "precision", "mrr", "citation_valid", "claim_support", "correct", "abstention")
            for values in ([row[key] for row in rows if row[key] is not None],)}


if __name__ == "__main__":
    case = Case("demo", "kk", ("a", "b"), frozenset({"a","b","noise"}), "answered", frozenset({"x"}))
    print(score_case(case, Prediction(("noise", "b", "b"), "answered", ("b",), ("x",)), 3))
