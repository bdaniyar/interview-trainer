import json
import os
import signal
from threading import Event, Thread
from uuid import uuid4

from sqlalchemy.exc import SQLAlchemyError
from .store import Store, LostLease


def calculate(payload, attempt):
    if attempt <= payload.get("fail_until", 0):
        raise ValueError("synthetic retryable failure")
    return dict(sum_squares=sum(i * i for i in range(payload["n"] + 1)))


def process(store, lease, lease_seconds=5, work=calculate):
    done = Event()
    lost = Event()

    def pulse():
        while not done.wait(lease_seconds / 3):
            try:
                if not store.heartbeat(lease, lease_seconds):
                    lost.set()
                    return
            except SQLAlchemyError:
                lost.set()
                return

    thread = Thread(target=pulse, daemon=True)
    thread.start()
    try:
        try:
            value = work(lease.payload, lease.attempts)
        except ValueError:
            if not lost.is_set():
                store.fail(lease, retryable=True)
            return
        if not lost.is_set():
            store.finish(lease, value)
    except (LostLease, SQLAlchemyError) as exc:
        print(
            json.dumps(
                dict(
                    event="ownership-or-database-conflict",
                    job_id=str(lease.id),
                    generation=lease.generation,
                    error=type(exc).__name__,
                )
            ),
            flush=True,
        )
    finally:
        done.set()
        thread.join(timeout=4)


def run(store, worker, stopped, seconds=5, work=calculate):
    while not stopped.is_set():
        try:
            lease = store.claim(worker, seconds)
        except SQLAlchemyError:
            stopped.wait(0.2)
            continue
        if lease is None:
            stopped.wait(0.1)
            continue
        print(
            json.dumps(
                dict(
                    event="claimed",
                    worker=worker,
                    job_id=str(lease.id),
                    generation=lease.generation,
                    attempt=lease.attempts,
                )
            ),
            flush=True,
        )
        process(store, lease, seconds, work)


def main():
    store = Store(os.environ["DATABASE_URL"])
    worker = "worker-" + uuid4().hex[:12]
    stopped = Event()
    signal.signal(signal.SIGTERM, lambda *_: stopped.set())
    signal.signal(signal.SIGINT, lambda *_: stopped.set())
    seconds = float(os.getenv("LEASE_SECONDS", "5"))
    try:
        run(store, worker, stopped, seconds)
    finally:
        store.engine.dispose()


if __name__ == "__main__":
    main()
