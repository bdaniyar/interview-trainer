"""Add deterministic Python and asyncio interview tasks to course lessons."""

from __future__ import annotations

try:
    from .curated_content import preserve_bundle
except ImportError:  # direct script execution
    from curated_content import preserve_bundle

import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"


@dataclass(frozen=True)
class Task:
    number: str
    title: str
    prompt: str
    starter: str
    solution: str
    tests: str
    skills: tuple[str, ...]


CORE_TASKS = [
    Task(
        "1.5", "Не потерять нулевой limit",
        "Верни default только для None. Целое значение от 0 до 100 сохрани; bool и остальные значения отклони через ValueError.",
        """def normalize_limit(value, default=20):
    raise NotImplementedError
""",
        """def normalize_limit(value, default=20):
    if value is None:
        return default
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 100:
        raise ValueError("limit must be an integer from 0 to 100")
    return value
""",
        """import pytest
from main import normalize_limit

def test_none_uses_default(): assert normalize_limit(None, 30) == 30
def test_zero_is_not_missing(): assert normalize_limit(0) == 0
def test_boundaries(): assert (normalize_limit(1), normalize_limit(100)) == (1, 100)
@pytest.mark.parametrize("value", [-1, 101, True, "10"])
def test_invalid(value):
    with pytest.raises(ValueError): normalize_limit(value)
""", ("truthiness", "validation"),
    ),
    Task(
        "1.7", "Изолировать вложенный payload",
        "Верни независимую глубокую копию payload. Мутация вложенных list/dict результата не должна менять оригинал.",
        """def clone_payload(payload):
    raise NotImplementedError
""",
        """from copy import deepcopy

def clone_payload(payload):
    return deepcopy(payload)
""",
        """from main import clone_payload

def test_nested_state_is_isolated():
    source = {"user": {"roles": ["reader"]}}
    result = clone_payload(source)
    assert result == source and result is not source
    result["user"]["roles"].append("writer")
    assert source == {"user": {"roles": ["reader"]}}
""", ("copy", "references"),
    ),
    Task(
        "2.3", "Индекс без тихих дублей",
        "Построй dict записей по id. Повторный id должен вызвать ValueError; входной list не изменяй.",
        """def index_by_id(records):
    raise NotImplementedError
""",
        """def index_by_id(records):
    result = {}
    for record in records:
        key = record["id"]
        if key in result:
            raise ValueError(f"duplicate id: {key}")
        result[key] = record
    return result
""",
        """import pytest
from main import index_by_id

def test_builds_index():
    rows = [{"id": 2}, {"id": 1}]
    assert index_by_id(rows) == {2: rows[0], 1: rows[1]}
def test_duplicate():
    with pytest.raises(ValueError, match="duplicate id: 1"):
        index_by_id([{"id": 1}, {"id": 1}])
def test_empty(): assert index_by_id([]) == {}
""", ("dict", "data-integrity"),
    ),
    Task(
        "2.4", "Нормализовать scopes",
        "Верни frozenset непустых scopes в lower-case без пробелов и дублей.",
        """def normalize_scopes(scopes):
    raise NotImplementedError
""",
        """def normalize_scopes(scopes):
    return frozenset(scope.strip().lower() for scope in scopes if scope.strip())
""",
        """from main import normalize_scopes

def test_normalizes(): assert normalize_scopes([" Read ", "WRITE", "read"]) == frozenset({"read", "write"})
def test_empty_values(): assert normalize_scopes(["", "  "]) == frozenset()
def test_immutable(): assert isinstance(normalize_scopes(["read"]), frozenset)
""", ("set", "normalization"),
    ),
    Task(
        "2.6", "Email активных пользователей",
        "Верни lower-case email активных пользователей с непустым email. Не изменяй вход.",
        """def active_emails(users):
    raise NotImplementedError
""",
        """def active_emails(users):
    return [
        user["email"].strip().lower()
        for user in users
        if user.get("active") and user.get("email", "").strip()
    ]
""",
        """from main import active_emails

def test_filters_and_normalizes():
    users = [
        {"active": True, "email": " A@EXAMPLE.COM "},
        {"active": False, "email": "b@example.com"},
        {"active": True},
    ]
    assert active_emails(users) == ["a@example.com"]
""", ("comprehension", "backend-transform"),
    ),
    Task(
        "2.7", "Стабильно отсортировать события",
        "Верни новый list событий по created_at по убыванию. Равные timestamps сохрани в исходном порядке.",
        """def sort_events(events):
    raise NotImplementedError
""",
        """def sort_events(events):
    return sorted(events, key=lambda event: event["created_at"], reverse=True)
""",
        """from main import sort_events

def test_descending_and_stable():
    rows = [
        {"id": "a", "created_at": 2}, {"id": "b", "created_at": 3},
        {"id": "c", "created_at": 3}, {"id": "d", "created_at": 1},
    ]
    result = sort_events(rows)
    assert [row["id"] for row in result] == ["b", "c", "a", "d"]
    assert result is not rows and [row["id"] for row in rows] == ["a", "b", "c", "d"]
""", ("sorting", "stability"),
    ),
    Task(
        "3.3", "Явная сигнатура pagination helper",
        "Реализуй build_page_query: resource positional-only; limit и offset keyword-only. Проверь resource, limit 1..100 и offset >= 0.",
        """def build_page_query(resource, /, *, limit=20, offset=0):
    raise NotImplementedError
""",
        """def build_page_query(resource, /, *, limit=20, offset=0):
    if not resource or not 1 <= limit <= 100 or offset < 0:
        raise ValueError("invalid pagination")
    return {"resource": resource, "limit": limit, "offset": offset}
""",
        """import inspect
import pytest
from main import build_page_query

def test_contract():
    assert build_page_query("users", limit=10, offset=5) == {"resource": "users", "limit": 10, "offset": 5}
def test_signature():
    kinds = [p.kind for p in inspect.signature(build_page_query).parameters.values()]
    assert kinds == [inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.KEYWORD_ONLY]
def test_invalid():
    with pytest.raises(ValueError): build_page_query("users", limit=0)
""", ("signature", "api-design"),
    ),
    Task(
        "3.5", "Объединить options",
        "Объедини base и keyword overrides, где overrides побеждают. Не изменяй входной dict.",
        """def merge_options(base, **overrides):
    raise NotImplementedError
""",
        """def merge_options(base, **overrides):
    return {**base, **overrides}
""",
        """from main import merge_options

def test_override(): assert merge_options({"limit": 20, "active": True}, limit=5) == {"limit": 5, "active": True}
def test_no_mutation():
    base = {"limit": 20}
    result = merge_options(base, offset=3)
    assert base == {"limit": 20} and result is not base
""", ("kwargs", "immutability"),
    ),
    Task(
        "3.9", "Stateful closure",
        "Верни next_value closure: начальное состояние start; каждый вызов увеличивает его на step и возвращает новое значение.",
        """def make_counter(start=0, step=1):
    raise NotImplementedError
""",
        """def make_counter(start=0, step=1):
    current = start
    def next_value():
        nonlocal current
        current += step
        return current
    return next_value
""",
        """from main import make_counter

def test_state():
    counter = make_counter(10, 2)
    assert [counter(), counter(), counter()] == [12, 14, 16]
def test_independent():
    first, second = make_counter(), make_counter(100)
    assert first() == 1 and second() == 101 and first() == 2
""", ("closure", "nonlocal"),
    ),
    Task(
        "3.10", "Исправить late binding",
        "Верни функции, каждая умножает аргумент на собственный multiplier из входа.",
        """def make_multipliers(multipliers):
    raise NotImplementedError
""",
        """def make_multipliers(multipliers):
    return [lambda value, factor=factor: value * factor for factor in multipliers]
""",
        """from main import make_multipliers

def test_captures_each_value():
    functions = make_multipliers([2, 3, 5])
    assert [function(4) for function in functions] == [8, 12, 20]
def test_empty(): assert make_multipliers([]) == []
""", ("late-binding", "closure"),
    ),
    Task(
        "3.11", "Decorator проверки роли",
        "Реализуй require_role(role). Первый аргумент wrapped-функции — user с roles; иначе PermissionError. Сохрани metadata.",
        """from functools import wraps

def require_role(role):
    raise NotImplementedError
""",
        """from functools import wraps

def require_role(role):
    def decorator(function):
        @wraps(function)
        def wrapper(user, *args, **kwargs):
            if role not in user.roles:
                raise PermissionError(f"missing role: {role}")
            return function(user, *args, **kwargs)
        return wrapper
    return decorator
""",
        """from dataclasses import dataclass
import pytest
from main import require_role

@dataclass
class User: roles: set[str]

@require_role("admin")
def delete(user, item_id): return item_id

def test_allows(): assert delete(User({"admin"}), 7) == 7
def test_denies():
    with pytest.raises(PermissionError): delete(User({"reader"}), 7)
def test_metadata(): assert delete.__name__ == "delete"
""", ("decorator", "authorization"),
    ),
    Task(
        "3.12", "Сохранить metadata wrapper",
        "Реализуй traced decorator через functools.wraps и добавь wrapper.traced = True.",
        """from functools import wraps

def traced(function):
    raise NotImplementedError
""",
        """from functools import wraps

def traced(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return function(*args, **kwargs)
    wrapper.traced = True
    return wrapper
""",
        """import inspect
from main import traced

@traced
def add(left: int, right: int = 1) -> int:
    "Add values."
    return left + right

def test_behavior(): assert add(2, right=3) == 5
def test_metadata():
    assert add.__name__ == "add" and add.__doc__ == "Add values."
    assert str(inspect.signature(add)) == "(left: int, right: int = 1) -> int"
def test_marker(): assert add.traced is True
""", ("functools.wraps", "introspection"),
    ),
    Task(
        "3.13", "Retry decorator",
        "Реализуй retry(attempts, exceptions, on_retry). Повторяй только указанные errors, вызови hook перед retry и подними последнюю ошибку.",
        """from functools import wraps

def retry(attempts, exceptions=(Exception,), on_retry=None):
    raise NotImplementedError
""",
        """from functools import wraps

def retry(attempts, exceptions=(Exception,), on_retry=None):
    if attempts < 1:
        raise ValueError("attempts must be positive")
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            for attempt in range(1, attempts + 1):
                try:
                    return function(*args, **kwargs)
                except exceptions:
                    if attempt == attempts:
                        raise
                    if on_retry:
                        on_retry(attempt)
        return wrapper
    return decorator
""",
        """import pytest
from main import retry

def test_retry_then_success():
    retries = []
    @retry(3, (ValueError,), retries.append)
    def work():
        if len(retries) < 2: raise ValueError("temporary")
        return "ok"
    assert work() == "ok" and retries == [1, 2]
def test_last_error():
    @retry(2, (ValueError,))
    def work(): raise ValueError("boom")
    with pytest.raises(ValueError, match="boom"): work()
def test_permanent_not_retried():
    @retry(3, (ValueError,))
    def work(): raise TypeError("bad")
    with pytest.raises(TypeError): work()
""", ("decorator-factory", "retry"),
    ),
    Task(
        "4.1", "Лениво взять первый элемент",
        "Верни первый элемент iterable либо default, не материализуя весь iterable.",
        """def first_or_default(iterable, default=None):
    raise NotImplementedError
""",
        """def first_or_default(iterable, default=None):
    return next(iter(iterable), default)
""",
        """from main import first_or_default

def test_list(): assert first_or_default([3, 4]) == 3
def test_lazy():
    touched = []
    def values():
        touched.append(1); yield "first"
        touched.append(2); yield "second"
    assert first_or_default(values()) == "first" and touched == [1]
def test_empty(): assert first_or_default(iter(()), "none") == "none"
""", ("iterable", "lazy"),
    ),
    Task(
        "4.8", "Разобрать optional integer",
        "None и пустая строка дают None; str/int преобразуются в int; bool и мусор дают ValueError с explicit cause.",
        """def parse_optional_int(value):
    raise NotImplementedError
""",
        """def parse_optional_int(value):
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        raise ValueError("invalid integer")
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("invalid integer") from exc
""",
        """import pytest
from main import parse_optional_int

@pytest.mark.parametrize(("value", "expected"), [(None, None), ("", None), ("42", 42), (-3, -3)])
def test_values(value, expected): assert parse_optional_int(value) == expected
@pytest.mark.parametrize("value", [True, "4.2", object()])
def test_invalid(value):
    with pytest.raises(ValueError): parse_optional_int(value)
""", ("exceptions", "input-validation"),
    ),
    Task(
        "4.12", "Transaction context manager",
        "Создай Transaction: enter возвращает resource; success вызывает commit, error — rollback; исключение не подавляется.",
        """class Transaction:
    def __init__(self, resource):
        self.resource = resource

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc, traceback):
        raise NotImplementedError
""",
        """class Transaction:
    def __init__(self, resource):
        self.resource = resource

    def __enter__(self):
        return self.resource

    def __exit__(self, exc_type, exc, traceback):
        if exc_type is None:
            self.resource.commit()
        else:
            self.resource.rollback()
        return False
""",
        """import pytest
from main import Transaction

class Resource:
    def __init__(self): self.calls = []
    def commit(self): self.calls.append("commit")
    def rollback(self): self.calls.append("rollback")

def test_commit():
    resource = Resource()
    with Transaction(resource) as value: assert value is resource
    assert resource.calls == ["commit"]
def test_rollback():
    resource = Resource()
    with pytest.raises(RuntimeError):
        with Transaction(resource): raise RuntimeError("boom")
    assert resource.calls == ["rollback"]
""", ("context-manager", "transaction"),
    ),
    Task(
        "5.4", "Создать User из mapping",
        "Реализуй staticmethod normalize_email и classmethod from_mapping. Поддержи subclass и проверь positive id/non-empty email.",
        """class User:
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email

    @staticmethod
    def normalize_email(value):
        raise NotImplementedError

    @classmethod
    def from_mapping(cls, payload):
        raise NotImplementedError
""",
        """class User:
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email

    @staticmethod
    def normalize_email(value):
        return value.strip().lower()

    @classmethod
    def from_mapping(cls, payload):
        user_id = payload["id"]
        email = cls.normalize_email(payload["email"])
        if user_id <= 0 or not email:
            raise ValueError("invalid user")
        return cls(user_id, email)
""",
        """import pytest
from main import User

def test_subclass_and_normalization():
    class Admin(User): pass
    value = Admin.from_mapping({"id": 7, "email": " A@Example.COM "})
    assert isinstance(value, Admin) and (value.user_id, value.email) == (7, "a@example.com")
def test_invalid():
    with pytest.raises(ValueError): User.from_mapping({"id": 0, "email": "a@x.io"})
""", ("classmethod", "staticmethod"),
    ),
    Task(
        "5.10", "Immutable BookingWindow",
        "Создай frozen slots dataclass BookingWindow(start,end); end строго больше start; duration возвращает разницу.",
        """from dataclasses import dataclass

# Реализуй BookingWindow.
""",
        """from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BookingWindow:
    start: int
    end: int

    def __post_init__(self):
        if self.end <= self.start:
            raise ValueError("end must be after start")

    @property
    def duration(self):
        return self.end - self.start
""",
        """from dataclasses import FrozenInstanceError
import pytest
from main import BookingWindow

def test_contract(): assert BookingWindow(10, 15).duration == 5
def test_validation():
    with pytest.raises(ValueError): BookingWindow(10, 10)
def test_frozen_slots():
    value = BookingWindow(1, 2)
    with pytest.raises((FrozenInstanceError, AttributeError)): value.start = 0
    assert not hasattr(value, "__dict__")
""", ("dataclass", "value-object"),
    ),
]


