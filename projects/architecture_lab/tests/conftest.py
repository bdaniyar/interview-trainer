import os
from threading import Event
from time import monotonic

import httpx
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url


@pytest.fixture
def databases():
    assert os.getenv("ARCH_PROJECT_TEST") == "1", "Use scripts/test_architecture_lab.sh"
    root = make_url(os.environ["ADMIN_DATABASE_URL"])
    assert root.host == "db" and root.database == "postgres"
    engines = {
        name: create_engine(root.set(database="arch_" + name))
        for name in ["orders", "notify", "mono"]
    }
    try:
        for name, engine in engines.items():
            with engine.begin() as conn:
                if name != "notify":
                    conn.execute(text("TRUNCATE bookings,outbox,inventory CASCADE"))
                    conn.execute(text("INSERT INTO inventory VALUES(1,1),(2,2)"))
                if name != "orders":
                    conn.execute(text("TRUNCATE notifications,inbox CASCADE"))
        yield engines
    finally:
        for engine in engines.values():
            engine.dispose()


@pytest.fixture
def clients(databases):
    with httpx.Client(base_url="http://orders:8000", timeout=5) as orders, httpx.Client(
        base_url="http://notifications:8000", timeout=5
    ) as notifications, httpx.Client(
        base_url="http://monolith:8000", timeout=5
    ) as monolith:
        for client in [orders, notifications, monolith]:
            end = monotonic() + 15
            while True:
                try:
                    if client.get("/health").status_code == 200:
                        break
                except httpx.HTTPError:
                    pass
                assert monotonic() < end, "API startup deadline"
                Event().wait(0.05)
        yield dict(orders=orders, notifications=notifications, monolith=monolith)
