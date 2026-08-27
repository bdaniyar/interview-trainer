from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class DomainConflict(Exception):
    pass

@app.exception_handler(DomainConflict)
def handle_conflict(request: Request, exc: DomainConflict):
    return JSONResponse({"error": str(exc)}, status_code=409)

@app.get("/conflict")
def conflict():
    raise DomainConflict("already booked")
