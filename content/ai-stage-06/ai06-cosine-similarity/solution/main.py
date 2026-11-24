from math import fsum, hypot, isfinite


def checked(vector):
    if not vector or any(type(value) not in (int, float) or not isfinite(value) for value in vector):
        raise ValueError("expected a nonempty finite real vector")
    if not any(vector):
        raise ValueError("zero vector")
    return tuple(vector)


def pair(a, b):
    a, b = checked(a), checked(b)
    if len(a) != len(b):
        raise ValueError("incompatible dimensions")
    return a, b


def dot(a, b):
    a, b = pair(a, b)
    return fsum(x * y for x, y in zip(a, b, strict=True))


def norm(a):
    return hypot(*checked(a))


def unit(a):
    scale = max(map(abs, a))
    scaled = tuple(x / scale for x in a)
    length = hypot(*scaled)
    return tuple(x / length for x in scaled)


def cosine(a, b):
    a, b = pair(a, b)
    similarity = fsum(x * y for x, y in zip(unit(a), unit(b), strict=True))
    return min(1.0, max(-1.0, similarity))


def top_k(query, candidates, k):
    if type(k) is not int or k < 0:
        raise ValueError("k must be a nonnegative integer")
    query = checked(query)
    if any(type(key) is not str or not key for key in candidates):
        raise ValueError("candidate IDs are nonempty strings")
    ranked = [(key, cosine(query, value)) for key, value in candidates.items()]
    return sorted(ranked, key=lambda result: (-result[1], result[0]))[:k]


if __name__ == "__main__":
    print(top_k((1, 0), {"side": (0, -2), "back": (-3, 0), "ahead": (5, 0)}, 2))
