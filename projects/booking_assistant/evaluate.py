"""Frozen offline contract scenarios with separate effect and safety metrics."""
import argparse
import asyncio
import json
from dataclasses import replace
from itertools import zip_longest
from pathlib import Path

from assistant import Assistant
from bookings import BookingRepository, Tools
from contracts import Budget, Call, ChatInput, ProviderUnavailable, Reply
from history import InMemoryHistory
from main import DEMO_ACTORS


DATA = Path(__file__).with_name("data")
AUTHORIZED = {("north", "alice"): {42, 43}, ("north", "bob"): {44}, ("south", "alice"): {45}}


class FixtureRepository(BookingRepository):
    def __init__(self, scenario):
        super().__init__()
        self.scenario = scenario
        self.second_read = asyncio.Event()

    async def read(self, principal, number):
        if self.scenario == "reverse" and number == 42:
            await self.second_read.wait()
        if self.scenario == "tool_timeout":
            await asyncio.Event().wait()
        if self.scenario == "tool_error":
            raise RuntimeError("INTERNAL_DEMO_NOTE")
        result = await super().read(principal, number)
        if self.scenario == "reverse" and number == 43:
            self.second_read.set()
        return result


class ScenarioProvider:
    def __init__(self, case):
        self.case = case
        self.entered = asyncio.Event()
        self.release = asyncio.Event()
        self.cleaned = False
        self.continuations = []
        self.contexts = []

    async def reply(self, context, exchanges):
        self.contexts.append((context.user, tuple(turn.user for turn in context.history)))
        if self.case["id"] in {"provider_timeout", "cancellation"}:
            self.entered.set()
            try:
                await self.release.wait()
            finally:
                self.cleaned = True
        if self.case["id"] == "unavailable":
            raise ProviderUnavailable("INTERNAL_DEMO_NOTE")
        if exchanges:
            self.continuations.append([
                [item.call_id, [booking["booking_id"] for booking in json.loads(item.body)["bookings"]]]
                for item in exchanges[-1].outputs
            ])
        if len(exchanges) < len(self.case.get("batches", ())):
            calls = tuple(Call(*values) for values in self.case["batches"][len(exchanges)])
            return Reply("tools", calls=calls)
        return Reply(self.case.get("reply", "final"), "Готово")


async def concurrent_case(service, history, north, south, first, provider):
    second = history.create(south)
    await service.chat(north, ChatInput(conversation_id=first, text="north-only"))
    await service.chat(south, ChatInput(conversation_id=second, text="south-only"))
    entered, release = asyncio.Event(), asyncio.Event()
    original = provider.reply

    async def overlap(context, exchanges):
        if context.user == "north-next":
            entered.set()
            await release.wait()
        return await original(context, exchanges)

    provider.reply = overlap
    running = asyncio.create_task(service.chat(north, ChatInput(conversation_id=first, text="north-next")))
    try:
        async with asyncio.timeout(1):
            await entered.wait()
            result = await service.chat(south, ChatInput(conversation_id=second, text="south-next"))
    finally:
        release.set()
        await running
    expected = [("north-only", ()), ("south-only", ()), ("south-next", ("south-only",)),
                ("north-next", ("north-only",))]
    return result, provider.contexts == expected


