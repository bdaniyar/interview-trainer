import asyncio
from fixtures import Result, demo, validate_trip

async def recover(send,request,*,allow_repair=False):
    for attempt in (1,2):
        try:
            outcome=await send(request,repair=attempt==2)
        except TimeoutError:
            return Result("timeout",request.correlation_id,attempt)
        if outcome.kind=="completed":
            try:
                trip=validate_trip(outcome.trip)
            except ValueError:
                return Result("invalid_domain",request.correlation_id,attempt)
            status="needs_clarification" if any(v is None for v in trip.values()) else "completed"
            return Result(status,request.correlation_id,attempt,trip)
        if attempt==2 or not allow_repair or outcome.kind not in {"incomplete","malformed","retryable"}:
            return Result(outcome.kind,request.correlation_id,attempt)
if __name__=="__main__":
    asyncio.run(demo(recover))
