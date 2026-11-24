"""P5 queries return metadata first, evidence text only after a second scoped check."""
import json
from contextlib import nullcontext
from dataclasses import dataclass

from projects.vector_search.contracts import Actor, Hit, Source, Space
from projects.vector_search.store import BASE, ELIGIBLE, ROW_FIELDS, Store

from .ranking import rerank, rrf


LEXICAL = f"""
    SELECT {ROW_FIELDS}, ts_rank_cd(c.lexemes, q.value) AS rank
    {BASE} CROSS JOIN plainto_tsquery('simple', %(text)s) AS q(value)
    WHERE {ELIGIBLE} AND c.lexemes @@ q.value
    ORDER BY rank DESC, c.document_id COLLATE "C", c.chunk_id COLLATE "C" LIMIT %(limit)s
"""
AUTHORIZED_KEYS = f"""
    WITH wanted AS (
        SELECT * FROM jsonb_to_recordset(%(wanted)s::jsonb)
        AS k(document_id text, version integer, chunk_id text, epoch bigint)
    ), safe AS MATERIALIZED (
        SELECT c.tenant, {ROW_FIELDS} {BASE}
        JOIN wanted k ON (c.document_id,c.version,c.chunk_id,d.access_epoch)
                        =(k.document_id,k.version,k.chunk_id,k.epoch)
        WHERE {ELIGIBLE}
    )
"""
METADATA = """SELECT s.document_id,s.version,s.space_id,s.chunk_id,s.section,s.start_offset,
s.end_offset,s.access_epoch FROM safe s"""
TEXT = """SELECT s.document_id,s.version,s.space_id,s.chunk_id,s.section,s.start_offset,
s.end_offset,s.access_epoch,p.body FROM safe s JOIN payloads p
ON (p.tenant,p.document_id,p.version,p.space_id,p.chunk_id)
=(s.tenant,s.document_id,s.version,s.space_id,s.chunk_id)"""


@dataclass(frozen=True)
class Evidence:
    source: Source
    text: str


class RetrievalStore(Store):
    def lexical(self, actor: Actor, text: str, space: Space, limit: int) -> tuple[Hit, ...]:
        params = self.bindings(actor, space, limit) | {"text": text}
        with self.connect() as db:
            self.check_space(db, space)
            rows = db.execute(LEXICAL, params).fetchall()
        return tuple(Hit(Source(*row[:-1]), float(row[-1])) for row in rows)

    def scoped_sources(self, actor, sources, space, *, with_text=False):
        params = self.bindings(actor, space, 1)
        if not sources:
            return ()
        wanted = [dict(document_id=s.document_id, version=s.version, chunk_id=s.chunk_id, epoch=s.epoch)
                  for s in dict.fromkeys(sources) if s.space_id == space.id]
        params["wanted"] = json.dumps(wanted)
        with self.connect() as db:
            self.check_space(db, space)
            rows = db.execute(AUTHORIZED_KEYS + (TEXT if with_text else METADATA), params).fetchall()
        if with_text:
            keyed = {Source(*row[:-1]): Evidence(Source(*row[:-1]), row[-1]) for row in rows}
        else:
            keyed = {Source(*row): Source(*row) for row in rows}
        return tuple(keyed[s] for s in dict.fromkeys(sources) if s in keyed)


def retrieve(store, actor, text, space, *, method, k, embed, scorer, window=5, lexical_text=None, step=lambda _name, **_attrs: nullcontext()):
    actor.require("read")
    if method not in {"fts", "dense", "hybrid", "rerank"}:
        raise ValueError("unknown retrieval method")
    lexical = store.lexical(actor, text if lexical_text is None else lexical_text, space, k) if method != "dense" else ()
    dense = store.dense(actor, embed(text), space, k) if method != "fts" else ()
    hits = {hit.source.key: hit.source for hit in (*lexical, *dense)}
    with step("rank", candidates=len(hits)):
        if method in {"fts", "dense"}:
            keys = [hit.source.key for hit in lexical or dense]
        else:
            keys = [key for key, _ in rrf(([hit.source.key for hit in lexical],
                                           [hit.source.key for hit in dense]), limit=k)]
    evidence = store.scoped_sources(actor, tuple(hits[key] for key in keys), space, with_text=True)
    if method == "rerank":
        with step("rerank", candidates=min(window, len(evidence))):
            by_key = {item.source.key: item for item in evidence}
            ordered = rerank(keys, by_key, window, lambda prefix: scorer(text, prefix, by_key))
            evidence = tuple(by_key[key] for key in ordered)
    return evidence
