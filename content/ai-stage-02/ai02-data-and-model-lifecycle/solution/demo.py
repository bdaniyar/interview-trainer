def run_examples(split):
    rows = [
        {"id": 3, "user_id": "a", "booked_at": 8, "features": {"nights": (2, 8), "refund": (True, 11)}, "label": 1},
        {"id": 4, "user_id": "b", "booked_at": 12, "features": {}, "label": 0},
    ]
    result = split(rows, 10, 12)
    assert result["train"][0]["features"] == {"nights": (2, 8)}
    assert result["test"][0]["id"] == 4
    print({name: [row["id"] for row in records] for name, records in result.items()})
