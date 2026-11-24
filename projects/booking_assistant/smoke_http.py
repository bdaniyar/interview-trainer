"""Exercise the demo from an independent process over a loopback socket."""
import argparse
import json
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    base = f"http://127.0.0.1:{args.port}/assistant"

    def post(route, actor, body=None):
        request = Request(base + route, method="POST", headers={
            "X-Demo-Actor": actor, "Content-Type": "application/json",
        }, data=json.dumps(body).encode() if body is not None else None)
        try:
            with urlopen(request, timeout=4) as response:
                return response.status, json.load(response)
        except HTTPError as error:
            return error.code, json.load(error)

    north = "north-alice"
    created, response = post("/conversations", north)
    assert created == 201
    key = response["conversation_id"]
    original = {"conversation_id": key, "text": "бронь 42"}
    status, lookup = post("/chat", north, original)
    assert status == 200 and lookup["reason"] == "completed"
    assert lookup["tools"][0]["bookings"] == [{"booking_id": 42, "status": "confirmed"}]
    status, denied = post("/chat", "south-alice", original)
    assert status == 404 and denied == {"detail": "conversation_unavailable"}
    status, proposal = post("/chat", north, original | {"text": "предложи отмену 42"})
    assert status == 200 and proposal["proposals"][0]["status"] == "pending"
    status, after = post("/chat", north, original)
    assert status == 200 and after["tools"] == lookup["tools"]
    print(json.dumps(lookup["trace"], indent=2))


if __name__ == "__main__":
    main()
