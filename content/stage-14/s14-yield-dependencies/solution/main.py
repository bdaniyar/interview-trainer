from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()
events = []

def get_resource():
    events.append("open")
    try:
        yield "db"
    finally:
        events.append("close")

@app.get("/resource")
def resource(value: Annotated[str, Depends(get_resource)]):
    return {"resource": value}
