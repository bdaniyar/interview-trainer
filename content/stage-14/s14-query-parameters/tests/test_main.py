from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
def test_defaults(): assert client.get("/items").json() == {"offset": 0, "limit": 20}
def test_values(): assert client.get("/items?offset=5&limit=10").json() == {"offset": 5, "limit": 10}
def test_invalid(): assert client.get("/items?limit=0").status_code == 422
