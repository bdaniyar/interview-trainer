from contracts import ToolCall, ToolResult
from fixtures import demo


def read_calls(output: list[dict], allowed: set[str]) -> list[ToolCall]:
    raise NotImplementedError


def continuation(output: list[dict], results: list[ToolResult], allowed: set[str]) -> list[dict]:
    raise NotImplementedError


if __name__ == "__main__":
    demo(read_calls, continuation)
