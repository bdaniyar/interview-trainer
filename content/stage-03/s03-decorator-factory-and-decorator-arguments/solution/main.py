from functools import wraps

def retry(attempts, exceptions=(Exception,), on_retry=None):
    if attempts < 1:
        raise ValueError("attempts must be positive")
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            for attempt in range(1, attempts + 1):
                try:
                    return function(*args, **kwargs)
                except exceptions:
                    if attempt == attempts:
                        raise
                    if on_retry:
                        on_retry(attempt)
        return wrapper
    return decorator
