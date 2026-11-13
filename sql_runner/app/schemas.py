from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CreateSession(StrictModel):
    dataset_id: Literal["shop-v1"] = "shop-v1"


class Generation(StrictModel):
    generation: int = Field(ge=1)


class Run(Generation):
    sql: str = Field(min_length=1, max_length=32768)


class SessionInfo(StrictModel):
    session_id: str
    generation: int
    dataset_id: str
    dataset_checksum: str
    postgres_major: Literal[17] = 17
    created_at: datetime
    expires_at: datetime
    cold_start_ms: int


class Error(StrictModel):
    kind: Literal["policy", "postgres", "resource", "infrastructure"]
    code: str
    message: str
    sqlstate: str | None = None
    position: int | None = None
    hint: str | None = None


class Column(StrictModel):
    name: str
    pg_type: str
    type_oid: int


class Result(StrictModel):
    session_id: str | None = None
    generation: int | None = None
    command: Literal["SELECT"] = "SELECT"
    columns: list[Column] = Field(default_factory=list)
    rows: list[list[str | bool | None]] = Field(default_factory=list)
    rows_returned: int = 0
    has_more: bool = False
    truncated: bool = False
    duration_ms: int = 0
    error: Error | None = None


class CatalogColumn(StrictModel):
    name: str
    pg_type: str
    nullable: bool


class ForeignKey(StrictModel):
    name: str
    columns: list[str]
    referenced_table: str
    referenced_columns: list[str]
    on_update: str
    on_delete: str


class Table(StrictModel):
    handle: str
    schema_name: Literal["lab"] = "lab"
    name: str
    columns: list[CatalogColumn]
    primary_key: list[str]
    foreign_keys: list[ForeignKey]


class Catalog(StrictModel):
    session_id: str
    generation: int
    tables: list[Table]


class CheckRequest(StrictModel):
    task_id: str = Field(min_length=1, max_length=180)
    task_revision: int = Field(ge=1, strict=True)
    grader_revision: str = Field(min_length=1, max_length=80)
    sql: str = Field(min_length=1, max_length=32768)


class CheckFeedback(StrictModel):
    code: Literal["passed", "policy", "columns", "types", "rows", "sql_error", "timeout", "result_limit"]
    sqlstate: str | None = Field(default=None, pattern=r"^[0-9A-Z]{5}$")


class CheckResult(StrictModel):
    task_id: str
    task_revision: int
    grader_revision: str
    dataset_checksum: str
    passed: bool
    tests_passed: int = Field(ge=0, le=16)
    tests_total: int = Field(ge=1, le=16)
    feedback: list[CheckFeedback] = Field(min_length=1, max_length=4)
