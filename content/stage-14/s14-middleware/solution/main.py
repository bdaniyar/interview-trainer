from uuid import uuid4
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def request_id(request: Request, call_next):
    value = request.headers.get("X-Request-ID") or str(uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = value
    return response

@app.get("/ping")
def ping():
    return {"pong": True}
