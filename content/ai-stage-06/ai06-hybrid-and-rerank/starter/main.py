def bm25(query, corpus, *, k1=1.2, b=.75):
    return []


def rrf(branches, *, rank_constant=60, limit=10):
    return []


def rerank(ordered, allowed, n, scorer):
    return ()


if __name__ == "__main__":
    print([key for key, _ in rrf((("a", "b"), ("b", "c")), limit=3)])
