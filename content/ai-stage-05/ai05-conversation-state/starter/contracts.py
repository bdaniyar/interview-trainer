from dataclasses import dataclass


@dataclass(frozen=True)
class Principal:
    tenant: str
    subject: str


@dataclass(frozen=True)
class Message:
    role: str
    text: str = ""
    call_ids: tuple[str, ...] = ()
    call_id: str | None = None


@dataclass(frozen=True)
class Conversation:
    owner: Principal
    units: tuple[tuple[Message, ...], ...] = ()


@dataclass(frozen=True)
class Context:
    messages: tuple[Message, ...]
    input_tokens: int
    reserved_output: int
