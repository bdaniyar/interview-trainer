from math import hypot

from .contracts import Actor, ChunkInput, Space


OWNER = Actor("north", "alice", frozenset({"read", "ingest", "share", "delete"}))
READER = Actor("north", "bob", frozenset({"read", "ingest"}))
SOUTH = Actor("south", "alice", OWNER.scopes)
SPACE = Space()
SPACE_V2 = Space("fixture-v2", revision="2")


def unit(values: tuple[float, ...]) -> tuple[float, ...]:
    return tuple(x / hypot(*values) for x in values)


def axis(first=1, second=0):
    return unit((first, second, *(0,) * 14))


def put(store, actor, doc, *, body="demo", version=1, space=SPACE, vector=None):
    return store.ingest(actor, doc, version, body, space,
                       (ChunkInput("part", "Guide", 0, body, vector or axis()),), expected_count=1)


def seed(store):
    vectors = {"a-close": axis(1, 2), "tie-z": axis(), "tie-a": axis(), "far": axis(-1)}
    for doc, vector in vectors.items():
        put(store, OWNER, doc, vector=vector)
    put(store, SOUTH, "tie-a")
    put(store, READER, "private")
    put(store, OWNER, "gone")
    store.delete(OWNER, "gone")
    put(store, OWNER, "changing", vector=axis())
    put(store, OWNER, "changing", version=2, vector=axis(0, 1))
    return vectors | {"changing": axis(0, 1)}


def oracle(query, vectors, k):
    """Independent full scan with the cosine formula, without database or project math."""
    scores = {}
    for key, vector in vectors.items():
        dot = sum(query[i] * vector[i] for i in range(len(query)))
        a = sum(value ** 2 for value in query) ** 0.5
        b = sum(value ** 2 for value in vector) ** 0.5
        scores[key] = 1 - dot / (a * b)
    return sorted(scores.items(), key=lambda record: (record[1], record[0]))[:k]
