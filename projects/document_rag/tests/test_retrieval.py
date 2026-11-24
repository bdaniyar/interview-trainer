import os
from uuid import uuid4

from projects.document_rag.ranking import bm25, rerank, rrf
from projects.document_rag.retrieval import RetrievalStore, retrieve
from projects.vector_search.cli import LOCAL_DSN
from projects.vector_search.fixtures import OWNER, READER, SOUTH, SPACE, axis, put


def test_real_fts_dense_fusion_rerank_and_latest_acl():
    store = RetrievalStore(os.environ.get("VECTOR_DSN", LOCAL_DSN))
    tag = "lex" + uuid4().hex[:9]
    a, b, denied = tag + "-a", tag + "-b", tag + "-secret"
    put(store, OWNER, a, body=f"{tag} арна", vector=axis(1, .9))
    put(store, OWNER, b, body=f"{tag} {tag} арна", vector=axis())
    put(store, READER, denied, body=f"{tag} {tag} north private", vector=axis())
    put(store, SOUTH, denied, body=f"{tag} {tag} south private", vector=axis())
    seen = []
    def scorer(text, prefix, rows):
        seen.extend(rows[key].source.document_id for key in prefix)
        return [(key, 1 if key[0] == a else 0) for key in prefix]
    for method in ("fts", "dense", "hybrid", "rerank"):
        evidence = retrieve(store, OWNER, tag, SPACE, method=method, k=100, embed=lambda _: axis(), scorer=scorer, window=100)
        ids = [item.source.document_id for item in evidence]
        assert denied not in ids and a in ids and b in ids
        assert all("private" not in item.text for item in evidence)
        if method == "rerank":
            assert ids[0] == a and denied not in seen
    first = store.lexical(OWNER, tag, SPACE, 10)
    source = next(hit.source for hit in first if hit.source.document_id == a)
    put(store, OWNER, a, version=2, body=f"{tag} new")
    assert store.scoped_sources(OWNER, (source,), SPACE, with_text=True) == ()
    assert store.scoped_sources(SOUTH, (source,), SPACE) == ()


def test_numeric_bm25_rank_constant_and_reranker_window():
    assert [key for key, _ in bm25(("x",), {"a": ("x",), "b": ("x", "x", "b", "b")})] == ["a", "b"]
    assert [key for key, _ in rrf((["a", "a", "b"], ["b", "c"]), limit=3)] == ["b", "a", "c"]
    assert rerank(("a", "b", "c", "foreign"), {"a", "b", "c"}, 2,
                  lambda keys: [(key, float(i)) for i, key in enumerate(keys)]) == ("b", "a", "c")
