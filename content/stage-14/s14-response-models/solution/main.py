from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserPublic(BaseModel):
    id: int
    email: str

@app.get("/users/me", response_model=UserPublic)
def me():
    return {"id": 1, "email": "a@example.com", "password_hash": "secret"}
