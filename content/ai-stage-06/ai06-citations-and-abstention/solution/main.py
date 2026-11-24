from contracts import Caller, Claim, Draft, Ref, Source


def assess(caller, records, supplied, draft, support, *, conflicting=False):
    if not isinstance(draft, Draft) or not isinstance(draft.claims, tuple):
        return "invalid"
    if conflicting:
        return "conflicting_evidence"
    if not supplied:
        return "insufficient_evidence"
    if not draft.claims:
        return "insufficient_evidence"
    for claim in draft.claims:
        if (not isinstance(claim, Claim) or not isinstance(claim.text, str) or not claim.text.strip()
                or not isinstance(claim.refs, tuple) or not claim.refs):
            return "invalid"
        for ref in claim.refs:
            if (not isinstance(ref, Ref) or type(ref.id) is not str or not ref.id
                    or type(ref.version) is not int or ref.version < 1):
                return "invalid"
            source = records.get(ref.id)
            if (source is None or source.deleted or source.tenant != caller.tenant
                    or source.owner != caller.subject):
                return "invalid_reference"
            if source.version != ref.version:
                return "stale_reference"
            if ref not in supplied:
                return "invalid_reference"
            if claim.text not in support.get(ref, ()):
                return "unsupported"
    return "answered"


if __name__ == "__main__":
    ref = Ref("rules", 2)
    data = {"rules": Source("rules", 2, "west", "ana")}
    print(assess(Caller("west", "ana"), data, {ref}, Draft((Claim("hours=24", (ref,)),)), {ref: {"hours=48"}}))
