"""Replace stage-wide examples with lesson-specific examples.

The original population script intentionally stays lightweight. This pass runs
after tasks and practice banks are built, so it can reuse a lesson's own code
prediction, starter contract, SQL exercise, or diagnostic scenario. Core Python
lessons use curated examples because those concepts need exact runtime behavior,
not a generic stage-level snippet.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

try:
    from .learning_materials import russianize_prose
except ImportError:  # direct `python tools/personalize_examples.py` execution
    from learning_materials import russianize_prose


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

# language, source, explanation. These are intentionally keyed by lesson number:
# adjacent lessons must demonstrate different mechanics rather than share a stage
# example with renamed variables.
CURATED: dict[str, tuple[str, str, str]] = {
    "0.1": ("text", "Вопрос: почему `is` и `==` дают разные ответы?\nПлан ответа: определение → механизм → пример → ограничение\nДополнительный вопрос: что изменит собственный `__eq__`?", "Диагностика проверяет не угадывание термина, а структуру объяснения и готовность к дополнительному вопросу."),
    "0.2": ("text", "Определение: Session — unit of work и identity map.\nМеханизм: владеет transaction state.\nПример: одна Session на request/use case.\nОграничение: после failed flush нужен rollback.", "Такой ответ коротко покрывает определение, механизм, практику и failure mode."),
    "0.3": ("text", "Проблема: live-события между API-инстансами.\nМоё решение: WebSocket + Redis Pub/Sub.\nГраница: PostgreSQL хранит durable history.\nПроверка: reconnect читает пропущенные события из БД.", "Защита проекта связывает конкретное решение с ограничением и способом проверки."),
    "1.1": ("python", "message = \"Learn with Pythoria\"\nalias = message\n\nprint(type(message).__name__)\nprint(message is alias)\n\nalias = alias.upper()\nprint(message, alias)", "Имена `message` и `alias` сначала связаны с одним `str`; новый assignment переводит только `alias` на новый объект."),
    "1.2": ("python", "left = [1, 2]\nright = [1, 2]\nsame = left\n\nprint(left == right)\nprint(left is right)\nprint(left is same)", "`==` вызывает equality protocol, а `is` сравнивает identity объектов."),
    "1.3": ("python", "roles = [\"reader\"]\noriginal_id = id(roles)\nroles.append(\"writer\")\n\nname = \"api\"\nold_name_id = id(name)\nname += \"-v2\"\n\nprint(id(roles) == original_id)\nprint(id(name) == old_name_id)", "List меняется с сохранением identity; операция со строкой создаёт новый immutable объект."),
    "1.4": ("python", "keys = {(1, 2): \"point\"}\nprint(keys[(1, 2)])\n\ntry:\n    {[1, 2]: \"broken\"}\nexcept TypeError as exc:\n    print(type(exc).__name__)", "Tuple из hashable элементов допустим как ключ, mutable list — нет."),
    "1.5": ("python", "class Queue:\n    def __init__(self, items):\n        self.items = list(items)\n\n    def __len__(self):\n        return len(self.items)\n\nprint(bool(Queue([])))\nprint(bool(Queue([\"job\"])))", "При отсутствии `__bool__` Python использует `__len__`: ноль означает falsy."),
    "1.6": ("python", "matrix = [[0] * 2 for _ in range(3)]\nalias = matrix[0]\nalias.append(1)\n\nprint(matrix)\nprint(alias is matrix[0])\nprint(alias is matrix[1])", "Comprehension создаёт независимые внутренние lists, а `alias` указывает только на первую строку."),
    "1.7": ("python", "from copy import copy, deepcopy\n\nsource = {\"profile\": {\"roles\": [\"reader\"]}}\nshallow = copy(source)\ndeep = deepcopy(source)\nsource[\"profile\"][\"roles\"].append(\"writer\")\n\nprint(shallow[\"profile\"][\"roles\"])\nprint(deep[\"profile\"][\"roles\"])", "Shallow copy разделяет вложенный graph, а deep copy рекурсивно создаёт независимые containers."),
    "1.8": ("python", "text = \"Алматы\"\npayload = text.encode(\"utf-8\")\nrestored = payload.decode(\"utf-8\")\n\nprint(type(text).__name__, type(payload).__name__)\nprint(restored == text)", "`str` — Unicode text, `bytes` — закодированное представление на I/O-границе."),
    "2.1": ("python", "events = [\"created\", \"paid\"]\nevents.append(\"sent\")\nlast = events.pop()\n\nprint(events)\nprint(last)", "List сохраняет порядок, поддерживает mutation и удобен для последовательного набора событий."),
    "2.2": ("python", "point = (43.2389, 76.8897)\nlatitude, longitude = point\nlocations = {point: \"Almaty\"}\n\nprint(latitude, longitude)\nprint(locations[point])", "Tuple выражает фиксированную запись и может быть dict key, если все элементы hashable."),
    "2.3": ("python", "users = {\n    7: {\"name\": \"Aida\"},\n    9: {\"name\": \"Daniyar\"},\n}\nusers[7][\"active\"] = True\n\nprint(users.get(8))\nprint(users[7])", "Dict моделирует lookup по уникальному ключу; `.get` явно выражает допустимое отсутствие."),
    "2.4": ("python", "requested = {\"read\", \"write\"}\ngranted = frozenset({\"read\", \"moderate\"})\n\nprint(requested & granted)\nprint(requested <= granted)", "Set operations прямо выражают пересечение и проверку подмножества permissions."),
    "2.5": ("python", "ordered_ids = [5, 3, 5]          # порядок и повторы\nunique_ids = set(ordered_ids)       # уникальность\nuser_by_id = {value: {} for value in unique_ids}  # lookup\n\nprint(ordered_ids, unique_ids, user_by_id.keys())", "Коллекцию выбирают по инварианту: порядок, повторы и доступ по ключу требуют разных структур."),
    "2.6": ("python", "rows = [\n    {\"id\": 1, \"active\": True},\n    {\"id\": 2, \"active\": False},\n]\nactive_ids = [row[\"id\"] for row in rows if row[\"active\"]]\n\nprint(active_ids)", "Comprehension объединяет преобразование и короткий filter без скрытых side effects."),
    "2.7": ("python", "users = [\n    {\"id\": 2, \"score\": 10},\n    {\"id\": 1, \"score\": 10},\n    {\"id\": 3, \"score\": 7},\n]\nresult = sorted(users, key=lambda user: (-user[\"score\"], user[\"id\"]))\nprint([user[\"id\"] for user in result])", "Tuple key задаёт основной порядок и детерминированный tie-breaker."),
    "3.1": ("python", "def normalize_email(value: str) -> str:\n    return value.strip().lower()\n\nhandlers = [normalize_email, str.upper]\nprint([handler(\" A@EXAMPLE.COM \") for handler in handlers])", "Функции — объекты: их можно хранить в коллекции, передавать и вызывать позже."),
    "3.2": ("python", "def create_user(email, active=True):\n    return {\"email\": email, \"active\": active}\n\nuser = create_user(\"a@example.com\", active=False)\nprint(user)", "`email` и `active` — parameters определения; переданные значения — arguments конкретного вызова."),
    "3.3": ("python", "def paginate(resource, /, *, limit=20, offset=0):\n    return resource[offset : offset + limit]\n\nprint(paginate([1, 2, 3], limit=2))", "`resource` скрывает имя positional-only параметра, а параметры pagination требуют явных keywords."),
    "3.4": ("python", "def add_tag(tag, tags=None):\n    if tags is None:\n        tags = []\n    tags.append(tag)\n    return tags\n\nprint(add_tag(\"python\"))\nprint(add_tag(\"sql\"))", "Sentinel/default `None` создаёт новый mutable list на каждый вызов и исключает shared state."),
    "3.5": ("python", "def audit(event, *entity_ids, request_id=None, **details):\n    return event, entity_ids, request_id, details\n\ncontext = {\"request_id\": \"req-7\", \"actor\": 42}\nprint(audit(\"updated\", 10, 11, **context))", "`*args` собирает positional IDs, `**kwargs` — дополнительные named fields; unpacking разворачивает mapping при вызове."),
    "3.6": ("python", "def find_user(user_id: int) -> dict[str, object] | None:\n    return None\n\nprint(find_user.__annotations__)\nprint(find_user(\"runtime is still dynamic\"))", "Annotations доступны инструментам и runtime introspection, но сами не запрещают неверный тип аргумента."),
    "3.7": ("python", "label = \"global\"\n\ndef outer():\n    label = \"enclosing\"\n    def inner():\n        label = \"local\"\n        return label\n    return inner(), label\n\nprint(outer(), label)", "Три разных bindings с одним именем находятся на local, enclosing и global уровнях."),
    "3.8": ("python", "attempts = 0\n\ndef make_counter():\n    count = 0\n    def next_value():\n        nonlocal count\n        count += 1\n        return count\n    return next_value\n\ncounter = make_counter()\nprint(counter(), counter())", "`nonlocal` меняет ближайший enclosing binding; global state для независимого counter не требуется."),
    "3.9": ("python", "def make_prefixer(prefix):\n    def render(value):\n        return f\"{prefix}:{value}\"\n    return render\n\nuser_key = make_prefixer(\"user\")\nprint(user_key(42))", "Closure продолжает видеть binding `prefix` после завершения внешней функции."),
    "3.10": ("python", "bad = [lambda: value for value in range(3)]\ngood = [lambda value=value: value for value in range(3)]\n\nprint([fn() for fn in bad])\nprint([fn() for fn in good])", "Late binding разрешает free variable при вызове; default argument фиксирует значение при создании lambda."),
    "3.11": ("python", "def require_active(function):\n    def wrapper(user):\n        if not user[\"active\"]:\n            raise PermissionError\n        return function(user)\n    return wrapper\n\n@require_active\ndef profile(user):\n    return user[\"name\"]", "Decorator заменяет имя `profile` на wrapper, который проверяет условие перед исходным вызовом."),
    "3.12": ("python", "from functools import wraps\n\ndef traced(function):\n    @wraps(function)\n    def wrapper(*args, **kwargs):\n        return function(*args, **kwargs)\n    return wrapper\n\n@traced\ndef health() -> dict[str, str]:\n    return {\"status\": \"ok\"}\n\nprint(health.__name__, health.__annotations__)", "`wraps` сохраняет metadata и `__wrapped__`, нужные introspection и framework-коду."),
    "3.13": ("python", "def retry(*, attempts):\n    def decorate(function):\n        def wrapper(*args, **kwargs):\n            for number in range(attempts):\n                try:\n                    return function(*args, **kwargs)\n                except TimeoutError:\n                    if number + 1 == attempts:\n                        raise\n        return wrapper\n    return decorate", "Decorator factory сначала фиксирует configuration, затем получает функцию и строит wrapper."),
    "3.14": ("python", "def mark(name):\n    def decorate(function):\n        def wrapper():\n            return f\"{name}({function()})\"\n        return wrapper\n    return decorate\n\n@mark(\"outer\")\n@mark(\"inner\")\ndef value():\n    return \"core\"\n\nprint(value())", "Декораторы применяются снизу вверх, а wrappers вызываются снаружи внутрь."),
    "4.1": ("python", "numbers = [10, 20]\niterator = iter(numbers)\n\nprint(iter(numbers) is numbers)\nprint(iter(iterator) is iterator)\nprint(next(iterator))", "List — iterable, создающий iterator; iterator хранит позицию и возвращает себя из `iter`."),
    "4.2": ("python", "class Countdown:\n    def __init__(self, start):\n        self.current = start\n\n    def __iter__(self):\n        return self\n\n    def __next__(self):\n        if self.current == 0:\n            raise StopIteration\n        self.current -= 1\n        return self.current + 1\n\nprint(list(Countdown(3)))", "Iterator protocol состоит из `__iter__`, stateful `__next__` и `StopIteration`."),
    "4.3": ("python", "def read_batches(rows, size):\n    for start in range(0, len(rows), size):\n        yield rows[start : start + size]\n\nstream = read_batches([1, 2, 3, 4, 5], 2)\nprint(next(stream))\nprint(list(stream))", "Generator сохраняет suspended frame между `yield` и лениво продолжает с текущей позиции."),
    "4.4": ("python", "source = range(1_000_000)\nlazy_squares = (value * value for value in source)\neager_squares = [value * value for value in range(3)]\n\nprint(next(lazy_squares))\nprint(eager_squares)", "Generator expression вычисляет элементы по запросу; list comprehension сразу материализует результат."),
    "4.7": ("python", "try:\n    int(\"not-a-number\")\nexcept ValueError as exc:\n    print(isinstance(exc, Exception))\n    print(type(exc).__mro__[:3])", "Иерархия позволяет перехватывать ожидаемый узкий тип, не скрывая системные и неожиданные ошибки."),
    "4.8": ("python", "def parse(value):\n    try:\n        result = int(value)\n    except ValueError:\n        return None\n    else:\n        return result\n    finally:\n        print(\"parse finished\")\n\nprint(parse(\"7\"))", "`else` выполняется только без exception, `finally` — при любом пути выхода."),
    "4.9": ("python", "def load_id(raw):\n    try:\n        return int(raw)\n    except ValueError:\n        print(\"invalid id\")\n        raise\n\ntry:\n    load_id(\"x\")\nexcept ValueError:\n    print(\"caller decides\")", "Bare `raise` повторно поднимает текущую ошибку с исходным traceback."),
    "4.10": ("python", "class InvalidUserId(ValueError):\n    pass\n\ndef parse_user_id(raw):\n    try:\n        return int(raw)\n    except ValueError as exc:\n        raise InvalidUserId(raw) from exc", "`raise from` добавляет domain context и сохраняет исходную причину в exception chain."),
    "4.11": ("python", "class BookingConflict(Exception):\n    def __init__(self, room_id):\n        self.room_id = room_id\n        super().__init__(f\"room {room_id} is already booked\")\n\ntry:\n    raise BookingConflict(42)\nexcept BookingConflict as exc:\n    print(exc.room_id)", "Custom exception несёт стабильный domain type и данные, а не заставляет caller разбирать строку."),
    "4.12": ("python", "class Transaction:\n    def __enter__(self):\n        print(\"begin\")\n        return self\n\n    def __exit__(self, kind, value, traceback):\n        print(\"rollback\" if kind else \"commit\")\n        return False\n\nwith Transaction():\n    print(\"write\")", "Context manager централизует acquire/cleanup и не подавляет исключение при `False`."),
    "4.13": ("python", "from contextlib import contextmanager\n\n@contextmanager\ndef transaction(session):\n    try:\n        yield session\n        session.commit()\n    except Exception:\n        session.rollback()\n        raise", "`@contextmanager` превращает generator с одним `yield` в protocol `with`, сохраняя cleanup рядом с acquire."),
    "5.1": ("python", "class User:\n    kind = \"account\"\n\n    def __init__(self, email):\n        self.email = email\n\nuser = User(\"a@example.com\")\nprint(user.email, user.kind, type(user).__name__)", "Instance хранит собственный `email`, а attribute lookup находит общий `kind` в class."),
    "5.2": ("python", "class BadCart:\n    items = []\n\nclass Cart:\n    def __init__(self):\n        self.items = []\n\na, b = Cart(), Cart()\na.items.append(1)\nprint(b.items)", "Mutable instance state создают в `__init__`; иначе class attribute разделяется всеми instances."),
    "5.3": ("python", "class Counter:\n    def __init__(self):\n        self.value = 0\n\n    def increment(self, amount=1):\n        self.value += amount\n        return self.value\n\ncounter = Counter()\nprint(counter.increment(2))", "При вызове bound method instance автоматически передаётся как `self`."),
    "5.4": ("python", "class UserId:\n    def __init__(self, value):\n        self.value = value\n\n    @classmethod\n    def from_text(cls, raw):\n        return cls(int(raw))\n\n    @staticmethod\n    def is_valid(raw):\n        return raw.isdigit()\n\nprint(UserId.from_text(\"7\").value, UserId.is_valid(\"7\"))", "Classmethod создаёт объект через polymorphic `cls`; staticmethod — namespaced helper без implicit receiver."),
    "5.5": ("python", "class JsonRenderable:\n    def render(self):\n        raise NotImplementedError\n\nclass User(JsonRenderable):\n    def render(self):\n        return {\"type\": \"user\"}\n\ndef response(item: JsonRenderable):\n    return item.render()\n\nprint(response(User()))", "Polymorphism позволяет caller работать через behavior contract, не проверяя конкретный класс."),
    "5.6": ("python", "class EmailSender:\n    def send(self, message):\n        return f\"sent: {message}\"\n\nclass RegistrationService:\n    def __init__(self, sender):\n        self.sender = sender\n\n    def register(self, email):\n        return self.sender.send(email)\n\nprint(RegistrationService(EmailSender()).register(\"a@example.com\"))", "Composition передаёт collaborator явно и не заставляет service наследоваться от sender."),
    "5.7": ("python", "class Serializer:\n    def dump(self, value):\n        return str(value)\n\nclass JsonSerializer(Serializer):\n    def dump(self, value):\n        base = super().dump(value)\n        return f'{{\"value\": \"{base}\"}}'\n\nprint(JsonSerializer().dump(7))", "Override заменяет behavior, а `super()` продолжает реализацию по MRO."),
    "5.8": ("python", "class TraceMixin:\n    def handle(self):\n        return [\"trace\", *super().handle()]\n\nclass Handler:\n    def handle(self):\n        return [\"handler\"]\n\nclass ApiHandler(TraceMixin, Handler):\n    pass\n\nprint(ApiHandler.__mro__)\nprint(ApiHandler().handle())", "Cooperative `super()` следует MRO `ApiHandler → TraceMixin → Handler`, а не жёстко названному parent."),
    "5.9": ("python", "from abc import ABC, abstractmethod\n\nclass Repository(ABC):\n    @abstractmethod\n    def get(self, item_id): ...\n\nclass MemoryRepository(Repository):\n    def get(self, item_id):\n        return {\"id\": item_id}\n\nprint(MemoryRepository().get(1))", "ABC запрещает создать неполную реализацию и документирует nominal interface."),
    "5.10": ("python", "from dataclasses import dataclass, field\n\n@dataclass(slots=True)\nclass User:\n    email: str\n    roles: list[str] = field(default_factory=list)\n\na, b = User(\"a@example.com\"), User(\"b@example.com\")\na.roles.append(\"admin\")\nprint(b.roles)", "`default_factory` создаёт независимый mutable default для каждого dataclass instance."),
    "5.11": ("python", "class PositiveInt(int):\n    def __new__(cls, value):\n        parsed = int(value)\n        if parsed <= 0:\n            raise ValueError(\"positive value required\")\n        return super().__new__(cls, parsed)\n\nprint(PositiveInt(\"7\"))", "Для immutable base создание и validation значения выполняют в `__new__`; `__init__` уже получает созданный объект."),
    "5.12": ("python", "class User:\n    def __init__(self, email):\n        self.email = email\n\n    def __repr__(self):\n        return f\"User(email={self.email!r})\"\n\n    def __str__(self):\n        return self.email\n\nuser = User(\"a@example.com\")\nprint(str(user), repr(user))", "`__repr__` помогает разработчику и отладке, `__str__` даёт удобное пользовательское представление."),
    "5.13": ("python", "from dataclasses import dataclass\n\n@dataclass(frozen=True)\nclass UserId:\n    value: int\n\nleft, right = UserId(7), UserId(7)\nprint(left == right)\nprint({left: \"Aida\"}[right])", "Равные immutable value objects имеют согласованные equality и hash и безопасны как dict keys."),
    "5.14": ("python", "class Page:\n    def __init__(self, items):\n        self.items = tuple(items)\n\n    def __len__(self): return len(self.items)\n    def __bool__(self): return bool(self.items)\n    def __contains__(self, item): return item in self.items\n    def __getitem__(self, index): return self.items[index]\n\npage = Page([10, 20])\nprint(len(page), bool(page), 20 in page, page[0])", "Набор dunder methods подключает объект к независимым Python protocols длины, truthiness, membership и indexing."),
    "6.1": ("python", "def double(value: int) -> int:\n    return value * 2\n\nprint(double(3))\nprint(double(\"a\"))", "Type checker отклонит второй вызов, но runtime Python выполнит operator строки без автоматической validation."),
    "6.2": ("python", "def normalize(value: str | None) -> str:\n    return value.strip() if value is not None else \"\"\n\nprint(normalize(None))\ntry:\n    normalize()\nexcept TypeError:\n    print(\"argument is still required\")", "Nullable type разрешает `None`, но отсутствие default не делает argument optional при вызове."),
    "6.3": ("python", "from collections.abc import Callable, Iterable\n\ndef transform(values: Iterable[int], operation: Callable[[int], str]) -> list[str]:\n    return [operation(value) for value in values]\n\nprint(transform((1, 2), lambda value: f\"id:{value}\"))", "Types описывают не конкретный list/function, а iterable input и связь callable input/output."),
    "6.4": ("python", "from typing import Literal, NotRequired, TypedDict\n\nclass UserPayload(TypedDict):\n    email: str\n    role: Literal[\"reader\", \"writer\"]\n    display_name: NotRequired[str]\n\npayload: UserPayload = {\"email\": \"a@example.com\", \"role\": \"reader\"}\nprint(payload)", "TypedDict проверяет статическую форму обычного dict, Literal сужает набор допустимых строк."),
    "6.6": ("python", "from typing import Protocol\n\nclass UserReader(Protocol):\n    def get(self, user_id: int) -> dict | None: ...\n\nclass MemoryUsers:\n    def get(self, user_id: int) -> dict | None:\n        return {\"id\": user_id}\n\ndef load(repo: UserReader, user_id: int):\n    return repo.get(user_id)\n\nprint(load(MemoryUsers(), 7))", "Structural Protocol принимает объект по доступному behavior без общего base class."),
    "7.5": ("python", "from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor\n\n# Blocking I/O часто удобно отправить в threads.\nwith ThreadPoolExecutor(max_workers=4) as pool:\n    io_results = list(pool.map(str.upper, [\"a\", \"b\"]))\n\n# CPU-bound pure Python оценивают для processes, учитывая IPC.\nprint(io_results, ProcessPoolExecutor)", "GIL не заменяет выбор workload: threads полезны для blocking I/O, processes обходят общий interpreter lock ценой IPC."),
    "7.6": ("python", "from threading import Lock\n\nlock = Lock()\nbalance = 0\n\ndef deposit(amount):\n    global balance\n    with lock:\n        current = balance\n        balance = current + amount", "Lock защищает всю read-modify-write critical section; отдельные операции чтения и записи недостаточны."),
    "8.1": ("python", "import asyncio\n\nasync def fetch(name, delay):\n    await asyncio.sleep(delay)\n    return name\n\nasync def main():\n    print(await asyncio.gather(fetch(\"a\", 0.02), fetch(\"b\", 0.01)))\n\nasyncio.run(main())", "Concurrency перекрывает ожидание двух I/O операций; это не параллельное выполнение CPU-bound Python."),
    "8.2": ("python", "import asyncio\n\nasync def answer():\n    return 42\n\ncoroutine = answer()\nprint(type(coroutine).__name__)\nprint(asyncio.run(coroutine))", "Вызов `async def` создаёт coroutine object; event loop выполняет его до результата."),
    "8.3": ("python", "import asyncio\n\nasync def worker(name):\n    print(name, \"start\")\n    await asyncio.sleep(0)\n    print(name, \"resume\")\n\nasync def main():\n    await asyncio.gather(worker(\"a\"), worker(\"b\"))\n\nasyncio.run(main())", "Task уступает управление только в await point, после чего loop может продолжить другую ready task."),
    "8.4": ("python", "import asyncio\n\nasync def main():\n    loop = asyncio.get_running_loop()\n    future = loop.create_future()\n    loop.call_soon(future.set_result, \"ready\")\n    print(await future)\n\nasyncio.run(main())", "Event loop выполняет ready callback, завершает Future и возобновляет ожидающую coroutine."),
    "8.5": ("python", "import asyncio\n\nasync def save():\n    await asyncio.sleep(0)\n    return \"saved\"\n\nasync def main():\n    task = asyncio.create_task(save(), name=\"save-user\")\n    print(task.get_name())\n    print(await task)\n\nasyncio.run(main())", "Task планирует coroutine и хранит её completion/result; reference нужно сохранить и дождаться."),
    "8.6": ("python", "import asyncio\n\nasync def item(value, delay):\n    await asyncio.sleep(delay)\n    return value\n\nasync def main():\n    result = await asyncio.gather(item(\"first\", 0.02), item(\"second\", 0))\n    print(result)\n\nasyncio.run(main())", "`gather` запускает операции конкурентно, но возвращает результаты в порядке переданных awaitables."),
    "8.7": ("python", "import asyncio\n\nasync def main():\n    try:\n        async with asyncio.timeout(0.01):\n            await asyncio.sleep(1)\n    except TimeoutError:\n        print(\"deadline exceeded\")\n\nasyncio.run(main())", "Timeout задаёт deadline scope, отменяет затянувшееся ожидание и сообщает caller через `TimeoutError`."),
    "8.8": ("python", "import asyncio\n\nasync def worker():\n    try:\n        await asyncio.sleep(10)\n    finally:\n        print(\"cleanup\")\n\nasync def main():\n    task = asyncio.create_task(worker())\n    await asyncio.sleep(0)\n    task.cancel()\n    try:\n        await task\n    except asyncio.CancelledError:\n        print(\"cancelled\")\n\nasyncio.run(main())", "Cancellation проходит через await, выполняет `finally` и обычно повторно распространяется caller."),
    "8.9": ("python", "import asyncio\nimport time\n\ndef blocking_read():\n    time.sleep(0.05)\n    return \"done\"\n\nasync def main():\n    result = await asyncio.to_thread(blocking_read)\n    print(result)\n\nasyncio.run(main())", "`to_thread` выносит неизбежный blocking call из event-loop thread; async-native client предпочтительнее."),
    "8.10": ("python", "class AsyncResource:\n    async def __aenter__(self):\n        return self\n\n    async def __aexit__(self, kind, value, traceback):\n        await self.close()\n\n    async def close(self):\n        pass", "Async context manager разрешает await во время acquire/release и гарантирует cleanup вокруг блока."),
    "8.11": ("python", "import asyncio\n\nasync def events():\n    for value in range(3):\n        await asyncio.sleep(0)\n        yield value\n\nasync def main():\n    async for event in events():\n        print(event)\n\nasyncio.run(main())", "Async generator лениво выдаёт значения и может ожидать I/O между итерациями."),
    "8.12": ("python", "decision = {\n    \"many_network_waits\": \"asyncio\",\n    \"blocking_library\": \"threads\",\n    \"cpu_bound_python\": \"processes\",\n}\nprint(decision)", "Модель конкурентности выбирают по workload, isolation и цене communication, а не по моде."),
    "9.1": ("python", "from threading import Thread, current_thread\n\ndef work():\n    print(current_thread().name)\n\nthread = Thread(target=work, name=\"email-worker\")\nthread.start()\nthread.join()", "Thread разделяет память процесса; `join` задаёт явную точку ожидания завершения."),
    "9.2": ("python", "from multiprocessing import Process, Queue\n\ndef calculate(output):\n    output.put(sum(value * value for value in range(10_000)))\n\nqueue = Queue()\nprocess = Process(target=calculate, args=(queue,))\nprocess.start(); process.join()\nprint(queue.get())", "Process имеет отдельную память, поэтому результат передаётся через IPC, а arguments должны сериализоваться."),
    "9.3": ("python", "from concurrent.futures import ThreadPoolExecutor, as_completed\n\ndef fetch(url):\n    return url.upper()\n\nwith ThreadPoolExecutor(max_workers=2) as pool:\n    futures = [pool.submit(fetch, url) for url in [\"/a\", \"/b\"]]\n    print([future.result() for future in as_completed(futures)])", "Executor управляет bounded pool и Future objects; порядок `as_completed` зависит от завершения, не input."),
    "10.1": ("sql", "CREATE TABLE authors (\n    id bigint PRIMARY KEY,\n    name text NOT NULL\n);\n\nCREATE TABLE articles (\n    id bigint PRIMARY KEY,\n    author_id bigint NOT NULL REFERENCES authors(id),\n    title text NOT NULL\n);", "Таблицы моделируют сущности, primary key идентифицирует строку, foreign key хранит допустимую связь."),
    "10.2": ("sql", "SELECT\n    id AS product_id,\n    price,\n    price * 1.12 AS price_with_tax\nFROM products;", "SELECT формирует projection: alias меняет имя result column, expression вычисляется для каждой строки."),
    "10.3": ("sql", "SELECT id, email\nFROM users\nWHERE active IS TRUE\n  AND created_at >= DATE '2026-01-01';", "WHERE оставляет только строки, для которых всё boolean expression истинно."),
    "10.4": ("sql", "SELECT id,\n       COALESCE(display_name, email) AS visible_name\nFROM users\nWHERE deleted_at IS NULL;", "`IS NULL` проверяет отсутствие значения, а COALESCE выбирает первое не-NULL выражение."),
    "10.5": ("sql", "SELECT id, created_at\nFROM events\nORDER BY created_at DESC, id DESC\nLIMIT 20 OFFSET 20;", "Уникальный `id` — tie-breaker: страницы остаются детерминированными при одинаковом времени."),
    "10.6": ("sql", "SELECT DISTINCT category\nFROM products\nWHERE category IS NOT NULL\nORDER BY category;", "DISTINCT удаляет одинаковые result rows; ORDER BY отдельно задаёт наблюдаемый порядок."),
    "10.7": ("sql", "SELECT\n    COUNT(*) AS order_count,\n    AVG(total) AS average_total,\n    SUM(total) FILTER (WHERE status = 'paid') AS paid_total\nFROM orders;", "Aggregates сворачивают набор строк; FILTER считает условную метрику без отдельного запроса."),
    "10.8": ("sql", "SELECT customer_id, SUM(total) AS revenue\nFROM invoices\nWHERE paid_at IS NOT NULL\nGROUP BY customer_id\nORDER BY customer_id;", "GROUP BY задаёт grain «одна строка на customer», после чего SUM считает значение внутри каждой группы."),
    "10.9": ("sql", "SELECT author_id, COUNT(*) AS article_count\nFROM articles\nGROUP BY author_id\nHAVING COUNT(*) >= 3;", "HAVING фильтрует уже сформированные группы; аналогичный predicate нельзя применить в WHERE до aggregation."),
    "10.10": ("sql", "SELECT a.id, a.title, u.email AS author_email\nFROM articles AS a\nJOIN users AS u ON u.id = a.author_id\nORDER BY a.id;", "INNER JOIN оставляет только пары строк, удовлетворяющие условию связи author_id → users.id."),
    "10.11": ("sql", "SELECT u.id, COUNT(s.id) AS active_sessions\nFROM users AS u\nLEFT JOIN sessions AS s\n  ON s.user_id = u.id AND s.revoked_at IS NULL\nGROUP BY u.id;", "Условие правой таблицы находится в ON, поэтому users без active sessions не исчезают."),
    "10.12": ("sql", "SELECT old.id AS old_id, new.id AS new_id\nFROM old_catalog AS old\nFULL OUTER JOIN new_catalog AS new ON new.sku = old.sku\nWHERE old.id IS NULL OR new.id IS NULL;", "FULL OUTER JOIN полезен для reconciliation: сохраняет unmatched rows с обеих сторон."),
    "10.13": ("sql", "SELECT employee.name, manager.name AS manager_name\nFROM employees AS employee\nLEFT JOIN employees AS manager ON manager.id = employee.manager_id;", "Self join использует два aliases одной таблицы, чтобы представить и employee, и его manager."),
    "10.14": ("sql", "SELECT id, total\nFROM invoices\nWHERE total > (SELECT AVG(total) FROM invoices);", "Scalar subquery вычисляет среднее один раз для сравнения каждой invoice."),
    "10.15": ("sql", "SELECT p.id, p.title\nFROM posts AS p\nWHERE p.created_at = (\n    SELECT MAX(inner_post.created_at)\n    FROM posts AS inner_post\n    WHERE inner_post.author_id = p.author_id\n);", "Correlated subquery ссылается на текущего outer author и выбирает его последний post."),
    "10.16": ("sql", "SELECT u.id\nFROM users AS u\nWHERE EXISTS (\n    SELECT 1 FROM sessions AS s\n    WHERE s.user_id = u.id AND s.revoked_at IS NULL\n);", "EXISTS выражает проверку наличия связанной строки и не размножает users как обычный JOIN."),
    "10.17": ("sql", "WITH monthly AS (\n    SELECT date_trunc('month', created_at) AS month, SUM(total) AS revenue\n    FROM invoices\n    GROUP BY date_trunc('month', created_at)\n)\nSELECT month, revenue\nFROM monthly\nWHERE revenue > 1000;", "CTE именует промежуточный result и отделяет aggregation от последующей фильтрации."),
    "10.19": ("sql", "SELECT id,\n       CASE\n           WHEN score >= 80 THEN 'high'\n           WHEN score >= 50 THEN 'medium'\n           ELSE 'low'\n       END AS score_band\nFROM assessments;", "CASE проверяет ветви сверху вниз и возвращает одно значение для каждой строки."),
    "10.20": ("sql", "SELECT email FROM newsletter_subscribers\nUNION\nSELECT email FROM registered_users\n\nINTERSECT\nSELECT email FROM verified_emails;", "Set operations требуют совместимых columns; UNION удаляет duplicates, INTERSECT оставляет общие строки."),
    "10.21": ("sql", "SELECT id, account_id, amount,\n       SUM(amount) OVER (\n           PARTITION BY account_id\n           ORDER BY created_at, id\n       ) AS running_balance\nFROM ledger_entries;", "Window aggregate сохраняет каждую ledger row и добавляет накопительный итог в пределах account."),
    "10.22": ("sql", "SELECT player_id, score,\n       ROW_NUMBER() OVER (ORDER BY score DESC, player_id) AS position,\n       DENSE_RANK() OVER (ORDER BY score DESC) AS score_rank\nFROM leaderboard;", "ROW_NUMBER всегда уникален, а DENSE_RANK даёт одинаковый rank равным scores без пропусков."),
    "10.23": ("sql", "SELECT id, project_id, created_at,\n       LAG(created_at) OVER (\n           PARTITION BY project_id\n           ORDER BY created_at, id\n       ) AS previous_event_at\nFROM project_events;", "PARTITION перезапускает окно для каждого project, ordering определяет предыдущую строку для LAG."),
    "10.25": ("sql", "UPDATE jobs\nSET status = 'running', started_at = now()\nWHERE id = $1 AND status = 'queued'\nRETURNING id, status, started_at;", "Conditional UPDATE объединяет проверку текущего state и изменение; RETURNING отдаёт фактически обновлённую строку."),
    "14.3": ("python", "from fastapi import FastAPI, Path\n\napp = FastAPI()\n\n@app.get(\"/articles/{article_id}\")\ndef article(article_id: int = Path(gt=0)):\n    return {\"article_id\": article_id}", "Router сначала сопоставляет path, затем FastAPI преобразует segment в `int` и применяет constraint `gt=0`."),
    "14.4": ("python", "from fastapi import FastAPI, Query\n\napp = FastAPI()\n\n@app.get(\"/articles\")\ndef articles(limit: int = Query(default=20, ge=1, le=100), offset: int = Query(default=0, ge=0)):\n    return {\"limit\": limit, \"offset\": offset}", "Query parameters имеют независимые defaults и boundary constraints; pagination contract виден в OpenAPI."),
}


STAGE_CONTEXT = {
    10: "Сначала определи grain результата, затем JOIN/filter/grouping и только после этого projection/order.",
    11: "Проверь invariant, конкурентный сценарий и фактический query plan вместо догадки.",
    12: "Зафиксируй method/path/headers/body, status и поведение повторного request.",
    13: "Назови threat, trust boundary, server-side check и безопасный отказ.",
    14: "Проследи request через router, validation, dependency, service и response model.",
    15: "Проверь missing, explicit null, invalid input и serialized output Pydantic v2.",
    16: "Укажи владельца Session/transaction и момент фактического SQL I/O.",
    17: "Review migration как versioned schema transition; autogenerate — только кандидат.",
    18: "Тестируй observable contract, failure path и изоляцию между cases.",
    19: "Определи key, value, TTL, invalidation, concurrency и outage fallback.",
    20: "Проследи delivery, duplicate, retry, idempotency и atomicity gap после DB commit.",
    21: "Разделяй build-time image и runtime container: DNS, ports, mounts, env и readiness.",
    22: "Перед командой назови изменяемое состояние: files, index, branch pointer или shared history.",
    23: "Свяжи command с конкретным process, file, permission, environment или port symptom.",
    24: "CI gate должен быть воспроизводимым, иметь понятный failure log и не раскрывать secrets.",
    25: "Сигнал полезен, когда содержит контекст, correlation и ведёт к конкретному действию.",
    26: "Проследи Django/DRF request, ORM query count, validation, permission и response.",
    27: "Проведи границу слоя и dependency direction; business rule не должен зависеть от framework.",
    28: "Сначала назови input constraints, структуру данных, complexity и boundary cases.",
    29: "Начни с требований и source of truth; добавляй компонент только под измеримый failure mode.",
    31: "Ответ строй как context → личное действие → результат → конкретный follow-up.",
    32: "Защищай только реализованный flow: проблема → решение → trade-off → failure mode → проверка.",
}


def load_index() -> tuple[dict[str, dict], dict[str, Path]]:
    curriculum = json.loads((CONTENT / "curriculum.json").read_text(encoding="utf-8"))
    lessons: dict[str, dict] = {}
    for stage in curriculum["stages"]:
        for lesson in stage["lessons"]:
            lessons[lesson["number"]] = {**lesson, "stage_number": stage["number"]}

    directories: dict[str, Path] = {}
    for path in CONTENT.glob("*/*/metadata.json"):
        metadata = json.loads(path.read_text(encoding="utf-8"))
        directories[metadata["slug"]] = path.parent
    return lessons, directories


def practice_index() -> dict[str, list[tuple[str, dict]]]:
    banks = json.loads((CONTENT / "practice_banks.json").read_text(encoding="utf-8"))
    result: dict[str, list[tuple[str, dict]]] = defaultdict(list)
    for kind, records in banks.items():
        if not isinstance(records, list):
            continue
        for record in records:
            result[record["lesson_number"]].append((kind, record))
    return result


def safe_identifier(value: str) -> str:
    result = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    if not result or result[0].isdigit():
        result = f"lesson_{result}"
    return result[:50]


def starter_example(directory: Path, lesson: dict) -> tuple[str, str, str] | None:
    metadata = json.loads((directory / "metadata.json").read_text(encoding="utf-8"))
    starter = directory / "starter" / "main.py"
    if not metadata.get("has_task") or not starter.exists():
        return None
    source = starter.read_text(encoding="utf-8").strip()
    if not source or "Автоматическая coding-задача для этого урока не требуется" in source:
        return None
    return (
        "python",
        source,
        f"Это публичный starter contract практики «{metadata.get('task_title', lesson['title'])}». Реализация и hidden assertions в lesson Markdown не раскрываются.",
    )


def practice_example(records: list[tuple[str, dict]]) -> tuple[str, str, str] | None:
    prediction = next((record for kind, record in records if kind == "python_prediction"), None)
    if prediction:
        return (
            "python",
            prediction["snippet"],
            f"Expected: `{prediction['expected_output']}`. {prediction['step_by_step']}",
        )

    sql = next((record for kind, record in records if kind == "sql" and record.get("solution_sql")), None)
    if sql:
        return (
            "sql",
            sql["solution_sql"],
            f"Разобранный пример «{sql['title']}»: result columns — {', '.join(sql['expected_columns'])}; comparison — {sql['comparison']}.",
        )

    scenario = next(((kind, record) for kind, record in records if kind != "sql"), None)
    if scenario:
        kind, record = scenario
        source = f"Сценарий: {record['prompt']}\n\nПроверка:\n{record['expected_reasoning']}"
        return "text", source, f"Это отдельный {kind} example для данного subtopic, а не общий пример stage."
    return None


def fallback_example(lesson: dict) -> tuple[str, str, str]:
    stage = lesson["stage_number"]
    title = lesson["title"]
    topics = [str(item).rstrip(".") for item in lesson.get("outline", [])[:4]] or [title]
    focus = "\n".join(f"- {item}" for item in topics)
    context = STAGE_CONTEXT.get(stage, "Объясни механизм, failure mode и способ проверки на конкретном backend-сценарии.")
    identifier = safe_identifier(lesson["slug"])

    if stage in {10, 11}:
        source = f"-- {lesson['number']} · {title}\n-- Focus: {', '.join(topics)}\nSELECT '{identifier}' AS example_key;"
        return "sql", source, context
    if stage == 12:
        method = "PATCH" if any(word in title.lower() for word in ("patch", "modification")) else "GET"
        source = f'{method} /examples/{identifier} HTTP/1.1\nAccept: application/json\nX-Request-ID: req-{lesson["number"].replace(".", "-")}'
        return "http", source, f"{context} Здесь route и request-id привязаны именно к теме «{title}»."
    if stage in {13, 14, 15, 16, 18, 20, 25, 26, 27, 28}:
        function_name = f"example_{identifier}"
        quoted_topics = ", ".join(repr(topic) for topic in topics)
        source = (
            f"def {function_name}() -> tuple[str, ...]:\n"
            f"    # {title}: проверяем отдельный contract урока.\n"
            f"    return ({quoted_topics},)\n\n"
            f"assert {function_name}()"
        )
        return "python", source, context
    if stage == 17:
        source = f'alembic revision -m "{identifier}"\n# review upgrade/downgrade for: {", ".join(topics)}\nalembic upgrade head'
        return "bash", source, context
    if stage in {19}:
        key = f"lesson:{lesson['number']}:{identifier}"
        source = f"SET {key} value EX 60\nGET {key}\nTTL {key}"
        return "text", source, context
    if stage in {21, 24}:
        source = f"# {lesson['number']} · {title}\nlesson:\n  key: {identifier}\n  checks:\n" + "".join(
            f"    - {topic}\n" for topic in topics
        )
        return "yaml", source.rstrip(), context
    if stage in {22, 23}:
        source = f"# {lesson['number']} · {title}\n# Focus: {', '.join(topics)}\nprintf '%s\\n' '{identifier}'"
        return "bash", source, context

    source = f"Тема: {title}\n\nФокус:\n{focus}\n\nРабочая проверка:\n{context}"
    return "text", source, "Этот micro-scenario сформирован из outline конкретного урока и не переиспользуется соседними subtopics."


def lesson_example(lesson: dict, directory: Path, practices: dict[str, list[tuple[str, dict]]]) -> tuple[str, str, str]:
    if lesson["number"] in CURATED:
        return CURATED[lesson["number"]]
    related = practices.get(lesson["number"], [])
    from_practice = practice_example(related)
    if from_practice:
        return from_practice
    from_starter = starter_example(directory, lesson)
    if from_starter:
        return from_starter
    return fallback_example(lesson)


def render_section(lesson: dict, example: tuple[str, str, str]) -> str:
    language, source, explanation = example
    return (
        "## Примеры кода\n\n"
        f"### {lesson['title']}: отдельный пример\n\n"
        f"```{language}\n{source.rstrip()}\n```\n\n"
        f"{russianize_prose(explanation.rstrip())}\n"
    )


def replace_section(markdown: str, section: str) -> str:
    pattern = r"^## Примеры кода\n.*?(?=^## |\Z)"
    if not re.search(pattern, markdown, re.MULTILINE | re.DOTALL):
        raise ValueError("lesson has no Примеры кода section")
    return re.sub(pattern, section.rstrip() + "\n\n", markdown, count=1, flags=re.MULTILINE | re.DOTALL)


def main() -> None:
    lessons, directories = load_index()
    practices = practice_index()
    rendered: dict[str, str] = {}
    published = 0
    for number, lesson in lessons.items():
        if lesson["content_status"] != "complete":
            continue
        directory = directories[lesson["implementation_slug"]]
        example = lesson_example(lesson, directory, practices)
        section = render_section(lesson, example)
        normalized = re.sub(r"\s+", " ", f"{example[0]}\n{example[1]}").strip()
        if normalized in rendered:
            raise ValueError(f"duplicate example for {number} and {rendered[normalized]}")
        rendered[normalized] = number
        lesson_path = directory / "lesson.md"
        lesson_path.write_text(
            replace_section(lesson_path.read_text(encoding="utf-8"), section),
            encoding="utf-8",
        )
        published += 1
    print(f"Personalized {published} lesson examples; duplicates: 0")


if __name__ == "__main__":
    main()
