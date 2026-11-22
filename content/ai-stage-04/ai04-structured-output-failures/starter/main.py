import asyncio
from fixtures import demo
async def recover(send,request,*,allow_repair=False):
    raise NotImplementedError
if __name__=="__main__":
    asyncio.run(demo(recover))
