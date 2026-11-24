from contracts import Outcome, Principal
from fixtures import demo


async def dispatch(name, arguments, principal: Principal, store, new_id) -> Outcome:
    raise NotImplementedError


if __name__ == "__main__":
    demo(dispatch)
