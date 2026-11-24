import asyncio

import pytest

from contracts import Outcome, Policy, Principal
from fixtures import Store
from main import get_my_booking


def actor(tenant="a", user="lee", scopes=frozenset({"booking:read"})):
    return Principal(tenant, user, scopes)


def store():
    return Store({71: Policy("a", "lee"), 12: Policy("a", "ken"),
                  44: Policy("b", "lee"), 18: Policy("a", "lee", revoked=True)},
                 {71: {"city": "Тараз", "private_note": "CANARY"},
                  12: {"city": "Актобе"}, 44: {"city": "Павлодар"}, 18: {"city": "Алматы"}})


def test_allowed_read_minimizes_payload_and_never_writes():
    repository = store()
    assert asyncio.run(get_my_booking({"booking_id": 71}, actor(), repository)) == Outcome(
        "ok", {"booking_id": 71, "city": "Тараз"})
    assert repository.policy_ids == [71] and repository.protected_reads == [71]
    assert repository.writes == []


@pytest.mark.parametrize("identifier", [12, 44, 18, 404])
def test_denied_and_nonexistent_have_same_shape(identifier):
    repository = store()
    assert asyncio.run(get_my_booking({"booking_id": identifier}, actor(), repository)) == Outcome("not_found")
    assert repository.policy_ids == [identifier]
    assert repository.protected_reads == repository.writes == []


@pytest.mark.parametrize(("caller", "status"), [(None, "unauthenticated"), (actor(scopes=frozenset()), "forbidden")])
def test_no_metadata_lookup_without_trusted_scope(caller, status):
    repository = store()
    assert asyncio.run(get_my_booking({"booking_id": 71}, caller, repository)) == Outcome(status)
    assert repository.policy_ids == repository.protected_reads == repository.writes == []


@pytest.mark.parametrize("patch", [{"user_id": "ken"}, {"tenant": "b"}, {"role": "admin"},
                                  {"scopes": ["booking:read"]}, {"booking_id": True}])
def test_request_cannot_inject_identity_or_coerce_id(patch):
    repository = store()
    assert asyncio.run(get_my_booking({"booking_id": 71} | patch, actor(), repository)) == Outcome("invalid_arguments")
    assert repository.policy_ids == repository.protected_reads == repository.writes == []


def test_concurrent_requests_do_not_reuse_other_principal():
    repository = store()

    async def go():
        return await asyncio.gather(get_my_booking({"booking_id": 71}, actor(), repository),
                                    get_my_booking({"booking_id": 71}, actor("b"), repository),
                                    get_my_booking({"booking_id": 44}, actor("b"), repository))

    assert [r.status for r in asyncio.run(go())] == ["ok", "not_found", "ok"]
    assert sorted(repository.protected_reads) == [44, 71]
    assert repository.writes == []
