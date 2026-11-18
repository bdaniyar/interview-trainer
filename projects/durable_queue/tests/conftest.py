import os
from threading import Event
from time import monotonic
import httpx
import pytest
from sqlalchemy import create_engine, text
from queue_app.store import Store


@pytest.fixture
def env():
    if os.getenv("QUEUE_PROJECT_TEST") != "1":
        pytest.skip("Use the disposable project test Compose")
    admin = create_engine(os.environ["ADMIN_DATABASE_URL"], pool_pre_ping=True)
    assert admin.url.host == "db" and admin.url.database == "queue_test"
    with admin.begin() as conn:
        conn.execute(text("TRUNCATE external_effects,effects,outbox,jobs"))
    store = Store(os.environ["DATABASE_URL"])
    try:
        yield store, admin
    finally:
        store.engine.dispose()
        admin.dispose()


@pytest.fixture
def api(env):
    url = os.environ["API_URL"]
    end = monotonic() + 20
    with httpx.Client(base_url=url, timeout=5) as client:
        while True:
            try:
                if client.get("/health").status_code == 200:
                    break
            except httpx.HTTPError:
                pass
            if monotonic() > end:
                raise RuntimeError("API did not start")
            Event().wait(0.05)
        yield client
