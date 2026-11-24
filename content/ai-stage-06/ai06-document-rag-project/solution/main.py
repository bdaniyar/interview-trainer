from dataclasses import replace
from hashlib import sha256

from contracts import Actor, Answer, Chunk, Document, Ref


def activate(state, actor, key, version, text, build):
    if "write" not in actor.scopes:
        return "forbidden"
    if not key or type(version) is not int or version < 1 or not text:
        return "invalid"
    current = state.get((actor.tenant, key))
    if current and (current.owner != actor.subject or current.deleted):
        return "forbidden"
    digest = sha256(text.encode()).hexdigest()
    if current and version <= current.version:
        return "replayed" if version == current.version and digest == current.digest else "conflict"
    try:
        chunks = tuple(build(text))
    except Exception:
        return "incomplete"
    if (not chunks or any(not isinstance(row, Chunk) or row.index != i or not row.text for i, row in enumerate(chunks))
            or "".join(row.text for row in chunks) != text):
        return "incomplete"
    state[actor.tenant, key] = Document(actor.subject, version, digest, chunks,
                                       current.epoch + 1 if current else 1,
                                       current.readers if current else frozenset())
    return "activated"


def revise_access(state, actor, key, *, reader=None, delete=False):
    doc = state.get((actor.tenant, key))
    if "write" not in actor.scopes or doc is None or doc.owner != actor.subject:
        return "forbidden"
    if delete and not doc.deleted:
        state[actor.tenant, key] = replace(doc, deleted=True, epoch=doc.epoch + 1)
    elif not doc.deleted and reader in doc.readers:
        state[actor.tenant, key] = replace(doc, readers=doc.readers - {reader}, epoch=doc.epoch + 1)
    return "updated"


def resolve(state, actor, ref):
    doc = state.get((ref.tenant, ref.key))
    if (ref.tenant != actor.tenant or not doc or doc.deleted
            or (actor.subject != doc.owner and actor.subject not in doc.readers)
            or (ref.version, ref.epoch) != (doc.version, doc.epoch)
            or not 0 <= ref.index < len(doc.chunks)):
        return None
    return doc.chunks[ref.index].text


def answer(state, actor, question, retrieve, generate):
    if "read" not in actor.scopes:
        return Answer("forbidden")
    try:
        candidates = tuple(retrieve(actor, question))
    except Exception:
        return Answer("retrieval_error")
    if any(not isinstance(ref, Ref) for ref in candidates):
        return Answer("retrieval_error")
    supplied = {}
    for ref in candidates:
        text = resolve(state, actor, ref)
        if text is not None:
            supplied[ref] = text
    if not supplied:
        return Answer("insufficient_evidence")
    try:
        chosen = generate(question, tuple(supplied.items()))
    except Exception:
        return Answer("generation_error")
    if chosen is None:
        return Answer("insufficient_evidence")
    if not isinstance(chosen, Ref) or chosen not in supplied:
        return Answer("invalid_citation")
    if any(resolve(state, actor, ref) != text for ref, text in supplied.items()):
        return Answer("stale_evidence")
    return Answer("answered", supplied[chosen], chosen)


if __name__ == "__main__":
    corpus = {}
    owner = Actor("north", "ari", frozenset({"read", "write"}))
    print(activate(corpus, owner, "map", 1, "Маршрут открыт", lambda value: (Chunk(0, value),)))
    source = Ref("north", "map", 1, 1, 0)
    print(answer(corpus, owner, "Маршрут?", lambda *_: (source,), lambda _, context: context[0][0]))
