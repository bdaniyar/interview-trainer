from fastapi.testclient import TestClient
from main import app, events

def test_cleanup():
    events.clear()
    response = TestClient(app).get("/resource")
    assert response.json() == {"resource": "db"}
    assert events == ["open", "close"]
