from dataclasses import replace
from hashlib import sha256

import pytest

from contracts import Cached, Embedding, Item, Space
from main import embed


SPACE = Space("fake", "r9", 2, True)
ITEMS = (Item("alpha", "алаш"), Item("beta", "пароль"), Item("gamma", "entry"))


def test_mapping_partial_success_and_retry_uses_only_failed():
    calls, cache = [], {}
    def provider(items, space):
        calls.append([item.id for item in items])
        return [Embedding("gamma", space, (-1., 0.)), Embedding("alpha", space, (0., 1.))]
    first = embed(ITEMS, SPACE, provider, cache)
    assert [o.status for o in first] == ["ok", "missing", "ok"]
    assert [o.vector for o in first] == [(0, 1), None, (-1, 0)]
    assert first[0].digest == sha256("алаш".encode()).hexdigest()
    def retry(items, space):
        calls.append([item.id for item in items])
        return [Embedding("beta", space, (1., 0.))]
    second = embed(ITEMS, SPACE, retry, cache)
    assert [o.status for o in second] == ["cached", "ok", "cached"]
    assert calls == [["alpha", "beta", "gamma"], ["beta"]]


@pytest.mark.parametrize("vector,space", [
    ((1.,), SPACE), ((2., 0.), SPACE), ((float("nan"), 1.), SPACE),
    ((0., 0.), SPACE), ((True, 0), SPACE), ((1., 0.), replace(SPACE, revision="old")),
    ((1., 0.), replace(SPACE, model="different")),
])
def test_invalid_vectors_do_not_poison_cache(vector, space):
    cache = {}
    result = embed(ITEMS[:1], SPACE, lambda *_: [Embedding("alpha", space, vector)], cache)
    assert result[0].status == "invalid" and not cache


def test_duplicate_per_id_keeps_independent_success():
    rows = [Embedding("alpha", SPACE, (1, 0)), Embedding("beta", SPACE, (0, 1)),
            Embedding("alpha", SPACE, (0, 1))]
    assert [o.status for o in embed(ITEMS, SPACE, lambda *_: rows, {})] == ["duplicate", "ok", "missing"]


@pytest.mark.parametrize("items", [(ITEMS[0], ITEMS[0]), (Item("", "valid"),), (Item("x", " "),)])
def test_bad_input_never_calls_provider(items):
    with pytest.raises(ValueError):
        embed(items, SPACE, lambda *_: pytest.fail("provider called"), {})


def test_wrong_cache_space_recomputed():
    digest = sha256(ITEMS[0].text.encode()).hexdigest()
    cache = {(SPACE, digest): Cached(replace(SPACE, normalized=False), digest, (0, 1))}
    outcome, = embed(ITEMS[:1], SPACE, lambda *_: [Embedding("alpha", SPACE, (1, 0))], cache)
    assert outcome.status == "ok" and outcome.vector == (1, 0)


def test_unknown_response_id_and_wrong_envelope():
    for value in ({"alpha": 1}, [Embedding("unknown", SPACE, (0, 1))]):
        assert embed(ITEMS[:1], SPACE, lambda *_: value, {})[0].status == "invalid"


def test_empty_and_transport_failure():
    assert embed((), SPACE, lambda *_: pytest.fail("empty batch"), {}) == ()
    def unavailable(*_):
        raise TimeoutError
    assert embed(ITEMS[:1], SPACE, unavailable, {})[0].status == "provider_error"
