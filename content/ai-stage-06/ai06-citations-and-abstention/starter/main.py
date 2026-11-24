from contracts import Caller, Claim, Draft, Ref, Source


def assess(caller, records, supplied, draft, support, *, conflicting=False):
    return "invalid"


if __name__ == "__main__":
    ref = Ref("rules", 2)
    data = {"rules": Source("rules", 2, "west", "ana")}
    print(assess(Caller("west", "ana"), data, {ref}, Draft((Claim("hours=24", (ref,)),)), {ref: {"hours=48"}}))
