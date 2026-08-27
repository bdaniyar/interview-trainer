def parse_optional_int(value):
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        raise ValueError("invalid integer")
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("invalid integer") from exc
