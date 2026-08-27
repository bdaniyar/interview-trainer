from fastapi.testclient import TestClient
from main import app

def test_secret_filtered():
    assert TestClient(app).get("/users/me").json() == {"id": 1, "email": "a@example.com"}
