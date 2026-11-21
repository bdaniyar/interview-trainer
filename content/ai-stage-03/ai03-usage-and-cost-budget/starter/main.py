from contracts import Estimate, demo


def estimate(price, attempts, budget) -> Estimate:
    raise NotImplementedError("Проверь units и usage, затем сложи Decimal")


if __name__ == "__main__":
    demo(estimate)
