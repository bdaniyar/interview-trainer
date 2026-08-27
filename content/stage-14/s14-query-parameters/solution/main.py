from typing import Annotated
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items")
def items(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    return {"offset": offset, "limit": limit}
