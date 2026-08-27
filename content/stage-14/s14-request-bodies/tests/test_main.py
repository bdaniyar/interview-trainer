from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
def test_created():
    response = client.post("/bookings", json={"room_id": 2, "guests": 3})
    assert response.status_code == 201
    assert response.json() == {"room_id": 2, "guests": 3}
def test_invalid(): assert client.post("/bookings", json={"room_id": 0, "guests": 9}).status_code == 422
