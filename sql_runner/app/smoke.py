"""Disposable internal HTTP smoke test, never touches the application backend."""
import json
from urllib.request import Request, urlopen


def main():
    base = "http://127.0.0.1:8002"

    def call(path, method="GET", data=None):
        body = json.dumps(data).encode() if data is not None else None
        request = Request(base + path, data=body, method=method,
                          headers={"Content-Type": "application/json"})
        with urlopen(request, timeout=30) as response:
            payload = response.read()
            return json.loads(payload) if payload else None

    session = call("/v1/sessions", "POST", {})
    path = "/v1/sessions/" + session["session_id"]
    generation = session["generation"]
    try:
        result = call(path + "/run", "POST", dict(generation=generation, sql="SELECT id,email FROM users ORDER BY id"))
        assert result["error"] is None and result["rows"][0] == ["1", "a@example.com"]
        catalog = call(path + f"/catalog?generation={generation}")
        table = next(t for t in catalog["tables"] if t["name"] == "orders")
        rows = call(path + f"/tables/{table['handle']}/rows?generation={generation}")
        assert len(rows["rows"]) == 5 and table["foreign_keys"]
        blocked = call(path + "/run", "POST", dict(generation=generation, sql="DELETE FROM users"))
        assert blocked["error"]["kind"] == "policy"
        reset = call(path + "/reset", "POST", dict(generation=generation))
        generation = reset["generation"]
        print(json.dumps(dict(session=session, result=result, catalog=catalog,
                              reset_generation=generation, status="passed"), indent=2))
    finally:
        call(path + f"?generation={generation}", "DELETE")


if __name__ == "__main__":
    main()
