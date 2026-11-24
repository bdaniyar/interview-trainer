from dataclasses import replace

import pytest

from contracts import Caller, Claim, Draft, Ref, Source
from main import assess


ACTOR = Caller("alfa", "ro")
REC = Source("offset-714", 8, "alfa", "ro")
REF = Ref(REC.id, REC.version)
CLAIM = Claim("limit=204", (REF,))


def evaluate(source=REC, claim=CLAIM, supplied=frozenset({REF}), support=frozenset({CLAIM.text})):
    return assess(ACTOR, {REC.id: source}, supplied, Draft((claim,)), {REF: support})


@pytest.mark.parametrize("patch,reason", [
    ({}, "answered"), ({"version": 9}, "stale_reference"), ({"tenant": "beta"}, "invalid_reference"),
    ({"owner": "foo"}, "invalid_reference"), ({"deleted": True}, "invalid_reference"),
])
def test_version_and_rights(patch, reason):
    assert evaluate(replace(REC, **patch)) == reason


def test_supplied_membership_even_if_catalog_is_current():
    assert evaluate(supplied={Ref("sent-elsewhere", 1)}) == "invalid_reference"


def test_unknown_id_is_invalid():
    assert evaluate(claim=Claim("limit=204", (Ref("invented", 1),))) == "invalid_reference"


def test_allowed_current_reference_cannot_launder_unsupported_claim():
    assert evaluate(claim=replace(CLAIM, text="limit=999")) == "unsupported"


def test_all_claims_and_all_references_are_checked():
    other = Ref("another", 1)
    records = {REF.id: REC, other.id: Source(other.id, 1, "alfa", "ro")}
    result = assess(ACTOR, records, {REF, other},
                    Draft((CLAIM, Claim("limit=204", (REF, other)))), {REF: {CLAIM.text}, other: {"unrelated"}})
    assert result == "unsupported"


@pytest.mark.parametrize("draft,expected", [
    (Draft(()), "insufficient_evidence"), (Draft((Claim("x", ()),)), "invalid"),
    (Draft((Claim(" ", (REF,)),)), "invalid"), ({"claims": []}, "invalid"),
    (Draft((Claim("x", (Ref("x", True),)),)), "invalid"),
])
def test_draft_shape_and_abstention(draft, expected):
    assert assess(ACTOR, {REC.id: REC}, {REF}, draft, {}) == expected


def test_no_evidence_and_conflicting_evidence():
    assert evaluate(supplied=set()) == "insufficient_evidence"
    assert assess(ACTOR, {REC.id: REC}, {REF}, Draft((CLAIM,)), {REF: {CLAIM.text}},
                  conflicting=True) == "conflicting_evidence"
