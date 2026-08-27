from __future__ import annotations

import os

import httpx
from fastapi import HTTPException


RUNNER_URL = os.getenv("RUNNER_URL", "http://localhost:8001")


async def execute_in_runner(payload: dict) -> dict:
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(f"{RUNNER_URL}/execute", json=payload)
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail="Runner недоступен") from exc
    if response.status_code >= 400:
        try:
            detail = response.json().get("detail", "Ошибка runner")
        except ValueError:
            detail = "Ошибка runner"
        raise HTTPException(status_code=response.status_code, detail=detail)
    return response.json()
