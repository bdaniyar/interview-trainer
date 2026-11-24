import asyncio
import time

from contracts import Budget, Observation, Outcome, Reply
from fixtures import demo


async def run_loop(model, execute, budget=Budget(), *, clock=time.monotonic) -> Outcome:
    observations = []
    used_bytes = steps = called = 0
    seen_ids = set()
    deadline = clock() + budget.seconds

    def end(reason, text=None):
        return Outcome(reason, text, steps, called, tuple(observations))

    try:
        async with asyncio.timeout(budget.seconds):
            while steps < budget.steps:
                if clock() >= deadline:
                    return end("timeout")
                steps += 1
                try:
                    reply = await model(tuple(observations))
                except TimeoutError:
                    return end("timeout")
                except Exception:
                    return end("provider_error")
                if clock() >= deadline:
                    return end("timeout")
                if not isinstance(reply, Reply):
                    return end("invalid_reply")
                if reply.kind == "final" and not reply.calls:
                    if isinstance(reply.text, str) and reply.text.strip():
                        return end("completed", reply.text)
                    return end("empty_final")
                if reply.kind in {"refusal", "incomplete"}:
                    return end(reply.kind)
                if reply.kind != "calls" or not reply.calls:
                    return end("invalid_reply")
                ids = {c.call_id for c in reply.calls}
                if any(not isinstance(key, str) or not key.strip() for key in ids) or len(ids) != len(reply.calls) or ids & seen_ids:
                    return end("duplicate_or_missing_id")
                if called + len(reply.calls) > budget.calls:
                    return end("call_limit")
                seen_ids.update(ids)
                for call in reply.calls:
                    if clock() >= deadline:
                        return end("timeout")
                    if used_bytes >= budget.output_bytes:
                        return end("output_limit")
                    called += 1
                    try:
                        async with asyncio.timeout(budget.tool_seconds):
                            output = await execute(call)
                    except TimeoutError:
                        return end("tool_timeout")
                    except Exception:
                        output = "tool_error"
                    if clock() >= deadline:
                        return end("timeout")
                    if not isinstance(output, str):
                        output = "tool_error"
                    size = len(output.encode("utf-8"))
                    if used_bytes + size > budget.output_bytes:
                        return end("output_limit")
                    used_bytes += size
                    observations.append(Observation(call.call_id, output))
            return end("step_limit")
    except TimeoutError:
        return end("timeout")


if __name__ == "__main__":
    demo(run_loop)
