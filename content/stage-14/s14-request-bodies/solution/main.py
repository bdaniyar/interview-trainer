from fastapi import FastAPI, status
from pydantic import BaseModel, Field

app = FastAPI()

class BookingCreate(BaseModel):
    room_id: int = Field(gt=0)
    guests: int = Field(ge=1, le=8)

@app.post("/bookings", status_code=status.HTTP_201_CREATED)
def create_booking(payload: BookingCreate):
    return payload
