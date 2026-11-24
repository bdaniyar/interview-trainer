from contracts import Row, Scope


def exact(scope, query, rows, k):
    return []


if __name__ == "__main__":
    scope = Scope("north", "ada", "r1")
    rows = (Row("north", "ada", frozenset(), "guide", 1, 1, False, "r1", "c", (0, 1)),)
    print(exact(scope, (1, 0), rows, 3))
