from pydantic import BaseModel, field_validator

class LoginInput(BaseModel):
    email: str

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value):
        value = str(value).strip().lower()
        parts = value.split("@")
        if len(parts) != 2 or not all(parts):
            raise ValueError("invalid email")
        return value
