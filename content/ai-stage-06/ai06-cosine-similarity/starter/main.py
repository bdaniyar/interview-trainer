def dot(a, b):
    return 0.0


def norm(a):
    return 0.0


def cosine(a, b):
    return 0.0


def top_k(query, candidates, k):
    return []


if __name__ == "__main__":
    print(top_k((1, 0), {"side": (0, -2), "back": (-3, 0), "ahead": (5, 0)}, 2))
