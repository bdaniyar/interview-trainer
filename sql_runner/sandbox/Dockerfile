# PostgreSQL 17.11, pinned manifest digest; parser 7.x uses the PG17 grammar.
FROM postgres:17@sha256:748a18a54d3842d43bc156f0840d78029b8d349e0feca98c12b9c4ce3404a6b3
USER root
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-venv \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --uid 65532 --no-create-home --shell /usr/sbin/nologin student \
    && python3 -m venv /opt/sql-venv \
    && /opt/sql-venv/bin/pip install --no-cache-dir 'psycopg[binary]==3.3.3' 'pglast==7.22'
WORKDIR /opt/runner
COPY sql_runner/__init__.py ./sql_runner/__init__.py
COPY sql_runner/app ./sql_runner/app
COPY sql_runner/resources ./sql_runner/resources
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
USER postgres
ENTRYPOINT ["/opt/sql-venv/bin/python", "-m", "sql_runner.app.bootstrap"]
