class AsyncRange:
    def __init__(self, start, stop):
        self.current, self.stop = start, stop
    def __aiter__(self):
        return self
    async def __anext__(self):
        if self.current >= self.stop:
            raise StopAsyncIteration
        value = self.current
        self.current += 1
        return value
