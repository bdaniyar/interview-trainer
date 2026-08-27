FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
RUN pip install --no-cache-dir \
        pytest==8.4.1 \
        fastapi==0.116.1 \
        httpx==0.28.1 \
        pydantic==2.11.7 \
        sqlalchemy==2.0.43 \
        alembic==1.19.1 \
    && groupadd --gid 65532 sandbox \
    && useradd --uid 65532 --gid 65532 --no-create-home --shell /usr/sbin/nologin sandbox \
    && mkdir /workspace \
    && chown sandbox:sandbox /workspace
WORKDIR /workspace
USER 65532:65532

CMD ["python", "--version"]
