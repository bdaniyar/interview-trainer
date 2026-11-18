ARG INDEX_BASE=pythoria-sql-sandbox:phase1
FROM ${INDEX_BASE}
USER root
COPY index_lab /opt/runner/index_lab
USER postgres
ENTRYPOINT ["/opt/sql-venv/bin/python", "-m", "index_lab.bootstrap"]
