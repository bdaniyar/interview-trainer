from contracts import Context
from fixtures import demo


def build_context(history, conversation_id, principal, policy, current, *, capacity, reserve, count) -> Context:
    raise NotImplementedError


if __name__ == "__main__":
    demo(build_context)
