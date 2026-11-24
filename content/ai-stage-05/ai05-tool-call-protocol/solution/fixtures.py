from contracts import ToolResult


def demo(read_calls, continuation):
    output = [
        {"type": "reasoning", "id": "rs_public", "summary": []},
        {"type": "function_call", "id": "fc_first", "call_id": "c-arrival",
         "name": "get_booking", "arguments": '{"booking_id":42}'},
        {"type": "function_call", "id": "fc_second", "call_id": "c-list",
         "name": "list_my_bookings", "arguments": "{}"},
    ]
    allowed = {"get_booking", "list_my_bookings"}
    results = [ToolResult("c-list", "2 bookings"), ToolResult("c-arrival", "2027-01-14")]
    print(read_calls(output, allowed))
    print(continuation(output, results, allowed)[-2:])
