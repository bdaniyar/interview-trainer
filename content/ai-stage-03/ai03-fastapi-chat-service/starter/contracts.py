from dataclasses import dataclass

from fastapi.testclient import TestClient


@dataclass(frozen=True)
class Generation:
    status: str
    text: str | None = None
    usage: int | None = None


class ProviderUnavailable(Exception):
    pass


def demo(create_app):
    class Catalog:
        async def generate(self, question):
            return Generation("completed", f"Каталог: {question}", 7)

    with TestClient(create_app(Catalog(), id_factory=lambda: "demo")) as client:
        result = client.post("/chat", json={"question": "Курс?"})
    assert result.status_code == 200
    assert result.json() == {"status": "completed", "text": "Каталог: Курс?", "usage": 7, "request_id": "demo"}
    print(result.json())