# Stage 8 task bundles are authored and reviewed in content/ (including the
# saved-submission compatibility tests for 8.1). Never rebuild them from a
# second, stale Python catalog.
ASYNC_TASKS: list[Task] = []


def indexes() -> tuple[dict[str, dict], dict[str, Path]]:
    curriculum = json.loads((CONTENT / "curriculum.json").read_text(encoding="utf-8"))
    lessons = {lesson["number"]: lesson for stage in curriculum["stages"] for lesson in stage["lessons"]}
    directories = {}
    for path in CONTENT.glob("*/*/metadata.json"):
        metadata = json.loads(path.read_text(encoding="utf-8"))
        directories[metadata["slug"]] = path.parent
    return lessons, directories


def replace_task(markdown: str, task: Task) -> str:
    section = (
        f"## Задача\n\n### {task.title}\n\n{task.prompt}\n\n"
        "Работай в main.py. Не меняй публичные имена и сигнатуры: скрытые тесты импортируют их напрямую. "
        "Проверь основной сценарий, граничные значения, повторные вызовы и распространение ошибок."
    )
    return re.sub(r"## Задача\n.*?(?=\n## Шпаргалка)", section, markdown, flags=re.DOTALL)


def write_task(task: Task, lesson: dict, directory: Path) -> None:
    if preserve_bundle(directory):
        return
    for folder, content in (("starter", task.starter), ("solution", task.solution)):
        target = directory / folder
        target.mkdir(exist_ok=True)
        (target / "main.py").write_text(content.rstrip() + "\n", encoding="utf-8")
    tests = directory / "tests"
    tests.mkdir(exist_ok=True)
    (tests / "test_main.py").write_text(task.tests.rstrip() + "\n", encoding="utf-8")
    metadata_path = directory / "metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata.update({
        "has_task": True,
        "has_solution": True,
        "xp": 25,
        "task_id": f"{lesson['id']}.practice",
        "task_title": task.title,
        "task_difficulty": "interview",
        "task_skills": list(task.skills),
        "task_estimated_minutes": 20,
    })
    metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lesson_path = directory / "lesson.md"
    lesson_path.write_text(replace_task(lesson_path.read_text(encoding="utf-8"), task), encoding="utf-8")


def main() -> None:
    lessons, directories = indexes()
    tasks = CORE_TASKS + ASYNC_TASKS
    if len({task.number for task in tasks}) != len(tasks):
        raise RuntimeError("duplicate task number")
    for task in tasks:
        lesson = lessons[task.number]
        write_task(task, lesson, directories[lesson["implementation_slug"]])
    print("Task catalog checked; existing bundles preserved. Stage 8 tasks are authored in content/.")


if __name__ == "__main__":
    main()
