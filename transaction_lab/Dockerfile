FROM pythoria-sql-sandbox:phase1
USER root
COPY transaction_lab /opt/runner/transaction_lab
USER postgres
ENTRYPOINT ["/opt/sql-venv/bin/python","-m","transaction_lab.bootstrap"]
