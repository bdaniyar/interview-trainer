import json
import os
import signal
from threading import Event

import httpx
from sqlalchemy.exc import SQLAlchemyError
from .store import Store


def deliver_once(store, send):
    event = store.claim_event()
    if event is None:
        return False
    # No database transaction or row lock spans the remote operation.
    try:
        send(str(event["id"]), event["payload"])
    except (httpx.HTTPError, TimeoutError):
        # The receiver may already have committed. Lease expiry permits retry
        # using the SAME key; its durable inbox must deduplicate the effect.
        print(
            json.dumps(
                dict(event="unknown-delivery-outcome", event_id=str(event["id"]))
            ),
            flush=True,
        )
        return False
    return store.ack_event(event)


def main():
    store = Store(os.environ["DATABASE_URL"])
    stopped = Event()
    signal.signal(signal.SIGTERM, lambda *_: stopped.set())
    receiver = os.getenv("RECEIVER_URL", "http://api:8000/demo-effects")
    with httpx.Client(timeout=2) as client:

        def send(key, payload):
            response = client.post(
                receiver, json=payload, headers={"Idempotency-Key": key}
            )
            response.raise_for_status()

        try:
            while not stopped.is_set():
                try:
                    deliver_once(store, send)
                except SQLAlchemyError:
                    pass
                stopped.wait(0.2)
        finally:
            store.engine.dispose()


if __name__ == "__main__":
    main()
