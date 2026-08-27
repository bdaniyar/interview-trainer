class AsyncResource:
    def __init__(self, opener, closer):
        self.opener, self.closer, self.resource = opener, closer, None
    async def __aenter__(self):
        self.resource = await self.opener()
        return self.resource
    async def __aexit__(self, exc_type, exc, traceback):
        await self.closer(self.resource)
        return False
