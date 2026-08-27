def batched(iterable, size):
    if size <= 0:
        raise ValueError("size must be positive")
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch
