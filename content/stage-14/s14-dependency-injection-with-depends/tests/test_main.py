from fastapi.testclient import TestClient
from main import app

client = TestClient(app)
def test_denied(): assert client.get("/admin").status_code == 403
def test_allowed(): assert client.get("/admin", headers={"X-Role": "admin"}).json() == {"role": "admin"}
