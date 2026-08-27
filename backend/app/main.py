from __future__ import annotations

import shlex
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from .content import content_repo
from .database import Base, SessionLocal, engine, get_db
from .models import Attempt, CodeFile, InterviewProgress, LessonProgress, UserState
from .runner_client import execute_in_runner
from .schemas import FilesPayload, InterviewAnswerPayload, PreferencesPayload, RunPayload, TerminalPayload, TheoryPayload


def get_state(db: Session) -> UserState:
    state = db.get(UserState, 1)
    if state is None:
        state = UserState(id=1)
        db.add(state)
        db.flush()
    return state


def get_progress(db: Session, slug: str) -> LessonProgress:
    progress = db.scalar(select(LessonProgress).where(LessonProgress.lesson_slug == slug))
    if progress is None:
        progress = LessonProgress(lesson_slug=slug)
        db.add(progress)
        db.flush()
    return progress


def saved_files(db: Session, slug: str) -> dict[str, str]:
    rows = db.scalars(select(CodeFile).where(CodeFile.lesson_slug == slug)).all()
    return {row.path: row.content for row in rows}


def persist_files(db: Session, slug: str, files: dict[str, str]) -> None:
    existing = {row.path: row for row in db.scalars(select(CodeFile).where(CodeFile.lesson_slug == slug)).all()}
    for path, row in existing.items():
        if path not in files:
            db.delete(row)
    for path, content in files.items():
        row = existing.get(path)
        if row:
            row.content = content
        else:
            db.add(CodeFile(lesson_slug=slug, path=path, content=content))


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        get_state(db)
        db.commit()
    yield


app = FastAPI(title="Pythoria API", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "backend"}


@app.get("/api/course")
def get_course(db: Session = Depends(get_db)):
    modules = content_repo.modules()
    progress_rows = {row.lesson_slug: row for row in db.scalars(select(LessonProgress)).all()}
    completed = 0
    for module in modules:
        for lesson in module["lessons"]:
            progress = progress_rows.get(lesson["slug"])
            lesson["status"] = progress.status if progress else "not_started"
            lesson["theory_completed"] = progress.theory_completed if progress else False
            lesson["task_completed"] = progress.task_completed if progress else False
            completed += int(bool(progress and progress.status == "completed"))
    state = get_state(db)
    total = sum(len(module["lessons"]) for module in modules)
    return {
        "title": "Python Backend Interview Trainer",
        "modules": modules,
        "summary": {
            "total": total,
            "completed": completed,
            "percent": round(completed / total * 100) if total else 0,
            "xp": state.xp,
            "last_opened_lesson": state.last_opened_lesson or modules[0]["lessons"][0]["slug"],
            "theme": state.theme,
        },
    }


@app.get("/api/lessons/{slug}")
def get_lesson(slug: str, db: Session = Depends(get_db)):
    lesson = content_repo.lesson(slug)
    files = saved_files(db, slug) or content_repo.starter_files(slug)
    progress = get_progress(db, slug)
    db.commit()
    return {
        **lesson,
        "files": files,
        "progress": {
            "status": progress.status,
            "theory_completed": progress.theory_completed,
            "task_completed": progress.task_completed,
        },
    }


@app.post("/api/lessons/{slug}/open")
def open_lesson(slug: str, db: Session = Depends(get_db)):
    content_repo.lesson(slug)
    progress = get_progress(db, slug)
    if progress.status == "not_started":
        progress.status = "in_progress"
    state = get_state(db)
    state.last_opened_lesson = slug
    db.commit()
    return {"status": progress.status}


@app.put("/api/lessons/{slug}/files")
def save_lesson_files(slug: str, payload: FilesPayload, db: Session = Depends(get_db)):
    content_repo.lesson(slug)
    persist_files(db, slug, payload.files)
    db.commit()
    return {"saved": True, "files": len(payload.files)}


@app.post("/api/run")
async def run_code(payload: RunPayload, db: Session = Depends(get_db)):
    content_repo.lesson(payload.lesson_slug)
    if payload.entrypoint not in payload.files or not payload.entrypoint.endswith(".py"):
        raise HTTPException(status_code=400, detail="Выбери существующий Python-файл")
    persist_files(db, payload.lesson_slug, payload.files)
    result = await execute_in_runner(
        {"mode": "run", "files": payload.files, "command": ["python", payload.entrypoint]}
    )
    db.add(
        Attempt(
            lesson_slug=payload.lesson_slug,
            kind="run",
            passed=result["exit_code"] == 0,
            stdout=result.get("stdout", ""),
            stderr=result.get("stderr", ""),
            exit_code=result["exit_code"],
        )
    )
    db.commit()
    return result


