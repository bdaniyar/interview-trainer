"""Create the local course tree without overwriting manually imported lessons."""

from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

MODULES = [
    (
        "python-model",
        "Модель Python и продвинутый ООП",
        [
            ("python-basics", "Устройство Python: базовая теория", ["objects", "namespaces", "MRO", "descriptors"]),
            ("is-vs-eq", "is vs ==", ["identity", "equality", "hashing"]),
            ("mutability-references", "Mutability and references", ["references", "mutable objects", "aliasing"]),
            ("data-model", "Data model и спецметоды", ["dunder methods", "protocols"]),
            ("iterator-protocol", "Iterator protocol", ["Iterable", "Iterator", "StopIteration"]),
            ("generators", "Generators", ["yield", "lazy evaluation", "generator expressions"]),
            ("context-managers", "Контекстные менеджеры", ["with", "__enter__", "__exit__"]),
            ("descriptors", "Дескрипторы в прикладном коде", ["__get__", "__set__", "property"]),
            ("metaclasses", "Метаклассы и __init_subclass__", ["type", "metaclass", "__init_subclass__"]),
        ],
    ),
    (
        "functions-api",
        "Функции, типизация и API",
        [
            ("functions-as-objects", "Functions as objects", ["callable", "first-class functions"]),
            ("legb", "LEGB", ["local", "enclosing", "global", "builtins"]),
            ("positional-only", "positional-only arguments", ["/", "signature"]),
            ("keyword-only", "keyword-only arguments", ["*", "signature"]),
            ("args-kwargs", "*args и **kwargs", ["packing", "unpacking"]),
            ("closures", "closures", ["free variables", "nonlocal"]),
            ("late-binding", "late binding", ["closures", "binding time"]),
            ("mutable-default-arguments", "Mutable default arguments", ["defaults", "sentinel", "None"]),
            ("decorators", "decorators", ["higher-order functions", "wrapping"]),
            ("functools-wraps", "functools.wraps", ["metadata", "__wrapped__"]),
            ("signatures", "signatures", ["inspect.signature", "parameters"]),
            ("annotations", "annotations", ["__annotations__", "typing"]),
            ("dataclasses", "dataclasses", ["field", "frozen", "slots"]),
            ("advanced-typing", "advanced typing", ["Union", "Literal", "overload"]),
            ("generic", "Generic", ["TypeVar", "generic classes"]),
            ("protocol", "Protocol", ["structural typing", "runtime_checkable"]),
            ("typeddict", "TypedDict", ["mapping shapes", "NotRequired"]),
        ],
    ),
    (
        "memory-performance",
        "Память, производительность и отладка",
        [
            ("references", "References", ["identity", "aliasing"]),
            ("object-lifetime", "Object lifetime", ["lifetime", "finalization"]),
            ("reference-counting", "Reference counting", ["sys.getrefcount", "CPython"]),
            ("cyclic-gc", "Cyclic garbage collector", ["cycles", "generations"]),
            ("gc-module", "gc", ["gc.collect", "gc.get_objects"]),
            ("weak-references", "weak references", ["weakref", "WeakValueDictionary"]),
            ("copying", "shallow copy и deep copy", ["copy", "deepcopy"]),
            ("profiling", "profiling", ["cProfile", "timeit"]),
            ("memory-profiling", "memory profiling", ["tracemalloc", "allocation"]),
        ],
    ),
    (
        "concurrency",
        "Конкурентность и асинхронность",
        [
            ("gil", "GIL", ["bytecode", "CPU-bound"]),
            ("threads", "threads", ["threading", "I/O-bound"]),
            ("processes", "processes", ["multiprocessing", "IPC"]),
            ("race-conditions", "race conditions", ["shared state", "atomicity"]),
            ("locks", "locks", ["Lock", "RLock"]),
            ("thread-pool", "ThreadPoolExecutor", ["Future", "Executor"]),
            ("process-pool", "ProcessPoolExecutor", ["pickle", "workers"]),
            ("coroutine", "coroutine", ["coroutine object", "awaitable"]),
            ("event-loop", "event loop", ["scheduling", "callbacks"]),
            ("async-await", "async / await", ["async def", "await"]),
            ("tasks", "tasks", ["create_task", "Task"]),
            ("gather", "gather", ["concurrent await", "exceptions"]),
            ("cancellation", "cancellation", ["CancelledError", "timeout"]),
            ("async-iterators", "async iterators", ["__aiter__", "__anext__"]),
            ("async-generators", "async generators", ["async yield", "aclose"]),
            ("async-context-managers", "async context managers", ["__aenter__", "__aexit__"]),
            ("asyncio-practice", "Asyncio: практика и backpressure", ["Queue", "Semaphore", "backpressure"]),
        ],
    ),
    (
        "reliability",
        "Надёжность, тесты и архитектура",
        [
            ("exceptions", "exceptions", ["try", "except", "finally"]),
            ("custom-exceptions", "custom exceptions", ["exception hierarchy", "domain errors"]),
            ("exception-chaining", "exception chaining", ["__context__", "__cause__"]),
            ("raise-from", "raise from", ["explicit cause", "traceback"]),
            ("pytest", "pytest", ["assert rewriting", "discovery"]),
            ("fixtures", "fixtures", ["scope", "yield fixtures"]),
            ("parametrization", "parametrization", ["pytest.mark.parametrize", "cases"]),
            ("mocks", "mocks", ["Mock", "patch", "autospec"]),
            ("async-testing", "async testing", ["pytest-asyncio", "event loop"]),
            ("dependency-injection", "dependency injection", ["dependencies", "inversion of control"]),
            ("inheritance-composition", "inheritance vs composition", ["delegation", "coupling"]),
            ("architecture-basics", "architecture basics", ["layers", "boundaries"]),
            ("package-design", "Архитектура пакетов и модулей", ["imports", "public API"]),
            ("contracts", "Контракты, фейки и интеграционные тесты", ["contracts", "fakes"]),
            ("backend-core-project", "Мини-проект: ядро backend-сервиса", ["service layer", "repository"]),
        ],
    ),
]

