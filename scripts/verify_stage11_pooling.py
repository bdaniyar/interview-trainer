"""Run the actual FastAPI/AsyncSession lesson code against PostgreSQL."""
import asyncio
import os
import sys

from httpx import ASGITransport, AsyncClient


async def main():
    context = {}
    exec(compile(sys.stdin.read(), "pooling-lesson", "exec"), context)
    app = context["make_app"](os.environ["DATABASE_URL"])
    async with app.router.lifespan_context(app):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://example.test") as client:
            for _ in range(3):
                response = await client.get("/value")
                assert response.status_code == 200 and response.json() == {"value": 42}, response.text
    print("FastAPI pooling example verified against PostgreSQL, three sequential requests through a pool of one.")


asyncio.run(main())
