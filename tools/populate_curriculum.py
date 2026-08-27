"""Publish complete P0/P1 curriculum records through the existing content pipeline.

The taxonomy stays the canonical planning source. Published lessons continue to
use the repository's established folder format and stable slug-based progress.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
CURRICULUM = CONTENT / "curriculum.json"

# Preserve the progress keys of lessons that already represented taxonomy topics.
EXISTING_MAP = {
    "1.1": "python-basics",
    "1.2": "is-vs-eq",
    "1.3": "mutability-references",
    "1.7": "copying",
    "3.1": "functions-as-objects",
    "3.2": "signatures",
    "3.3": "positional-only",
    "3.4": "mutable-default-arguments",
    "3.5": "args-kwargs",
    "3.6": "annotations",
    "3.7": "legb",
    "3.9": "closures",
    "3.10": "late-binding",
    "3.11": "decorators",
    "3.12": "functools-wraps",
    "4.2": "iterator-protocol",
    "4.3": "generators",
    "4.7": "exceptions",
    "4.10": "exception-chaining",
    "4.11": "custom-exceptions",
    "4.12": "context-managers",
    "5.6": "inheritance-composition",
    "5.10": "dataclasses",
    "5.14": "data-model",
    "5.16": "descriptors",
    "5.18": "metaclasses",
    "6.1": "advanced-typing",
    "6.4": "typeddict",
    "6.5": "generic",
    "6.6": "protocol",
    "7.1": "object-lifetime",
    "7.2": "cyclic-gc",
    "7.3": "weak-references",
    "7.5": "gil",
    "7.6": "race-conditions",
    "8.2": "coroutine",
    "8.3": "async-await",
    "8.4": "event-loop",
    "8.5": "tasks",
    "8.6": "gather",
    "8.8": "cancellation",
    "8.10": "async-context-managers",
    "8.11": "async-iterators",
    "9.1": "threads",
    "9.2": "processes",
    "9.3": "thread-pool",
    "9.4": "process-pool",
    "18.2": "pytest",
    "18.3": "fixtures",
    "18.5": "parametrization",
    "18.6": "mocks",
    "18.11": "async-testing",
    "27.5": "package-design",
    "27.6": "architecture-basics",
    "27.7": "dependency-injection",
    "29.1": "backend-core-project",
}

PRESERVE_TASKS = {
    "python-basics",
    "is-vs-eq",
    "mutability-references",
    "mutable-default-arguments",
    "iterator-protocol",
    "generators",
}

STAGE_GUIDES = {
    0: ("Собеседование проверяет не объём терминов, а способность построить точное объяснение и применить его к сценарию.", "Сначала классифицируй вопрос, затем дай определение, механизм, минимальный пример и ограничение.", "Перечислять технологии без связи с решённой проблемой.", "Сформулируй ответ как определение → механизм → пример → trade-off."),
    1: ("Python-код работает с объектами и связями имён с объектами; это основа мутаций, аргументов функций и ключей словаря.", "Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.", "Объяснять переменную как коробку, которая всегда содержит независимое значение.", "Проследи identity и состояние объекта после двух присваиваний и одной мутации."),
    2: ("Коллекция выбирается по требуемым операциям: порядок, уникальность, доступ по ключу, мутабельность и стоимость поиска.", "Начинай с инварианта данных и операций, а затем выбирай list, tuple, dict или set.", "Выбирать коллекцию по привычке и игнорировать порядок, дубликаты или хешируемость.", "Выбери структуру для набора API-записей и обоснуй lookup, порядок и дубликаты."),
    3: ("Функция — объект с сигнатурой, областью видимости и состоянием замыкания; её контракт должен быть понятен вызывающему коду.", "Разделяй момент определения функции, момент вызова и момент разрешения свободного имени.", "Скрывать неясный API за **kwargs или забывать о времени вычисления defaults.", "Разбери сигнатуру helper-функции и объясни, какие вызовы допустимы и почему."),
    4: ("Итерация, исключения и context managers — протоколы управления потоком и освобождением ресурсов.", "Думай о протоколе как о договоре между вызывающим кодом и объектом: кто начинает, кто завершает и как сигнализируется ошибка.", "Перехватывать Exception без стратегии либо удерживать весь поток данных в памяти.", "Покажи happy path, завершение протокола и поведение при исключении."),
    5: ("ООП в backend полезно как способ выразить состояние, поведение и границы ответственности, а не как соревнование по наследованию.", "У объекта есть тип, instance state и protocol-facing methods; composition обычно делает зависимости явнее.", "Создавать глубокую иерархию ради переиспользования нескольких строк.", "Сравни composition и inheritance для сервиса уведомлений и назови цену изменения."),
    6: ("Type hints улучшают статический анализ и контракты, но сами по себе не валидируют runtime-данные.", "Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.", "Считать Any безопасным escape hatch либо путать Optional с необязательным аргументом.", "Опиши тип входа API helper так, чтобы mypy видел ошибочный вызов до запуска."),
    7: ("Детали CPython помогают объяснять lifetime, memory и ограничения потоков, но не заменяют измерения.", "Разделяй спецификацию Python и конкретную реализацию CPython; GIL относится к выполнению bytecode, не к бизнес-инвариантам.", "Считать GIL автоматической защитой shared state или вызывать gc.collect как универсальную оптимизацию.", "Классифицируй проблему как lifetime, allocation, race или CPU contention перед выбором инструмента."),
    8: ("asyncio даёт кооперативную конкурентность для I/O-bound работы: задача уступает loop только в await point.", "Event loop планирует готовые tasks; await не создаёт отдельный поток и не ускоряет CPU-bound код.", "Вызвать time.sleep или синхронный HTTP-клиент внутри async endpoint.", "Найди blocking участок, обозначь cancellation boundary и выбери способ конкурентного запуска."),
    9: ("Threads и processes решают разные задачи и имеют разную цену обмена состоянием.", "Thread разделяет память процесса; process изолирован и требует сериализации/IPC.", "Отправлять непиклируемый объект в process pool или делить mutable state без lock.", "Выбери executor для I/O-bound и CPU-bound функций и объясни ограничения."),
    10: ("SQL описывает требуемый набор строк; корректность начинается с cardinality, NULL semantics и явного порядка.", "Мысленно двигайся FROM/JOIN → WHERE → GROUP → HAVING → SELECT → ORDER/LIMIT.", "Использовать LIMIT без детерминированного ORDER BY или фильтровать правую таблицу LEFT JOIN в WHERE.", "Предскажи cardinality результата и проверь, не размножает ли JOIN строки."),
    11: ("PostgreSQL обеспечивает ограничения и конкурентную работу ближе к данным; индекс и transaction boundary проектируются под запросы и инварианты.", "Constraint защищает истину, transaction объединяет изменения, index ускоряет конкретный access path.", "Добавлять индекс на каждый столбец или держать transaction открытой во время сетевого вызова.", "Назови инвариант, конкурентный сценарий и точку, где его гарантирует база."),
    12: ("HTTP — контракт между клиентом и сервером: method, target, headers, body, status и cache semantics.", "Отделяй transport, HTTP semantics и доменную операцию; status code сообщает результат обработки запроса.", "Возвращать 200 для любой ошибки или считать POST автоматически неидемпотентным при любом дизайне.", "Спроектируй request/response контракт и объясни retry, idempotency и error body."),
    13: ("Security строится слоями: аутентификация, авторизация, validation, безопасное хранение секретов и ограничение злоупотреблений.", "Всегда определяй threat, trust boundary, проверяемое утверждение и последствия компрометации.", "Считать CORS авторизацией, JWT шифрованием или хранить пароль быстрым hash.", "Назови атакующего, актив, проверку на сервере и безопасный отказ."),
    14: ("FastAPI связывает ASGI request lifecycle, routing, validation, dependency graph и response serialization.", "Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.", "Открывать Session глобально или выполнять blocking I/O в async route.", "Проследи request от router через dependency и service до response model."),
    15: ("Pydantic v2 преобразует и валидирует данные на границе; модель должна явно описывать required, nullable и default semantics.", "Сначала приходит недоверенный input, затем core schema выполняет validation, после чего model_dump управляет serialization.", "Путать str | None с полем, которое можно полностью не передать.", "Проверь missing, explicit null, неверный тип и сериализованный результат."),
    16: ("SQLAlchemy 2.x управляет SQL, identity map, unit of work и transaction lifecycle; Session не является простым соединением.", "Один request/use case обычно владеет одной Session и явно завершает commit или rollback.", "Коммитить внутри repository, допускать N+1 или делить AsyncSession между concurrent tasks.", "Опиши session scope, момент flush/commit и количество SQL-запросов."),
    17: ("Alembic хранит версионированную историю изменений схемы; autogenerate создаёт кандидат на migration, а не доказательство корректности.", "Migration — воспроизводимый переход между версиями, который нужно review, test и безопасно раскатывать.", "Слепо принимать autogenerate или совмещать несовместимое изменение в один deploy.", "Предложи expand/contract sequence для изменения schema без остановки API."),
    18: ("Тест подтверждает observable contract в изолированном сценарии; хорошие tests детерминированы и объясняют failure.", "Arrange создаёт условия, Act выполняет одно поведение, Assert проверяет значимый результат.", "Mock не в том namespace, shared fixture state или тест только happy path.", "Выдели unit boundary, integration boundary и критичный failure case."),
    19: ("Redis — быстрый in-memory data store для cache и временного состояния, но источник истины выбирается по durability requirements.", "Для cache всегда определяй key, value, TTL, invalidation и fallback.", "Использовать Pub/Sub как историю или забыть TTL и invalidation.", "Разбери cache miss, stale value, Redis outage и concurrent refill."),
    20: ("Background work отделяет latency запроса от выполнения, но добавляет delivery, retry и idempotency concerns.", "Между DB commit и publish есть atomicity gap; outbox переносит событие в ту же transaction.", "Повторять side effect без idempotency или считать exactly-once свойством одного флага.", "Проследи событие от commit через broker/worker до повторной доставки."),
    21: ("Docker image — неизменяемый шаблон filesystem, container — запущенный изолированный process с configuration runtime.", "Разделяй build-time layers, runtime config, network DNS и persistent volumes.", "Использовать localhost между containers или считать depends_on проверкой readiness.", "Диагностируй container через logs, env, DNS, port и healthcheck по порядку."),
    22: ("Git хранит snapshots и граф commits; working tree, index, local branch и remote-tracking branch — разные состояния.", "Перед командой определяй, что именно меняется: файлы, index, branch pointer или shared history.", "Rebase shared commits или удалять secret из файла без ротации.", "Выбери безопасный способ отменить локальное и уже опубликованное изменение."),
    23: ("Linux basics нужны для запуска процесса, чтения логов, environment и диагностики ports/permissions.", "Процесс видит filesystem, env, user permissions, descriptors и network namespace.", "Менять permissions на 777 вместо поиска владельца и требуемого доступа.", "Найди процесс, его exit code, порт, env и последнюю ошибку в log."),
    24: ("CI повторяемо выполняет quality gates для commit; CD продвигает проверенный artifact по окружениям.", "Pipeline должен собирать один artifact и падать на воспроизводимой проверке с понятным log.", "Игнорировать flaky test или собирать другой код на каждом environment.", "Разбери failure по шагу, версии runtime, env и отличию от local run."),
    25: ("Observability отвечает на вопросы о поведении системы через logs, metrics и traces.", "Сначала сформулируй вопрос, затем выбери signal и labels с контролируемой cardinality.", "Логировать secrets или использовать user_id как Prometheus label.", "По росту p95 при стабильной средней выбери следующие metrics и logs."),
    26: ("Django/DRF предоставляет batteries-included стек: ORM, migrations, admin, auth и API abstractions.", "Django project содержит configuration, apps группируют domain capability, DRF serializer задаёт API boundary.", "Путать select_related и prefetch_related или переносить FastAPI patterns дословно.", "Сравни request flow и data access одного endpoint в DRF и FastAPI."),
    27: ("Архитектура управляет зависимостями и стоимостью изменений; pattern полезен только при конкретной проблеме.", "Высокоуровневое правило не должно зависеть от детали storage/framework без необходимости.", "Добавлять repository/service слои без поведения и тем самым создавать pass-through boilerplate.", "Назови направление зависимости, seam для теста и ожидаемое изменение."),
    28: ("Для Junior backend важны базовые структуры и сложность реальных transformations, а не редкие олимпиадные трюки.", "Выбери структуру по операциям и оцени dominant time/space term.", "Писать O(n²), когда один dict даёт линейный проход, или оптимизировать без constraints.", "Реши задачу сначала корректно, затем назови complexity и граничные случаи."),
    29: ("Junior system design начинается с требований, request path, source of truth и failure modes.", "Сначала обеспечь корректность простого монолита; масштабируй измеренный bottleneck.", "Начинать с microservices, не определив нагрузку, consistency и ownership.", "Уточни traffic, consistency, latency и failure behavior перед схемой компонентов."),
    30: ("Инфраструктурные концепции нужны для понимания deploy, но не заменяют уверенный Python/backend фундамент.", "Proxy принимает traffic, application process выполняет код, managed services предоставляют инфраструктурные capabilities.", "Выдавать знакомство с kubectl за production Kubernetes experience.", "Опиши один честный deploy path и границы собственного опыта."),
    31: ("Сильный screening answer коротко связывает опыт с ролью и подтверждается конкретным действием кандидата.", "Используй STAR для поведения и context → decision → trade-off → verification для техники.", "Читать заученный список технологий без результата и личного вклада.", "Сформулируй ответ на 60–90 секунд и подготовь один проверяемый follow-up."),
    32: ("Resume Defense проверяет каждую заявленную технологию через конкретную роль в StudyHub, Hotel Booking или Share Recipe.", "Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.", "Приписывать себе production scale, AWS, Kubernetes, Kafka или RabbitMQ без фактического опыта.", "Защити один claim, назвав точный flow, failure mode и способ проверки."),
}

SOURCES = {
    0: [("Python Developer's Guide — communication", "https://devguide.python.org/")],
    1: [("Python Data Model", "https://docs.python.org/3.12/reference/datamodel.html"), ("Python execution model", "https://docs.python.org/3.12/reference/executionmodel.html")],
    2: [("Python built-in types", "https://docs.python.org/3.12/library/stdtypes.html")],
    3: [("Python function definitions", "https://docs.python.org/3.12/reference/compound_stmts.html#function-definitions"), ("functools", "https://docs.python.org/3.12/library/functools.html")],
    4: [("Iterator types", "https://docs.python.org/3.12/library/stdtypes.html#iterator-types"), ("Exceptions", "https://docs.python.org/3.12/tutorial/errors.html"), ("contextlib", "https://docs.python.org/3.12/library/contextlib.html")],
    5: [("Python Data Model", "https://docs.python.org/3.12/reference/datamodel.html"), ("dataclasses", "https://docs.python.org/3.12/library/dataclasses.html")],
    6: [("typing", "https://docs.python.org/3.12/library/typing.html")],
    7: [("gc", "https://docs.python.org/3.12/library/gc.html"), ("threading", "https://docs.python.org/3.12/library/threading.html")],
    8: [("asyncio", "https://docs.python.org/3.12/library/asyncio.html"), ("Coroutines and Tasks", "https://docs.python.org/3.12/library/asyncio-task.html")],
    9: [("concurrent.futures", "https://docs.python.org/3.12/library/concurrent.futures.html"), ("multiprocessing", "https://docs.python.org/3.12/library/multiprocessing.html")],
    10: [("PostgreSQL queries", "https://www.postgresql.org/docs/current/queries.html"), ("PostgreSQL functions", "https://www.postgresql.org/docs/current/functions.html")],
    11: [("PostgreSQL indexes", "https://www.postgresql.org/docs/current/indexes.html"), ("Concurrency control", "https://www.postgresql.org/docs/current/mvcc.html")],
    12: [("HTTP Semantics RFC 9110", "https://www.rfc-editor.org/rfc/rfc9110"), ("MDN HTTP", "https://developer.mozilla.org/en-US/docs/Web/HTTP")],
    13: [("OAuth 2.0 RFC 6749", "https://www.rfc-editor.org/rfc/rfc6749"), ("PKCE RFC 7636", "https://www.rfc-editor.org/rfc/rfc7636"), ("JWT RFC 7519", "https://www.rfc-editor.org/rfc/rfc7519")],
    14: [("FastAPI tutorial", "https://fastapi.tiangolo.com/tutorial/"), ("FastAPI dependencies", "https://fastapi.tiangolo.com/tutorial/dependencies/")],
    15: [("Pydantic models", "https://docs.pydantic.dev/2.11/concepts/models/"), ("Pydantic validators", "https://docs.pydantic.dev/2.11/concepts/validators/")],
    16: [("SQLAlchemy 2.0 Session", "https://docs.sqlalchemy.org/en/20/orm/session_basics.html"), ("ORM Querying Guide", "https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html")],
    17: [("Alembic tutorial", "https://alembic.sqlalchemy.org/en/latest/tutorial.html"), ("Autogenerate", "https://alembic.sqlalchemy.org/en/latest/autogenerate.html")],
    18: [("pytest documentation", "https://docs.pytest.org/en/stable/"), ("pytest fixtures", "https://docs.pytest.org/en/stable/how-to/fixtures.html")],
    19: [("Redis data types", "https://redis.io/docs/latest/develop/data-types/"), ("Redis caching", "https://redis.io/docs/latest/develop/use/client-side-caching/")],
    20: [("Celery tasks", "https://docs.celeryq.dev/en/stable/userguide/tasks.html"), ("Kafka concepts", "https://kafka.apache.org/documentation/#intro_concepts_and_terms")],
    21: [("Docker concepts", "https://docs.docker.com/get-started/docker-concepts/"), ("Compose reference", "https://docs.docker.com/reference/compose-file/")],
    22: [("Git reference", "https://git-scm.com/docs"), ("Pro Git", "https://git-scm.com/book/en/v2")],
    23: [("GNU Coreutils manual", "https://www.gnu.org/software/coreutils/manual/coreutils.html"), ("Bash manual", "https://www.gnu.org/software/bash/manual/")],
    24: [("GitHub Actions documentation", "https://docs.github.com/en/actions")],
    25: [("Prometheus concepts", "https://prometheus.io/docs/concepts/"), ("Grafana fundamentals", "https://grafana.com/docs/grafana/latest/fundamentals/"), ("Sentry concepts", "https://docs.sentry.io/concepts/")],
    26: [("Django documentation", "https://docs.djangoproject.com/en/5.2/"), ("Django REST Framework guide", "https://www.django-rest-framework.org/")],
    27: [("Python abc", "https://docs.python.org/3.12/library/abc.html"), ("FastAPI dependencies", "https://fastapi.tiangolo.com/tutorial/dependencies/")],
    28: [("Python collections", "https://docs.python.org/3.12/library/collections.html"), ("Sorting HOWTO", "https://docs.python.org/3.12/howto/sorting.html")],
    29: [("PostgreSQL high availability", "https://www.postgresql.org/docs/current/high-availability.html"), ("Redis architecture", "https://redis.io/docs/latest/operate/oss_and_stack/management/architecture/")],
    30: [("NGINX documentation", "https://nginx.org/en/docs/"), ("Kubernetes concepts", "https://kubernetes.io/docs/concepts/"), ("Terraform documentation", "https://developer.hashicorp.com/terraform/docs")],
    31: [("GitHub code review guide", "https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests")],
    32: [("FastAPI documentation", "https://fastapi.tiangolo.com/"), ("PostgreSQL documentation", "https://www.postgresql.org/docs/current/"), ("Redis documentation", "https://redis.io/docs/latest/")],
}

EXAMPLES = {
    1: ("python", "payload = {\"roles\": [\"reader\"]}\nalias = payload\nalias[\"roles\"].append(\"writer\")\nassert payload[\"roles\"] == [\"reader\", \"writer\"]"),
    2: ("python", "records = [{\"id\": 2}, {\"id\": 1}, {\"id\": 2}]\nby_id = {record[\"id\"]: record for record in records}\nordered = sorted(by_id.values(), key=lambda row: row[\"id\"] )"),
    3: ("python", "def list_users(limit: int = 20, *, active: bool | None = None) -> list[dict]:\n    \"\"\"Явный API: active нельзя передать случайно позиционно.\"\"\"\n    return []"),
    4: ("python", "from contextlib import contextmanager\n\n@contextmanager\ndef transaction(session):\n    try:\n        yield session\n        session.commit()\n    except Exception:\n        session.rollback()\n        raise"),
    5: ("python", "from dataclasses import dataclass\n\n@dataclass(frozen=True, slots=True)\nclass UserId:\n    value: int\n\n    def __post_init__(self):\n        if self.value <= 0:\n            raise ValueError(\"user id must be positive\")"),
    6: ("python", "from typing import Protocol\n\nclass UserReader(Protocol):\n    def get(self, user_id: int) -> dict | None: ...\n\ndef load_name(repo: UserReader, user_id: int) -> str | None:\n    user = repo.get(user_id)\n    return user[\"name\"] if user else None"),
    8: ("python", "import asyncio\n\nasync def load_pair(client):\n    first, second = await asyncio.gather(\n        client.get(\"/users/1\"),\n        client.get(\"/users/2\"),\n    )\n    return first, second"),
    9: ("python", "from concurrent.futures import ThreadPoolExecutor\n\nwith ThreadPoolExecutor(max_workers=4) as pool:\n    results = list(pool.map(read_remote_resource, urls))"),
    10: ("sql", "SELECT u.id, u.email, COUNT(o.id) AS orders_count\nFROM users AS u\nLEFT JOIN orders AS o ON o.user_id = u.id\nGROUP BY u.id, u.email\nORDER BY u.id;"),
    11: ("sql", "BEGIN;\nSELECT id FROM rooms WHERE id = 42 FOR UPDATE;\nINSERT INTO bookings(room_id, starts_at, ends_at) VALUES (42, $1, $2);\nCOMMIT;"),
    12: ("http", "PATCH /users/42 HTTP/1.1\nContent-Type: application/json\nIf-Match: \"user-v7\"\n\n{\"display_name\": \"Aida\"}"),
    13: ("python", "def can_edit(user, article) -> bool:\n    return user.id == article.author_id or \"moderator\" in user.roles"),
    14: ("python", "from typing import Annotated\nfrom fastapi import APIRouter, Depends\n\nrouter = APIRouter(prefix=\"/users\")\n\n@router.get(\"/{user_id}\")\ndef get_user(user_id: int, service: Annotated[UserService, Depends()]):\n    return service.get_or_404(user_id)"),
    15: ("python", "from pydantic import BaseModel, Field\n\nclass BookingCreate(BaseModel):\n    room_id: int = Field(gt=0)\n    guests: int = Field(ge=1, le=8)"),
    16: ("python", "from sqlalchemy import select\nfrom sqlalchemy.orm import selectinload\n\nstatement = (\n    select(User)\n    .options(selectinload(User.roles))\n    .where(User.active.is_(True))\n)\nusers = session.scalars(statement).all()"),
    17: ("bash", "alembic revision --autogenerate -m \"add booking status\"\nalembic upgrade head\nalembic current"),
    18: ("python", "import pytest\n\n@pytest.mark.parametrize((\"value\", \"expected\"), [(0, False), (1, True)])\ndef test_is_positive(value, expected):\n    assert is_positive(value) is expected"),
    19: ("text", "GET cache:user:42 → miss\nSELECT user FROM PostgreSQL\nSET cache:user:42 value EX 60\nUPDATE user → COMMIT → DEL cache:user:42"),
    20: ("python", "def handle(message, repository):\n    if repository.was_processed(message.id):\n        return\n    repository.apply(message.payload)\n    repository.mark_processed(message.id)"),
    21: ("dockerfile", "FROM python:3.12-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nCMD [\"python\", \"-m\", \"app\"]"),
    22: ("bash", "git status\ngit add backend/app.py tests/test_app.py\ngit commit -m \"fix booking conflict handling\"\ngit push -u origin fix/booking-conflict"),
    23: ("bash", "ps aux | rg uvicorn\nss -ltnp | rg 8000\ntail -n 100 /var/log/app.log\nprintf '%s\\n' \"$APP_ENV\""),
    24: ("yaml", "steps:\n  - run: python -m pytest\n  - run: ruff check .\n  - run: docker build -t app:${GITHUB_SHA} ."),
    25: ("python", "logger.info(\n    \"booking_created\",\n    extra={\"booking_id\": booking.id, \"request_id\": request_id},\n)"),
    26: ("python", "queryset = (\n    Order.objects\n    .select_related(\"user\")\n    .prefetch_related(\"items\")\n    .filter(status=Order.Status.PAID)\n)"),
    27: ("python", "class BookingService:\n    def __init__(self, repository, clock):\n        self.repository = repository\n        self.clock = clock\n\n    def cancel(self, booking_id):\n        booking = self.repository.get(booking_id)\n        booking.cancel(at=self.clock.now())"),
    28: ("python", "def deduplicate(values):\n    seen = set()\n    return [value for value in values if not (value in seen or seen.add(value))]"),
    29: ("text", "Client → reverse proxy → FastAPI → service → PostgreSQL\n                                  ↘ Redis\n                                  ↘ outbox → worker"),
    30: ("nginx", "location /api/ {\n    proxy_pass http://api:8000;\n    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n}"),
    32: ("text", "Проблема → моё решение → почему так → failure mode → как проверил\nГраница опыта → что изучил бы перед production rollout"),
}

POINT_EXPLANATIONS = [
    ("apirouter", "`APIRouter` группирует связанные path operations и их общие prefix, tags или dependencies; router подключают к приложению через `include_router`, не создавая второе приложение."),
    ("path operation", "Path operation связывает HTTP method и path с Python callable; FastAPI строит validation/dependency graph при регистрации route и вызывает handler для подходящего request."),
    ("response model", "Response model задаёт внешний контракт, выполняет serialization/validation результата и не должна случайно раскрывать внутренние ORM-поля."),
    ("dependency", "Dependency объявляет вход handler/service явно; FastAPI разрешает graph зависимостей на request, cache-ит результат в его рамках и выполняет cleanup yield-dependency."),
    ("lifespan", "Lifespan управляет ресурсами уровня приложения: код до `yield` создаёт client/pool, код после `yield` гарантированно закрывает их при shutdown."),
    ("middleware", "Middleware оборачивает весь ASGI request/response flow; оно подходит для cross-cutting concern, но не должно прятать доменную авторизацию."),
    ("prefix", "Router prefix добавляется ко всем путям группы и позволяет собирать модульный API без повторения `/users` или `/v1` в каждом decorator."),
    ("decorator", "Decorator получает callable и возвращает callable; для framework route decorator также регистрирует функцию и её metadata во время импорта модуля."),
    ("type hint", "Type hint описывает контракт для checker/IDE; обычный Python не запрещает другое runtime-значение, а FastAPI/Pydantic отдельно используют annotation для schema и validation."),
    ("optional", "`T | None` разрешает значение `None`, но не делает аргумент или поле необязательным без default; missing и explicit null — разные состояния."),
    ("typeddict", "`TypedDict` описывает статическую форму обычного dict и не создаёт runtime validation; required/NotRequired keys проверяет type checker."),
    ("protocol", "`Protocol` задаёт structural contract: объект подходит по доступным методам и атрибутам, даже без наследования от общего base class."),
    ("generic", "`Generic` связывает типы входа и результата через type variable, чтобы checker сохранял конкретный тип вместо потери информации в `Any`."),
    ("identity", "Identity отвечает на вопрос «тот же ли это объект» и сравнивается через `is`; равенство — отдельный протокол `__eq__`, обычно сравнивающий значения."),
    ("binding", "Binding — связь имени с объектом в namespace; assignment меняет связь имени, а mutation меняет состояние уже связанного объекта."),
    ("truthiness", "Truthiness определяется `__bool__`, затем `__len__`, а при отсутствии обоих объект считается truthy; это протокол, не проверка типа."),
    ("shallow copy", "Shallow copy создаёт новый внешний container, но сохраняет references на вложенные объекты; поэтому nested mutation может быть общей."),
    ("deep copy", "`deepcopy` рекурсивно копирует object graph с memo для циклов, но ownership и ресурсы часто требуют явной domain-specific копии."),
    ("encoding", "Текстовый `str` хранит Unicode, а `bytes` — конкретные байты; encode/decode всегда выполняют на явной границе с выбранной encoding и error policy."),
    ("list", "`list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations."),
    ("tuple", "`tuple` — immutable sequence; hashability зависит от всех элементов, а неизменяемость контейнера не делает mutable элементы неизменяемыми."),
    ("dict", "`dict` хранит mapping hashable keys к values и сохраняет insertion order; lookup в среднем O(1), но correctness опирается на equality/hash contract."),
    ("frozenset", "`frozenset` — immutable hashable set и подходит как key или элемент другого set, если требуется множество без mutations."),
    ("comprehension", "Comprehension создаёт новую коллекцию из явного source/filter/expression; nested comprehensions стоит заменять обычным циклом, когда теряется читаемость."),
    ("sorting", "Python sort стабилен и использует key один раз на элемент; `sorted` создаёт новый list, а `.sort()` меняет существующий и возвращает `None`."),
    ("signature", "Signature — публичный контракт вызова: kinds параметров, defaults и annotations определяют допустимые positional/keyword arguments и помогают introspection."),
    ("positional-only", "Параметры до `/` нельзя передавать по имени; это позволяет сохранить внутреннее имя параметра вне публичного API."),
    ("keyword-only", "Параметры после `*` требуют явного имени и уменьшают риск перепутать несколько flags или числовых аргументов."),
    ("*args", "`*args` собирает лишние positional arguments в tuple, а `**kwargs` — keyword arguments в dict; они не должны скрывать неясный публичный контракт."),
    ("scope", "LEGB ищет имя в local, enclosing, global и builtins; assignment делает имя local, если не объявлены `global` или `nonlocal`."),
    ("closure", "Closure хранит ссылки на enclosing bindings, а не snapshot каждого значения; late binding особенно заметен в callbacks, созданных в цикле."),
    ("functools.wraps", "`functools.wraps` переносит metadata и `__wrapped__`, чтобы introspection, FastAPI и отладка видели исходную функцию."),
    ("iterable", "Iterable умеет создать iterator через `__iter__`; один iterable может создавать новые независимые iterators для повторных обходов."),
    ("stopiteration", "`StopIteration` — внутренний сигнал исчерпания iterator; consumer вроде `for` перехватывает его и завершает цикл."),
    ("yield from", "`yield from` делегирует значения и часть generator protocol вложенному iterator, включая завершение и возвращаемое значение."),
    ("finally", "`finally` выполняет cleanup при normal return и exception; он не должен без необходимости подавлять исходную ошибку новым return/raise."),
    ("raise from", "`raise ... from exc` сохраняет причинную цепочку в `__cause__`, добавляя domain context без потери исходной диагностики."),
    ("context manager", "Context manager заключает acquire/use/release в `with`; `__exit__` получает exception info и подавляет ошибку только при truthy return."),
    ("class attribute", "Class attribute разделяется instances до тех пор, пока instance не перекроет имя; mutable class state часто создаёт утечку между объектами."),
    ("classmethod", "`classmethod` получает класс и подходит для альтернативного constructor или polymorphic class-level behavior; `staticmethod` не получает implicit receiver."),
    ("inheritance", "Inheritance выражает отношение is-a и участвует в MRO; если нужно только переиспользовать collaborator, composition обычно делает зависимость яснее."),
    ("composition", "Composition передаёт объекту collaborators явно и позволяет заменять их независимо, не связывая доменные типы общей иерархией."),
    ("mro", "MRO задаёт детерминированный порядок поиска атрибутов при multiple inheritance; `super()` продолжает поиск по MRO фактического класса."),
    ("dataclass", "`dataclass` генерирует init/repr/equality по объявленным fields; mutable defaults задают через `default_factory`, а invariants — в `__post_init__`."),
    ("__slots__", "`__slots__` ограничивает набор instance attributes и может уменьшить memory, но усложняет inheritance/weakrefs и не является универсальной оптимизацией."),
    ("descriptor", "Descriptor с `__get__`/`__set__` управляет attribute access на уровне класса; `property`, methods и многие ORM fields построены на этом protocol."),
    ("metaclass", "Metaclass создаёт class object и может проверять/изменять class namespace; для большинства registration hooks проще `__init_subclass__`."),
    ("reference counting", "CPython уменьшает reference count при исчезновении binding и обычно освобождает объект на нуле; cycles отдельно находит cyclic GC."),
    ("weak reference", "Weak reference наблюдает объект, не продлевая lifetime; после удаления сильных references обращение возвращает `None`."),
    ("gil", "CPython GIL допускает выполнение Python bytecode одним thread за раз, но отпускается вокруг части I/O/native calls и не защищает бизнес-инварианты от races."),
    ("event loop", "Event loop запускает ready callbacks/tasks и ждёт I/O; cooperative task уступает управление только в await point."),
    ("coroutine", "Вызов `async def` создаёт coroutine object; код начнёт выполняться при await или scheduling как Task."),
    ("taskgroup", "`TaskGroup` задаёт structured concurrency: scope ждёт дочерние tasks, отменяет siblings при ошибке и возвращает grouped failures."),
    ("gather", "`gather` запускает awaitables конкурентно и сохраняет порядок результатов по входу; failure/cancellation policy нужно выбирать явно."),
    ("semaphore", "Semaphore ограничивает число одновременных операций, защищая downstream/pool; это backpressure, а не гарантия скорости."),
    ("thread", "Threads разделяют память процесса и удобны для blocking I/O, но shared mutable state требует synchronization и корректной lifetime management."),
    ("process", "Processes изолируют память и подходят для CPU-bound Python, но требуют serialization/IPC и имеют более дорогой startup."),
    ("select", "`SELECT` формирует result columns после FROM/JOIN/WHERE/GROUP/HAVING; порядок строк существует только при явном `ORDER BY`."),
    ("where", "`WHERE` фильтрует строки до grouping; SQL three-valued logic отбрасывает и `FALSE`, и `UNKNOWN`."),
    ("having", "`HAVING` фильтрует сформированные группы и aggregates, тогда как `WHERE` отбирает исходные строки до `GROUP BY`."),
    ("exists", "`EXISTS` проверяет наличие хотя бы одной строки correlated subquery и часто прямо выражает semi-join без размножения строк."),
    ("window", "Window function считает значение по partition, не сворачивая строки как GROUP BY; порядок внутри `OVER` задаёт frame/ranking semantics."),
    ("constraint", "Constraint хранит invariant рядом с данными и защищает его от всех writers; API переводит conflict в понятную domain/HTTP error."),
    ("foreign key", "Foreign key запрещает reference на отсутствующую parent row и требует осознанной политики update/delete, индексов и transaction order."),
    ("mvcc", "MVCC даёт statements snapshot версий строк; locks и isolation level определяют, какие concurrent anomalies возможны."),
    ("explain", "`EXPLAIN (ANALYZE, BUFFERS)` сравнивает estimates с фактическими rows/time/I/O; запуск ANALYZE действительно выполняет statement."),
    ("status code", "Status code сообщает результат HTTP operation: 2xx success, 4xx client/request state, 5xx server failure; error body добавляет стабильный machine-readable code."),
    ("http method", "Method задаёт semantics запроса; safety/idempotency описывают повторяемость намерения, а не наличие body или выбранный framework."),
    ("authentication", "Authentication устанавливает identity, authorization проверяет право этой identity выполнить конкретное действие над resource."),
    ("authorization", "Authorization выполняется server-side на каждом resource/action и не заменяется скрытой кнопкой, CORS или данными из непроверенного token."),
    ("oauth", "OAuth 2.0 делегирует authorization клиенту через tokens; Authorization Code + PKCE связывает code exchange с инициировавшим public client."),
    ("pkce", "PKCE отправляет challenge в authorize request и verifier при token exchange, поэтому перехваченного code недостаточно без verifier."),
    ("sql injection", "SQL injection появляется при смешивании данных и SQL syntax; параметры передают отдельно через driver/ORM expression, а не экранируют вручную."),
    ("csrf", "CSRF использует автоматически отправляемые browser credentials; защита включает SameSite и CSRF token/origin checks для state-changing requests."),
    ("xss", "XSS исполняет attacker-controlled script в origin приложения; защита начинается с contextual escaping, safe templates и ограничения unsafe HTML."),
    ("basemodel", "Pydantic `BaseModel` превращает недоверенный input в типизированный объект по core schema; validation errors относятся к границе входа, не бизнес-правилам."),
    ("field validator", "Field validator проверяет/нормализует отдельное поле в выбранном mode; cross-field invariant обычно понятнее в model validator."),
    ("model_dump", "`model_dump` управляет serialization validated model, aliases и include/exclude; это явная граница между внутренней моделью и response payload."),
    ("engine", "SQLAlchemy Engine владеет dialect и connection pool; Session запрашивает connection по необходимости и возвращает её после завершения transaction."),
    ("flush", "Flush синхронизирует pending ORM state с БД внутри текущей transaction и получает generated values, но не делает изменения durable как commit."),
    ("rollback", "Rollback отменяет текущую transaction и возвращает Session в usable state; после flush error продолжать без rollback нельзя."),
    ("n+1", "N+1 возникает, когда список загружается одним query, а relationship каждого объекта — отдельным; query-count test и eager-loading делают проблему видимой."),
    ("selectinload", "`selectinload` делает отдельный batched query по parent keys и обычно подходит для one-to-many без размножения parent rows."),
    ("joinedload", "`joinedload` загружает relationship через JOIN; для collections он размножает SQL rows и требует учитывать cardinality/`unique()`."),
    ("alembic", "Alembic хранит последовательность revision scripts; autogenerate предлагает diff metadata/schema, который нужно review и проверить upgrade/downgrade."),
    ("pytest", "pytest test должен проверять observable contract; fixtures управляют setup/cleanup, parametrization — cases, а mocks изолируют только внешнюю границу."),
    ("redis", "Redis хранит данные в памяти и полезен для cache/TTL/atomic counters, но durability, eviction и outage policy нужно проектировать явно."),
    ("container", "Container — изолированный process из image, а не VM; сеть, environment и persistent volumes задаются отдельно при runtime."),
    ("depends_on", "Compose `depends_on` задаёт порядок запуска, но readiness требует healthcheck или retry до фактической готовности dependency."),
    ("rebase", "Rebase переносит commits на новую base и меняет их hashes; published shared history без координации переписывать нельзя."),
    ("git reset", "`reset` двигает local branch/index/working tree в зависимости от mode; опубликованную ошибку безопаснее исправлять новым `revert` commit."),
    ("null", "`NULL` означает отсутствие известного значения; сравнение с ним делают через `IS NULL`, а многие выражения дают `UNKNOWN`."),
    ("idempot", "Идемпотентность означает, что повтор одного логического запроса не создаёт новый эффект; обычно её поддерживают ключом и ограничением уникальности."),
    ("transaction", "Transaction задаёт атомарную границу: либо все связанные изменения становятся видимыми, либо выполняется rollback."),
    ("index", "Index — отдельная структура доступа с ценой записи и хранения; полезность зависит от конкретного predicate, ordering и selectivity."),
    ("await", "`await` приостанавливает текущую coroutine и отдаёт управление event loop, пока awaitable не станет готов."),
    ("cancel", "Cancellation — управляющий сигнал: cleanup выполняют в `finally`, а отмену обычно не поглощают без веской причины."),
    ("session", "Session владеет identity map и transaction state; после ошибки flush требуется rollback до дальнейшей работы."),
    ("cache", "Для cache заранее определяют key, TTL, invalidation и fallback, иначе ускорение создаёт stale-data bug."),
    ("lock", "Lock сериализует критическую секцию, но корректность требует единого порядка захвата и короткого времени удержания."),
    ("join", "JOIN соединяет строки по условию и может изменить cardinality; перед SELECT полезно оценить связь one-to-one/one-to-many."),
    ("group", "GROUP BY формирует группы до вычисления aggregates, а HAVING фильтрует уже агрегированные группы."),
    ("jwt", "JWT подписан, но обычно не зашифрован; сервер обязан проверить signature, issuer, audience и время действия."),
    ("password", "Пароль хранят через специализированный медленный password hash с солью, а не через быстрый общий hash."),
    ("docker", "Container запускает изолированный process из image; данные вне writable layer сохраняют в volume."),
    ("fixture", "Fixture создаёт dependency теста и управляет cleanup; scope выбирают по требуемой изоляции, а не ради скорости любой ценой."),
    ("mock", "Mock ставят в namespace использования и проверяют только значимое взаимодействие с внешней границей."),
    ("generator", "Generator хранит suspended execution frame и выдаёт значения лениво; после исчерпания он не перезапускается."),
    ("iterator", "Iterator возвращает себя из `__iter__` и сигнализирует завершение через `StopIteration`."),
    ("mutable", "Mutable объект меняется с сохранением identity, поэтому alias наблюдает ту же мутацию."),
    ("hash", "Равные hashable-объекты обязаны иметь одинаковый hash, а состояние, влияющее на equality, не должно меняться в ключе."),
    ("cors", "CORS ограничивает чтение response браузерным frontend и не заменяет server-side authentication/authorization."),
    ("retry", "Retry подходит для transient failure, ограничивается числом попыток и backoff с jitter; permanent errors нужно возвращать сразу."),
    ("websocket", "WebSocket держит долгоживущее соединение; масштабирование требует shared fan-out, а durable history хранится отдельно."),
    ("pub/sub", "Redis Pub/Sub доставляет только активным subscribers и не является durable очередью или историей."),
    ("coverage", "Coverage показывает исполненные строки/ветки, но не доказывает качество assertions и полноту failure scenarios."),
]

STAGE_POINT_FALLBACKS = {
    0: "Зафиксируй, какую способность оценивает пункт `{point}`, и подготовь короткое доказательство из своего кода вместо перечисления терминов.",
    1: "Для `{point}` проследи конкретный object, его type/identity и все bindings до и после операции.",
    2: "Для `{point}` назови поддерживаемые операции, порядок, уникальность, mutability и стоимость ключевого доступа.",
    3: "Для `{point}` отдели definition time от call time и покажи влияние на signature, scope или state функции.",
    4: "Для `{point}` опиши protocol: кто инициирует шаг, какое состояние сохраняется, как выглядит завершение и error path.",
    5: "Для `{point}` укажи, где хранится state, как Python ищет behavior и почему выбран composition/inheritance.",
    6: "Для `{point}` покажи, что видит static checker, что реально происходит runtime и где нужна отдельная validation.",
    7: "Для `{point}` отдели гарантию Python от детали CPython и сначала измерь lifetime, allocations или contention.",
    8: "Для `{point}` проследи coroutine/task по await points, cancellation и cleanup, не предполагая отдельный thread.",
    9: "Для `{point}` сравни shared memory, serialization, startup cost и подходящий I/O/CPU workload.",
    10: "Для `{point}` сначала определи grain/cardinality результата, затем NULL и ordering semantics.",
    11: "Для `{point}` назови защищаемый invariant, concurrent transaction и evidence из constraint или query plan.",
    12: "Для `{point}` зафиксируй observable HTTP contract: request semantics, response status/body и повтор запроса.",
    13: "Для `{point}` назови threat, trust boundary, server-side check и безопасный failure response.",
    14: "Для `{point}` проследи request через router, validation/dependencies, handler/service и response serialization.",
    15: "Для `{point}` различай missing, explicit null, invalid input и serialized output Pydantic v2.",
    16: "Для `{point}` укажи Session/transaction owner, момент SQL I/O и последствия rollback или lazy load.",
    17: "Для `{point}` опиши проверяемый schema transition и отдельно риски upgrade, deploy compatibility и rollback.",
    18: "Для `{point}` сформулируй observable contract, isolation boundary и failure, который обязан поймать test.",
    19: "Для `{point}` определи Redis key/value, TTL, invalidation, concurrency и fallback при outage.",
    20: "Для `{point}` проследи delivery от commit до side effect, включая duplicate, retry и idempotency.",
    21: "Для `{point}` раздели image/build-time и container/runtime, затем проверь DNS, ports, mounts и lifecycle.",
    22: "Для `{point}` сначала назови изменяемое состояние Git: working tree, index, branch pointer или shared history.",
    23: "Для `{point}` свяжи command с конкретным process, file, permission, environment или network symptom.",
    24: "Для `{point}` определи reproducible quality gate, trigger, artifact и безопасное управление secret.",
    25: "Для `{point}` укажи сигнал, labels/context, способ correlation и действие инженера по наблюдаемому symptom.",
    26: "Для `{point}` сопоставь Django/DRF abstraction с request, ORM query count, validation и permissions.",
    27: "Для `{point}` проведи границу слоя и dependency direction, затем покажи test без реальной инфраструктуры.",
    28: "Для `{point}` назови input constraints, data structure, complexity и boundary cases до написания кода.",
    29: "Для `{point}` начни с requirements/source of truth и только затем добавляй component под измеримый failure mode.",
    30: "Для `{point}` объясни роль в deploy path и честно отдели знакомство с концепцией от production operation.",
    31: "Для `{point}` подготовь ответ на 60–90 секунд: context, личное действие, результат и проверяемый follow-up.",
    32: "Для `{point}` отвечай только по реализованному flow: проблема, своё решение, trade-off, failure mode и test/metric.",
}


def existing_directories() -> dict[str, Path]:
    result: dict[str, Path] = {}
    for path in CONTENT.glob("*/*/metadata.json"):
        metadata = json.loads(path.read_text(encoding="utf-8"))
        result[metadata["slug"]] = path.parent
    return result


def explain_point(point: str, guide: tuple[str, str, str, str], stage_number: int) -> str:
    lowered = point.lower()
    for keyword, explanation in POINT_EXPLANATIONS:
        if keyword in lowered:
            return explanation
    return STAGE_POINT_FALLBACKS[stage_number].format(point=point.rstrip("."))


def extract_existing(path: Path) -> tuple[str | None, str | None]:
    metadata_path = path / "metadata.json"
    if not metadata_path.exists():
        return None, None
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    lesson_path = path / "lesson.md"
    if not lesson_path.exists():
        return None, None
    text = lesson_path.read_text(encoding="utf-8")
    is_seed = metadata.get("slug") in PRESERVE_TASKS
    if metadata.get("generated_by") == "populate_curriculum.py" and (not is_seed or "## Learning objectives" in text):
        return None, None
    if "Материал урока пока не добавлен" in text or "Задача будет добавлена позже" in text:
        return None, None
    text = re.sub(r"^# .+?\n+", "", text, count=1)
    task_match = re.search(r"(?:^|\n)## Задача\n+(.*?)(?=\n## [^\n]+|\Z)", text, re.DOTALL)
    theory = re.split(r"(?:^|\n)## Задача\n", text, maxsplit=1)[0].strip()
    # Existing seed lessons become a subsection of the normalized Theory block.
    theory = re.sub(r"^(#{2,}) ", lambda match: "#" + match.group(1) + " ", theory, flags=re.MULTILINE)
    task = task_match.group(1).strip() if task_match else None
    return theory or None, task


def lesson_markdown(lesson: dict, stage: dict, existing_theory: str | None, existing_task: str | None) -> str:
    stage_number = stage["number"]
    guide = STAGE_GUIDES[stage_number]
    outline = lesson.get("outline") or [lesson["title"]]
    objectives = outline[:3]
    sources = SOURCES[stage_number]
    theory = existing_theory or "\n\n".join(
        [guide[0], f"В теме **{lesson['title']}** важно уверенно объяснять следующие части:"]
        + [f"### {point.rstrip('.')}\n\n{explain_point(point, guide, stage_number)}" for point in outline[:7]]
    )
    example = EXAMPLES.get(stage_number)
    example_block = (
        f"```{example[0]}\n{example[1]}\n```\n\nРазбирая пример, проговори вход, наблюдаемый результат, скрытое состояние и failure path."
        if example
        else "Сформулируй минимальный пример из текущего проекта: один happy path, одна граница и одна ошибка. Не добавляй инфраструктуру, не относящуюся к механизму."
    )
    task = existing_task or (
        f"Разбери backend-сценарий: **{guide[3]}**\n\n"
        "Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. "
        "Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса."
    )
    answer_points = outline[:4] + [guide[1]]
    source_lines = "\n".join(f"- [{name}]({url})" for name, url in sources)
    outline_lines = "\n".join(f"- {item}" for item in outline[:8])
    objective_lines = "\n".join(
        [f"- объяснить `{item}` своими словами и связать с backend-сценарием;" for item in objectives]
        + ["- распознать типичную ошибку и предложить проверяемое исправление."]
    )
    answer_lines = "\n".join(f"- {item}" for item in answer_points)
    return f"""# {lesson['title']}

