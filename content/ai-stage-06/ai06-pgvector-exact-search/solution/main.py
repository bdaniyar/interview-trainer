from math import fsum, hypot, isfinite

from contracts import Row, Scope


def eligible(scope, row):
    return (row.tenant == scope.tenant and row.space == scope.space
            and not row.deleted and row.version == row.active_version
            and (scope.subject == row.owner or scope.subject in row.readers))


def unit(vector):
    if not vector or not all(type(x) in (int, float) and isfinite(x) for x in vector):
        raise ValueError("invalid vector")
    length = hypot(*vector)
    if not length:
        raise ValueError("zero norm")
    return tuple(x / length for x in vector)


def exact(scope, query, rows, k):
    if type(k) is not int or k < 0:
        raise ValueError("invalid limit")
    if not scope.may_read:
        raise PermissionError("read scope required")
    query = unit(query)
    results = []
    for row in rows:
        if eligible(scope, row):
            if len(row.embedding) != len(query):
                raise ValueError("wrong embedding dimension")
            similarity = fsum(x * y for x, y in zip(query, unit(row.embedding), strict=True))
            distance = 1 - max(-1.0, min(1.0, similarity))
            results.append((row.document, row.version, row.chunk_id, distance))
    return sorted(results, key=lambda row: (row[3], row[0], row[2]))[:k]


if __name__ == "__main__":
    scope = Scope("north", "ada", "r1")
    rows = (Row("north", "ada", frozenset(), "guide", 1, 1, False, "r1", "c", (0, 1)),)
    print(exact(scope, (1, 0), rows, 3))
