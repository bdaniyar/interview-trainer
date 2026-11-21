from dataclasses import dataclass


@dataclass(frozen=True)
class Block:
    conversation_id: str | None
    messages: tuple[str, ...]
    tokens: int
    required: bool = False
    priority: int = 0


def demo(select):
    policy = Block(None, ("policy",), 3, True)
    pair = Block("a", ("call", "result"), 6, priority=2)
    current = Block("a", ("question",), 4)
    chosen = select([policy, pair, current], "a", 10, 2)
    assert chosen == [policy, current]
    print([block.messages for block in chosen])
