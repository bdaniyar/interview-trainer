from contracts import Booking, Call, Principal, Reply


class DemoRepository:
    def __init__(self):
        self.owners = {42: Principal("north", "alice"), 77: Principal("south", "alice")}
        self.rows = {42: Booking(42, "confirmed", "private notes"),
                     77: Booking(77, "pending", "private notes")}
        self.reads = []

    def owned_ids(self, principal):
        return tuple(number for number, owner in self.owners.items() if owner == principal)

    def owner_of(self, booking_id):
        return self.owners.get(booking_id)

    async def read(self, booking_id):
        self.reads.append(booking_id)
        return self.rows[booking_id]


class DemoProvider:
    async def reply(self, prompt, observations):
        if not observations:
            return Reply("tools", calls=(Call("draft-1", "get_booking", {"booking_id": 42}),))
        observation = observations[0]
        if not observation.bookings:
            return Reply("final", "Бронирование недоступно")
        number, status = observation.bookings[0]
        return Reply("final", f"Бронь {number}: {status}")
