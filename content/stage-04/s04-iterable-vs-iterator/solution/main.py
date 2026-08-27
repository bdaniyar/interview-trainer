def first_or_default(iterable, default=None):
    return next(iter(iterable), default)
