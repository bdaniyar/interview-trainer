def make_counter(start=0, step=1):
    current = start
    def next_value():
        nonlocal current
        current += step
        return current
    return next_value
