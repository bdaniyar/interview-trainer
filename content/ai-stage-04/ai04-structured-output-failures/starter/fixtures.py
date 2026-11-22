import re
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class Request:
    text:str
    correlation_id:str
@dataclass(frozen=True)
class Outcome:
    kind:str
    trip:dict|None=None
@dataclass(frozen=True)
class Result:
    status:str
    correlation_id:str
    attempts:int
    trip:dict|None=None

def validate_trip(value):
    if not isinstance(value,dict) or set(value)!={"city","check_in","check_out","guests"}:
        raise ValueError("Невалидная форма")
    city,guests=value["city"],value["guests"]
    if city is not None and (not isinstance(city,str) or not city.strip()):
        raise ValueError("Пустой город")
    if guests is not None and (type(guests) is not int or guests<1):
        raise ValueError("Нет положительного числа гостей")
    dates=[]
    for key in ("check_in","check_out"):
        raw=value[key]
        if raw is not None and (not isinstance(raw,str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}",raw)):
            raise ValueError("Некорректная дата")
        dates.append(date.fromisoformat(raw) if raw is not None else None)
    if all(dates) and dates[0]>=dates[1]:
        raise ValueError("Интервал")
    return value.copy()
async def demo(recover):
    async def send(request,*,repair):
        return Outcome("incomplete")
    result=await recover(send,Request("Летом в Риддер","demo"),allow_repair=True)
    assert result.attempts==2 and result.status=="incomplete"
    print(result)
