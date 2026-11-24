from pydantic import ValidationError

from contracts import BookingArgs, Outcome, Principal
from fixtures import demo


async def get_my_booking(arguments: dict, principal: Principal | None, store) -> Outcome:
    if principal is None:
        return Outcome("unauthenticated")
    if "booking:read" not in principal.scopes:
        return Outcome("forbidden")
    try:
        request = BookingArgs.model_validate(arguments)
    except ValidationError:
        return Outcome("invalid_arguments")
    policy = await store.policy(request.booking_id)
    if (policy is None or policy.revoked or policy.tenant != principal.tenant
            or policy.owner != principal.subject):
        return Outcome("not_found")
    row = await store.read(request.booking_id)
    if row is None:
        return Outcome("not_found")
    return Outcome("ok", {"booking_id": request.booking_id, "city": row["city"]})


if __name__ == "__main__":
    demo(get_my_booking)
