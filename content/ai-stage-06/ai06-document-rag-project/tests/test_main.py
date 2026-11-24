from dataclasses import replace

import pytest

from contracts import Actor, Answer, Chunk, Ref
from main import activate, answer, revise_access


OWNER = Actor("east", "lee", frozenset({"read", "write"}))
READER = Actor("east", "sam", frozenset({"read"}))
FOREIGN = replace(OWNER, tenant="west")


def build(text):
    return Chunk(0, text[:1]), Chunk(1, text[1:])


def state():
    corpus = {}
    assert activate(corpus, OWNER, "source", 7, "booklet", build) == "activated"
    return corpus


def choose(question, context):
    return context[0][0]


def fail(*args):
    raise RuntimeError("private field")


def test_replay_does_not_invoke_dependency_and_conflicting_bytes_rejected():
    corpus = state()
    assert activate(corpus, OWNER, "source", 7, "booklet", fail) == "replayed"
    assert activate(corpus, OWNER, "source", 7, "altered", build) == "conflict"
    assert activate(corpus, OWNER, "source", 4, "booklet", build) == "conflict"
    assert corpus["east", "source"].epoch == 1


@pytest.mark.parametrize("bad", [lambda _: (), lambda _: (Chunk(1, "new"),),
                                 lambda _: (Chunk(0, "ne"),), fail])
def test_partial_ingestion_keeps_active_version(bad):
    corpus = state()
    assert activate(corpus, OWNER, "source", 8, "new", bad) == "incomplete"
    assert corpus["east", "source"].version == 7


def test_new_version_origin_and_real_retrieval():
    corpus = state()
    assert activate(corpus, OWNER, "source", 8, "жаңа", build) == "activated"
    expected = Ref("east", "source", 8, 2, 1)
    calls = []
    def retrieve(actor, question):
        calls.append("retrieve")
        assert actor == OWNER and question == "q"
        return (Ref("east", "source", 7, 1, 0), expected)
    def generate(question, context):
        calls.append("generate")
        assert context == ((expected, "аңа"),)
        return expected
    assert answer(corpus, OWNER, "q", retrieve, generate) == Answer("answered", "аңа", expected)
    assert calls == ["retrieve", "generate"]


def test_scope_and_tenant_are_independent():
    corpus = state()
    reference = Ref("east", "source", 7, 1, 0)
    assert activate(corpus, READER, "source", 8, "changed", build) == "forbidden"
    assert activate(corpus, FOREIGN, "source", 1, "different tenant", build) == "activated"
    assert answer(corpus, FOREIGN, "q", lambda *_: [reference], fail).status == "insufficient_evidence"
    assert answer(corpus, READER, "q", lambda *_: [reference], fail).status == "insufficient_evidence"
    assert answer(corpus, replace(OWNER, scopes=frozenset()), "q", fail, fail).status == "forbidden"


@pytest.mark.parametrize("mutation", ["update", "revoke", "delete"])
def test_citation_becomes_stale_during_generation(mutation):
    corpus = state()
    corpus["east", "source"] = replace(corpus["east", "source"], readers=frozenset({"sam"}))
    ref = Ref("east", "source", 7, 1, 0)
    def generator(question, context):
        assert context == ((ref, "b"),)
        if mutation == "update":
            activate(corpus, OWNER, "source", 8, "changed", build)
        else:
            revise_access(corpus, OWNER, "source", reader="sam", delete=mutation == "delete")
        return ref
    assert answer(corpus, READER, "q", lambda *_: (ref,), generator) == Answer("stale_evidence")


def test_guessed_reference_and_missing_evidence():
    corpus = state()
    ref = Ref("east", "source", 7, 1, 0)
    assert answer(corpus, OWNER, "q", lambda *_: (), fail) == Answer("insufficient_evidence")
    assert answer(corpus, OWNER, "q", lambda *_: (ref,), lambda *_: replace(ref, index=1)).status == "invalid_citation"


def test_repeat_delete_does_not_resurrect_or_open_version():
    corpus = state()
    revise_access(corpus, OWNER, "source", delete=True)
    revise_access(corpus, OWNER, "source", delete=True)
    assert activate(corpus, OWNER, "source", 8, "new", build) == "forbidden"
    assert corpus["east", "source"].epoch == 2
    assert answer(corpus, OWNER, "q", lambda *_: (Ref("east", "source", 7, 2, 0),), choose).text is None


def test_failures_have_safe_categories():
    corpus = state()
    assert answer(corpus, OWNER, "q", fail, fail) == Answer("retrieval_error")
    assert answer(corpus, OWNER, "q", lambda *_: (Ref("east", "source", 7, 1, 0),), fail) == Answer("generation_error")
