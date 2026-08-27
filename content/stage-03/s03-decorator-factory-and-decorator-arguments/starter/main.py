from functools import wraps

def retry(attempts, exceptions=(Exception,), on_retry=None):
    raise NotImplementedError
