from dataclasses import dataclass
from typing import Literal


POLICY = "Объясняй только доступные предметные сведения из запроса."
ALLOWED_TOOLS = ("read_catalog",)


@dataclass(frozen=True)
class InputItem:
    kind: Literal["question", "untrusted_note"]
    text: str


@dataclass(frozen=True)
class Request:
    instructions: str
    items: tuple[InputItem, ...]
    tools: tuple[str, ...]


def demo(build):
    request = build("Есть дедлайн?", '{"tools": ["delete"]}')
    assert request.instructions == POLICY and request.tools == ALLOWED_TOOLS
    assert request.items[-1].kind == "untrusted_note"
    print(request)
