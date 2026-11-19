import json
import os
import signal
from threading import Event

import httpx
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


class Relay:
    def __init__(self, url):
        self.engine = create_engine(
            url, pool_pre_ping=True, connect_args={"connect_timeout": 3}
        )

    def claim(self):
        with self.engine.begin() as conn:
            conn.execute(
                text(
                    """UPDATE outbox SET state='failed',lease_until=NULL
              WHERE state='sending' AND lease_until<=clock_timestamp() AND attempts>=5"""
                )
            )
            row = conn.execute(text("""WITH picked AS (SELECT id FROM outbox
              WHERE attempts<5 AND ((state='pending' AND available_at<=clock_timestamp()) OR
                (state='sending' AND lease_until<=clock_timestamp()))
              ORDER BY created_at,id FOR UPDATE SKIP LOCKED LIMIT 1)
              UPDATE outbox o SET state='sending',generation=generation+1,attempts=attempts+1,
                lease_until=clock_timestamp()+INTERVAL '5 seconds'
              FROM picked p WHERE o.id=p.id RETURNING o.*""")).mappings().first()
            return dict(row) if row else None

    def finish(self, event, *, delivered):
        with self.engine.begin() as conn:
            row = conn.execute(
                text("""UPDATE outbox SET state=CASE WHEN :delivered THEN 'delivered'
                WHEN attempts>=5 THEN 'failed' ELSE 'pending' END,
                lease_until=NULL,available_at=clock_timestamp()+:delay*INTERVAL '1 second'
              WHERE id=:id AND state='sending' AND generation=:generation
                AND lease_until>clock_timestamp() RETURNING id"""),
                dict(
                    id=event["id"],
                    generation=event["generation"],
                    delivered=delivered,
                    delay=min(8, 0.2 * 2 ** (event["attempts"] - 1)),
                ),
            ).first()
            return row is not None

    def once(self, receiver, *, timeout=2):
        event = self.claim()
        if event is None:
            return False
        payload = event["payload"]
        try:
            # No DB transaction spans this HTTP request.
            response = httpx.post(
                receiver,
                json=payload,
                timeout=timeout,
                headers={"X-Correlation-ID": payload["correlation_id"]},
            )
            response.raise_for_status()
        except httpx.HTTPError:
            self.finish(event, delivered=False)
            print(
                json.dumps(
                    dict(
                        event="delivery-unknown-or-rejected",
                        event_id=str(event["id"]),
                        correlation_id=payload["correlation_id"],
                        attempt=event["attempts"],
                    )
                ),
                flush=True,
            )
            return False
        return self.finish(event, delivered=True)


def main():
    relay = Relay(os.environ["ORDERS_DATABASE_URL"])
    stopped = Event()
    signal.signal(signal.SIGTERM, lambda *_: stopped.set())
    try:
        while not stopped.is_set():
            try:
                relay.once(os.environ["NOTIFICATION_URL"] + "/events")
            except SQLAlchemyError:
                pass
            stopped.wait(0.2)
    finally:
        relay.engine.dispose()


if __name__ == "__main__":
    main()
