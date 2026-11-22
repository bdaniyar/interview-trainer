from types import SimpleNamespace
from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr

class WireTrip(BaseModel):
    model_config=ConfigDict(extra="forbid",frozen=True)
    city:StrictStr|None
    check_in:StrictStr|None
    check_out:StrictStr|None
    guests:StrictInt|None

class Envelope(BaseModel):
    model_config=ConfigDict(extra="forbid",frozen=True)
    trip:WireTrip

@dataclass(frozen=True)
class ExtractionResult:
    status:str
    model:str|None
    prompt_version:str
    schema_version:str
    trip:WireTrip|None=None

def demo(parse):
    result=parse(SimpleNamespace(status="completed",model="offline",schema_version="trip.schema.v1",
        output=[],output_parsed={"trip":{"city":"Костанай","check_in":None,"check_out":None,"guests":1}}),"trip.prompt.v1")
    assert result.status=="completed" and result.trip.city=="Костанай"
    print(result)
