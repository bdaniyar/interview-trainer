from collections.abc import Mapping

from contracts import Principal, Tool, ToolCall, ToolResult
from fixtures import demo


async def execute_tool(call: ToolCall, principal: Principal, registry: Mapping[str, Tool]) -> ToolResult:
    raise NotImplementedError


if __name__ == "__main__":
    demo(execute_tool)