> [!IMPORTANT]
> **{lesson['priority']} · вероятность на интервью: {lesson['interview_probability']} · {lesson['estimated_minutes']} минут.** {lesson['market_evidence']}

## Learning objectives

После урока ты сможешь:

{objective_lines}

## Theory

{theory}

## Mental model

{guide[1]}

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

{example_block}

## Common mistakes

**Ошибка:** {guide[2]}

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **{lesson['title']}** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: {guide[3]} Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

{answer_lines}

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- {guide[2]}
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

{outline_lines}

## Задача

{task}

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **{lesson['title']}**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

{source_lines}

Последняя проверка версий: **{lesson['last_verified']}**.
"""


def interview_questions(lesson: dict, stage: dict) -> list[dict]:
    guide = STAGE_GUIDES[stage["number"]]
    outline = lesson.get("outline") or [lesson["title"]]
    answer = outline[:4] + [guide[1]]
    common = [guide[2], "Ответ без механизма, примера и ограничения"]
    sets = [stage["slug"], "full-junior-backend"]
    if lesson["priority"] in {"P0", "P1"}:
        sets.append("interview-crash-course")
    if stage["number"] == 32:
        sets.append("resume-defense")
    return [
        {
            "question": f"Объясни тему «{lesson['title']}» как на Junior Python Backend interview.",
            "level": "normal",
            "priority": lesson["priority"],
            "interview_probability": lesson["interview_probability"],
            "answer": answer,
            "expected_answer": {
                "must_mention": answer,
                "good_additions": ["конкретный backend example", "trade-off или failure mode"],
                "common_wrong_answers": common,
                "red_flags": [guide[2]],
                "follow_up_questions": [guide[3]],
            },
            "follow_ups": [guide[3]],
            "tags": [stage["slug"], lesson["priority"].lower()],
            "sets": sets,
        },
        {
            "question": f"Сценарий по теме «{lesson['title']}»: {guide[3]} Что проверишь первым?",
            "level": "scenario",
            "priority": lesson["priority"],
            "interview_probability": lesson["interview_probability"],
            "answer": ["Уточнить требования и observable symptom", guide[1], "Назвать edge case", "Предложить test/log/metric для проверки"],
            "expected_answer": {
                "must_mention": ["assumptions", "mechanism", "failure mode", "verification"],
                "good_additions": ["альтернатива и trade-off"],
                "common_wrong_answers": ["Сразу называть технологию до уточнения проблемы"],
                "red_flags": [guide[2]],
                "follow_up_questions": ["Что произойдёт при повторе или частичном отказе?"],
            },
            "follow_ups": ["Что произойдёт при повторе или частичном отказе?"],
            "tags": [stage["slug"], "scenario"],
            "sets": sets,
        },
    ]


def metadata_for(lesson: dict, stage: dict, slug: str, order: int, has_task: bool, has_solution: bool) -> dict:
    outline = lesson.get("outline") or [lesson["title"]]
    return {
        "id": lesson["id"],
        "slug": slug,
        "title": lesson["title"],
        "module_slug": stage["slug"],
        "module_title": f"Stage {stage['number']} · {stage['title']}",
        "module_order": stage["number"],
        "order": order,
        "duration": lesson["estimated_minutes"],
        "estimated_minutes": lesson["estimated_minutes"],
        "xp": 25 if has_task else 5,
        "topics": outline[:8],
        "description": f"{lesson['priority']} · {lesson['title']}: mental model, interview rubric и backend-сценарий.",
        "has_task": has_task,
        "has_solution": has_solution,
        "priority": lesson["priority"],
        "priority_note": lesson["priority_note"],
        "interview_probability": lesson["interview_probability"],
        "market_frequency": lesson["market_frequency"],
        "market_evidence": lesson["market_evidence"],
        "priority_basis": lesson["priority_basis"],
        "why_it_matters": f"Помогает объяснить {lesson['title']} и применить тему без типичной backend-ошибки.",
        "difficulty": lesson["difficulty"],
        "prerequisites": lesson["prerequisites"],
        "modes": lesson["modes"],
        "tracks": lesson["tracks"],
        "content_status": lesson["content_status"],
        "last_verified": lesson["last_verified"],
        "generated_by": "populate_curriculum.py",
    }


def main() -> None:
    curriculum = json.loads(CURRICULUM.read_text(encoding="utf-8"))
    directories = existing_directories()
    active_slugs: set[str] = set()
    order = 0
    published = 0
    planned = 0
    for stage in curriculum["stages"]:
        for lesson in stage["lessons"]:
            order += 1
            mapped_slug = EXISTING_MAP.get(lesson["number"])
            if mapped_slug:
                lesson["implementation_slug"] = mapped_slug
                directory = directories[mapped_slug]
                slug = mapped_slug
            else:
                slug = lesson["slug"]
                directory = CONTENT / stage["slug"] / slug
                lesson["implementation_slug"] = slug
            active_slugs.add(slug)
            directory.mkdir(parents=True, exist_ok=True)
            if lesson["content_status"] == "planned":
                planned += 1
                metadata = metadata_for(lesson, stage, slug, order, False, False)
                (directory / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                continue

            published += 1
            existing_theory, existing_task = extract_existing(directory)
            has_preserved_task = slug in PRESERVE_TASKS and (directory / "tests").exists()
            metadata = metadata_for(lesson, stage, slug, order, has_preserved_task, has_preserved_task)
            (directory / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            lesson_path = directory / "lesson.md"
            preserve_seed_lesson = (
                has_preserved_task
                and lesson_path.exists()
                and "## Learning objectives" in lesson_path.read_text(encoding="utf-8")
            )
            if not preserve_seed_lesson:
                lesson_path.write_text(
                    lesson_markdown(lesson, stage, existing_theory, existing_task), encoding="utf-8"
                )
            (directory / "interview.json").write_text(
                json.dumps(interview_questions(lesson, stage), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            starter = directory / "starter" / "main.py"
            if not starter.exists():
                starter.parent.mkdir(parents=True, exist_ok=True)
                starter.write_text(
                    f'"""Практическая заметка к уроку: {lesson["title"]}."""\n\n# Автоматическая coding-задача для этого урока не требуется.\n',
                    encoding="utf-8",
                )

    # Old URLs stay loadable, while unmapped placeholders no longer clutter navigation.
    for slug, directory in directories.items():
        if slug in active_slugs:
            continue
        metadata_path = directory / "metadata.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata["content_status"] = "archived"
        metadata["archive_reason"] = "Replaced by the backend-interview taxonomy; slug kept for saved progress compatibility."
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    CURRICULUM.write_text(json.dumps(curriculum, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Published {published} P0/P1 lessons; registered {planned} planned P2/P3 lessons")


if __name__ == "__main__":
    main()
