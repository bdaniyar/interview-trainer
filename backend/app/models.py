from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class UserState(Base):
    __tablename__ = "user_state"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    xp: Mapped[int] = mapped_column(Integer, default=0)
    last_opened_lesson: Mapped[str | None] = mapped_column(String(120), nullable=True)
    interview_index: Mapped[int] = mapped_column(Integer, default=0)
    theme: Mapped[str] = mapped_column(String(20), default="dark")


class LessonProgress(Base):
    __tablename__ = "lesson_progress"
    __table_args__ = (UniqueConstraint("lesson_slug", name="uq_progress_lesson"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lesson_slug: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="not_started")
    theory_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    task_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CodeFile(Base):
    __tablename__ = "code_files"
    __table_args__ = (UniqueConstraint("lesson_slug", "path", name="uq_code_lesson_path"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lesson_slug: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    path: Mapped[str] = mapped_column(String(240), nullable=False)
    content: Mapped[str] = mapped_column(Text, default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lesson_slug: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    kind: Mapped[str] = mapped_column(String(20), nullable=False)
    passed: Mapped[bool] = mapped_column(Boolean, default=False)
    tests_passed: Mapped[int] = mapped_column(Integer, default=0)
    tests_total: Mapped[int] = mapped_column(Integer, default=0)
    stdout: Mapped[str] = mapped_column(Text, default="")
    stderr: Mapped[str] = mapped_column(Text, default="")
    exit_code: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class InterviewProgress(Base):
    __tablename__ = "interview_progress"
    __table_args__ = (UniqueConstraint("question_id", name="uq_interview_question"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[str] = mapped_column(String(180), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=True)
    answer: Mapped[str] = mapped_column(Text, default="")
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
