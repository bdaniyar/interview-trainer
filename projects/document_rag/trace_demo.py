"""Capture actual local SDK spans for one synthetic lifecycle."""
import asyncio
import json
import os
from uuid import uuid4

from projects.vector_search.contracts import Actor

from .corpus_data import LOCAL_DSN, SCOPES
from .retrieval import RetrievalStore
from .service import RagService


async def main():
    service = RagService(RetrievalStore(os.environ.get("RAG_DSN", LOCAL_DSN)))
    suffix = uuid4().hex
    actor = Actor("north", "trace-" + suffix, SCOPES)
    try:
        service.ingest(actor, "trace-" + suffix, 1, "# Boat\n\nFact: boat = B3\n")
        answer = await service.ask(actor, "Boat berth?", method="rerank")
        assert answer.status == "answered"
        print(json.dumps(service.telemetry.snapshot(), ensure_ascii=False, indent=2))
    finally:
        service.telemetry.provider.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
