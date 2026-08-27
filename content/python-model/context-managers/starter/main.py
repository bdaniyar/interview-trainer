class Transaction:
    def __init__(self, resource):
        self.resource = resource

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc, traceback):
        raise NotImplementedError