WORKING = {
    "python-basics": {
        "description": "Объекты, пространства имён, data model, MRO, дескрипторы и метаклассы.",
        "markdown": r'''# Устройство Python

Добро пожаловать в курс Python для опытных разработчиков. Здесь мы не учимся писать `if` и `for` — мы разбираем, почему Python ведёт себя именно так, и как использовать это в реальном backend-коде.

На платформе можно читать теорию и сразу применять её на практике, редактировать файлы в браузере, запускать решение и проверять его тестами.

## Как Python смотрит на объекты

В Python почти всё — объекты: числа, строки, функции, классы и даже сами классы классов.

```python
message = "Learn with Pythoria"
```

Переменная `message` не хранит строку внутри себя. Она связывает имя с объектом строки.

```python
a = [1, 2]
b = a  # b ссылается на тот же список
b.append(3)

print(a)  # [1, 2, 3]
print(b)  # [1, 2, 3]
```

> [!NOTE]
> Имя связывается с объектом, а не «копирует значение» автоматически.

## Пространства имён

Пространство имён хранит соответствие между именем и объектом. Чаще всего встречаются локальное пространство функции, глобальное пространство модуля и встроенное пространство.

```python
title = "Backend powers the world"

def show():
    title = "Coding is magic"
    print(title)

show()
print(title)
```

## Mutability и immutability

`list`, `dict`, `set` изменяемы; `int`, `str`, `tuple` обычно неизменяемы.

| Тип | Изменяемость | Хешируемость |
| --- | --- | --- |
| `list` | да | нет |
| `dict` | да | нет |
| `str` | нет | да |
| `tuple` | нет | зависит от элементов |

## Data model и dunder-методы

Когда ты пишешь `len(obj)`, `print(obj)` или `obj[0]`, Python использует протоколы data model и специальные методы.

```python
class LessonBox:
    def __init__(self, topic):
        self.topic = topic

    def __repr__(self):
        return f"LessonBox(topic={self.topic!r})"

    def __str__(self):
        return f"Урок: {self.topic}"
```

## MRO и поиск атрибутов

MRO определяет порядок поиска методов при наследовании. Для `class D(B, C)` Python пройдёт цепочку `D -> B -> C -> A -> object` согласно C3-линеаризации.

## Дескрипторы

Дескриптор управляет доступом к атрибуту через `__get__`, `__set__` и `__delete__`. На этой идее построены `property`, методы и многие ORM.

## Метаклассы

Обычный объект создаётся классом, а класс обычно создаётся метаклассом `type`.

```python
class Event:
    pass

print(type(Event))    # <class 'type'>
print(type(Event()))  # <class '__main__.Event'>
```

## Задача

В `main.py` создай класс `MagicBox`:

- конструктор принимает строку `text`;
- `__str__` возвращает `Message: <text>`;
- `__repr__` возвращает `MagicBox(text='<text>')`;
- `__len__` возвращает длину `text`;
- `__bool__` возвращает `False` для пустой строки, иначе `True`.

Создай объекты `filled = MagicBox("Coding is magic")` и `empty = MagicBox("")`, затем переменные `filled_str`, `filled_repr`, `filled_len`, `filled_bool`, `empty_bool`. Ничего не печатай: тесты проверят переменные модуля.
''',
        "starter": '''class MagicBox:
    """Объект сообщения с поддержкой стандартных протоколов Python."""

    # Реализуй класс здесь
    pass


filled = MagicBox("Coding is magic")
empty = MagicBox("")

# Запиши результаты в переменные ниже
filled_str = None
filled_repr = None
filled_len = None
filled_bool = None
empty_bool = None
''',
        "solution": '''class MagicBox:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return f"Message: {self.text}"

    def __repr__(self):
        return f"MagicBox(text={self.text!r})"

    def __len__(self):
        return len(self.text)

    def __bool__(self):
        return bool(self.text)


filled = MagicBox("Coding is magic")
empty = MagicBox("")
filled_str = str(filled)
filled_repr = repr(filled)
filled_len = len(filled)
filled_bool = bool(filled)
empty_bool = bool(empty)
''',
        "tests": '''import main


def test_magic_box_protocols():
    box = main.MagicBox("hello")
    assert str(box) == "Message: hello"
    assert repr(box) == "MagicBox(text='hello')"
    assert len(box) == 5
    assert bool(box) is True


def test_empty_box_is_falsy():
    assert bool(main.MagicBox("")) is False


def test_required_module_values():
    assert main.filled_str == "Message: Coding is magic"
    assert main.filled_repr == "MagicBox(text='Coding is magic')"
    assert main.filled_len == 15
    assert main.filled_bool is True
    assert main.empty_bool is False
''',
        "interview": [
            {"question": "Почему присваивание b = a не копирует список?", "answer": ["Имена a и b связываются с одним объектом", "Мутация видна через обе ссылки", "Для копии нужен явный copy/deepcopy"]},
            {"question": "Что определяет MRO?", "answer": ["Порядок поиска атрибутов", "Используется C3-линеаризация", "Особенно важен при множественном наследовании"]},
        ],
    },
    "is-vs-eq": {
        "description": "Идентичность объектов, равенство значений и контракт __eq__.",
        "markdown": '''# `is` vs `==`

`is` отвечает на вопрос «это один и тот же объект?», а `==` — «считаются ли значения равными?». Эти операции нельзя взаимозаменять.

```python
a = [1, 2]
b = [1, 2]
c = a

print(a == b)  # True
print(a is b)  # False
print(a is c)  # True
```

## Почему `is None` — правильно

`None` — singleton: в процессе существует один объект `None`. Проверка идентичности не вызывает пользовательский `__eq__` и точно выражает намерение.

> [!WARNING]
> Не полагайся на интернирование строк и малых целых: это деталь реализации, а не контракт задачи.

## Задача

Реализуй `compare_objects(left, right)`, которая возвращает словарь с ключами `same_identity` и `same_value`.
''',
        "starter": '''def compare_objects(left, right):
    """Верни признаки идентичности и равенства объектов."""
    pass
''',
        "solution": '''def compare_objects(left, right):
    return {"same_identity": left is right, "same_value": left == right}
''',
        "tests": '''from main import compare_objects


def test_same_object():
    value = [1]
    assert compare_objects(value, value) == {"same_identity": True, "same_value": True}


def test_equal_distinct_objects():
    assert compare_objects([1], [1]) == {"same_identity": False, "same_value": True}


def test_different_values():
    assert compare_objects([1], [2]) == {"same_identity": False, "same_value": False}
''',
        "interview": [{"question": "Когда использовать is вместо ==?", "answer": ["Для singleton-объектов, прежде всего None", "Когда важна именно идентичность", "is не вызывает __eq__"]}],
    },
    "mutability-references": {
        "description": "Алиасинг, мутации и безопасная работа с изменяемыми данными.",
        "markdown": '''# Mutability and references

Переменные в Python — имена, связанные с объектами. Если два имени ссылаются на изменяемый объект, мутация наблюдается через обе ссылки.

```python
original = {"roles": ["reader"]}
alias = original
alias["roles"].append("writer")
assert original["roles"] == ["reader", "writer"]
```

Переприсваивание имени не меняет прежний объект, а связывает имя с новым. Мутация, напротив, сохраняет identity объекта.

## Задача

Реализуй `append_marker(items, marker)`: добавь marker в переданный список и верни **тот же** список. Не создавай копию.
''',
        "starter": '''def append_marker(items, marker):
    """Добавь marker и верни исходный объект items."""
    pass
''',
        "solution": '''def append_marker(items, marker):
    items.append(marker)
    return items
''',
        "tests": '''from main import append_marker


def test_mutates_original():
    items = [1, 2]
    append_marker(items, 3)
    assert items == [1, 2, 3]


def test_returns_same_object():
    items = []
    result = append_marker(items, "x")
    assert result is items


def test_accepts_any_marker():
    marker = {"ready": True}
    items = []
    assert append_marker(items, marker) == [marker]
''',
        "interview": [
            {"question": "Чем мутация отличается от переприсваивания?", "answer": ["Мутация меняет состояние существующего объекта", "Переприсваивание связывает имя с другим объектом", "Алиасы видят мутацию, но не переприсваивание имени"]},
            {"question": "Что будет выведено и почему?", "code": "a = []\nb = a\n\nb.append(1)\n\nprint(a)", "expected": "[1]", "reason": "a и b содержат ссылки на один объект list.", "answer": ["Будет выведено [1]", "Присваивание b = a не создаёт копию", "append изменяет общий объект списка"]},
        ],
    },
    "mutable-default-arguments": {
        "description": "Время вычисления default-значений и безопасный sentinel-паттерн.",
        "markdown": '''# Mutable default arguments

Значения параметров по умолчанию вычисляются один раз — при выполнении `def`. Поэтому список в сигнатуре сохраняется между вызовами.

```python
def broken(value, bucket=[]):
    bucket.append(value)
    return bucket
```

Используй `None` как sentinel и создавай новый список внутри вызова.

## Задача

Реализуй `add_tag(tag, tags=None)`. Функция возвращает список с добавленным тегом. Вызовы без `tags` не должны делить состояние; переданный список нужно изменить на месте.
''',
        "starter": '''def add_tag(tag, tags=None):
    """Добавь tag без утечки состояния между вызовами."""
    pass
''',
        "solution": '''def add_tag(tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags
''',
        "tests": '''from main import add_tag


def test_calls_do_not_share_state():
    assert add_tag("python") == ["python"]
    assert add_tag("backend") == ["backend"]


def test_mutates_explicit_list():
    tags = ["api"]
    result = add_tag("async", tags)
    assert result is tags
    assert tags == ["api", "async"]


def test_signature_default_is_safe():
    assert add_tag.__defaults__ == (None,)
''',
        "interview": [{"question": "Когда вычисляются default arguments?", "answer": ["Один раз при выполнении def", "Объект хранится в function.__defaults__", "Для нового mutable-объекта на вызов используют None/sentinel"]}],
    },
    "iterator-protocol": {
        "description": "Iterable, iterator, __iter__, __next__ и StopIteration.",
        "markdown": '''# Iterator protocol

Iterable возвращает iterator из `__iter__`. Iterator хранит состояние обхода, возвращает себя из `__iter__` и выдаёт элементы через `__next__`. Когда элементы закончились, он поднимает `StopIteration`.

```python
iterator = iter([10, 20])
next(iterator)  # 10
next(iterator)  # 20
```

Цикл `for` скрывает эти вызовы, но использует тот же протокол.

## Задача

Создай iterator-класс `Countdown(start)`, который выдаёт числа от `start` до `1`. После окончания каждый следующий `next()` должен поднимать `StopIteration`.
''',
        "starter": '''class Countdown:
    def __init__(self, start):
        # Сохрани состояние итератора
        pass

    def __iter__(self):
        pass

    def __next__(self):
        pass
''',
        "solution": '''class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value
''',
        "tests": '''import pytest
from main import Countdown


def test_iterator_protocol():
    countdown = Countdown(3)
    assert iter(countdown) is countdown


def test_iteration_order():
    assert list(Countdown(4)) == [4, 3, 2, 1]


def test_stop_iteration_is_stable():
    countdown = Countdown(1)
    assert next(countdown) == 1
    with pytest.raises(StopIteration):
        next(countdown)
    with pytest.raises(StopIteration):
        next(countdown)


def test_empty_input():
    assert list(Countdown(0)) == []
''',
        "interview": [{"question": "В чём разница между iterable и iterator?", "answer": ["Iterable создаёт iterator через __iter__", "Iterator хранит состояние обхода и реализует __next__", "Iterator обычно возвращает self из __iter__"]}],
    },
    "generators": {
        "description": "yield, ленивые последовательности и корректная работа с потоком.",
        "markdown": '''# Generators

Функция с `yield` возвращает generator object. Её выполнение приостанавливается между значениями, поэтому весь результат не нужно держать в памяти.

```python
def squares(limit):
    for value in range(limit):
        yield value ** 2
```

Генератор одноразовый: после исчерпания продолжить его нельзя. Для нового обхода вызови generator-функцию заново.

## Задача

Реализуй генератор `batched(iterable, size)`, который лениво группирует элементы в списки размера `size`. Последняя группа может быть короче. При `size <= 0` подними `ValueError`.
''',
        "starter": '''def batched(iterable, size):
    """Лениво группируй элементы iterable в списки."""
    pass
''',
        "solution": '''def batched(iterable, size):
    if size <= 0:
        raise ValueError("size must be positive")
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch
''',
        "tests": '''import inspect
import pytest
from main import batched


def test_is_generator_function():
    assert inspect.isgeneratorfunction(batched)


def test_groups_values():
    assert list(batched(range(5), 2)) == [[0, 1], [2, 3], [4]]


def test_is_lazy():
    seen = []
    source = (seen.append(i) or i for i in range(5))
    result = batched(source, 2)
    assert seen == []
    assert next(result) == [0, 1]
    assert seen == [0, 1]


def test_rejects_invalid_size():
    with pytest.raises(ValueError):
        next(batched([1], 0))
''',
        "interview": [{"question": "Почему генератор экономит память?", "answer": ["Вычисляет значения по требованию", "Хранит состояние выполнения, а не весь результат", "Подходит для больших и бесконечных потоков"]}],
    },
}


