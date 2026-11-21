from dataclasses import dataclass

@dataclass(frozen=True)
class Generation:
    status: str
    text: str | None = None
    usage: int | None = None


class ProviderUnavailable(Exception):
    pass
