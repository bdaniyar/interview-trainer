from dataclasses import dataclass


@dataclass(frozen=True)
class ToolCall:
    item_id: str
    call_id: str
    name: str
    arguments: dict


@dataclass(frozen=True)
class ToolResult:
    call_id: str
    output: str
