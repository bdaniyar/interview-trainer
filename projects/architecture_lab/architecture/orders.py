"""Booking application service and PostgreSQL repository, no HTTP dependency."""

from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Protocol
from uuid import uuid4

from sqlalchemy import create_engine, text


class Conflict(ValueError):
    pass


class SoldOut(Conflict):
    pass


def digest(value):
    return sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


class BookingEvents(Protocol):
    def record(self, connection, event: dict) -> None: ...


@dataclass
class BookingRepository:
    connection: object

    def insert(self, key, room):
        return (
            self.connection.execute(
                text(
                    """INSERT INTO bookings(id,request_key,request_hash,room_id)
          VALUES(:id,:key,:hash,:room) ON CONFLICT(request_key) DO NOTHING RETURNING *"""
                ),
                dict(id=uuid4(), key=key, hash=digest(dict(room_id=room)), room=room),
            )
            .mappings()
            .first()
        )

    def existing(self, key):
        return (
            self.connection.execute(
                text("SELECT * FROM bookings WHERE request_key=:key"), dict(key=key)
            )
            .mappings()
            .one()
        )

    def reserve_one(self, room):
        row = self.connection.execute(
            text("""UPDATE inventory SET available=available-1
          WHERE id=:room AND available>0 RETURNING id"""),
            dict(room=room),
        ).first()
        if row is None:
            raise SoldOut("No unit available")


class BookingService:
    def __init__(self, url, events: BookingEvents):
        self.engine = create_engine(
            url, pool_pre_ping=True, connect_args={"connect_timeout": 3}
        )
        self.events = events

    def place(self, key, room, correlation, *, after_record=None):
        with self.engine.begin() as conn:
            repo = BookingRepository(conn)
            if not conn.execute(
                text("SELECT EXISTS(SELECT 1 FROM inventory WHERE id=:id)"),
                dict(id=room),
            ).scalar_one():
                raise SoldOut("Unknown inventory")
            row = repo.insert(key, room)
            if row is None:
                row = repo.existing(key)
                if row["request_hash"] != digest(dict(room_id=room)):
                    raise Conflict("Idempotency key already names another booking")
                return dict(row), False
            repo.reserve_one(room)
            event = dict(
                event_id=str(uuid4()),
                order_id=str(row["id"]),
                kind="booking.created",
                correlation_id=correlation,
            )
            self.events.record(conn, event)
            if after_record:
                after_record(conn)
            return dict(row), True

    def get(self, booking):
        with self.engine.connect() as conn:
            row = (
                conn.execute(
                    text("SELECT * FROM bookings WHERE id=:id"), dict(id=booking)
                )
                .mappings()
                .first()
            )
            return dict(row) if row else None


class OutboxAdapter:
    def record(self, connection, event):
        connection.execute(
            text(
                """INSERT INTO outbox(id,payload) VALUES(:id,CAST(:payload AS jsonb))"""
            ),
            dict(id=event["event_id"], payload=json.dumps(event)),
        )


class LocalNotificationAdapter:
    """Same deployable and transaction; notification module owns its table API."""

    def record(self, connection, event):
        from .notifications import receive_on

        receive_on(connection, event)
