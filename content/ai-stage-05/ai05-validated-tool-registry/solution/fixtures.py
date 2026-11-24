import asyncio

from contracts import BookingArgs, BookingView, Principal, Tool, ToolCall


def demo(execute):
    async def read(caller, args):
        assert caller.subject == "student" and args.booking_id == 42
        return {"city": "Астана"}

    async def run():
        tools = {"get_booking": Tool(BookingArgs, BookingView, read)}
        caller = Principal("training", "student")
        for request in ('{"booking_id":42}', '{"booking_id":"42"}'):
            print(await execute(ToolCall("c-public", "get_booking", request), caller, tools))

    asyncio.run(run())
