from contracts import Draft, Excerpt, Outcome, Principal


def rag(question, principal, retrieve, generate, limit=500, reserve=64):
    return Outcome("invalid_input")


if __name__ == "__main__":
    caller = Principal("north", "asyl")
    first = Excerpt("hours", "north", "asyl", "До 18:00.", 1)
    print(rag("До скольких?", caller, lambda *_: (first,),
              lambda ctx: Draft(ctx.evidence[0].text, (ctx.evidence[0].id,))))
