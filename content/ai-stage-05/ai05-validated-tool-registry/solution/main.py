from collections.abc import Mapping

from pydantic import ValidationError

from contracts import Principal, Tool, ToolCall, ToolResult
from fixtures import demo


async def execute_tool(call: ToolCall, principal: Principal, registry: Mapping[str, Tool]) -> ToolResult:
    tool = registry.get(call.name)
    if tool is None:
        return ToolResult(call.call_id, "unknown_tool")
    if len(call.arguments.encode("utf-8")) > 512:
        return ToolResult(call.call_id, "invalid_arguments")
    try:
        args = tool.arguments.model_validate_json(call.arguments, strict=True)
    except ValidationError:
        return ToolResult(call.call_id, "invalid_arguments")
    try:
        data = await tool.read(principal, args)
        if data is None:
            return ToolResult(call.call_id, "not_found")
        output = tool.output.model_validate(data, strict=True).model_dump_json()
    except Exception:
        return ToolResult(call.call_id, "tool_error")
    if len(output.encode("utf-8")) > 512:
        return ToolResult(call.call_id, "output_limit")
    return ToolResult(call.call_id, "ok", output)


if __name__ == "__main__":
    demo(execute_tool)
