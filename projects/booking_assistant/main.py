"""Local FastAPI demo with server-mapped synthetic identities."""
from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from assistant import Assistant
from bookings import BookingRepository, Tools
from contracts import Budget, ChatInput, ChatResult, Principal, Provider, StrictModel
from history import ConversationBusy, ConversationUnavailable, History, InMemoryHistory
from providers import ScriptedProvider


DEMO_ACTORS = {
    "north-alice": Principal("north", "alice", frozenset({"booking:read", "booking:propose"})),
    "north-bob": Principal("north", "bob", frozenset({"booking:read"})),
    "south-alice": Principal("south", "alice", frozenset({"booking:read"})),
    "north-observer": Principal("north", "observer", frozenset()),
}
HTTP_STATUS = {
    "completed": 200, "refusal": 200, "incomplete": 200,
    "invalid_provider": 502, "provider_unavailable": 503, "deadline": 504,
    "step_budget": 429, "call_budget": 429, "output_budget": 429, "context_budget": 422,
}


class ConversationCreated(StrictModel):
    conversation_id: str


def demo_principal(x_demo_actor: Annotated[str | None, Header()] = None) -> Principal:
    principal = DEMO_ACTORS.get(x_demo_actor)
    if principal is None:
        raise HTTPException(401, detail="authentication_required")
    return principal


def get_assistant(request: Request) -> Assistant:
    return request.app.state.assistant


@asynccontextmanager
async def scripted_provider() -> AsyncIterator[Provider]:
    yield ScriptedProvider()


def create_app(
    *,
    repository: BookingRepository | None = None,
    history: History | None = None,
    budget: Budget = Budget(),
    provider_context: Callable[[], AbstractAsyncContextManager[Provider]] = scripted_provider,
) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app):
        async with provider_context() as provider:
            app.state.assistant = Assistant(
                provider, Tools(repository if repository is not None else BookingRepository()),
                history if history is not None else InMemoryHistory(), budget,
            )
            yield

    app = FastAPI(title="Controlled Booking Assistant", lifespan=lifespan)

    @app.exception_handler(RequestValidationError)
    async def validation_error(_request, _exc):
        return JSONResponse({"detail": "invalid_input"}, status_code=422)

    @app.post("/assistant/conversations", status_code=201)
    async def create_conversation(principal: Annotated[Principal, Depends(demo_principal)],
                                  service: Annotated[Assistant, Depends(get_assistant)]) -> ConversationCreated:
        return ConversationCreated(conversation_id=service.history.create(principal))

    @app.post("/assistant/chat", responses={code: {"model": ChatResult}
                                           for code in set(HTTP_STATUS.values()) - {200}})
    async def chat(request: ChatInput, response: Response,
                   principal: Annotated[Principal, Depends(demo_principal)],
                   service: Annotated[Assistant, Depends(get_assistant)]) -> ChatResult:
        try:
            result = await service.chat(principal, request)
        except ConversationUnavailable:
            raise HTTPException(404, detail="conversation_unavailable") from None
        except ConversationBusy:
            raise HTTPException(409, detail="conversation_busy") from None
        response.status_code = HTTP_STATUS[result.reason]
        return result

    return app


app = create_app()
