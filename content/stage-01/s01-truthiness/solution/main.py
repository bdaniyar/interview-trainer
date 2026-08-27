def normalize_limit(value, default=20):
    if value is None:
        return default
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 100:
        raise ValueError("limit must be an integer from 0 to 100")
    return value
