from pydantic import BaseModel, model_validator

class BookingPeriod(BaseModel):
    start: int
    end: int

    @model_validator(mode="after")
    def validate_order(self):
        if self.end <= self.start:
            raise ValueError("end must be after start")
        return self
