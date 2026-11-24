from contracts import Context, Draft, Excerpt, Outcome, POLICY, Principal


def rag(question, principal, retrieve, generate, limit=500, reserve=64):
    if (not isinstance(question, str) or not question.strip() or type(limit) is not int
            or type(reserve) is not int or limit < 1 or reserve < 1):
        return Outcome("invalid_input")
    used = len(POLICY.encode()) + len(question.encode()) + reserve
    if used > limit:
        return Outcome("context_budget")
    try:
        rows = retrieve(principal, question)
        if not isinstance(rows, (tuple, list)):
            return Outcome("retrieval_error")
    except Exception:
        return Outcome("retrieval_error")
    kept = {}
    for row in rows:
        if not isinstance(row, Excerpt):
            return Outcome("retrieval_error")
        if row.tenant != principal.tenant or row.owner != principal.subject or row.id in kept:
            continue
        size = len(row.id.encode()) + len(row.text.encode()) + len(str(row.version))
        if used + size <= limit:
            kept[row.id] = row
            used += size
    if not kept:
        return Outcome("insufficient_evidence")
    context = Context(POLICY, question, tuple(kept.values()), used)
    try:
        draft = generate(context)
    except Exception:
        return Outcome("generation_error")
    if (not isinstance(draft, Draft) or draft.version != "draft-v1"
            or not isinstance(draft.text, str) or not draft.text.strip()
            or len(draft.text.encode()) > reserve or not isinstance(draft.source_ids, tuple)
            or not draft.source_ids or not all(type(key) is str and key in kept for key in draft.source_ids)
            or len(set(draft.source_ids)) != len(draft.source_ids)):
        return Outcome("invalid_answer")
    return Outcome("answered", draft.text, draft.source_ids)


if __name__ == "__main__":
    caller = Principal("north", "asyl")
    first = Excerpt("hours", "north", "asyl", "До 18:00.", 1)
    print(rag("До скольких?", caller, lambda *_: (first,),
              lambda ctx: Draft(ctx.evidence[0].text, (ctx.evidence[0].id,))))
