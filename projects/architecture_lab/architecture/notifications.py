"""Notification module's durable inbox/effect, also used within the monolith."""

from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import json
from .orders import Conflict, digest


def receive_on(conn, event):
    row = conn.execute(
        text(
            """INSERT INTO inbox(event_id,request_hash,payload)
      VALUES(:id,:hash,CAST(:payload AS jsonb)) ON CONFLICT(event_id) DO NOTHING RETURNING event_id"""
        ),
        dict(id=event["event_id"], hash=digest(event), payload=json.dumps(event)),
    ).first()
    if row is None:
        prior = conn.execute(
            text("SELECT request_hash FROM inbox WHERE event_id=:id"),
            dict(id=event["event_id"]),
        ).scalar_one()
        if prior != digest(event):
            raise Conflict("Event ID reused with different payload")
        return False
    conn.execute(
        text("""INSERT INTO notifications(order_id,event_id,kind,correlation_id)
      VALUES(:order,:event,:kind,:correlation)"""),
        dict(
            order=event["order_id"],
            event=event["event_id"],
            kind=event["kind"],
            correlation=event["correlation_id"],
        ),
    )
    return True


class NotificationStore:
    def __init__(self, url):
        self.engine = create_engine(
            url, pool_pre_ping=True, connect_args={"connect_timeout": 3}
        )

    def receive(self, event):
        try:
            with self.engine.begin() as conn:
                return receive_on(conn, event)
        except IntegrityError as error:
            if getattr(error.orig, "sqlstate", None) == "23505":
                raise Conflict("Notification business key already handled") from None
            raise

    def get(self, order):
        with self.engine.connect() as conn:
            row = (
                conn.execute(
                    text(
                        "SELECT order_id,event_id,kind,correlation_id FROM notifications WHERE order_id=:id"
                    ),
                    dict(id=order),
                )
                .mappings()
                .first()
            )
            return dict(row) if row else None
