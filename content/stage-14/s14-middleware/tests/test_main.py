from uuid import UUID
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
def test_preserves(): assert client.get("/ping", headers={"X-Request-ID": "abc"}).headers["X-Request-ID"] == "abc"
def test_generates(): UUID(client.get("/ping").headers["X-Request-ID"])
