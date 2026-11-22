import re
from datetime import date
from typing import Annotated
from pydantic import BaseModel,ConfigDict,Field,field_validator,model_validator

class TripRequest(BaseModel):
    model_config=ConfigDict(extra="forbid",str_strip_whitespace=True)
    city: Annotated[str,Field(strict=True,min_length=1,max_length=120)]|None
    check_in: date|None
    check_out: date|None
    guests: Annotated[int,Field(strict=True,gt=0)]|None

    @field_validator("check_in","check_out",mode="before")
    @classmethod
    def exact_date(cls,value):
        if value is None or type(value) is date:
            return value
        if isinstance(value,str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}",value):
            return date.fromisoformat(value)
        raise ValueError("Требуется дата YYYY-MM-DD")

    @model_validator(mode="after")
    def ordered_dates(self):
        if self.check_in and self.check_out and self.check_out<=self.check_in:
            raise ValueError("Выезд должен быть позже въезда")
        return self
if __name__=="__main__":
    from fixtures import demo
    demo(TripRequest)
