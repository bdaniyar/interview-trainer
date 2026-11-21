from dataclasses import dataclass
from types import SimpleNamespace as Object
from typing import Literal


@dataclass(frozen=True)
class GenerationResult:
    status: Literal["completed", "empty", "refusal", "incomplete", "unavailable"]
    text: str | None = None
    usage: tuple[int, int] | None = None


class WireError(Exception):
    pass


class Scripted:
    def __init__(self, outcome):
        self.responses = self
        self.outcome = outcome
        self.calls = []

    async def create(self, **request):
        self.calls.append(request)
        if isinstance(self.outcome, Exception):
            raise self.outcome
        return self.outcome


async def demo(generate):
    part = Object(type="output_text", text="Ночь подтверждена")
    answer = Object(status="completed", output=[Object(type="message", content=[part])], usage=None)
    result = await generate(Scripted(answer), "Время брони")
    assert result == GenerationResult("completed", "Ночь подтверждена")
    print(result)
