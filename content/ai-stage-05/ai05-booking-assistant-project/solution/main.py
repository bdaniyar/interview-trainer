import asyncio

from contracts import Call, Observation, Principal, Provider, Repository, Result, Trace
from fixtures import DemoProvider, DemoRepository


TOOLS = {"get_booking", "list_my_bookings"}


async def execute(call: Call, principal: Principal, repository: Repository) -> Observation:
    if call.name not in TOOLS:
        return Observation(call.id, "unknown_tool")
    if call.name == "get_booking":
        if set(call.arguments) != {"booking_id"}:
            return Observation(call.id, "invalid_arguments")
        number = call.arguments["booking_id"]
        if type(number) is not int or number <= 0:
            return Observation(call.id, "invalid_arguments")
        ids = (number,)
    elif call.arguments:
        return Observation(call.id, "invalid_arguments")
    try:
        if call.name == "list_my_bookings":
            ids = repository.owned_ids(principal)
        if any(repository.owner_of(number) != principal for number in ids):
            return Observation(call.id, "unavailable")
        rows = [await repository.read(number) for number in ids]
    except Exception:
        return Observation(call.id, "tool_error")
    return Observation(call.id, "ok", tuple((row.id, row.status) for row in rows))


async def run_assistant(prompt: str, principal: Principal, provider: Provider,
                        repository: Repository) -> Result:
    try:
        reply = await provider.reply(prompt, ())
    except Exception:
        return Result("provider_error")
    trace = ()
    if reply.kind == "tools":
        if len(reply.calls) > 3:
            return Result("call_budget")
        ids = [call.id for call in reply.calls]
        if (not ids or any(not isinstance(key, str) or not key.strip() for key in ids)
                or len(set(ids)) != len(ids)
                or any(not isinstance(call.arguments, dict) for call in reply.calls)):
            return Result("invalid_provider")
        by_id = {}

        async def collect(call):
            observation = await execute(call, principal, repository)
            by_id[observation.call_id] = observation

        async with asyncio.TaskGroup() as group:
            for call in reply.calls:
                group.create_task(collect(call))
        ordered = tuple(by_id[key] for key in ids)
        trace = tuple(Trace(1, call.name if call.name in TOOLS else "unknown", f"call-{index}",
                            by_id[call.id].outcome)
                      for index, call in enumerate(reply.calls, start=1))
        try:
            reply = await provider.reply(prompt, ordered)
        except Exception:
            return Result("provider_error", trace=trace)
        if reply.kind == "tools":
            return Result("step_budget", trace=trace)
    if reply.calls:
        return Result("invalid_provider", trace=trace)
    if reply.kind in {"refusal", "incomplete"}:
        return Result(reply.kind, trace=trace)
    if reply.kind != "final" or not isinstance(reply.text, str) or not reply.text.strip():
        return Result("invalid_provider", trace=trace)
    return Result("completed", reply.text, trace)


async def main():
    result = await run_assistant("Покажи мою бронь", Principal("north", "alice"),
                                 DemoProvider(), DemoRepository())
    print(result.reason, result.text)


if __name__ == "__main__":
    asyncio.run(main())
