import asyncio

from contracts import Call, Reply


def demo(run_loop):
    async def model(history):
        if history:
            return Reply("final", f"Завершены {len(history)} проверки")
        return Reply("calls", calls=(Call("one", "get_booking"), Call("two", "list_my_bookings")))

    async def execute(call):
        return f"{call.name}: ready"

    print(asyncio.run(run_loop(model, execute)))
