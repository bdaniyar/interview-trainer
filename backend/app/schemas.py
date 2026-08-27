from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


ALLOWED_SUFFIXES = {".py", ".txt", ".json", ".md", ".toml", ".yaml", ".yml"}


class FilesPayload(BaseModel):
    files: dict[str, str] = Field(default_factory=dict)

    @field_validator("files")
    @classmethod
    def validate_files(cls, files: dict[str, str]) -> dict[str, str]:
        if not files or len(files) > 24:
            raise ValueError("Должно быть от 1 до 24 файлов")
        total = 0
        for path, content in files.items():
            parts = path.replace("\\", "/").split("/")
            if not path or path.startswith("/") or ".." in parts or any(not part for part in parts):
                raise ValueError(f"Недопустимый путь: {path}")
            suffix = "." + path.rsplit(".", 1)[-1].lower() if "." in path else ""
            if suffix not in ALLOWED_SUFFIXES:
                raise ValueError(f"Недопустимый тип файла: {path}")
            encoded = len(content.encode("utf-8"))
            if encoded > 100_000:
                raise ValueError(f"Файл слишком большой: {path}")
            total += encoded
        if total > 500_000:
            raise ValueError("Проект слишком большой")
        return files


class RunPayload(FilesPayload):
    lesson_slug: str
    entrypoint: str = "main.py"


class TerminalPayload(FilesPayload):
    lesson_slug: str
    command: str


class TheoryPayload(BaseModel):
    completed: bool = True


class PreferencesPayload(BaseModel):
    theme: str

    @field_validator("theme")
    @classmethod
    def validate_theme(cls, value: str) -> str:
        if value not in {"dark", "light"}:
            raise ValueError("theme must be dark or light")
        return value


class InterviewAnswerPayload(BaseModel):
    question_id: str
    answer: str = ""

    model_config = ConfigDict(str_strip_whitespace=True)
