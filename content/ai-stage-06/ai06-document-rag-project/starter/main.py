from contracts import Actor, Answer, Chunk, Ref


def activate(state, actor, key, version, text, build):
    return "incomplete"


def revise_access(state, actor, key, *, reader=None, delete=False):
    return "forbidden"


def answer(state, actor, question, retrieve, generate):
    return Answer("insufficient_evidence")


if __name__ == "__main__":
    corpus = {}
    owner = Actor("north", "ari", frozenset({"read", "write"}))
    print(activate(corpus, owner, "map", 1, "Маршрут открыт", lambda value: (Chunk(0, value),)))
    source = Ref("north", "map", 1, 1, 0)
    print(answer(corpus, owner, "Маршрут?", lambda *_: (source,), lambda _, context: context[0][0]))
