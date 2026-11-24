"""Rank-only fusion and bounded reranking independent of provider scores."""
from collections import Counter, defaultdict
from math import fsum, isfinite, log1p


def bm25(query, corpus, *, k1=1.2, b=.75):
    if not isfinite(k1) or not isfinite(b) or not k1 > 0 or not 0 <= b <= 1:
        raise ValueError("invalid BM25 settings")
    if not corpus:
        return []
    average = sum(map(len, corpus.values())) / len(corpus)
    if not average:
        return []
    terms = tuple(dict.fromkeys(query))
    counts = {key: Counter(tokens) for key, tokens in corpus.items()}
    idfs = {}
    for term in terms:
        df = sum(term in counter for counter in counts.values())
        idfs[term] = log1p((len(corpus) - df + .5) / (df + .5))
    scores = []
    for key, tokens in corpus.items():
        length_factor = k1 * (1 - b + b * len(tokens) / average)
        score = fsum(idfs[term] * (k1 + 1) * frequency / (frequency + length_factor)
                     for term in terms if (frequency := counts[key][term]))
        if score > 0:
            scores.append((key, score))
    return sorted(scores, key=lambda item: (-item[1], item[0]))


def rrf(branches, *, rank_constant=60, limit=10):
    if type(rank_constant) is not int or rank_constant < 1 or type(limit) is not int or limit < 0:
        raise ValueError("invalid fusion settings")
    scores = defaultdict(list)
    for ordered in branches:
        for rank, key in enumerate(dict.fromkeys(ordered), 1):
            scores[key].append(1 / (rank_constant + rank))
    return sorted(((key, fsum(parts)) for key, parts in scores.items()),
                  key=lambda item: (-item[1], item[0]))[:limit]


def rerank(ordered, allowed, n, scorer):
    if type(n) is not int or n < 0:
        raise ValueError("invalid rerank window")
    ids = tuple(key for key in dict.fromkeys(ordered) if key in allowed)
    prefix = ids[:n]
    if not prefix:
        return ids
    rows = list(scorer(prefix))
    ranks = dict(rows)
    if len(rows) != len(ranks) or ranks.keys() != set(prefix):
        raise ValueError("reranker IDs must match the window")
    if any(type(score) not in (int, float) or not isfinite(score) for score in ranks.values()):
        raise ValueError("reranker scores must be finite")
    return tuple(sorted(prefix, key=lambda key: (-ranks[key], key))) + ids[n:]


if __name__ == "__main__":
    print([key for key, _ in rrf((("a", "b"), ("b", "c")), limit=3)])
