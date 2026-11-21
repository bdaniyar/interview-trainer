from fastapi.testclient import TestClient


class Echo:
    async def generate(self, question, conversation_id):
        return f"Ответ на {question}"


def exercise(factory):
    app = factory("ana", {17: "ana", 18: "tim"}, Echo())
    with TestClient(app) as client:
        body = {"question": "Статус?", "conversation_id": 17}
        response = client.post("/chat", json=body)
        assert response.json() == {"conversation_id": 17, "text": "Ответ на Статус?"}
        assert client.post("/chat", json={**body, "conversation_id": 18}).status_code == 404
        print(response.json())
