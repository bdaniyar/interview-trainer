FROM ghcr.io/astral-sh/uv:0.11.24@sha256:99ea34acedc870ba4ad11a1f540a1c04267c9f30aadc465a94406f52dfda2c36 AS installer
FROM python:3.12.13-slim-bookworm@sha256:4766d8b510c428e595d74b9cc5bbb2fae8e26316fffb4adc89908d79aacd58a2
WORKDIR /app
COPY projects/document_rag/requirements.txt /tmp/requirements.txt
RUN --mount=from=installer,source=/uv,target=/bin/uv \
    uv pip sync --system --require-hashes --no-cache /tmp/requirements.txt
COPY projects/vector_search /app/projects/vector_search
COPY projects/document_rag /app/projects/document_rag
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
USER 65532:65532
CMD ["python","-m","uvicorn","projects.document_rag.main:app","--host","0.0.0.0","--port","8000"]
