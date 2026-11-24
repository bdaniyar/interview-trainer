"""Typed structural and fixture-specific extractive support checks."""
from .pipeline import Claim, Draft
from .scripted import facts_for, topic


def verdict(draft, supplied, current, *, question):
    if not isinstance(draft, Draft) or draft.kind not in ("answer", "abstain", "conflict"):
        return "invalid_answer"
    if draft.kind != "answer":
        if draft.claims:
            return "invalid_answer"
        return "conflict" if draft.kind == "conflict" else "insufficient_evidence"
    if (not isinstance(draft.claims, tuple) or not draft.claims or len(draft.claims) > 8
            or any(not isinstance(claim, Claim) for claim in draft.claims)):
        return "invalid_answer"
    available = {item.source: facts_for(item) for item in supplied}
    for claim in draft.claims:
        if (type(claim.text) is not str or not 1 <= len(claim.text) <= 100
                or not isinstance(claim.sources, tuple) or not 1 <= len(claim.sources) <= 12):
            return "invalid_answer"
        if any(source not in available for source in claim.sources):
            return "invalid_answer"
        if any(source not in current for source in claim.sources):
            return "stale_evidence"
        if (not claim.text.startswith(f"{topic(question)}=")
                or any(claim.text not in available[source] for source in claim.sources)):
            return "unsupported"
    return "answered"
