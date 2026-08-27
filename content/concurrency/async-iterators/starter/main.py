class AsyncRange:
    def __init__(self, start, stop):
        self.current, self.stop = start, stop
    def __aiter__(self):
        raise NotImplementedError
    async def __anext__(self):
        raise NotImplementedError