async def run_case(case, tools_factory=Tools):
    name = case["id"]
    repository = FixtureRepository(name)
    original_records = repository.records.copy()
    tools = tools_factory(repository)
    provider = ScenarioProvider(case)
    budget = replace(Budget(), **case.get("budget", {}))
    history = InMemoryHistory()
    service = Assistant(provider, tools, history, budget)
    principal = DEMO_ACTORS[case.get("actor", "north-alice")]
    conversation = history.create(principal)
    request = ChatInput(conversation_id=conversation, text="Synthetic request")
    isolation_ok = True
    if name == "concurrency":
        result, isolation_ok = await concurrent_case(service, history, principal,
                                                     DEMO_ACTORS["south-alice"], conversation, provider)
    elif name == "cancellation":
        task = asyncio.create_task(service.chat(principal, request))
        async with asyncio.timeout(1):
            await provider.entered.wait()
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        isolation_ok = not history.entries[conversation].busy and not history.entries[conversation].turns
        result = None
    else:
        result = await service.chat(principal, request)
    reason = result.reason if result else ("cancelled" if task.cancelled() and provider.cleaned else "invalid")
    outcomes = [tool.outcome for tool in result.tools] if result else []
    proposal_ok = True
    if case.get("proposal"):
        proposals = result.proposals if result else ()
        proposal_ok = (len(proposals) == 1 and len(proposals[0].proposal_id) == 32
                       and proposals[0].status == "pending" and proposals[0].arguments == {"booking_id": 42}
                       and (proposals[0].owner_tenant, proposals[0].owner_subject) == principal.owner
                       and all("owner_" not in output.body for turn in history.entries[conversation].turns
                               for exchange in turn.exchanges for output in exchange.outputs))
    elif result and result.proposals:
        proposal_ok = False
    read_ids = [number for _, number in repository.reads]
    unauthorized_reads = sum(number not in AUTHORIZED.get(owner, ()) for owner, number in repository.reads)
    violations = sum(
        actual != "unavailable" for actual, expected in zip_longest(outcomes, case.get("outcomes", ()))
        if expected == "unavailable"
    )
    budget_failure = (result is not None and
                      (result.usage.steps > budget.steps or result.usage.calls > budget.calls
                       or result.usage.output_bytes > budget.output_bytes
                       or result.usage.context_units > budget.context_units
                       or (case["reason"].endswith("_budget") and reason != case["reason"])))
    performance = {
        "successful_task": reason == "completed" and reason == case["reason"]
        and outcomes == case.get("outcomes", []) and read_ids == case.get("reads", []) and proposal_ok,
        "authorization_violations": violations,
        "unauthorized_protected_reads": unauthorized_reads,
        "booking_writes": len(repository.writes) + int(repository.records != original_records),
        "incorrect_tool_invocation_counts": int(len(tools.invocations) != case.get("invocations", 0)),
        "call_id_correlation_failures": int(provider.continuations != case.get("continuations", [])),
        "budget_violations": int(budget_failure),
        "history_isolation_failures": int(not isolation_ok),
        "terminal_state_correct": reason == case["reason"],
    }
    matched = (performance["terminal_state_correct"] and outcomes == case.get("outcomes", [])
               and read_ids == case.get("reads", []) and proposal_ok
               and not any(value for key, value in performance.items()
                           if key not in {"successful_task", "terminal_state_correct"}))
    return {"id": name, "matched": matched, "reason": reason, "outcomes": outcomes,
            "protected_reads": len(read_ids), "invocations": len(tools.invocations), **performance}


async def evaluate(tools_factory=Tools):
    cases = [json.loads(line) for line in (DATA / "workflows.jsonl").read_text().splitlines()]
    results = [await run_case(case, tools_factory) for case in cases]
    totals = {key: sum(result[key] for result in results) for key in (
        "matched", "successful_task", "authorization_violations", "unauthorized_protected_reads",
        "booking_writes", "incorrect_tool_invocation_counts", "call_id_correlation_failures",
        "budget_violations", "history_isolation_failures", "terminal_state_correct",
    )}
    return {"kind": "scripted_application_contract", "workflows": len(cases),
            "expected_completed": sum(case["reason"] == "completed" for case in cases),
            "protected_read_attempts": sum(result["protected_reads"] for result in results),
            "tool_invocations": sum(result["invocations"] for result in results),
            "totals": totals, "cases": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = asyncio.run(evaluate())
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return int(report["totals"]["matched"] != report["workflows"])


if __name__ == "__main__":
    raise SystemExit(main())
