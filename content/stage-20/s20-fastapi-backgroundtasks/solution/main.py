from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, Field

class EventBody(BaseModel):
    value: str = Field(min_length=1, max_length=20)

def make_app(sink):
    app = FastAPI()
    @app.post('/events', status_code=202)
    def event(body: EventBody, tasks: BackgroundTasks):
        tasks.add_task(sink, body.value)
        return {'accepted': True}
    return app
