"""Loopback smoke with the frozen P5 corpus loaded in a disposable database."""
import argparse
import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from uuid import uuid4


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=18766)
    args = parser.parse_args()
    root = f"http://127.0.0.1:{args.port}"

    def request(path, data=None, *, actor="north-alice", method="POST"):
        req = Request(root + path, data=json.dumps(data).encode() if data is not None else None,
                      headers={"Content-Type": "application/json", "X-Demo-Actor": actor}, method=method)
        try:
            with urlopen(req, timeout=5) as response:
                return response.status, json.load(response)
        except HTTPError as error:
            return error.code, json.load(error)

    status, body = request("/ask", {"question": "Қайық қай айлаққа тоқтайды?", "method": "rerank"})
    assert status == 200 and body["status"] == "answered" and body["answer"] == "boat=B3", body
    assert body["request_id"] and all(c["sources"] for c in body["claims"])
    status, body = request("/ask", {"question": "What is the vault access code?"})
    assert status == 200 and body["status"] == "insufficient_evidence" and not body["claims"]
    status, body = request("/ask", {"question": "What is the vault access code?"}, actor="south-alice")
    assert status == 200 and body["answer"] == "vault=SOUTH271"
    assert request("/search", {"question": "vault", "tenant": "south"}) == (422, {"detail": "invalid_input"})
    key = "smoke-" + uuid4().hex
    try:
        payload = {"document_id": key, "version": 1, "markdown": "# Weather\n\nFact: weather = SUNNY\n"}
        assert request("/documents", payload) == (200, {"status": "activated"})
        assert request("/documents", payload) == (200, {"status": "replayed"})
        status, body = request("/ask", {"question": "Weather?", "method": "fts"})
        assert status == 200 and body["answer"] == "weather=SUNNY"
        assert request(f"/documents/{key}", method="DELETE", actor="south-alice") == (
            404, {"detail": "document_unavailable"})
    finally:
        assert request(f"/documents/{key}", method="DELETE") == (200, {"status": "deleted"})
    status, body = request("/ask", {"question": "Weather?", "method": "fts"})
    assert status == 200 and body["status"] == "insufficient_evidence"
    print("P5 loopback: multiline locale, tenancy, strict DTO, ingest/replay, tombstone and citation passed")


if __name__ == "__main__":
    main()
