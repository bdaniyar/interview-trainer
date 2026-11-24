"""Transactional lifecycle and parameterized retrieval over disposable PostgreSQL."""
import json
from contextlib import contextmanager

import psycopg

from .contracts import AccessDenied, Actor, ChunkInput, Hit, InvalidVector, Source, Space, VersionConflict, digest, vector_param


ROW_FIELDS = """c.document_id, c.version, c.space_id, c.chunk_id, c.section,
c.start_offset, c.end_offset, d.access_epoch"""
ELIGIBLE = """
    c.tenant = %(tenant)s AND c.space_id = %(space)s
    AND NOT d.deleted AND d.active_version = c.version
    AND (d.owner_name = %(subject)s OR EXISTS (
        SELECT 1 FROM document_grants g WHERE g.tenant = d.tenant
        AND g.document_id = d.id AND g.subject = %(subject)s
    ))
"""
BASE = "FROM chunks c JOIN documents d ON (d.tenant, d.id) = (c.tenant, c.document_id)"
EXACT = f"""
    WITH eligible AS MATERIALIZED (
        SELECT {ROW_FIELDS}, c.embedding {BASE} WHERE {ELIGIBLE}
    )
    SELECT document_id, version, space_id, chunk_id, section, start_offset, end_offset, access_epoch,
           embedding <=> %(vector)s::vector AS distance FROM eligible
    ORDER BY distance, document_id COLLATE "C", chunk_id COLLATE "C" LIMIT %(limit)s
"""
ANN = """
    WITH allowed AS MATERIALIZED (
        SELECT d.id, d.active_version, d.access_epoch FROM documents d
        WHERE d.tenant = %(tenant)s AND NOT d.deleted
          AND (d.owner_name = %(subject)s OR EXISTS (
              SELECT 1 FROM document_grants g WHERE g.tenant = d.tenant
              AND g.document_id = d.id AND g.subject = %(subject)s
          ))
    ), nearest AS MATERIALIZED (
        SELECT c.document_id, c.version, c.space_id, c.chunk_id, c.section,
               c.start_offset, c.end_offset, c.embedding <=> %(vector)s::vector AS distance
        FROM chunks c
        WHERE c.tenant = %(tenant)s AND c.space_id = %(space)s AND EXISTS (
            SELECT 1 FROM allowed a WHERE (a.id,a.active_version) = (c.document_id,c.version) OFFSET 0
        )
        ORDER BY c.embedding <=> %(vector)s::vector LIMIT %(limit)s
    )
    SELECT n.document_id,n.version,n.space_id,n.chunk_id,n.section,n.start_offset,n.end_offset,
           a.access_epoch,n.distance FROM nearest n
    JOIN allowed a ON (a.id,a.active_version)=(n.document_id,n.version)
    ORDER BY n.distance, n.document_id COLLATE "C", n.chunk_id COLLATE "C"
"""
LOCK_DOC = """SELECT owner_name, active_version, deleted FROM documents
              WHERE tenant=%s AND id=%s FOR UPDATE"""


