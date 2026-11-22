from fixtures import demo
def score(factual, grounded, authorized, ambiguous=False):
    if any(type(value) is not bool for value in (factual, grounded, authorized, ambiguous)):
        raise ValueError("Требуются bool")
    if not (factual and grounded and authorized):
        return "fail"
    return "clarify" if ambiguous else "pass"
if __name__ == "__main__":
    demo(score)
