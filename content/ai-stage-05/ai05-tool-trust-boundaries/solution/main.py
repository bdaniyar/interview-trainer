import json

from pydantic import ValidationError

from contracts import Args, Outcome, Principal, Proposal
from fixtures import demo


SCOPES = {"get_booking": "booking:read", "propose_cancel": "booking:propose"}


async def dispatch(name, arguments, principal: Principal, store, new_id) -> Outcome:
    scope = SCOPES.get(name)
    if scope is None:
        return Outcome("unknown_tool")
    if scope not in principal.scopes:
        return Outcome("forbidden")
    if len(arguments.encode("utf-8")) > 512:
        return Outcome("invalid_arguments")
    try:
        args = Args.model_validate_json(arguments)
    except ValidationError:
        return Outcome("invalid_arguments")

    key = args.booking_id
    try:
        if await store.ownership(key) != (principal.tenant, principal.subject):
            return Outcome("not_found")
        if name == "propose_cancel":
            proposal = Proposal(new_id(), principal.tenant, principal.subject, "cancel_booking",
                                key, (("booking_id", key),), "pending", "Требуется проверка человека")
            return Outcome("pending", proposal=proposal)
        row = await store.read(key)
        if row is None:
            return Outcome("not_found")
        booking = {"booking_id": key, "city": row["city"]}
        if not isinstance(booking["city"], str):
            return Outcome("tool_error")
        if len(json.dumps(booking, ensure_ascii=False).encode("utf-8")) > 512:
            return Outcome("output_limit")
        return Outcome("ok", booking=booking)
    except Exception:
        return Outcome("tool_error")


if __name__ == "__main__":
    demo(dispatch)