def placeholder_markdown(title: str, topics: list[str]) -> str:
    bullets = "\n".join(f"- `{topic}`" for topic in topics)
    return f"""# {title}

Материал урока пока не добавлен. Структура уже готова для будущего импорта.

## Что нужно изучить

{bullets}

> [!NOTE]
> Пришли материал с заголовками `TOPIC:` и `MATERIAL:` — он будет встроен в этот урок без создания дубля.

## Задача

Задача и hidden tests будут добавлены позже.
"""


def write(path: Path, value: str, force: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if force or not path.exists():
        path.write_text(value, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="overwrite generated lesson files")
    args = parser.parse_args()
    order = 0
    catalog = []
    for module_index, (module_slug, module_title, lessons) in enumerate(MODULES, start=1):
        module_item = {"slug": module_slug, "title": module_title, "order": module_index, "lessons": []}
        for slug, title, topics in lessons:
            order += 1
            lesson_dir = CONTENT / module_slug / slug
            working = WORKING.get(slug)
            metadata = {
                "slug": slug,
                "title": title,
                "module_slug": module_slug,
                "module_title": module_title,
                "order": order,
                "duration": 18 + order % 13,
                "xp": 25 if working else 5,
                "topics": topics,
                "description": working["description"] if working else f"Учебный блок: {', '.join(topics)}.",
                "has_task": bool(working),
                "has_solution": bool(working),
            }
            write(lesson_dir / "metadata.json", json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", args.force)
            write(lesson_dir / "lesson.md", textwrap.dedent(working["markdown"] if working else placeholder_markdown(title, topics)).strip() + "\n", args.force)
            starter = working["starter"] if working else f'''"""Заготовка для урока: {title}."""\n\n\ndef main():\n    raise NotImplementedError("Задача будет добавлена позже")\n'''
            write(lesson_dir / "starter" / "main.py", textwrap.dedent(starter).lstrip(), args.force)
            if working:
                write(lesson_dir / "tests" / "test_main.py", textwrap.dedent(working["tests"]).lstrip(), args.force)
                write(lesson_dir / "solution" / "main.py", textwrap.dedent(working["solution"]).lstrip(), args.force)
                write(lesson_dir / "interview.json", json.dumps(working["interview"], ensure_ascii=False, indent=2) + "\n", args.force)
            module_item["lessons"].append(metadata)
        catalog.append(module_item)
    write(CONTENT / "course.json", json.dumps({"title": "Python для опытных разработчиков", "lessons_count": order, "modules": catalog}, ensure_ascii=False, indent=2) + "\n", args.force)
    print(f"Seeded {order} lessons in {CONTENT}")


if __name__ == "__main__":
    main()
