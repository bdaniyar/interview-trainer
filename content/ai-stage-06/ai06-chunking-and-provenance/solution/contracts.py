from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    document_id: str
    version: int
    chunk_id: str
    page: int
    section: str | None
    start: int
    end: int
    text: str
    digest: str
