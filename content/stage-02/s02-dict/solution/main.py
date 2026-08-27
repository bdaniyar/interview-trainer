def index_by_id(records):
    result = {}
    for record in records:
        key = record["id"]
        if key in result:
            raise ValueError(f"duplicate id: {key}")
        result[key] = record
    return result