@app.post("/api/check")
async def check_code(payload: RunPayload, db: Session = Depends(get_db)):
    lesson = content_repo.lesson(payload.lesson_slug)
    if not lesson["has_task"]:
        raise HTTPException(status_code=409, detail="Задача для этого урока пока не добавлена")
    tests = content_repo.hidden_tests(payload.lesson_slug)
    if not tests:
        raise HTTPException(status_code=409, detail="Hidden tests пока не добавлены")
    persist_files(db, payload.lesson_slug, payload.files)
    result = await execute_in_runner(
        {
            "mode": "check",
            "files": payload.files,
            "tests": tests,
            "command": ["pytest", "-v", "--tb=short", "-p", "no:cacheprovider", "tests"],
        }
    )
    passed = result["exit_code"] == 0 and result.get("tests_total", 0) > 0
    progress = get_progress(db, payload.lesson_slug)
    state = get_state(db)
    xp_awarded = 0
    if passed and not progress.task_completed:
        progress.task_completed = True
        progress.status = "completed"
        state.xp += 20
        xp_awarded = 20
    elif not passed and progress.status == "not_started":
        progress.status = "in_progress"
    db.add(
        Attempt(
            lesson_slug=payload.lesson_slug,
            kind="check",
            passed=passed,
            tests_passed=result.get("tests_passed", 0),
            tests_total=result.get("tests_total", 0),
            stdout=result.get("stdout", ""),
            stderr=result.get("stderr", ""),
            exit_code=result["exit_code"],
        )
    )
    db.commit()
    return {**result, "passed": passed, "xp_awarded": xp_awarded, "xp": state.xp}


@app.post("/api/terminal")
async def terminal(payload: TerminalPayload, db: Session = Depends(get_db)):
    persist_files(db, payload.lesson_slug, payload.files)
    db.commit()
    try:
        parts = shlex.split(payload.command)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Некорректная команда") from exc
    if not parts:
        return {"stdout": "", "stderr": "", "exit_code": 0, "duration_ms": 0, "timed_out": False}
    if parts[0] == "pwd" and len(parts) == 1:
        return {"stdout": "/workspace\n", "stderr": "", "exit_code": 0, "duration_ms": 0, "timed_out": False}
    if parts[0] == "ls" and len(parts) == 1:
        return {"stdout": "\n".join(sorted(payload.files)) + "\n", "stderr": "", "exit_code": 0, "duration_ms": 0, "timed_out": False}
    if parts[0] == "python" and len(parts) == 2 and parts[1] in payload.files and parts[1].endswith(".py"):
        command = parts
    elif parts == ["pytest"]:
        command = ["pytest", "-q", "-p", "no:cacheprovider"]
    else:
        raise HTTPException(status_code=400, detail="Разрешены: python <file.py>, pytest, ls, pwd, clear")
    return await execute_in_runner({"mode": "terminal", "files": payload.files, "command": command})


@app.post("/api/progress/{slug}/theory")
def complete_theory(slug: str, payload: TheoryPayload, db: Session = Depends(get_db)):
    content_repo.lesson(slug)
    progress = get_progress(db, slug)
    state = get_state(db)
    xp_awarded = 0
    if payload.completed and not progress.theory_completed:
        progress.theory_completed = True
        if progress.status == "not_started":
            progress.status = "in_progress"
        state.xp += 5
        xp_awarded = 5
    db.commit()
    return {"theory_completed": progress.theory_completed, "xp_awarded": xp_awarded, "xp": state.xp}


@app.get("/api/lessons/{slug}/solution")
def get_solution(slug: str):
    return {"files": content_repo.solution_files(slug)}


@app.get("/api/interview")
def interview(set_slug: str | None = None, db: Session = Depends(get_db)):
    catalog = content_repo.interview_sets()
    active_set = set_slug or catalog.get("default_set") or None
    questions = content_repo.interview_questions(active_set)
    completed = {row.question_id for row in db.scalars(select(InterviewProgress)).all()}
    state = get_state(db)
    return {
        "questions": [{**item, "completed": item["id"] in completed} for item in questions],
        "current_index": min(state.interview_index, max(0, len(questions) - 1)),
        "sets": catalog.get("sets", []),
        "active_set": active_set,
    }


@app.post("/api/interview/complete")
def complete_interview(payload: InterviewAnswerPayload, db: Session = Depends(get_db)):
    valid_ids = {item["id"] for item in content_repo.interview_questions()}
    if payload.question_id not in valid_ids:
        raise HTTPException(status_code=404, detail="Вопрос не найден")
    row = db.scalar(select(InterviewProgress).where(InterviewProgress.question_id == payload.question_id))
    state = get_state(db)
    xp_awarded = 0
    if row is None:
        db.add(InterviewProgress(question_id=payload.question_id, answer=payload.answer))
        state.xp += 5
        xp_awarded = 5
    else:
        row.answer = payload.answer
    db.commit()
    return {"completed": True, "xp_awarded": xp_awarded, "xp": state.xp}


@app.put("/api/preferences")
def preferences(payload: PreferencesPayload, db: Session = Depends(get_db)):
    state = get_state(db)
    state.theme = payload.theme
    db.commit()
    return {"theme": state.theme}
