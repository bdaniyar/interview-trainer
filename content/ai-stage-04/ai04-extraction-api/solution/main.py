import asyncio
import re
from datetime import date
from typing import Annotated
from uuid import uuid4

from fastapi import Depends,FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel,ConfigDict,Field,ValidationError,field_validator,model_validator
from fixtures import PROMPT_VERSION,SCHEMA_VERSION,ProviderFailure,demo

class Query(BaseModel):
    model_config=ConfigDict(extra="forbid",str_strip_whitespace=True)
    text:Annotated[str,Field(strict=True,min_length=1,max_length=500)]

class Trip(BaseModel):
    model_config=ConfigDict(extra="forbid",str_strip_whitespace=True)
    city:Annotated[str,Field(strict=True,min_length=1)]|None
    check_in:date|None
    check_out:date|None
    guests:Annotated[int,Field(strict=True,gt=0)]|None

    @field_validator("check_in","check_out",mode="before")
    @classmethod
    def full_date(cls,value):
        if value is None:
            return None
        if isinstance(value,str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}",value):
            return date.fromisoformat(value)
        raise ValueError("exact date required")

    @model_validator(mode="after")
    def order(self):
        if self.check_in and self.check_out and self.check_in>=self.check_out:
            raise ValueError("invalid dates")
        return self

class Reply(BaseModel):
    request_id:str
    status:str
    trip:Trip|None=None
    model:str
    prompt_version:str=PROMPT_VERSION
    schema_version:str=SCHEMA_VERSION
    category:str|None=None

def create_app(provider,*,timeout=0.5):
    app=FastAPI()
    def dependency():
        return provider
    def reply(state,request_id,model,trip=None):
        return Reply(request_id=request_id,model=model,status=state,trip=trip,
                     category=None if state=="completed" else state)
    def failure(state,http,request_id,model):
        return JSONResponse(reply(state,request_id,model).model_dump(mode="json"),status_code=http)
    @app.exception_handler(RequestValidationError)
    async def invalid(request,exc):
        return failure("invalid_request",422,str(uuid4()),provider.identity)
    @app.post("/extract-trip",response_model=Reply)
    async def extract(query:Query,client=Depends(dependency)):
        request_id=str(uuid4())
        try:
            async with asyncio.timeout(timeout):
                raw=await client.extract(query.text)
        except TimeoutError:
            return failure("timeout",504,request_id,client.identity)
        except ProviderFailure:
            return failure("unavailable",503,request_id,client.identity)
        if raw.status in {"refusal","incomplete"}:
            return reply(raw.status,request_id,client.identity)
        if raw.status!="completed":
            return failure("invalid_trip",502,request_id,client.identity)
        try:
            trip=Trip.model_validate(raw.data)
        except ValidationError:
            return failure("invalid_trip",502,request_id,client.identity)
        status="needs_clarification" if any(v is None for v in trip.model_dump().values()) else "completed"
        return reply(status,request_id,client.identity,trip)
    return app
if __name__=="__main__":
    demo(create_app)
