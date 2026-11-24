"""Production-shaped orchestration over local, synthetic providers and PostgreSQL."""
import asyncio
from dataclasses import dataclass
from uuid import uuid4

from projects.vector_search.contracts import AccessDenied

from .chunking import prepare
from .citations import verdict
from .corpus_data import SPACE
from .pipeline import ContextBudget, context_for
from .retrieval import retrieve
from .scripted import batch, embed, generate, lexical_query, rerank_script
from .telemetry import INDEX_REVISION, MODEL_REVISION, PROMPT_REVISION, Telemetry, fail


@dataclass(frozen=True)
class Answer:
    request_id: str
    status: str
    method: str
    retrieved: int
    context_bytes: int = 0
    claims: tuple = ()


async def scripted_generation(context):
    return generate(context)


class RagService:
    def __init__(self, store, *, telemetry=None, embed_batch=batch, generate_draft=scripted_generation,
                 deadline=3.0):
        self.store = store
        self.telemetry = telemetry if telemetry is not None else Telemetry()
        self.embed_batch = embed_batch
        self.generate_draft = generate_draft
        self.deadline = deadline

    def ingest(self, actor, key, version, body):
        actor.require("ingest")
        with self.telemetry.span("ingest", embedding_revision=SPACE.revision,
                                 request_id=uuid4().hex, index_revision=INDEX_REVISION) as span:
            def traced_batch(texts):
                with self.telemetry.span("embed", count=len(texts), embedding_revision=SPACE.revision):
                    return self.embed_batch(texts)
            with self.telemetry.span("chunk", input_bytes=len(body.encode())) as tagging:
                chunks = prepare(key, version, body, traced_batch)
                tagging.set_attribute("chunks", len(chunks))
            result = self.store.ingest(actor, key, version, body, SPACE, chunks, expected_count=len(chunks))
            span.set_attribute("outcome", result)
            return result

    def _retrieve(self, actor, question, method, k):
        with self.telemetry.span("retrieve", method=method, index_revision=INDEX_REVISION) as span:
            def traced_embed(text):
                with self.telemetry.span("embed", count=1, embedding_revision=SPACE.revision):
                    return embed(text)
            evidence = retrieve(self.store, actor, question, SPACE, method=method, k=k, embed=traced_embed,
                                scorer=rerank_script, window=4, lexical_text=lexical_query(question),
                                step=self.telemetry.span)
            span.set_attribute("candidates", len(evidence))
            return evidence

    async def search(self, actor, question, method, k, request_id):
        actor.require("read")
        with self.telemetry.span("search", request_id=request_id, index_revision=INDEX_REVISION):
            async with asyncio.timeout(self.deadline):
                return await asyncio.to_thread(self._retrieve, actor, question, method, k)

    async def ask(self, actor, question, method="dense", k=6):
        actor.require("read")
        request_id = uuid4().hex
        retrieved = context_bytes = 0
        with self.telemetry.span("request", request_id=request_id, index_revision=INDEX_REVISION,
                                 model_revision=MODEL_REVISION, prompt_revision=PROMPT_REVISION) as root:
            def finish(status, claims=()):
                root.set_attribute("retrieved", retrieved)
                root.set_attribute("context_bytes", context_bytes)
                root.set_attribute("outcome", status)
                if status not in {"answered", "insufficient_evidence", "conflict"}:
                    fail(root, status)
                return Answer(request_id, status, method, retrieved, context_bytes, claims)

            try:
                async with asyncio.timeout(self.deadline):
                    try:
                        candidates = await asyncio.to_thread(self._retrieve, actor, question, method, k)
                        evidence = await asyncio.to_thread(
                            self.store.scoped_sources, actor, tuple(item.source for item in candidates),
                            SPACE, with_text=True,
                        )
                        retrieved = len(evidence)
                    except AccessDenied:
                        raise
                    except TimeoutError:
                        return finish("deadline")
                    except Exception:
                        return finish("retrieval_error")
                    try:
                        context = context_for(question, evidence)
                    except ContextBudget:
                        return finish("context_budget")
                    context_bytes = context.used_bytes
                    if not context.evidence:
                        return finish("insufficient_evidence")
                    with self.telemetry.span("generate", context_bytes=context_bytes,
                                             model_revision=MODEL_REVISION) as generation:
                        try:
                            draft = await self.generate_draft(context)
                        except TimeoutError:
                            fail(generation, "deadline")
                            return finish("deadline")
                        except Exception:
                            fail(generation, "generation_error")
                            return finish("generation_error")
                    with self.telemetry.span("validate", supplied=len(context.evidence)) as validation:
                        requested = tuple(item.source for item in context.evidence)
                        try:
                            current = await asyncio.to_thread(self.store.scoped_sources, actor, requested, SPACE)
                        except AccessDenied:
                            raise
                        except TimeoutError:
                            return finish("deadline")
                        except Exception:
                            fail(validation, "retrieval_error")
                            return finish("retrieval_error")
                        try:
                            status = ("stale_evidence" if current != requested
                                      else verdict(draft, context.evidence, frozenset(current), question=question))
                        except (TypeError, ValueError):
                            status = "invalid_answer"
                        validation.set_attribute("outcome", status)
                        if status not in {"answered", "insufficient_evidence", "conflict"}:
                            fail(validation, status)
                    return finish(status, draft.claims if status == "answered" else ())
            except TimeoutError:
                return finish("deadline")
