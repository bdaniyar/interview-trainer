from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(min_length=3)
    age: int = Field(ge=14, le=120)
