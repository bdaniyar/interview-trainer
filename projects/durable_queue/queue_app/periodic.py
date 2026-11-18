import os
import json
import signal
from threading import Event
from time import time
from sqlalchemy.exc import SQLAlchemyError
from .store import Store


def periodic_key(name, epoch, period):
    if not isinstance(name, str) or not 1 <= len(name) <= 64:
        raise ValueError("invalid schedule name")
    if (
        any(isinstance(v, bool) or not isinstance(v, int) for v in [epoch, period])
        or epoch < 0
        or period < 1
    ):
        raise ValueError("invalid UTC epoch/period")
    return f"periodic:{name}:{epoch//period}"


def enqueue_periodic(store, name, epoch, period, payload):
    return store.submit(periodic_key(name, epoch, period), payload)


def main():
    store = Store(os.environ["DATABASE_URL"])
    stopped = Event()
    signal.signal(signal.SIGTERM, lambda *_: stopped.set())
    try:
        while not stopped.is_set():
            try:
                enqueue_periodic(store, "training", int(time()), 60, {"n": 10})
            except SQLAlchemyError:
                print(
                    json.dumps(dict(event="periodic-database-unavailable")), flush=True
                )
            stopped.wait(1)
    finally:
        store.engine.dispose()


if __name__ == "__main__":
    main()
