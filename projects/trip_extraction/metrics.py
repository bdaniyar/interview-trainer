"""Pure scoring contract. The dataset labels come from reviewed synthetic cases."""
FIELDS = ("city", "check_in", "check_out", "guests")

METRICS = ("schema_validity", "domain_validity", "field_accuracy", "unknown_correctness",
           "exact_match", "refusal_handling", "outcome_accuracy")


def score(cases, outputs):
    """Return numerator, denominator, nullable rate and mismatches for a single partition."""
    counts = {name: [0, 0] for name in METRICS}

    def record(metric, passed):
        counts[metric][0] += int(passed)
        counts[metric][1] += 1

    errors = {}
    for case in cases:
        identifier = case["id"]
        if identifier in errors:
            raise ValueError("duplicate evaluation case")
        actual = outputs.get(identifier, {})
        issues = errors[identifier] = []
        expected_status = case["status"]
        actual_status = actual.get("status")
        record("outcome_accuracy", actual_status == expected_status)
        if actual_status != expected_status:
            issues.append("status")
        for metric, field in (("schema_validity", "schema_valid"), ("domain_validity", "domain_valid")):
            if actual.get(field) is not None:
                record(metric, actual[field] is True)
        if expected_status == "refusal":
            record("refusal_handling", actual_status == "refusal" and actual.get("trip") is None)
            if actual.get("trip") is not None:
                issues.append("refusal_payload")
        if (expected := case.get("trip")) is not None:
            observed = actual.get("trip")
            all_match = actual_status == expected_status
            for field in FIELDS:
                same = (
                    observed is not None and field in observed
                    and type(observed[field]) is type(expected[field])
                    and observed[field] == expected[field]
                )
                record("unknown_correctness" if expected[field] is None else "field_accuracy", same)
                if not same:
                    issues.append(field)
                    all_match = False
            record("exact_match", all_match)
        elif actual.get("trip") is not None and expected_status != "refusal":
            issues.append("unexpected_payload")

    report = {
        name: {"passed": passed, "total": total, "rate": passed / total if total else None}
        for name, (passed, total) in counts.items()
    }
    return {"metrics": report, "errors": errors}
