def compare_waits(delays):
    total = longest = 0
    for delay in delays:
        if delay < 0:
            raise ValueError("delay must be non-negative")
        total += delay
        longest = max(longest, delay)
    return total, longest
