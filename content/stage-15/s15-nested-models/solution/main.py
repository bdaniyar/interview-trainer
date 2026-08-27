from pydantic import BaseModel, Field

class Address(BaseModel):
    city: str
    country_code: str = Field(min_length=2, max_length=2)

class UserProfile(BaseModel):
    id: int = Field(gt=0)
    address: Address
    tags: list[str] = Field(default_factory=list)
