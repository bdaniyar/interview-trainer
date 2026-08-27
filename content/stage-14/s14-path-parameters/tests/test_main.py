from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
def test_valid(): assert client.get("/users/7").json() == {"user_id": 7}
def test_invalid(): assert client.get("/users/0").status_code == 422
