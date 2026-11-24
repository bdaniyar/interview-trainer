from contracts import Embedding, Item, Space


def embed(items, space, provider, cache):
    return ()


if __name__ == "__main__":
    space = Space("fake", "r1", 2, True)
    print([o.status for o in embed((Item("a", "Текст"), Item("b", "Бет")), space,
                                   lambda items, s: [Embedding("b", s, (1.0, 0.0))], {})])
