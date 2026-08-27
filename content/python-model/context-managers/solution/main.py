class Transaction:
    def __init__(self, resource):
        self.resource = resource

    def __enter__(self):
        return self.resource

    def __exit__(self, exc_type, exc, traceback):
        if exc_type is None:
            self.resource.commit()
        else:
            self.resource.rollback()
        return False
