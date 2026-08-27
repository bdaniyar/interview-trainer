def build_page_query(resource, /, *, limit=20, offset=0):
    if not resource or not 1 <= limit <= 100 or offset < 0:
        raise ValueError("invalid pagination")
    return {"resource": resource, "limit": limit, "offset": offset}
