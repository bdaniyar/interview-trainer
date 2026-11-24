"""Scripted provider for the offline HTTP demo."""
import json
import re

from contracts import Call, Context, Exchange, Reply


class ScriptedProvider:
    async def reply(self, context: Context, exchanges: tuple[Exchange, ...]) -> Reply:
        if exchanges:
            results = [json.loads(item.body) for item in exchanges[-1].outputs]
            bookings = [row for result in results for row in result.get("bookings", ())]
            if bookings:
                rows = ", ".join(f'{row["booking_id"]} ({row["status"]})' for row in bookings)
                return Reply("final", f"Бронирования: {rows}.")
            if any(result.get("proposal") for result in results):
                return Reply("final", "Предложение отмены создано. Бронирование сохранено.")
            return Reply("final", "Доступных бронирований для этого запроса нет.")
        text = context.user.casefold()
        if text == "список":
            return Reply("tools", calls=(Call("demo-list", "list_my_bookings", "{}"),))
        match = re.fullmatch(r"(бронь|предложи отмену) ([0-9]{1,10})", text)
        if match:
            tool = "get_booking" if match[1] == "бронь" else "propose_cancel"
            arguments = json.dumps({"booking_id": int(match[2])})
            return Reply("tools", calls=(Call("demo-booking", tool, arguments),))
        return Reply("final", "В учебном режиме доступны команды «список», «бронь 42» и «предложи отмену 42».")
