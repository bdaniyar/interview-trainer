from contracts import Case, Prediction


def score_case(case, prediction, k):
    return {}


def summarize(rows):
    return {}


if __name__ == "__main__":
    case = Case("demo", "kk", ("a", "b"), frozenset({"a","b","noise"}), "answered", frozenset({"x"}))
    print(score_case(case, Prediction(("noise", "b", "b"), "answered", ("b",), ("x",)), 3))
