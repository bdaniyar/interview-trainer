from dataclasses import dataclass
import os
import re


SQL_BYTES = 32 * 1024
RESULT_BYTES = 1024 * 1024
CELL_BYTES = 64 * 1024
ROW_LIMIT = 500
STATEMENT_MS = 2000
LOCK_MS = 500
PYTHON = "/opt/sql-venv/bin/python"
LABEL = "org.pythoria.sql-runner"


@dataclass(frozen=True)
class Settings:
    image: str = "pythoria-sql-sandbox:phase1"
    namespace: str = "pythoria-sql-local"
    max_sessions: int = 2
    idle_seconds: float = 900
    absolute_seconds: int = 1800
    query_seconds: float = 5
    provision_seconds: float = 20
    reap_seconds: float = 30

    def __post_init__(self):
        if not re.fullmatch(r"[a-zA-Z0-9_-]{1,80}", self.namespace):
            raise ValueError("Invalid controller namespace")
        if not 1 <= self.max_sessions <= 2:
            raise ValueError("Local runner supports at most two sessions")
        if min(self.idle_seconds, self.absolute_seconds, self.query_seconds,
               self.provision_seconds, self.reap_seconds) <= 0:
            raise ValueError("Budgets must be positive")

    @classmethod
    def from_env(cls):
        return cls(image=os.getenv("SQL_SANDBOX_IMAGE", cls.image),
                   namespace=os.getenv("SQL_RUNNER_NAMESPACE", cls.namespace))
