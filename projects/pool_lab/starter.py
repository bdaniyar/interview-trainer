"""Repair this route so every request releases its connection."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import TimeoutError


def make_app(sessions, after_write):
    app = FastAPI()
    # This list makes the leak reproducible even when Python runs GC.
    app.state.open_sessions = []

    @app.exception_handler(TimeoutError)
    async def exhausted(_request: Request, _error: TimeoutError):
        return JSONResponse(status_code=503, content={"detail": "Connection pool busy"})

    @app.post("/values/{number}")
    async def store(number: int, fail: bool = False):
        session = sessions()
        app.state.open_sessions.append(session)
        await session.execute(
            text("INSERT INTO values_received(number) VALUES (:number)"),
            {"number": number},
        )
        await after_write(number)
        if fail:
            raise HTTPException(status_code=409, detail="Request rejected")
        # Missing ownership and transaction cleanup.
        return {"number": number}

    return app
