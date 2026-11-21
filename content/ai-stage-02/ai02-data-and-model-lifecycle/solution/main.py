from collections import defaultdict
from demo import run_examples


def split_bookings(rows, validation_at, test_at):
    if validation_at >= test_at:
        raise ValueError("Возрастающие границы обязательны")
    result = {name: [] for name in ("train", "validation", "test", "quarantine")}
    periods = defaultdict(set)
    entries = []
    seen_ids = set()
    for row in sorted(rows, key=lambda item: (item["booked_at"], item["id"])):
        if row["id"] in seen_ids:
            raise ValueError("Повтор ID")
        seen_ids.add(row["id"])
        time = row["booked_at"]
        period = "train" if time < validation_at else "validation" if time < test_at else "test"
        periods[row["user_id"]].add(period)
        entries.append((row, period))
    for row, period in entries:
        target = period if len(periods[row["user_id"]]) == 1 else "quarantine"
        features = {name: data for name, data in row["features"].items()
                    if data[1] <= row["booked_at"]}
        result[target].append({**row, "features": features})
    return result


if __name__ == "__main__":
    run_examples(split_bookings)
