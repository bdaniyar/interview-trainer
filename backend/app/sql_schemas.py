"""Public SQL DTOs. No executor/Docker/application persistence dependencies."""
from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class RequestModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SqlCreate(RequestModel):
    lesson_slug: str = Field(min_length=1, max_length=160)


class SqlGeneration(RequestModel):
    generation: int = Field(ge=1)


class SqlRun(SqlGeneration):
    sql: str = Field(min_length=1, max_length=32768)

    @field_validator("sql")
    @classmethod
    def sql_budget(cls, value):
        if "\x00" in value or len(value.encode("utf-8")) > 32768:
            raise ValueError("SQL exceeds UTF-8 budget or contains NUL")
        return value


class SqlLesson(BaseModel):
    lesson_id: str
    lesson_slug: str
    dataset_id: Literal["shop-v1"] = "shop-v1"
    task_id: str = "guided-select"
    task_revision: int = 1
    mode: Literal["lesson_read"] = "lesson_read"
    starter_sql: str
    prompt: str
    can_check: bool = False
    expected_columns: list[str] = Field(default_factory=list)
    completed: bool = False


class RunnerSession(BaseModel):
    session_id: str = Field(min_length=1, max_length=128)
    generation: int = Field(ge=1)
    dataset_id: Literal["shop-v1"]
    dataset_checksum: str = Field(pattern=r"^[a-f0-9]{64}$")
    postgres_major: Literal[17]
    created_at: datetime
    expires_at: datetime
    cold_start_ms: int = Field(ge=0)

    @field_validator("created_at", "expires_at")
    @classmethod
    def aware_time(cls, value):
        if value.utcoffset() is None:
            raise ValueError("Session timestamps require a timezone")
        return value


class SqlSession(RunnerSession):
    lesson_id: str
    lesson_slug: str
    task_id: str = "guided-select"


class SqlError(BaseModel):
    kind: Literal["policy", "postgres", "resource", "infrastructure"]
    code: str = Field(max_length=128)
    message: str = Field(max_length=2048)
    sqlstate: str | None = Field(default=None, max_length=5)
    position: int | None = Field(default=None, ge=1)
    hint: str | None = Field(default=None, max_length=512)


class SqlColumn(BaseModel):
    name: str = Field(max_length=128)
    pg_type: str = Field(max_length=128)
    type_oid: int


class SqlResult(BaseModel):
    session_id: str
    generation: int
    command: Literal["SELECT"]
    columns: list[SqlColumn] = Field(max_length=128)
    rows: list[list[str | bool | None]] = Field(max_length=500)
    rows_returned: int = Field(ge=0, le=500)
    has_more: bool
    truncated: bool
    duration_ms: int = Field(ge=0)
    error: SqlError | None = None
    session_closed: bool = False


class SqlCatalogColumn(BaseModel):
    name: str
    pg_type: str
    nullable: bool


class SqlForeignKey(BaseModel):
    name: str
    columns: list[str]
    referenced_table: str
    referenced_columns: list[str]
    on_update: str
    on_delete: str


class SqlTable(BaseModel):
    handle: str
    schema_name: Literal["lab"]
    name: str
    columns: list[SqlCatalogColumn]
    primary_key: list[str]
    foreign_keys: list[SqlForeignKey]


class SqlCatalog(BaseModel):
    session_id: str
    generation: int
    tables: list[SqlTable] = Field(max_length=4)


class SqlCheck(RequestModel):
    request_id: UUID
    sql: str = Field(min_length=1, max_length=32768)

    @field_validator("sql")
    @classmethod
    def sql_budget(cls, value):
        return SqlRun.sql_budget(value)


FeedbackCode = Literal["passed", "policy", "columns", "types", "rows", "sql_error", "timeout", "result_limit"]


class GradeFeedback(BaseModel):
    code: FeedbackCode
    sqlstate: str | None = Field(default=None, pattern=r"^[0-9A-Z]{5}$")


class RunnerGrade(BaseModel):
    task_id: str
    task_revision: int
    grader_revision: str
    dataset_checksum: str
    passed: bool = Field(strict=True)
    tests_passed: int = Field(ge=0, le=16, strict=True)
    tests_total: int = Field(ge=1, le=16, strict=True)
    feedback: list[GradeFeedback] = Field(min_length=1, max_length=4)

    @model_validator(mode="after")
    def coherent(self):
        if self.tests_passed > self.tests_total or self.passed != (self.tests_passed == self.tests_total):
            raise ValueError("Inconsistent grading summary")
        if self.passed != all(item.code == "passed" and item.sqlstate is None for item in self.feedback):
            raise ValueError("Inconsistent grading feedback")
        return self


class PublicFeedback(GradeFeedback):
    message: str = Field(max_length=300)


class SqlCheckResult(BaseModel):
    request_id: UUID
    task_id: str
    task_revision: int
    grader_revision: str
    passed: bool
    tests_passed: int
    tests_total: int
    completed: bool
    feedback: list[PublicFeedback]
