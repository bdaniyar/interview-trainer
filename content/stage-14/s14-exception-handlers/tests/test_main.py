from fastapi.testclient import TestClient
from main import app

def test_handler():
    response = TestClient(app).get("/conflict")
    assert response.status_code == 409
    assert response.json() == {"error": "already booked"}
