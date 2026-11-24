from contracts import Outcome, Principal
from fixtures import demo


async def get_my_booking(arguments: dict, principal: Principal | None, store) -> Outcome:
    raise NotImplementedError


if __name__ == "__main__":
    demo(get_my_booking)
