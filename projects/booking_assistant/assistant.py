"""Compose the typed provider, authorized tools and an owned conversation."""
import asyncio
import time
from collections.abc import Callable
from uuid import uuid4

from bookings import Tools
from contracts import (
    Budget, Call, ChatInput, ChatResult, Exchange, Output, Principal, Provider,
    ProviderUnavailable, Reply, ToolResult, TraceEvent, Turn, Usage,
)
from history import ContextTooLarge, History, build_context, units


def valid_calls(reply: Reply, seen: set[str]) -> bool:
    ids = set()
    for call in reply.calls:
        if not isinstance(call, Call) or not all(
            isinstance(value, str) for value in (call.id, call.name, call.arguments_json)
        ):
            return False
        if not call.id.strip() or not call.name.strip() or units(call.id) > 96 or units(call.name) > 96:
            return False
        if call.id in ids or call.id in seen:
            return False
        ids.add(call.id)
    return bool(ids)


class Assistant:
    def __init__(self, provider: Provider, tools: Tools, history: History,
                 budget: Budget = Budget(), clock: Callable[[], float] = time.monotonic):
        self.provider = provider
        self.tools = tools
        self.history = history
        self.budget = budget
        self.clock = clock

    async def chat(self, principal: Principal, request: ChatInput) -> ChatResult:
        request_id = uuid4().hex
        started = self.clock()
        budget = self.budget
        steps = calls = output_bytes = context_units = 0
        exchanges = ()
        seen = set()
        safe_results = []
        trace = []

        def record(event, outcome, tool=None, alias=None):
            trace.append(TraceEvent(request_id=request_id, step=steps, event=event,
                                    tool=tool, call_id=alias, outcome=outcome, calls=calls,
                                    output_bytes=output_bytes,
                                    elapsed_ms=int((self.clock() - started) * 1000)))

        def finish(reason, answer=None):
            record("terminal", reason)
            status = {"completed": "completed", "refusal": "refused", "incomplete": "incomplete"}
            return ChatResult(
                request_id=request_id, conversation_id=request.conversation_id,
                status=status.get(reason, "failed"), reason=reason, text=answer,
                tools=tuple(safe_results),
                proposals=tuple(result.proposal for result in safe_results if result.proposal),
                usage=Usage(steps=steps, calls=calls, output_bytes=output_bytes, context_units=context_units),
                limits=budget, trace=tuple(trace),
            )

        async def run_tool(call, alias, completed):
            name = call.name if call.name in Tools.schemas else "unknown"
            try:
                async with asyncio.timeout(budget.tool_timeout):
                    result = await self.tools.execute(principal, alias, call.name, call.arguments_json)
            except TimeoutError:
                result = ToolResult(call=alias, tool=name, outcome="tool_timeout")
            except Exception:
                result = ToolResult(call=alias, tool=name, outcome="tool_error")
            if units(result.model_dump_json()) > budget.result_bytes:
                result = ToolResult(call=alias, tool=name, outcome="result_too_large")
            completed[call.id] = result

        async with self.history.claim(principal, request.conversation_id) as conversation:
            try:
                async with asyncio.timeout(budget.deadline):
                    for step in range(budget.steps):
                        context, context_units = build_context(conversation.turns, request.text, exchanges, budget)
                        steps = step + 1
                        try:
                            reply = await self.provider.reply(context, exchanges)
                        except (ProviderUnavailable, TimeoutError):
                            raise
                        except Exception:
                            return finish("invalid_provider")
                        if (not isinstance(reply, Reply) or not isinstance(reply.calls, tuple)
                                or reply.kind not in ("final", "tools", "refusal", "incomplete")):
                            return finish("invalid_provider")
                        record("model", reply.kind)
                        if reply.kind != "tools":
                            if reply.calls or not isinstance(reply.text, str):
                                return finish("invalid_provider")
                            if reply.kind in {"refusal", "incomplete"}:
                                return finish(reply.kind)
                            if not reply.text.strip():
                                return finish("invalid_provider")
                            size = units(reply.text)
                            if size > budget.reserved_units or output_bytes + size > budget.output_bytes:
                                return finish("output_budget")
                            output_bytes += size
                            result = finish("completed", reply.text)
                            conversation.append(Turn(request.text, exchanges, reply.text))
                            return result
                        if steps == budget.steps:
                            return finish("step_budget")
                        if calls + len(reply.calls) > budget.calls:
                            return finish("call_budget")
                        if not valid_calls(reply, seen):
                            return finish("invalid_provider")
                        if output_bytes >= budget.output_bytes:
                            return finish("output_budget")

                        # Complete in any order, but bridge back to the provider by wire ID.
                        completed = {}
                        async with asyncio.TaskGroup() as group:
                            for call in reply.calls:
                                calls += 1
                                group.create_task(run_tool(call, f"call-{calls}", completed))
                        ordered = tuple(completed[call.id] for call in reply.calls)
                        size = sum(units(result.model_dump_json()) for result in ordered)
                        if output_bytes + size > budget.output_bytes:
                            for result in ordered:
                                record("tool", "discarded_by_budget", result.tool, result.call)
                            return finish("output_budget")
                        output_bytes += size
                        safe_results.extend(ordered)
                        outputs = tuple(Output(call.id, result.observation())
                                        for call, result in zip(reply.calls, ordered, strict=True))
                        for call, result in zip(reply.calls, ordered, strict=True):
                            seen.add(call.id)
                            record("tool", result.outcome, result.tool, result.call)
                        exchanges += (Exchange(reply.calls, outputs),)
            except ContextTooLarge:
                return finish("context_budget")
            except TimeoutError:
                return finish("deadline")
            except ProviderUnavailable:
                return finish("provider_unavailable")
            except UnicodeError:
                return finish("invalid_provider")
            return finish("step_budget")