class Store:
    def __init__(self, dsn: str):
        self.dsn = dsn

    @contextmanager
    def connect(self):
        with psycopg.connect(self.dsn, connect_timeout=4) as connection:
            connection.execute("SET LOCAL statement_timeout = '5s'")
            yield connection

    def check_space(self, db, space: Space):
        identity = db.execute(
            "SELECT model,revision,dimension,normalized FROM spaces WHERE id = %s", (space.id,)
        ).fetchone()
        if identity != (space.model, space.revision, space.dimension, space.normalized):
            raise InvalidVector("embedding space mismatch")

    def ingest(self, actor: Actor, document_id: str, version: int, body: str, space: Space,
               chunks: tuple[ChunkInput, ...], *, expected_count: int) -> str:
        actor.require("ingest")
        if (not document_id or not body or type(version) is not int or version < 1
                or not expected_count or len(chunks) != expected_count
                or len({chunk.chunk_id for chunk in chunks}) != expected_count):
            raise ValueError("incomplete or invalid document")
        prepared = []
        for item in chunks:
            end = item.start + len(item.text)
            if (not item.chunk_id or not item.text or item.start < 0
                    or body[item.start:end] != item.text):
                raise ValueError("invalid chunk provenance")
            prepared.append((item, end, digest(item.text), vector_param(item.vector, space)))
        covered = 0
        for start, end in sorted((item.start, end) for item, end, _, _ in prepared):
            if start > covered:
                raise ValueError("chunk coverage has a gap")
            covered = max(covered, end)
        if covered != len(body):
            raise ValueError("chunk coverage is incomplete")
        # Unambiguous replay even if chunk policy changed for the same document bytes.
        content_hash = digest(json.dumps([body, [(item.chunk_id, item.section, item.start, end, fingerprint, vec)
                                                for item, end, fingerprint, vec in prepared]], ensure_ascii=False))
        key = (actor.tenant, document_id)
        with self.connect() as db:
            self.check_space(db, space)
            db.execute("INSERT INTO documents (tenant,id,owner_name) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING",
                       (*key, actor.subject))
            owner, active, deleted = db.execute(LOCK_DOC, key).fetchone()
            if owner != actor.subject or deleted:
                raise AccessDenied("document unavailable")
            known = db.execute(
                "SELECT space_id,content_hash FROM versions WHERE (tenant,document_id,version)=(%s,%s,%s)",
                (*key, version),
            ).fetchone()
            if known == (space.id, content_hash):
                return "replayed"
            if known or (active is not None and version <= active):
                raise VersionConflict("version already used")
            db.execute("INSERT INTO versions VALUES (%s,%s,%s,%s,%s,%s)",
                       (*key, version, space.id, content_hash, expected_count))
            with db.cursor() as cursor:
                cursor.executemany(
                    """INSERT INTO chunks VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::vector,
                       to_tsvector('simple', %s))""",
                    [(*key, version, space.id, item.chunk_id, item.section, item.start, end, fingerprint,
                      vec, item.text) for item, end, fingerprint, vec in prepared],
                )
                cursor.executemany("INSERT INTO payloads VALUES (%s,%s,%s,%s,%s,%s)",
                                   [(*key, version, space.id, item.chunk_id, item.text)
                                    for item, *_ in prepared])
            db.execute("UPDATE documents SET active_version=%s, access_epoch=access_epoch+1 WHERE (tenant,id)=(%s,%s)",
                       (version, *key))
        return "activated"

    def owner_lock(self, db, actor, document_id):
        row = db.execute(LOCK_DOC, (actor.tenant, document_id)).fetchone()
        if row is None or row[0] != actor.subject:
            raise AccessDenied("document unavailable")
        return row

    def delete(self, actor: Actor, document_id: str) -> None:
        actor.require("delete")
        with self.connect() as db:
            self.owner_lock(db, actor, document_id)
            db.execute("""UPDATE documents SET active_version=NULL, deleted=true, access_epoch=access_epoch+1
                          WHERE (tenant,id)=(%s,%s) AND NOT deleted""", (actor.tenant, document_id))

    def grant(self, actor: Actor, document_id: str, subject: str, enabled: bool) -> None:
        actor.require("share")
        with self.connect() as db:
            if self.owner_lock(db, actor, document_id)[2]:
                raise AccessDenied("document unavailable")
            params = (actor.tenant, document_id, subject)
            if enabled:
                result = db.execute("INSERT INTO document_grants VALUES (%s,%s,%s) ON CONFLICT DO NOTHING", params)
            else:
                result = db.execute("DELETE FROM document_grants WHERE (tenant,document_id,subject)=(%s,%s,%s)", params)
            if result.rowcount:
                db.execute("UPDATE documents SET access_epoch=access_epoch+1 WHERE (tenant,id)=(%s,%s)",
                           (actor.tenant, document_id))

    def bindings(self, actor, space, limit):
        actor.require("read")
        if type(limit) is not int or not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        return dict(tenant=actor.tenant, subject=actor.subject, space=space.id, limit=limit)

    def dense(self, actor: Actor, vector: tuple[float, ...], space: Space = Space(), limit: int = 5,
              *, approximate: bool = False, ef_search: int = 40) -> tuple[Hit, ...]:
        params = self.bindings(actor, space, limit)
        params["vector"] = vector_param(vector, space)
        with self.connect() as db:
            self.check_space(db, space)
            if approximate:
                if type(ef_search) is not int or not 1 <= ef_search <= 1000:
                    raise ValueError("invalid ef_search")
                db.execute("SELECT set_config('hnsw.ef_search', %s, true)", (str(ef_search),))
            rows = db.execute(ANN if approximate else EXACT, params).fetchall()
        return tuple(Hit(Source(*row[:-1]), float(row[-1])) for row in rows)
