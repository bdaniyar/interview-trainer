"""Actual HTTP traffic through Uvicorn to FastAPI and a bounded PostgreSQL pool."""
import asyncio
import os
import socket

import httpx
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
import uvicorn

from submission import make_app


def test_checkout_timeout_recovery_commit_and_rollback():
    asyncio.run(exercise_pool())


async def exercise_pool():
    engine = create_async_engine(os.environ["POOL_DSN"], pool_size=1, max_overflow=0,
                                 pool_timeout=.35, pool_pre_ping=True)
    sessions = async_sessionmaker(engine)
    checked_out = asyncio.Event()
    release = asyncio.Event()

    async def after_write(number):
        if number == 1:
            checked_out.set()
            await asyncio.wait_for(release.wait(), timeout=5)

    app = make_app(sessions, after_write)
    bound = socket.socket()
    bound.bind(("127.0.0.1", 0))
    bound.listen(16)
    port = bound.getsockname()[1]
    server = uvicorn.Server(uvicorn.Config(app, log_level="warning", timeout_graceful_shutdown=3))
    task = asyncio.create_task(server.serve(sockets=[bound]))
    try:
        async with asyncio.timeout(5):
            while not server.started:
                if task.done():
                    await task
                    raise AssertionError("ASGI server did not start")
                await asyncio.sleep(.025)
        async with httpx.AsyncClient(base_url=f"http://127.0.0.1:{port}", timeout=4) as client:
            first = asyncio.create_task(client.post("/values/1"))
            await asyncio.wait_for(checked_out.wait(), timeout=3)
            assert engine.pool.checkedout() == 1
            exhausted = await client.post("/values/2")
            assert exhausted.status_code == 503, exhausted.text
            release.set()
            accepted = await first
            assert accepted.status_code == 200 and accepted.json() == {"number": 1}
            assert engine.pool.checkedout() == 0, "First request still holds its connection"
            rejected = await client.post("/values/3?fail=true")
            assert rejected.status_code == 409, rejected.text
            assert engine.pool.checkedout() == 0, "Failing request still holds its connection"
            recovered = await client.post("/values/4")
            assert recovered.status_code == 200 and recovered.json() == {"number": 4}
        async with engine.connect() as conn:
            numbers = (await conn.execute(text("SELECT number FROM values_received ORDER BY number"))).scalars().all()
        assert numbers == [1, 4], "Only accepted requests may commit their rows"
        assert engine.pool.checkedout() == 0
    finally:
        release.set()
        server.should_exit = True
        try:
            await asyncio.wait_for(task, timeout=5)
        finally:
            bound.close()
            await engine.dispose()
