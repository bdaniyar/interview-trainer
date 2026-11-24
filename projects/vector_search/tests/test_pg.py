import os
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from uuid import uuid4

import psycopg
import pytest

from projects.vector_search.cli import LOCAL_DSN
from projects.vector_search.contracts import AccessDenied, Actor, ChunkInput, InvalidVector, VersionConflict
from projects.vector_search.fixtures import OWNER, READER, SOUTH, SPACE, SPACE_V2, axis, oracle, put
from projects.vector_search.store import Store


@pytest.fixture
def lab():
    return Store(os.environ.get("VECTOR_DSN", LOCAL_DSN)), uuid4().hex[:10]


def docs(store, actor=OWNER, space=SPACE):
    return [hit.source.document_id for hit in store.dense(actor, axis(), space, limit=100)]


def test_actual_extension_dimensions_and_runtime_role(lab):
    store, _ = lab
    with store.connect() as db:
        assert db.execute("SELECT current_setting('server_version_num')::int/10000").fetchone()[0] == 17
        assert db.execute("SELECT extversion FROM pg_extension WHERE extname='vector'").fetchone()[0] == "0.8.2"
        assert db.execute("SELECT has_schema_privilege(current_user,'public','CREATE')").fetchone() == (False,)
        assert db.execute("SELECT vector_dims('[1,2]'::vector)").fetchone() == (2,)
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            db.execute("CREATE TABLE unauthorized_test(id int)")


def test_exact_matches_oracle_and_stable_ties_with_acl(lab):
    store, prefix = lab
    vectors = {"z": axis(), "a": axis(), "b": axis(2, 3), "c": axis(-1)}
    for key, vector in vectors.items():
        put(store, OWNER, prefix + key, vector=vector)
    put(store, READER, prefix + "private")
    put(store, SOUTH, prefix + "south")
    put(store, OWNER, prefix + "gone")
    store.delete(OWNER, prefix + "gone")
    rows = [hit for hit in store.dense(OWNER, axis(), limit=100) if hit.source.document_id.startswith(prefix)]
    expected = oracle(axis(), {prefix + key: value for key, value in vectors.items()}, 100)
    assert [row.source.document_id for row in rows] == [key for key, _ in expected]
    assert [row.score for row in rows] == pytest.approx([score for _, score in expected], abs=1e-6)


def test_replay_and_activation_are_scoped_by_space_and_version(lab):
    store, prefix = lab
    assert put(store, OWNER, prefix) == "activated"
    assert put(store, OWNER, prefix) == "replayed"
    assert put(store, OWNER, prefix, version=2, space=SPACE_V2) == "activated"
    assert put(store, OWNER, prefix) == "replayed"
    assert prefix not in docs(store) and prefix in docs(store, space=SPACE_V2)
    with pytest.raises(VersionConflict):
        put(store, OWNER, prefix, version=2, space=SPACE_V2, body="changed")
    assert put(store, SOUTH, prefix, body="same ID in other tenant") == "activated"
    assert prefix in docs(store, SOUTH)


def test_partial_invalid_input_or_wrong_dimension_leaves_old_active(lab):
    store, key = lab
    put(store, OWNER, key)
    with pytest.raises(ValueError):
        store.ingest(OWNER, key, 2, "new", SPACE, (ChunkInput("a", "", 0, "n", axis()),), expected_count=1)
    with pytest.raises(InvalidVector):
        put(store, OWNER, key, version=2, vector=(1., 0.))
    with pytest.raises(InvalidVector):
        put(store, OWNER, key, version=2, space=replace(SPACE, revision="other"))
    assert next(row.source.version for row in store.dense(OWNER, axis(), limit=100)
                if row.source.document_id == key) == 1


def test_grant_revocation_scope_owner_and_tombstone(lab):
    store, key = lab
    put(store, OWNER, key)
    assert key not in docs(store, READER)
    store.grant(OWNER, key, READER.subject, True)
    assert key in docs(store, READER) and key not in docs(store, SOUTH)
    store.grant(OWNER, key, READER.subject, False)
    assert key not in docs(store, READER)
    with pytest.raises(AccessDenied):
        put(store, READER, key, version=2)
    with pytest.raises(AccessDenied):
        docs(store, Actor("north", OWNER.subject, frozenset()))
    store.delete(OWNER, key)
    store.delete(OWNER, key)
    with pytest.raises(AccessDenied):
        put(store, OWNER, key, version=2)
    assert key not in docs(store)


def test_quotes_are_literal_parameters_and_concurrent_replay_is_idempotent(lab):
    store, key = lab
    key += "'; SELECT 1 --"
    with ThreadPoolExecutor(max_workers=2) as pool:
        result = list(pool.map(lambda _: put(store, OWNER, key), range(2)))
    assert sorted(result) == ["activated", "replayed"]
    assert docs(store).count(key) == 1


def test_ann_and_exact_keep_same_scope_even_if_order_differs(lab):
    store, key = lab
    put(store, OWNER, key)
    put(store, SOUTH, key + "-south")
    rows = store.dense(OWNER, axis(), limit=100, approximate=True, ef_search=100)
    assert key in {hit.source.document_id for hit in rows}
    assert key + "-south" not in {hit.source.document_id for hit in rows}
