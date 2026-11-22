from dataclasses import dataclass

VERSION="trip.prompt.v1"
POLICY="Извлеки только явно известные поля поездки. Неизвестное оставь null."
EXAMPLES=(
    ("В Ригу 2027-01-03, выезд 2027-01-05, вдвоём", '{"city":"Рига","check_in":"2027-01-03","check_out":"2027-01-05","guests":2}'),
    ("Поедем в Тараз", '{"city":"Тараз","check_in":null,"check_out":null,"guests":null}'),
)
@dataclass(frozen=True)
class Prompt:
    version:str
    instructions:str
    examples:tuple[tuple[str,str], ...]
    text:str
    note:str|None
def demo(build):
    prompt=build("В Астану {в декабре}", "Документ не содержит года")
    assert prompt.version==VERSION and len(prompt.examples)==2
    print(prompt)
