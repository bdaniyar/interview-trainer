from collections import Counter
from hashlib import sha256
from math import hypot, isclose, isfinite

from contracts import Cached, Embedding, Item, Outcome, Space


def valid(space, vector):
    return (type(vector) is tuple and len(vector) == space.dimension
            and all(type(value) in (int, float) and isfinite(value) for value in vector)
            and any(vector) and (not space.normalized or isclose(hypot(*vector), 1, abs_tol=1e-6)))


def embed(items, space, provider, cache):
    if (not space.model or not space.revision or type(space.dimension) is not int
            or space.dimension < 1 or type(space.normalized) is not bool):
        raise ValueError("invalid space")
    counts = Counter(item.id for item in items)
    if any(not item.id or not item.text.strip() or counts[item.id] != 1 for item in items):
        raise ValueError("invalid or duplicate batch input")
    digests = {item.id: sha256(item.text.encode()).hexdigest() for item in items}
    outcomes, pending = {}, []
    for item in items:
        digest = digests[item.id]
        entry = cache.get((space, digest))
        if (isinstance(entry, Cached) and entry.space == space and entry.digest == digest
                and valid(space, entry.vector)):
            outcomes[item.id] = Outcome(item.id, digest, "cached", entry.vector)
        else:
            pending.append(item)

    if pending:
        try:
            response = provider(tuple(pending), space)
        except (TimeoutError, ConnectionError):
            response = None
        expected = {item.id for item in pending}
        malformed = set()
        by_id = {}
        if isinstance(response, (list, tuple)):
            for row in response:
                if not isinstance(row, Embedding) or type(row.id) is not str:
                    continue
                if row.id in by_id:
                    malformed.add(row.id)
                by_id[row.id] = row
            unexpected = bool(by_id.keys() - expected)
        else:
            unexpected = False
        for item in pending:
            key, digest = item.id, digests[item.id]
            row = by_id.get(key)
            if key in malformed:
                status = "duplicate"
            elif response is None:
                status = "provider_error"
            elif unexpected or not isinstance(response, (list, tuple)):
                status = "invalid"
            elif row is None:
                status = "missing"
            elif row.space != space or not valid(space, row.vector):
                status = "invalid"
            else:
                outcomes[key] = Outcome(key, digest, "ok", row.vector)
                cache[(space, digest)] = Cached(space, digest, row.vector)
                continue
            outcomes[key] = Outcome(key, digest, status)
    return tuple(outcomes[item.id] for item in items)


if __name__ == "__main__":
    space = Space("fake", "r1", 2, True)
    print([o.status for o in embed((Item("a", "Текст"), Item("b", "Бет")), space,
                                   lambda items, s: [Embedding("b", s, (1.0, 0.0))], {})])
