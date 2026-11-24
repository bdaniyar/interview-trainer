import time

from contracts import Budget, Outcome
from fixtures import demo


async def run_loop(model, execute, budget=Budget(), *, clock=time.monotonic) -> Outcome:
    raise NotImplementedError


if __name__ == "__main__":
    demo(run_loop)
