from pydantic import BaseModel, ConfigDict

class UserPatch(BaseModel):
    model_config = ConfigDict(extra="forbid")
    display_name: str | None = None
    age: int | None = None
