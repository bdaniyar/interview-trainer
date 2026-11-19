import json
import os
from time import monotonic
from typing import Literal
from uuid import UUID, uuid4

from fastapi import FastAPI, Header, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, StrictInt
from sqlalchemy.exc import OperationalError

from .orders import BookingService, Conflict, LocalNotificationAdapter, OutboxAdapter
from .notifications import NotificationStore


class Booking(BaseModel):
    model_config = ConfigDict(extra="forbid")
    room_id: StrictInt = Field(ge=1, le=9223372036854775807)


class BookingEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")
    event_id: UUID
    order_id: UUID
    kind: Literal["booking.created"]
    correlation_id: str = Field(
        min_length=1, max_length=64, pattern=r"^[A-Za-z0-9_-]+$"
    )


def instrument(app):
    @app.exception_handler(OperationalError)
    async def unavailable(_request, _error):
        return JSONResponse(
            status_code=503,
            content={"detail": "Database unavailable; retry with same key"},
        )

    @app.middleware("http")
    async def observe(request: Request, call_next):
        correlation = request.headers.get("X-Correlation-ID", "")
        if (
            not correlation
            or len(correlation) > 64
            or any(
                not (c.isascii() and (c.isalnum() or c in "_-")) for c in correlation
            )
        ):
            correlation = uuid4().hex
        request.state.correlation = correlation
        start = monotonic()
        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation
        print(
            json.dumps(
                dict(
                    event="http",
                    service=app.title,
                    path=request.url.path,
                    status=response.status_code,
                    correlation_id=correlation,
                    duration_ms=round((monotonic() - start) * 1000, 2),
                )
            ),
            flush=True,
        )
        return response

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


def orders_app():
    mono = os.getenv("MODE") == "monolith"
    app = instrument(FastAPI(title="modular-monolith" if mono else "booking-service"))
    service = BookingService(
        os.environ["ORDERS_DATABASE_URL"],
        LocalNotificationAdapter() if mono else OutboxAdapter(),
    )

    @app.post("/bookings")
    def place(
        body: Booking,
        request: Request,
        response: Response,
        idempotency_key: str = Header(
            alias="Idempotency-Key", min_length=1, max_length=128
        ),
    ):
        try:
            row, created = service.place(
                idempotency_key, body.room_id, request.state.correlation
            )
        except Conflict as error:
            raise HTTPException(409, str(error)) from None
        response.status_code = 201 if created else 200
        return row

    @app.get("/bookings/{booking_id}")
    def get(booking_id: UUID):
        row = service.get(booking_id)
        if row is None:
            raise HTTPException(404, "Unknown booking")
        return row

    if mono:
        local_notifications = NotificationStore(os.environ["ORDERS_DATABASE_URL"])

        @app.get("/notifications/{order_id}")
        def notification(order_id: UUID):
            row = local_notifications.get(order_id)
            if row is None:
                raise HTTPException(404, "Unknown notification")
            return row

    return app


def notifications_app():
    app = instrument(FastAPI(title="notification-service"))
    store = NotificationStore(os.environ["NOTIFICATIONS_DATABASE_URL"])

    @app.post("/events")
    def receive(body: BookingEvent):
        try:
            created = store.receive(body.model_dump(mode="json"))
        except Conflict as error:
            raise HTTPException(409, str(error)) from None
        return {"created": created}

    @app.get("/notifications/{order_id}")
    def get(order_id: UUID):
        row = store.get(order_id)
        if row is None:
            raise HTTPException(404, "Not delivered yet")
        return row

    return app
