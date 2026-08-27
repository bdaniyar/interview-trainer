class AsyncResource:
    def __init__(self, opener, closer):
        self.opener, self.closer, self.resource = opener, closer, None
    async def __aenter__(self):
        raise NotImplementedError
    async def __aexit__(self, exc_type, exc, traceback):
        raise NotImplementedError
