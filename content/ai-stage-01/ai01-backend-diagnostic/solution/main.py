import asyncio

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from demo import exercise


class Question(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    question: str = Field(min_length=1, max_length=240)
    conversation_id: int = Field(gt=0, strict=True)


class Answer(BaseModel):
    conversation_id: int
    text: str


def create_app(actor, owners, provider, timeout=0.5) -> FastAPI:
    app = FastAPI()
    ownership = dict(owners)

    def get_provider():
        return provider

    @app.post("/chat", response_model=Answer)
    async def chat(query: Question, generator=Depends(get_provider)):
        if ownership.get(query.conversation_id) != actor:
            raise HTTPException(404, "Беседа не найдена")
        try:
            async with asyncio.timeout(timeout):
                reply = await generator.generate(query.question, query.conversation_id)
        except TimeoutError:
            raise HTTPException(504, "Время ожидания истекло") from None
        return Answer(conversation_id=query.conversation_id, text=reply)

    return app


if __name__ == "__main__":
    exercise(create_app)
