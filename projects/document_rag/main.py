"""FastAPI demo with typed DTOs and an injected, synthetic server actor."""
import os
from contextlib import asynccontextmanager
from typing import Annotated, Literal
from uuid import uuid4

import psycopg
from fastapi import Depends, FastAPI, Header, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

from projects.vector_search.contracts import AccessDenied, Actor, Source, VersionConflict

from .corpus_data import ACTORS, LOCAL_DSN, SPACE
from .retrieval import RetrievalStore
from .service import RagService
from .telemetry import INDEX_REVISION, MODEL_REVISION, PROMPT_REVISION


DocId = Annotated[str, StringConstraints(pattern=r"^[a-z0-9][a-z0-9-]{0,63}$")]
Text = Annotated[str, StringConstraints(min_length=1, max_length=16_000, pattern=r"\S")]
Method = Literal["fts", "dense", "hybrid", "rerank"]
Terminal = Literal["answered", "conflict", "insufficient_evidence", "stale_evidence", "unsupported",
                   "invalid_answer", "retrieval_error", "generation_error", "deadline", "context_budget"]
STATUS_CODES = {"stale_evidence": 409, "unsupported": 502, "invalid_answer": 502,
                "retrieval_error": 503, "generation_error": 502, "deadline": 504, "context_budget": 422}


class Strict(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")


class RevisionInput(Strict):
    version: int = Field(ge=1, le=2_147_483_647)
    markdown: Text

    @field_validator("markdown")
    @classmethod
    def valid_text(cls, value):
        value.encode()
        return value


class DocumentInput(RevisionInput):
    document_id: DocId


class ACLInput(Strict):
    subject: DocId
    enabled: bool


class Query(Strict):
    question: str = Field(min_length=1, max_length=600, pattern=r"\S")
    method: Method = "dense"
    limit: int = Field(default=6, ge=1, le=12)

    @field_validator("question")
    @classmethod
    def valid_question(cls, value):
        value.encode()
        return value


class Citation(Strict):
    document_id: str
    version: int
    chunk_id: str
    section: str
    start: int
    end: int

    @classmethod
    def from_source(cls, source: Source):
        return cls(document_id=source.document_id, version=source.version, chunk_id=source.chunk_id,
                   section=source.section, start=source.start, end=source.end)


class ClaimResult(Strict):
    text: str
    sources: tuple[Citation, ...]


class SearchResult(Strict):
    request_id: str
    method: Method
    sources: tuple[Citation, ...]
    index_revision: str = INDEX_REVISION
    embedding_revision: str = SPACE.revision


class AnswerResult(Strict):
    request_id: str
    status: Terminal
    method: Method
    answer: str | None
    claims: tuple[ClaimResult, ...]
    retrieved: int
    context_bytes: int
    model_revision: str = MODEL_REVISION
    prompt_revision: str = PROMPT_REVISION
    index_revision: str = INDEX_REVISION
    embedding_revision: str = SPACE.revision


class MutationResult(Strict):
    status: Literal["activated", "replayed", "deleted", "updated"]


def actor_from_header(x_demo_actor: Annotated[str | None, Header()] = None) -> Actor:
    actor = ACTORS.get(x_demo_actor)
    if actor is None:
        raise HTTPException(401, detail="authentication_required")
    return actor


def get_service(request: Request) -> RagService:
    return request.app.state.rag


Principal = Annotated[Actor, Depends(actor_from_header)]
Service = Annotated[RagService, Depends(get_service)]


def create_app(service: RagService | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app):
        instance = service if service is not None else RagService(
            RetrievalStore(os.environ.get("RAG_DSN", LOCAL_DSN))
        )
        app.state.rag = instance
        try:
            yield
        finally:
            instance.telemetry.provider.shutdown()

    app = FastAPI(title="Document Knowledge Assistant", lifespan=lifespan)

    @app.exception_handler(RequestValidationError)
    async def invalid_input(_request, _error):
        return JSONResponse({"detail": "invalid_input"}, status_code=422)

    @app.exception_handler(AccessDenied)
    async def no_access(_request, error):
        unavailable = str(error) == "document unavailable"
        return JSONResponse({"detail": "document_unavailable" if unavailable else "insufficient_scope"},
                            status_code=404 if unavailable else 403)

    @app.exception_handler(VersionConflict)
    async def conflict(_request, _error):
        return JSONResponse({"detail": "version_conflict"}, status_code=409)

    @app.exception_handler(psycopg.Error)
    async def storage_failure(_request, _error):
        return JSONResponse({"detail": "storage_unavailable"}, status_code=503)

    @app.exception_handler(ValueError)
    async def invalid_operation(_request, _error):
        return JSONResponse({"detail": "invalid_operation"}, status_code=422)

    @app.post("/documents", response_model=MutationResult)
    def create_document(payload: DocumentInput, principal: Principal, rag: Service):
        return MutationResult(status=rag.ingest(principal, payload.document_id, payload.version, payload.markdown))

    @app.post("/documents/{document_id}/versions", response_model=MutationResult)
    def new_version(document_id: DocId, payload: RevisionInput, principal: Principal, rag: Service):
        return MutationResult(status=rag.ingest(principal, document_id, payload.version, payload.markdown))

    @app.delete("/documents/{document_id}", response_model=MutationResult)
    def delete_document(document_id: DocId, principal: Principal, rag: Service):
        rag.store.delete(principal, document_id)
        return MutationResult(status="deleted")

    @app.post("/documents/{document_id}/acl", response_model=MutationResult)
    def acl(document_id: DocId, payload: ACLInput, principal: Principal, rag: Service):
        principal.require("share")
        if f"{principal.tenant}-{payload.subject}" not in ACTORS:
            raise HTTPException(404, detail="subject_unavailable")
        rag.store.grant(principal, document_id, payload.subject, payload.enabled)
        return MutationResult(status="updated")

    @app.post("/search")
    async def search(payload: Query, principal: Principal, rag: Service) -> SearchResult:
        request_id = uuid4().hex
        try:
            evidence = await rag.search(principal, payload.question, payload.method, payload.limit, request_id)
        except TimeoutError:
            raise HTTPException(504, detail="deadline") from None
        return SearchResult(method=payload.method, request_id=request_id,
                            sources=tuple(Citation.from_source(item.source) for item in evidence))

    @app.post("/ask")
    async def ask(payload: Query, principal: Principal, rag: Service, response: Response) -> AnswerResult:
        result = await rag.ask(principal, payload.question, payload.method, payload.limit)
        response.status_code = STATUS_CODES.get(result.status, 200)
        claims = tuple(ClaimResult(text=claim.text, sources=tuple(Citation.from_source(s) for s in claim.sources))
                       for claim in result.claims)
        return AnswerResult(request_id=result.request_id, status=result.status, method=payload.method,
                            answer="; ".join(claim.text for claim in claims) if claims else None,
                            claims=claims, retrieved=result.retrieved, context_bytes=result.context_bytes)

    return app


app = create_app()
