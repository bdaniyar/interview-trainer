"""Topic-specific learning copy for the curriculum publisher.

The module deliberately separates teaching material from taxonomy metadata.
Every published lesson gets a Learn flow; high-frequency Junior topics can
override the generic stage-aware material with a reviewed dossier below.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, replace


@dataclass(frozen=True)
class LessonDossier:
    what: str
    mechanism: str
    nuance: str
    backend: str | None
    mistakes: tuple[str, ...]
    required: tuple[str, ...]
    useful: tuple[str, ...]
    skip_deep: tuple[str, ...]
    practices: tuple[str, ...]
    question: str
    short_answer: str
    junior_answer: str
    follow_up_question: str
    follow_up_answer: str
    example: str = ""
    rubric: tuple[str, ...] = field(default_factory=tuple)


# Термины языка и имена API остаются без перевода внутри `inline code`, но
# обычный объясняющий текст должен быть русским. Учебный план исторически
# хранит названия подтем на английском, поэтому генератор нормализует их перед
# публикацией, а не заставляет читателя разбирать смешанные предложения.
PROSE_TRANSLATIONS = {
    "malformed request vs semantically invalid/validation": "синтаксически некорректный запрос и семантическая ошибка валидации",
    "server-selected vs client-known resource identifier": "идентификатор ресурса выбирает сервер или заранее знает клиент",
    "alternatives: async client,": "альтернативы: асинхронный клиент,",
    "worker/process": "отдельный обработчик или процесс",
    "dependency/version/env/timezone/order differences": "различия зависимостей, версий, окружения, часового пояса и порядка выполнения",
    "publish before commit may process rolled-back state": "публикация до фиксации транзакции может обработать состояние, которое затем будет отменено",
    "business change and outbox row in one transaction": "бизнес-изменение и запись outbox в одной транзакции",
    "runs after response in same application process": "выполняется после ответа в том же процессе приложения",
    "avoid commits hidden across repository calls": "избегать скрытой фиксации транзакции внутри вызовов репозитория",
    "GIL is not a general lock for application data": "GIL не является общей блокировкой данных приложения",
    "business row + outbox row in one DB transaction": "бизнес-запись и запись outbox в одной транзакции БД",
    "async only when dependency stack benefits": "асинхронность нужна, только когда от неё выигрывает весь стек зависимостей",
    "event loop serves other work while waiting": "цикл событий выполняет другую работу во время ожидания",
    "CPU-bound pure Python → process pool/worker": "вычислительный код на чистом Python → пул процессов или отдельный обработчик",
    "Repository, working tree, index and commit": "репозиторий, рабочее дерево, индекс и коммит",
    "WebSocket connects client to one process": "WebSocket соединяет клиента с одним процессом",
    "backend bugs with": "ошибки backend-кода со значениями",
    "and empty collections": "и пустыми коллекциями",
    "one parent query plus per-row child query": "один запрос родительских строк и отдельный дочерний запрос для каждой строки",
    "refresh/password reset/rate-limit state": "состояние обновления токена, сброса пароля и ограничения частоты запросов",
    "state/redirect validation still needed": "проверка параметра state и адреса перенаправления всё ещё обязательна",
    "service-to-service uses container port": "обращение между сервисами использует порт контейнера",
    "short-lived one-time state/hashed token": "короткоживущее одноразовое состояние или хешированный токен",
    "threadpool behavior for sync endpoint": "поведение пула потоков для синхронного эндпоинта",
    "DB constraint/conditional write/lock": "ограничение БД, условная запись или блокировка",
    "FastAPI/Pydantic use hints at runtime": "FastAPI и Pydantic используют аннотации во время выполнения",
    "connection/session/client lifecycle": "жизненный цикл соединения, сессии или клиента",
    "do not casually rebase shared history": "не переписывать общую историю через rebase без координации",
    "reviewing behavior, not personality": "обсуждение поведения, а не личности",
    "CPU-heavy work must leave event loop": "тяжёлые вычисления нельзя выполнять в цикле событий",
    "debug/info/warning/error/exception": "уровни `debug`, `info`, `warning`, `error` и `exception`",
    "do not mock implementation details": "не подменять внутренние детали реализации",
    "shared client/pool initialization": "инициализация общего клиента или пула",
    "shared mutable class attribute bug": "ошибка общего изменяемого атрибута класса",
    "split only for measured CPU/problem/organizational boundary": "разделение оправдано только измеренной нагрузкой на CPU, особенностью задачи или организационной границей",
    "why mutable global state is risky in backend services": "почему изменяемое глобальное состояние опасно в backend-сервисах",
    "publish before commit can observe rolled-back state": "публикация до фиксации может увидеть состояние, которое затем будет отменено",
    "real disposable Redis for integration boundary": "одноразовый реальный Redis для интеграционной границы",
    "rate limiter/session behavior depends on risk": "поведение ограничителя частоты и сессии зависит от риска",
    "difference from application Redis cache": "отличие от кеша Redis на уровне приложения",
    "Revision, upgrade and downgrade": "Ревизия, применение и откат миграции",
    "rename may look like drop/add": "переименование может выглядеть как удаление и добавление",
    "backward compatibility": "обратная совместимость",
    "generated diff is a draft": "сгенерированная разница является черновиком",
    "works locally but fails in CI": "локально работает, но падает в CI",
    "deduplicate preserving order": "удаление дубликатов с сохранением порядка",
    "safe destructive operations": "безопасные разрушающие операции",
    "merge revision": "объединяющая ревизия",
    "multiple heads": "несколько головных ревизий",
    "generator-based context manager": "контекстный менеджер на основе генератора",
    "pipeline failure awareness": "понимание ошибок конвейера команд",
    "manual review": "ручная проверка",
    "team workflow": "командный процесс работы",
    "relative/absolute paths": "относительные и абсолютные пути",
    "collisions awareness": "понимание коллизий",
    "foreground/background": "передний и фоновый режим",
    "backfill": "заполнение существующих данных",
    "batching": "пакетная обработка",
    "graceful termination": "корректное завершение",
    "average complexity": "средняя сложность",
    "ownership awareness": "понимание владельца файла",
    "validate brackets": "проверка скобочной последовательности",
    "read/write/execute": "чтение, запись и выполнение",
    "sorted invariant": "инвариант отсортированности",
    "merge intervals": "объединение интервалов",
    "reading logs": "чтение журналов",
    "key extraction": "извлечение ключа",
    "dominant term": "доминирующий член сложности",
    "frequency map": "таблица частот",
    "time vs space": "время и память",
    "boundaries": "границы",
    "stable sort": "стабильная сортировка",
    "DFS basics": "основы обхода в глубину",
    "no need to memorize every sort implementation": "не нужно запоминать реализацию каждого алгоритма сортировки",
    "versioned schema transition": "версионированного перехода схемы",
    "deploy compatibility": "совместимость при развёртывании",
    "time/space complexity": "временной и пространственной сложностью",
    "data-structure operation": "операцию со структурой данных",
    "boundary cases": "граничных случаев",
    "shell command": "команду оболочки",
    "network state": "состоянием сети",
    "user permissions": "правами пользователя",
    "file permission": "правами доступа к файлу",
    "environment": "окружением",
    "network namespace": "сетевое пространство имён",
    "filesystem": "файловую систему",
    "descriptors": "дескрипторы",
    "reproducible CI/CD gate": "воспроизводимой проверки CI/CD",
    "versioned artifact": "версионируемым артефактом",
    "secrets": "секретов",
    "trigger": "условием запуска",
    "Context manager": "Контекстный менеджер",
    "acquire/use/release": "получение, использование и освобождение ресурса",
    "exception info": "информацию об исключении",
    "truthy return": "истинный результат",
    "Declarative ORM models": "Декларативные ORM-модели",
    "Python classes and attributes": "классы и атрибуты Python",
    "tables": "таблицами",
    "SQL dialect": "диалектом SQL",
    "connection pool": "пулом соединений",
    "application-level factory": "фабрика уровня приложения",
    "Database constraints": "Ограничения базы данных",
    "invariants": "инварианты",
    "writers": "клиенты записи",
    "primary key": "первичный ключ",
    "foreign key": "внешний ключ",
    "Django project": "Проект Django",
    "configuration": "конфигурацию",
    "apps": "приложения",
    "domain capability": "доменную возможность",
    "DRF serializer": "сериализатор DRF",
    "production migration strategy": "стратегия миграций рабочего окружения",
    "versioned and reviewable": "версионированной и проверяемой",
    "encryption": "шифрование",
    "integrity": "целостность",
    "authentication": "аутентификацию",
    "certificate": "сертификату",
    "returned value": "возвращённое значение",
    "representation": "представление",
    "Raw dict": "Необработанный словарь",
    "generated schema": "сгенерированной схемы",
    "typed access": "типизированного доступа",
    "field errors": "ошибок отдельных полей",
    "one thread executing Python bytecode in one CPython process": "один поток выполняет байткод Python в одном процессе CPython",
    "Django could reduce custom work for admin/content-heavy product": "Django может сократить объём собственной разработки для продукта с админкой и большим количеством контента",
    "candidate did not administer a production monitoring cluster": "кандидат не утверждает, что администрировал промышленный кластер мониторинга",
    "ignoring future files does not remove tracked/history content": "игнорирование будущих файлов не удаляет уже отслеживаемые данные и историю",
    "translating infrastructure errors into domain/API errors": "преобразование инфраструктурных ошибок в доменные ошибки или ошибки API",
    "communities/roles/discussions/materials/Q&A/moderation": "сообщества, роли, обсуждения, материалы, вопросы и ответы, модерация",
    "PostgreSQL/Redis/object storage/WebSocket are I/O-bound": "работа с PostgreSQL, Redis, объектным хранилищем и WebSocket ограничена ожиданием ввода-вывода",
    "intercepted code cannot be exchanged without verifier": "перехваченный код нельзя обменять без проверочного значения",
    "database race conditions are separate from Python GIL": "гонки данных в базе не предотвращаются GIL языка Python",
    "model declaration is not production schema migration": "объявление модели не является миграцией рабочей схемы базы данных",
    "Celery can coexist but does not alone solve dual write": "Celery можно использовать вместе с этим решением, но сам по себе он не устраняет проблему двойной записи",
    "Sentry groups application errors with stack/context": "Sentry группирует ошибки приложения вместе со стеком и контекстом",
    "split only for measured CPU/problem/organizational граница": "разделение оправдано только измеренной нагрузкой на CPU, особенностью задачи или организационной границей",
    "Pub/Sub distributes live events between instances": "Pub/Sub распределяет события реального времени между экземплярами приложения",
    "candidate configured and used them in a pet-project": "кандидат настраивал и использовал эти инструменты в учебном проекте",
    "avoid pretending project is production-perfect": "не выдавать учебный проект за безупречную промышленную систему",
    "current scale does not justify second language": "текущий масштаб не оправдывает добавление второго языка",
    "why mutable global состояние is risky in backend services": "почему изменяемое глобальное состояние опасно в backend-сервисах",
    "FastAPI is not universally superior to Django": "FastAPI не лучше Django во всех возможных задачах",
    "ORM does not protect raw string interpolation": "ORM не делает безопасной ручную подстановку строк в SQL",
    "added build/deploy/observability complexity": "дополнительная сложность сборки, развёртывания и наблюдаемости",
    "deliberate denormalization only with reason": "осознанная денормализация допустима только при понятной причине",
    "equality before range as a heuristic, not dogma": "равенство перед диапазоном — практическая эвристика, а не догма",
    "publish before commit can observe rolled-back состояние": "публикация до фиксации может увидеть состояние, которое затем будет отменено",
    "Celery may still be delivery/execution layer": "Celery всё ещё может быть слоем доставки и выполнения",
    "Redis ephemeral acceleration/coordination": "Redis используется для временного ускорения и координации",
    "identifiers/order fields require allowlist": "идентификаторы и поля сортировки требуют списка разрешённых значений",
    "modern lifespan over scattered legacy hooks": "современный lifespan предпочтительнее разрозненных устаревших обработчиков",
    "no promises impossible to combine with study": "не обещать нагрузку, несовместимую с учёбой",
    "Redis Pub/Sub for cross-instance live fan-out": "Redis Pub/Sub для рассылки событий между экземплярами приложения",
    "problem is atomicity, not merely “background”": "главная проблема — атомарность, а не просто фоновое выполнение",
    "PKCE does not replace all CSRF protections": "PKCE не заменяет все меры защиты от CSRF",
    "comparison with Django without tribalism": "сравнение с Django без предвзятого выбора технологии",
    "do not swallow cancellation accidentally": "не поглощать отмену задачи случайно",
    "no simplistic universal performance rule": "нет простого универсального правила производительности",
    "not a relational source of truth by default": "по умолчанию это не реляционный источник истины",
    "Prometheus collects time-series metrics": "Prometheus собирает метрики временных рядов",
    "async stack suits WebSockets and I/O waits": "асинхронный стек подходит для WebSocket и ожидания ввода-вывода",
    "execution begins when awaited/scheduled": "выполнение начинается после ожидания через await или планирования",
    "fakes only when semantics are sufficient": "подмены допустимы только когда их семантики достаточно для проверки",
    "start order is not application readiness": "порядок запуска не гарантирует готовность приложения",
    "bounded async fetch with timeout": "асинхронную загрузку с ограничением параллельности и тайм-аутом",
    "Grafana visualizes data and dashboards": "Grafana визуализирует данные на панелях мониторинга",
    "mature ecosystem and development speed": "зрелая экосистема и скорость разработки",
    "model code does not update an existing DB": "код модели не обновляет существующую базу данных",
    "never reversible encryption/plain hash": "не использовать обратимое шифрование или обычный быстрый хеш",
    "appropriate challenge/header context": "подходящий контекст проверочного значения или заголовка",
    "avoiding exception-driven normal flow": "не использовать исключения для обычного управления потоком",
    "direct publish after commit may be lost": "прямая публикация после фиксации транзакции может потеряться",
    "real disposable Redis for integration граница": "одноразовый реальный Redis для интеграционной границы",
    "relevance to API-returned user content": "применимость к пользовательскому контенту, возвращаемому через API",
    "why planner may prefer sequential scan": "почему планировщик может предпочесть последовательное сканирование",
    "API instances fan out to local clients": "экземпляры API рассылают события своим локальным клиентам",
    "browser automatically sends cookies": "браузер автоматически отправляет cookie",
    "no concurrent use of one AsyncSession": "не использовать одну AsyncSession конкурентно",
    "practical factory/callback examples": "практические примеры фабрики и функции обратного вызова",
    "required nullable field distinction": "различие между обязательным и допускающим null полем",
    "when module-level function is simpler": "когда функция уровня модуля проще",
    "avoid premature version complexity": "избегать преждевременного усложнения версий",
    "durable background job → queue/worker": "надёжная фоновая задача → очередь и обработчик",
    "fail policy depends on endpoint risk": "политика отказа зависит от риска конкретного эндпоинта",
    "fixed/sliding/token bucket concepts": "модели фиксированного окна, скользящего окна и корзины токенов",
    "no print-debugging as final solution": "не оставлять отладку через print как окончательное решение",
    "rate limiter/session поведение depends on risk": "поведение ограничителя частоты и сессии зависит от риска",
    "relationship with FastAPI/Pydantic": "связь с FastAPI и Pydantic",
    "configuration captured by closure": "конфигурация, захваченная замыканием",
    "connections are expensive/limited": "соединения дороги и ограничены",
    "data migration/rollback awareness": "понимание миграции данных и отката",
    "difference from application Redis кеш": "отличие от кеша Redis на уровне приложения",
    "evaluation at function definition": "вычисление в момент определения функции",
    "gates do not guarantee correctness": "автоматические проверки не гарантируют корректность",
    "generated ID may appear after flush": "созданный идентификатор может появиться после синхронизации с БД",
    "not a replacement for Celery/outbox": "не является заменой Celery или шаблону outbox",
    "object creation vs initialization": "создание объекта и его инициализация",
    "offline subscriber misses message": "отключённый подписчик пропускает сообщение",
    "realistic order/customer examples": "реалистичные примеры заказов и клиентов",
    "reconnect fetches missed messages": "после переподключения пропущенные сообщения загружаются отдельно",
    "top-K without excessive complexity": "поиск первых K элементов без лишней сложности",
    "“high-load” without measured traffic": "слова о высокой нагрузке без измеренного трафика",
    "response schemas separate from ORM models": "схемы ответа отделены от ORM-моделей",
    "custom validation response only with reason": "собственный формат ошибки валидации нужен только при ясной причине",
    "avoid DB I/O inside schema validation": "не выполняй обращения к БД внутри валидации схемы",
    "no claim that one is universally better": "ни один вариант не является безусловно лучшим",
    "TestClient/AsyncClient according to stack": "TestClient или AsyncClient выбирают в соответствии со стеком",
    "trusted/untrusted boundaries": "границы доверенных и недоверенных данных",
    "FastAPI: typed API/async flexibility": "FastAPI: типизированный API и гибкая асинхронность",
    "Django: batteries, ORM, admin, auth ecosystem": "Django: готовая экосистема с ORM, админкой и аутентификацией",
    "request lifecycle": "жизненный цикл запроса",
    "transaction lifecycle": "жизненный цикл транзакции",
    "process lifecycle": "жизненный цикл процесса",
    "data-access flow": "процесс доступа к данным",
    "request flow": "обработка запроса",
    "response serialization": "сериализация ответа",
    "output representation": "представление результата",
    "explicit null": "явное значение null",
    "invalid input": "некорректные входные данные",
    "mental model": "модель понимания",
    "await points": "точки приостановки await",
    "await point": "точка приостановки await",
    "happy path": "основной сценарий",
    "failure path": "сценарий ошибки",
    "failure mode": "режим отказа",
    "edge-case": "граничный случай",
    "edge case": "граничный случай",
    "boundary values": "граничные значения",
    "trade-off": "компромисс",
    "server-side": "на стороне сервера",
    "build-time": "во время сборки",
    "prediction": "предсказание результата",
    "code prediction": "предсказание результата кода",
    "find the bug": "найди ошибку",
    "small task": "небольшая задача",
    "rewrite": "улучшение кода",
    "interview explanation": "ответ на собеседовании",
    "follow-up": "дополнительный вопрос",
}


def russianize_prose(value: str) -> str:
    """Translate explanatory prose while preserving code/API identifiers."""

    pieces = re.split(r"(`[^`]*`)", value)
    translations = sorted(PROSE_TRANSLATIONS.items(), key=lambda item: len(item[0]), reverse=True)
    for index in range(0, len(pieces), 2):
        prose = pieces[index]
        for source, target in translations:
            pattern = rf"(?<![A-Za-z]){re.escape(source)}(?![A-Za-z])"

            def replacement(match: re.Match[str], translated: str = target) -> str:
                if match.group(0)[:1].isupper() and translated[:1].islower():
                    return translated[:1].upper() + translated[1:]
                return translated

            prose = re.sub(pattern, replacement, prose, flags=re.IGNORECASE)
        pieces[index] = prose
    return "".join(pieces)


def russianize_dossier(dossier: LessonDossier) -> LessonDossier:
    scalar_fields = (
        "what",
        "mechanism",
        "nuance",
        "question",
        "short_answer",
        "junior_answer",
        "follow_up_question",
        "follow_up_answer",
    )
    sequence_fields = ("mistakes", "required", "useful", "skip_deep", "practices", "rubric")
    changes = {name: russianize_prose(getattr(dossier, name)) for name in scalar_fields}
    changes["backend"] = russianize_prose(dossier.backend) if dossier.backend else None
    changes.update(
        {name: tuple(russianize_prose(item) for item in getattr(dossier, name)) for name in sequence_fields}
    )
    return replace(dossier, **changes)


CURATED: dict[str, LessonDossier] = {
    "1.2": LessonDossier(
        what=(
            "`==` сравнивает значения по протоколу равенства, а `is` проверяет, являются ли два "
            "выражения ссылками на один и тот же объект. Равные объекты не обязаны быть одним объектом."
        ),
        mechanism=(
            "Для `left == right` Python вызывает реализацию `__eq__`; пользовательский класс может определить "
            "собственное понятие равенства. `left is right` не вызывает методы объекта и сравнивает identity. "
            "`id(obj)` возвращает идентификатор, уникальный среди живых объектов текущего процесса."
        ),
        nuance=(
            "Сравнивай с `None` через `is None`: `None` — singleton, а пользовательский `__eq__` может вести себя "
            "неожиданно. Не используй `is` для строк и чисел: interning — оптимизация реализации, не контракт программы."
        ),
        backend=None,
        mistakes=(
            "`status is 'paid'` может случайно сработать в одном запуске и сломаться в другом; для значения нужна проверка `status == 'paid'`.",
            "`value == None` способен вызвать переопределённый `__eq__`; точнее писать `value is None`.",
        ),
        required=("различать value equality и identity", "использовать `is None`", "понимать роль `__eq__`"),
        useful=("знать, что `id()` имеет смысл только в пределах жизни объекта",),
        skip_deep=("детали interning и адресации объектов в конкретной версии CPython",),
        practices=(
            "**A · Code prediction.** Предскажи `a == b`, `a is b` и `a is c` для двух равных списков и одного alias.",
            "**B · Find the bug.** Исправь `if role is \"admin\": ...` и объясни, почему ошибка нестабильна.",
            "**E · Interview explanation.** Ответь за 30–60 секунд, не смешивая identity, equality и hashability.",
        ),
        question="В чём разница между `is` и `==` и почему принято писать `x is None`?",
        short_answer="`==` сравнивает значения, `is` — identity объектов. С `None` используют `is`, потому что это singleton.",
        junior_answer=(
            "`==` проверяет равенство значений и обычно вызывает `__eq__`. `is` отвечает на другой вопрос: "
            "ссылаются ли оба имени на один объект. Поэтому два списка `[1]` равны через `==`, но обычно не идентичны. "
            "С `None` пишут `is None`: это точно выражает identity-проверку и не вызывает чужой `__eq__`."
        ),
        follow_up_question="Почему нельзя проверять строки через `is`?",
        follow_up_answer="Python может интернировать некоторые строки, но это не гарантируется для произвольных значений; сравнение значения должно использовать `==`.",
        example="""```python
a = [1, 2]
b = [1, 2]
c = a

print(a == b)  # True
print(a is b)  # False
print(a is c)  # True
```""",
        rubric=("разные вопросы value/identity", "`__eq__`", "`is None`", "не полагаться на interning"),
    ),
    "1.7": LessonDossier(
        what=(
            "Копирование создаёт отдельный объект, но глубина копии определяет, останутся ли общими вложенные объекты. "
            "Shallow copy отделяет только внешний контейнер; deep copy пытается скопировать весь достижимый object graph."
        ),
        mechanism=(
            "`list.copy()`, срез `[:]`, `dict.copy()` и `copy.copy()` создают новый внешний объект и переносят в него "
            "те же references на элементы. `copy.deepcopy()` идёт рекурсивно и хранит memo, чтобы не копировать один объект "
            "несколько раз и обрабатывать циклы."
        ),
        nuance=(
            "`deepcopy` не делает автоматически корректную доменную копию: соединения, файловые дескрипторы, ORM entities "
            "и shared caches часто нельзя или не нужно дублировать. Иногда правильнее собрать новый объект явно."
        ),
        backend="При нормализации вложенного JSON shallow copy может оставить общий список ролей; mutation копии тогда изменит исходный payload.",
        mistakes=(
            "Считать `payload.copy()` независимой копией всех вложенных данных.",
            "Применять `deepcopy()` к ORM graph вместо явного DTO/serialization boundary.",
        ),
        required=("видеть разницу shallow/deep", "предсказывать nested mutation", "знать `copy.copy` и `copy.deepcopy`"),
        useful=("понимать memo и циклические ссылки на уровне идеи",),
        skip_deep=("внутренний dispatch table модуля `copy`",),
        practices=(
            "**A · Code prediction.** Измени список внутри shallow copy и предскажи исходный payload.",
            "**C · Rewrite.** Собери новую API-модель явно вместо безусловного `deepcopy` ORM-объекта.",
            "**D · Small task.** Реализуй функцию, которая копирует dict и отдельно копирует список `roles`.",
        ),
        question="Чем shallow copy отличается от deep copy?",
        short_answer="Shallow copy создаёт новый внешний контейнер, но делит вложенные объекты; deep copy рекурсивно копирует graph.",
        junior_answer=(
            "При shallow copy внешний list или dict новый, а его элементы — те же объекты. Поэтому изменение вложенного списка "
            "видно и в оригинале. `deepcopy` рекурсивно копирует graph, но дороже и не всегда соответствует смыслу domain data. "
            "Для сложных объектов я предпочту явное построение нужной копии."
        ),
        follow_up_question="Почему `deepcopy` может быть плохим выбором для SQLAlchemy model?",
        follow_up_answer="ORM entity связана с Session, lazy relationships и identity map; механическое копирование graph не создаёт корректную новую запись и может загрузить лишние данные.",
        example="""```python
source = {"roles": ["reader"]}
shallow = source.copy()
shallow["roles"].append("writer")

print(source["roles"])
# ['reader', 'writer']
```""",
    ),
    "1.8": LessonDossier(
        what=(
            "`int`, `float` и `Decimal` представляют числа с разными гарантиями. `str` хранит Unicode-текст, а `bytes` — "
            "последовательность байтов. Между текстом и байтами всегда есть явная граница encoding."
        ),
        mechanism=(
            "Обычный `float` следует IEEE 754 и хранит число в двоичной форме; многие десятичные дроби не представимы точно. "
            "`Decimal` хранит десятичное представление и управляемый контекст точности. `text.encode('utf-8')` создаёт bytes, "
            "а `raw.decode('utf-8')` восстанавливает str при совпадающей кодировке."
        ),
        nuance=(
            "`0.1 + 0.2 == 0.3` даёт `False` из-за округления binary float. Для денег обычно используют `Decimal` в Python "
            "и `NUMERIC/DECIMAL` в БД; вход для `Decimal` лучше брать из строки, а не из уже неточного float."
        ),
        backend="HTTP/JSON приносит текст, файлы и сокеты — bytes, а база должна хранить деньги типом с десятичной точностью.",
        mistakes=(
            "Создать `Decimal(0.1)` и ожидать точное `0.1`; лучше `Decimal('0.1')`.",
            "Декодировать произвольные bytes без согласованной encoding/error policy.",
        ),
        required=("объяснить погрешность float", "различать str/bytes", "уметь encode/decode", "выбрать Decimal для денег"),
        useful=("знать про `math.isclose` для приближённых сравнений",),
        skip_deep=("битовая раскладка IEEE 754 и Unicode normalization algorithms",),
        practices=(
            "**A · Code prediction.** Проверь `0.1 + 0.2 == 0.3` и объясни результат.",
            "**B · Find the bug.** Найди потерю точности в `Decimal(0.1)`.",
            "**D · Small task.** Преобразуй UTF-8 bytes в str и корректно обработай ошибочную последовательность.",
        ),
        question="Почему float не подходит для точных денежных расчётов и чем `str` отличается от `bytes`?",
        short_answer="Float хранит двоичное приближение; для денег нужен Decimal/NUMERIC. `str` — Unicode, `bytes` — конкретные байты.",
        junior_answer=(
            "Многие десятичные дроби нельзя точно записать в двоичном float, поэтому операции накапливают небольшую погрешность. "
            "Для денег используют `Decimal` и SQL `NUMERIC`, создавая Decimal из строки. `str` представляет Unicode-текст, "
            "а `bytes` — данные на границе файла или сети; переход выполняют явными `encode` и `decode` с одной кодировкой."
        ),
        follow_up_question="Как корректно сравнивать результаты обычных scientific float-вычислений?",
        follow_up_answer="Обычно через допустимую абсолютную/относительную погрешность, например `math.isclose`, а не прямое `==`.",
        example="""```python
from decimal import Decimal

print(0.1 + 0.2 == 0.3)                 # False
print(Decimal("0.1") + Decimal("0.2"))  # 0.3

raw = "Алматы".encode("utf-8")
print(raw.decode("utf-8"))              # Алматы
```""",
    ),
    "2.1": LessonDossier(
        what=(
            "`list` — упорядоченная изменяемая последовательность. Она хранит references на элементы, поддерживает индексы, "
            "срезы и дубликаты; один список может содержать объекты разных типов."
        ),
        mechanism=(
            "`append(x)` добавляет один элемент, `extend(iterable)` добавляет элементы iterable, `insert(i, x)` сдвигает хвост. "
            "Доступ по индексу обычно O(1), поиск значения и удаление по значению — O(n), вставка в начало — O(n). "
            "Срез создаёт новый внешний list, но остаётся shallow copy."
        ),
        nuance=(
            "Методы `append`, `extend`, `sort` меняют список на месте и возвращают `None`. Во время обхода не стоит менять "
            "размер того же списка: элементы можно пропустить. Для очереди с частым удалением слева лучше `collections.deque`."
        ),
        backend="Список естественен для упорядоченного JSON-массива результатов API; для быстрого поиска по id дополнительно строят dict.",
        mistakes=(
            "`items = items.append(value)` заменит переменную на `None`.",
            "`matrix = [[0] * 3] * 3` создаёт три ссылки на одну строку, поэтому изменение одной строки видно во всех.",
        ),
        required=("append vs extend", "индексы и срезы", "mutability и aliases", "базовая сложность операций"),
        useful=("deque для очереди", "stable sort и key function"),
        skip_deep=("стратегия over-allocation CPython в точных коэффициентах",),
        practices=(
            "**A · Code prediction.** Что произойдёт после `rows = [[0]] * 3; rows[0].append(1)`?",
            "**B · Find the bug.** Исправь `items = items.sort(key=...)`.",
            "**C · Rewrite.** Замени цикл накопления квадратов простой читаемой comprehension.",
            "**D · Small task.** Верни уникальные элементы списка с сохранением порядка.",
        ),
        question="Что такое list, какие у него основные операции и их сложность?",
        short_answer="List — ordered mutable sequence; индекс и append обычно O(1), поиск и вставка в начало — O(n).",
        junior_answer=(
            "`list` хранит упорядоченную последовательность references, допускает дубликаты и меняется на месте. Доступ по "
            "индексу и append обычно O(1), а поиск значения, удаление по значению и вставка в начало — O(n). `append` добавляет "
            "один объект, `extend` — все элементы iterable. Срез создаёт новый внешний список, но копия остаётся shallow."
        ),
        follow_up_question="Когда вместо list выбрать set, dict или deque?",
        follow_up_answer="Set — для уникальности и быстрого membership, dict — для lookup по ключу, deque — для частых операций с обоих концов.",
        example="""```python
items = ["created", "paid"]
items.append("shipped")
items.extend(["delivered", "closed"])

print(items[1:3])
# ['paid', 'shipped']
```""",
    ),
    "2.2": LessonDossier(
        what=(
            "`tuple` — упорядоченная неизменяемая последовательность. После создания нельзя заменить, добавить или удалить "
            "элемент, но tuple может содержать mutable object, состояние которого всё ещё меняется."
        ),
        mechanism=(
            "Запятые создают tuple: `(value,)` — tuple из одного элемента, а `(value)` — просто value в скобках. "
            "Packing собирает значения, unpacking распределяет их по именам. Tuple может быть dict key, только если каждый "
            "его элемент hashable."
        ),
        nuance=(
            "Immutability контейнера не гарантирует deep immutability: `([1],)` нельзя хешировать, а внутренний list можно менять. "
            "Для сущности с именованными полями и поведением dataclass обычно понятнее позиционного tuple."
        ),
        backend="Tuple удобен для внутренней фиксированной пары `(host, port)` или составного hashable key; JSON всё равно сериализует его как array.",
        mistakes=(
            "`single = (42)` создаёт int, не tuple; нужна запятая: `(42,)`.",
            "Считать любой tuple hashable: `([1],)` содержит unhashable list.",
        ),
        required=("immutability", "packing/unpacking", "одиночный tuple", "условия hashability"),
        useful=("понимать, когда dataclass яснее tuple",),
        skip_deep=("memory layout tuple в CPython",),
        practices=(
            "**A · Code prediction.** Определи тип `(1)` и `(1,)`.",
            "**B · Find the bug.** Объясни `TypeError` для `{([1],): 'value'}`.",
            "**C · Rewrite.** Замени нечитабельный 6-позиционный tuple на dataclass.",
        ),
        question="Чем tuple отличается от list и когда tuple можно использовать как ключ dict?",
        short_answer="Tuple неизменяем и может быть ключом dict, если все его элементы hashable; list изменяем и не hashable.",
        junior_answer=(
            "Tuple — ordered immutable sequence. Его структуру нельзя изменить после создания, поэтому tuple из hashable "
            "элементов сам hashable и может быть ключом dict. Но tuple с list внутри уже не hashable, и внутренний list можно "
            "мутировать. Одноэлементный tuple записывается с запятой: `(value,)`."
        ),
        follow_up_question="Почему tuple с list внутри не является hashable?",
        follow_up_answer="Hash ключа должен оставаться стабильным; list меняется и не имеет hash, поэтому содержащий его tuple тоже нельзя хешировать.",
        example="""```python
point = (43.2389, 76.8897)
latitude, longitude = point
locations = {point: "Almaty"}

print(latitude, locations[point])
# 43.2389 Almaty
```""",
    ),
    "2.3": LessonDossier(
        what=(
            "`dict` — изменяемое отображение пар «ключ — значение». Ключи уникальны и должны быть хешируемыми; значения "
            "могут быть любыми. Начиная с Python 3.7 порядок вставки гарантирован языком."
        ),
        mechanism=(
            "Словарь использует хеш-таблицу: по хешу ключа ищется позиция, затем проверка равенства подтверждает совпадение. "
            "Поиск, вставка и удаление в среднем работают за O(1). `keys()`, `values()` и `items()` возвращают динамические "
            "представления. Обновление существующего ключа меняет значение, но не перемещает ключ."
        ),
        nuance=(
            "`data[key]` поднимает `KeyError`, `.get(key)` возвращает `None`, `.get(key, default)` — переданное значение по "
            "умолчанию и не меняет словарь. `.setdefault(key, default)` при отсутствии вставляет значение по умолчанию и "
            "всегда возвращает итоговое значение. Для накопления "
            "многих групп часто яснее `defaultdict(list)`."
        ),
        backend="Словарь удобен для индексирования ORM/DTO-объектов по идентификатору и для чтения необязательных HTTP-заголовков или полей JSON.",
        mistakes=(
            "`user['email']` падает с `KeyError`, если поле действительно необязательное; используй `.get` только когда отсутствие допустимо.",
            "`data[[1, 2]] = 'value'` падает с `TypeError: unhashable type: 'list'`.",
            "`bucket = data.setdefault('roles', [])` изменяет dict при отсутствующем ключе — в отличие от `.get`.",
        ),
        required=("хешируемые и уникальные ключи", "`.get` и `[]`", "`.setdefault`", "порядок вставки", "средняя сложность поиска O(1)"),
        useful=("объединение через `|` и `update`", "представления и безопасная итерация", "когда выбрать `defaultdict`"),
        skip_deep=("размер таблицы и внутренний алгоритм разрешения коллизий CPython",),
        practices=(
            "**A · Code prediction.** Обнови существующий ключ и предскажи `list(data)`.",
            "**B · Find the bug.** Исправь чтение необязательного `Authorization` без сокрытия обязательных полей.",
            "**C · Rewrite.** Перепиши ручное группирование сначала с `setdefault`, затем сравни с `defaultdict(list)`.",
            "**D · Small task.** Построй индекс пользователей по id и отклони дубликаты.",
            "**F · Сценарий из backend-разработки.** Выбери структуру для ответа API, где важны порядок и поиск по идентификатору.",
        ),
        question="Что такое `dict`, как работает поиск и чем `.get()` отличается от `[]` и `.setdefault()`?",
        short_answer="`dict` — изменяемое отображение на основе хеш-таблицы; поиск в среднем работает за O(1), а ключи должны быть хешируемыми. `[]` даёт `KeyError`, `.get` не меняет словарь, а `.setdefault` может вставить значение.",
        junior_answer=(
            "`dict` хранит пары «ключ — значение»; ключи уникальны и хешируемы. В среднем поиск работает за O(1), потому что "
            "сначала используется хеш, а затем проверка равенства. `data[key]` нужен, когда ключ обязателен, и поднимет `KeyError` при ошибке. "
            "`.get` удобен для допустимо отсутствующего значения и не меняет dict. `.setdefault` возвращает значение, но при "
            "отсутствии ещё и вставляет значение по умолчанию. Словарь сохраняет порядок вставки, а замена значения не перемещает ключ."
        ),
        follow_up_question="Когда `.setdefault()` лучше заменить на `defaultdict(list)`?",
        follow_up_answer="Когда код систематически группирует много значений по ключам: `defaultdict` убирает повторяющееся создание контейнера. Для единичной вставки `.setdefault` проще и не меняет тип отображения.",
        example="""```python
user = {"id": 1, "name": "Daniyar"}

print(user.get("name"))              # Daniyar
print(user.get("email"))             # None
print(user.get("email", "unknown"))  # unknown

roles = user.setdefault("roles", [])
roles.append("reader")
print(user["roles"])                 # ['reader']
```""",
        rubric=("изменяемое отображение", "хешируемые уникальные ключи", "средняя сложность O(1)", "порядок вставки", "поведение `.get` и `.setdefault`"),
    ),
    "3.1": LessonDossier(
        what=(
            "Функция в Python — обычный first-class object. Её можно присвоить имени, положить в коллекцию, передать "
            "аргументом и вернуть из другой функции. Вызов происходит только при добавлении `()`."
        ),
        mechanism=(
            "Выполнение `def` создаёт function object и связывает его с именем. Object хранит code, globals, defaults, "
            "annotations и closure. Любой объект с `__call__` является callable; higher-order function принимает или возвращает callable."
        ),
        nuance=(
            "Передавай саму функцию как `handler`, а не результат `handler()`. Type hints для callback описывают через "
            "`Callable[[ArgType], ReturnType]`; для сложной сигнатуры часто понятнее `Protocol` с `__call__`."
        ),
        backend="Router, dependency и middleware получают callables; таблица обработчиков команд может отображать имя события в функцию.",
        mistakes=(
            "`handlers = {'created': send_email()}` вызывает функцию при создании dict и сохраняет результат вместо callable.",
            "Скрывать несовместимые callback signatures за `Callable[..., Any]`.",
        ),
        required=("function object vs call", "передача/возврат функций", "callable", "higher-order function"),
        useful=("атрибуты `__name__`, `__defaults__`, `__annotations__`",),
        skip_deep=("bytecode и внутреннее устройство PyFunctionObject",),
        practices=(
            "**A · Code prediction.** Сравни `registry['job']` и `registry['job']()`.",
            "**B · Find the bug.** Найди преждевременный вызов callback при построении registry.",
            "**D · Small task.** Реализуй `apply_twice(fn, value)`.",
            "**E · Interview explanation.** Приведи два признака first-class function.",
        ),
        question="Что значит, что функции в Python являются объектами первого класса?",
        short_answer="Функцию можно хранить, передавать и возвращать как любое другое значение; вызывается она через `()`.",
        junior_answer=(
            "При выполнении `def` Python создаёт function object и связывает его с именем. Этот объект можно передать "
            "callback-ом, сохранить в dict обработчиков или вернуть из factory. Пока я не добавил `()`, функция не вызывается. "
            "Так устроены decorators, route handlers и многие dependency APIs."
        ),
        follow_up_question="Чем callable object отличается от function?",
        follow_up_answer="Function — конкретный встроенный тип callable. Экземпляр пользовательского класса тоже callable, если класс реализует `__call__`.",
        example="""```python
def normalize_email(value: str) -> str:
    return value.strip().lower()

pipeline = [normalize_email]
step = pipeline[0]

print(step(" A@EXAMPLE.COM "))
# a@example.com
```""",
    ),
    "3.11": LessonDossier(
        what=(
            "Decorator — callable, который получает декорируемый объект и возвращает объект-замену. Для функции заменой "
            "обычно служит wrapper, добавляющий поведение до и после исходного вызова."
        ),
        mechanism=(
            "`@audit` над `def save` эквивалентен `save = audit(save)` и выполняется при definition/import time. Wrapper "
            "должен принять совместимые arguments, вызвать исходную функцию и вернуть её результат. Для async function нужен async wrapper с await."
        ),
        nuance=(
            "Используй `functools.wraps`, иначе теряются `__name__`, annotations, signature metadata и `__wrapped__`; это мешает "
            "FastAPI, introspection и debugging. Decorator не должен случайно проглатывать return value или exceptions."
        ),
        backend="Декораторы естественны для регистрации routes и технического tracing; доменную авторизацию часто яснее выразить dependency/service policy.",
        mistakes=(
            "Wrapper вызывает `fn(*args, **kwargs)`, но забывает `return`, поэтому caller получает `None`.",
            "Обычный sync wrapper вокруг `async def` возвращает coroutine object, но не ожидает его.",
            "Decorator скрывает signature без `@wraps(fn)`.",
        ),
        required=("эквивалентность `@decorator` присваиванию", "wrapper args/result", "definition time", "`functools.wraps`"),
        useful=("различать decorator и decorator factory", "порядок нескольких decorators"),
        skip_deep=("переписывание signatures через `inspect.Signature`",),
        practices=(
            "**A · Code prediction.** Определи порядок `before/original/after`.",
            "**B · Find the bug.** Верни потерянный результат из wrapper.",
            "**C · Rewrite.** Добавь `@wraps` и async-compatible вариант.",
            "**D · Small task.** Напиши decorator, считающий число вызовов.",
        ),
        question="Как работает decorator функции и зачем нужен `functools.wraps`?",
        short_answer="Decorator заменяет функцию результатом `decorator(function)`; wraps сохраняет metadata и ссылку на исходную функцию.",
        junior_answer=(
            "Запись `@audit` выполняется при определении функции и равна `handler = audit(handler)`. Audit возвращает wrapper, "
            "который принимает arguments, вызывает исходную функцию и возвращает результат. `functools.wraps` сохраняет имя, "
            "docstring, annotations и `__wrapped__`, поэтому framework и отладчик продолжают видеть исходный контракт."
        ),
        follow_up_question="В каком порядке применяются два decorators?",
        follow_up_answer="Применяются снизу вверх: `@a @b def f` даёт `f = a(b(f))`; при вызове внешний wrapper `a` начинает первым.",
        example="""```python
from functools import wraps

def audit(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(f"calling {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper

@audit
def total(values):
    return sum(values)

print(total([2, 3]))  # 5
```""",
    ),
    "8.3": LessonDossier(
        what=(
            "`await` приостанавливает текущую coroutine до готовности awaitable и позволяет event loop выполнять другие "
            "готовые tasks. Это кооперативная конкурентность, а не автоматический новый thread или parallel CPU execution."
        ),
        mechanism=(
            "`async def` при вызове создаёт coroutine object. Когда coroutine запущена task-ом, она выполняется до `await`. "
            "Если awaitable ещё не готов, task сохраняет state и уступает loop; после события продолжает со следующей строки."
        ),
        nuance=(
            "Два последовательных `await` остаются последовательными. Конкурентный запуск требует tasks/`gather`/`TaskGroup`. "
            "`time.sleep`, sync DB driver или CPU loop внутри async endpoint блокирует весь event-loop thread."
        ),
        backend="Async endpoint полезен, когда весь I/O path — HTTP client, DB driver, queue — предоставляет awaitable API.",
        mistakes=(
            "Вызвать coroutine без `await`: работа не выполнится, возможен warning `coroutine was never awaited`.",
            "Использовать `time.sleep()` в `async def`; нужно `await asyncio.sleep()` или вынести blocking call.",
            "Ожидать две независимые операции последовательно и называть это concurrent execution.",
        ),
        required=("coroutine object", "suspension point", "event loop", "последовательный vs concurrent await", "blocking code"),
        useful=("create_task/gather", "cancellation cleanup", "timeouts"),
        skip_deep=("реализация selectors/proactors и bytecode coroutine",),
        practices=(
            "**A · Code prediction.** Определи порядок вывода двух tasks с `sleep(0)`.",
            "**B · Find the bug.** Найди `requests.get`/`time.sleep` внутри async endpoint.",
            "**C · Rewrite.** Запусти независимые I/O calls через `gather`.",
            "**D · Small task.** Реализуй bounded async fetch с timeout.",
        ),
        question="Что делает `await` и создаёт ли он конкурентность автоматически?",
        short_answer="Await приостанавливает текущую coroutine и отдаёт loop управление; сам по себе он не создаёт thread и два последовательных await не становятся concurrent.",
        junior_answer=(
            "`await` работает внутри coroutine: если операция не готова, state текущей task сохраняется, а event loop может "
            "выполнять другие tasks. После готовности выполнение продолжится со следующей строки. Это полезно для I/O-bound "
            "кода. Один await не создаёт новую task, поэтому для независимых операций нужны `create_task`, `gather` или `TaskGroup`."
        ),
        follow_up_question="Что произойдёт, если вызвать blocking функцию внутри event loop?",
        follow_up_answer="Она не отдаёт управление, поэтому задержит все tasks этого loop; нужен async-native API, `to_thread` для blocking I/O или отдельный process/worker для CPU work.",
        example="""```python
import asyncio

async def fetch(name, delay):
    await asyncio.sleep(delay)
    return name

async def main():
    result = await asyncio.gather(fetch("profile", 0.02), fetch("orders", 0.01))
    print(result)  # ['profile', 'orders']

asyncio.run(main())
```""",
    ),
    "10.10": LessonDossier(
        what=(
            "`INNER JOIN` соединяет строки двух источников по условию и оставляет только совпавшие пары. Строка без пары "
            "с любой стороны в результат не попадёт."
        ),
        mechanism=(
            "Сначала формируются пары, для которых выражение `ON` истинно. Связь one-to-many размножает строку стороны one: "
            "один user с тремя orders даст три result rows. После JOIN применяются WHERE, grouping и projection."
        ),
        nuance=(
            "JOIN не устраняет duplicates. Если условие отсутствует или неполное, появляется Cartesian multiplication. "
            "`DISTINCT` может скрыть ошибку cardinality, но не исправляет неверную связь. Всегда определяй grain результата."
        ),
        backend="Типичный запрос связывает `orders.user_id` с `users.id`, чтобы вернуть заказ и email владельца одним result set.",
        mistakes=(
            "Забыть `ON` или часть composite key и получить резкий рост числа строк.",
            "Добавить `DISTINCT` вместо проверки one-to-many cardinality.",
            "Выбрать INNER JOIN, когда бизнес-требование должно сохранить users без orders.",
        ),
        required=("условие ON", "только matched rows", "one-to-many cardinality", "Cartesian product"),
        useful=("aliases", "оценка grain", "проверка FK/index по join key"),
        skip_deep=("внутренние алгоритмы hash/merge/nested-loop join до чтения EXPLAIN",),
        practices=(
            "**A · Result prediction.** По двум маленьким таблицам посчитай число result rows вручную.",
            "**B · Find the bug.** Найди отсутствующее условие JOIN.",
            "**C · Rewrite.** Замени correlated lookup понятным JOIN, не меняя cardinality.",
            "**D · SQL task.** Верни `order_id` и email владельца заказа.",
        ),
        question="Как работает INNER JOIN и почему он может увеличить число строк?",
        short_answer="INNER JOIN оставляет пары, удовлетворяющие ON; one-to-many даёт несколько rows на одну строку стороны one.",
        junior_answer=(
            "INNER JOIN объединяет только совпавшие строки по условию `ON`. Перед запросом я определяю grain: например, "
            "одна строка результата на order. Если у user несколько orders, user повторится для каждого заказа — это не SQL duplicate, "
            "а cardinality связи. Отсутствующее условие создаёт Cartesian product, и `DISTINCT` не должен маскировать такую ошибку."
        ),
        follow_up_question="Когда вместо INNER JOIN нужен LEFT JOIN?",
        follow_up_answer="Когда нужно сохранить все строки левой таблицы, включая те, для которых связь не найдена; поля правой стороны тогда будут NULL.",
        example="""```sql
SELECT o.id AS order_id, u.email
FROM orders AS o
JOIN users AS u ON u.id = o.user_id
ORDER BY o.id;
```

| order_id | email |
|---:|---|
| 10 | a@example.com |
| 11 | a@example.com |
| 12 | b@example.com |""",
    ),
    "10.17": LessonDossier(
        what=(
            "CTE (common table expression) — именованный промежуточный result, объявленный через `WITH` и доступный "
            "основному statement. Он помогает разбить длинный SQL на последовательные понятные шаги."
        ),
        mechanism=(
            "Каждый CTE имеет имя и query в скобках. Следующий CTE или основной SELECT обращается к нему как к таблице. "
            "Обычный CTE живёт только во время одного statement; recursive CTE может ссылаться на себя по специальным правилам."
        ),
        nuance=(
            "CTE — прежде всего средство выразительности, не гарантированная оптимизация. Современный PostgreSQL может встроить "
            "не recursive CTE в plan; `MATERIALIZED`/`NOT MATERIALIZED` влияют на это. Junior достаточно читать EXPLAIN, а не обещать ускорение."
        ),
        backend="CTE удобно отделяет выбор paid orders, aggregation по пользователю и финальный фильтр отчёта в одном statement.",
        mistakes=(
            "Считать, что `WITH` автоматически ускоряет запрос.",
            "Спрятать неверную cardinality в цепочке CTE и не проверять результат каждого шага.",
            "Использовать CTE из одного простого SELECT, когда он только увеличивает объём кода.",
        ),
        required=("синтаксис WITH", "scope одного statement", "читаемые этапы", "нет гарантии ускорения"),
        useful=("multiple CTE", "recursive CTE на уровне идеи", "planner/materialization caveat"),
        skip_deep=("тонкости cost model materialization без EXPLAIN конкретного запроса",),
        practices=(
            "**A · Result prediction.** Назови grain каждого шага monthly и итогового SELECT.",
            "**B · Find the bug.** Найди фильтр, применённый до нужной aggregation.",
            "**C · Rewrite.** Разбей вложенный отчёт на два именованных CTE.",
            "**D · SQL task.** Найди users с paid revenue выше порога.",
        ),
        question="Что такое CTE и гарантирует ли он ускорение SQL-запроса?",
        short_answer="CTE — именованный промежуточный query через WITH; он улучшает структуру, но сам по себе не гарантирует производительность.",
        junior_answer=(
            "CTE объявляется через `WITH name AS (...)` и доступен последующему query как временный result. Я использую его, "
            "чтобы дать имя этапу — например, сначала посчитать revenue по месяцу, затем отфильтровать итог. Это не обещание "
            "ускорения: PostgreSQL может встроить или материализовать CTE, поэтому производительность проверяют через EXPLAIN."
        ),
        follow_up_question="Чем CTE отличается от view?",
        follow_up_answer="CTE существует только в одном statement; view — сохранённое определение query в schema и может использоваться разными statements.",
        example="""```sql
WITH paid_totals AS (
    SELECT user_id, SUM(total) AS revenue
    FROM orders
    WHERE status = 'paid'
    GROUP BY user_id
)
SELECT user_id, revenue
FROM paid_totals
WHERE revenue >= 100;
```

Сначала `paid_totals` даёт одну строку на user, затем внешний query фильтрует уже рассчитанный revenue.""",
    ),
    "14.8": LessonDossier(
        what=(
            "Внедрение зависимостей — передача нужной зависимости извне вместо создания её внутри обработчика. В FastAPI "
            "`Depends` описывает граф зависимостей, который фреймворк разрешает для каждого запроса."
        ),
        mechanism=(
            "FastAPI читает сигнатуру эндпоинта и его зависимости, вызывает их в правильном порядке и передаёт результаты дальше. "
            "Одинаковая зависимость по умолчанию вычисляется один раз в рамках запроса. Одна зависимость может зависеть от другой; "
            "вариант с `yield` выполняет подготовку до обработчика и освобождает ресурс после ответа или ошибки."
        ),
        nuance=(
            "Кеш в рамках запроса не является глобальным кешем. Не храни `Session` или текущего пользователя в глобальной "
            "переменной модуля. Зависимости удобны на границе фреймворка — для аутентификации, сессии и настроек, — но сложные "
            "бизнес-правила лучше оставить сервису."
        ),
        backend="`get_current_user` может зависеть от функции разбора токена, а эндпоинт получает уже проверенного пользователя; подмена зависимости упрощает тестирование.",
        mistakes=(
            "Вызвать зависимость вручную как обычную функцию и ожидать, что FastAPI разрешит её вложенные зависимости.",
            "Создать глобальную SQLAlchemy Session и возвращать её всем запросам.",
            "Поместить всю бизнес-логику в огромный граф зависимостей, который трудно тестировать отдельно.",
        ),
        required=("зачем нужно внедрение зависимостей", "граф зависимостей", "кеш в рамках запроса", "освобождение ресурса после `yield`", "подмены в тестах"),
        useful=("псевдонимы с `Annotated`", "`use_cache=False`", "граница между зависимостью и сервисом"),
        skip_deep=("внутренние классы FastAPI, разрешающие граф зависимостей",),
        practices=(
            "**A · Предсказание порядка.** Расположи вызовы родительской зависимости, вложенной зависимости, эндпоинта и освобождения ресурса.",
            "**B · Find the bug.** Найди глобальную Session в модуле зависимостей.",
            "**C · Rewrite.** Вынеси чтение X-Role в `require_admin`.",
            "**D · Small task.** Реализуй защищённый эндпоинт `/admin` со скрытыми тестами.",
        ),
        question="Как работает `Depends` в FastAPI и каков жизненный цикл зависимости?",
        short_answer="`Depends` объявляет граф зависимостей; FastAPI разрешает его для запроса, переиспользует одинаковые зависимости и освобождает ресурсы зависимости с `yield`.",
        junior_answer=(
            "`Depends` позволяет эндпоинту явно объявить, что ему нужны текущий пользователь, `Session` или настройки. FastAPI "
            "строит граф по сигнатурам, вызывает зависимости и передаёт результаты обработчику. Внутри одного запроса одинаковая "
            "зависимость обычно выполняется один раз. Если она использует `yield`, код после `yield` освобождает ресурс. В тестах "
            "зависимость можно подменить."
        ),
        follow_up_question="Чем кеш зависимости в рамках запроса отличается от singleton?",
        follow_up_answer="Результат переиспользуется только внутри одного запроса; для следующего запроса зависимость вычисляется заново. Singleton живёт между запросами на уровне приложения.",
        example="""```python
from typing import Annotated
from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()

def require_admin(x_role: Annotated[str | None, Header()] = None) -> str:
    if x_role != "admin":
        raise HTTPException(403, "admin role required")
    return x_role

@app.get("/admin")
def admin(role: Annotated[str, Depends(require_admin)]):
    return {"role": role}
```""",
    ),
    "16.4": LessonDossier(
        what=(
            "SQLAlchemy `Session` — рабочая область ORM: она отслеживает сущности, хранит карту идентичности, собирает "
            "изменения как единицу работы и управляет транзакцией. Это не просто одно соединение с базой данных."
        ),
        mechanism=(
            "Новая сущность после `add` переходит в состояние pending; при `flush` операции INSERT/UPDATE/DELETE уходят в текущую "
            "транзакцию, а объект становится persistent. Карта идентичности гарантирует один объект Python на пару «класс модели — "
            "первичный ключ» внутри Session. После `close` или `expunge` объект становится detached, и ленивая загрузка больше не "
            "имеет активного контекста Session."
        ),
        nuance=(
            "Session получает соединение по необходимости. `flush` отправляет SQL, но не фиксирует транзакцию; после ошибки "
            "во время `flush` нужен `rollback`. Обычно один запрос или сценарий использования владеет одной Session. Одну "
            "AsyncSession нельзя одновременно использовать из нескольких задач."
        ),
        backend="Зависимость FastAPI с `yield` создаёт Session на запрос, сервис задаёт границу транзакции, а завершающий код закрывает Session.",
        mistakes=(
            "Создать глобальную Session для всего приложения — состояние и транзакция начнут протекать между запросами.",
            "Фиксировать транзакцию внутри каждого метода репозитория и разрушать атомарность сценария использования.",
            "Продолжить работу после IntegrityError без `rollback()`.",
        ),
        required=("карта идентичности", "единица работы", "основные состояния сущности", "`flush` и `commit`", "область жизни в рамках запроса"),
        useful=("`expire` и `refresh`", "`autoflush`", "контекстный менеджер транзакции"),
        skip_deep=("внутренний алгоритм упорядочивания единицы работы",),
        practices=(
            "**A · Code prediction.** Два `session.get(User, 1)` — сравни идентичность результатов.",
            "**B · Find the bug.** Найди глобальную Session и `commit` в репозитории.",
            "**C · Rewrite.** Перенеси `commit` на границу сервиса или сценария использования.",
            "**D · Small task.** Реализуй `load_twice` и пройди скрытый тест карты идентичности.",
        ),
        question="Что такое SQLAlchemy Session и зачем ей карта идентичности?",
        short_answer="Session объединяет единицу работы, карту идентичности и состояние транзакции; в одной Session одна строка БД представлена одним объектом Python.",
        junior_answer=(
            "Session отслеживает ORM-объекты и их изменения, объединяет их в единицу работы и владеет состоянием транзакции. "
            "Карта идентичности хранит загруженные объекты по классу и первичному ключу, поэтому повторный `get` в той же Session "
            "обычно возвращает тот же объект Python. `Flush` отправляет SQL внутри транзакции, а `commit` завершает её. Для каждого "
            "веб-запроса обычно создают отдельную Session."
        ),
        follow_up_question="Чем `flush` отличается от `commit`?",
        follow_up_answer="`Flush` синхронизирует состояние ORM с БД внутри открытой транзакции и может получить созданный идентификатор; `commit` фиксирует транзакцию. После `rollback` результат `flush` не сохраняется.",
        example="""```python
with Session(engine) as session:
    first = session.get(User, 1)
    second = session.get(User, 1)

    print(first is second)  # True: identity map
```""",
    ),
}

# Русская версия расширенных карточек. Технические идентификаторы и названия
# протоколов остаются в исходном виде, но все объясняющие предложения написаны
# по-русски. Эта таблица является источником опубликованного текста.
COMPACT_RU: dict[str, tuple[str, str, str, str | None, str]] = {
    "1.1": (
        "Имя в Python — это запись в пространстве имён, связанная с объектом; обычное присваивание связывает имя и не копирует объект.",
        "У каждого объекта есть тип, идентичность и значение. После `a = b` оба имени указывают на один объект: новое присваивание имени меняет только связь, а мутация видна через все ссылки.",
        "Аргументы функций подчиняются той же модели: функция может изменить переданный список, но присваивание нового объекта локальному параметру не меняет имя вызывающего кода.",
        None,
        "Представление переменной как независимой коробки приводит к неверным выводам об alias и аргументах функций.",
    ),
    "1.3": (
        "Изменяемый объект можно изменить с сохранением identity; неизменяемый объект нельзя изменить на месте — операция создаёт новый объект или новую связь имени.",
        "`list`, `dict` и `set` имеют изменяющие операции. `int`, `str`, `bytes` и `tuple` неизменяемы. При этом tuple может содержать изменяемый элемент.",
        "Важна семантика типа: `+=` может изменить существующий list, но для строки создаёт новый объект.",
        "Общий изменяемый default в обработчиках или конфигурации способен переносить состояние между вызовами.",
        "Смешение мутации и перепривязки приводит к неожиданному изменению данных вызывающей стороны через общую ссылку.",
    ),
    "1.4": (
        "Hashable-объект имеет стабильный hash и согласованное равенство, поэтому может быть ключом dict или элементом set.",
        "Hash table использует `hash(key)` для поиска кандидатов, а `==` — для подтверждения совпадения. Равные объекты обязаны иметь одинаковый hash; значимое для равенства состояние ключа не должно меняться.",
        "Tuple является hashable только тогда, когда hashable все его элементы. При собственном `__eq__` решение о `__hash__` должно быть явным и согласованным.",
        None,
        "List или dict в роли ключа вызывает `TypeError`; изменяемый hashable-ключ способен нарушить корректность lookup.",
    ),
    "1.5": (
        "Truthiness — протокол преобразования объекта к логическому значению в условиях вроде `if value`.",
        "Python вызывает `__bool__`, затем при его отсутствии использует `__len__`; без обоих методов объект считается truthy. `None`, числовой ноль и пустые стандартные коллекции являются falsy.",
        "Проверка `if value` объединяет несколько состояний. Используй `is None`, если ноль, пустая строка или пустой список являются допустимыми данными.",
        "Offset `0` и пустой JSON-массив могут быть корректными значениями и не должны смешиваться с отсутствующим параметром.",
        "Замена `if limit is None` на `if not limit` ошибочно отклоняет допустимый ноль.",
    ),
    "1.6": (
        "Aliases — несколько имён или ячеек контейнера, указывающих на один объект; вложенная мутация через любую ссылку меняет тот же объект.",
        "Присваивание и повторение последовательности копируют ссылки. `[[]] * 3` трижды помещает ссылку на один внутренний список, поэтому изменение одной строки видно во всех позициях.",
        "Независимые вложенные значения создавай comprehension-выражением: `[[] for _ in range(3)]`.",
        None,
        "Умножение последовательности с изменяемым вложенным значением создаёт общее состояние, которое легко пропустить в простом тесте.",
    ),
    "2.4": (
        "`set` — изменяемая неупорядоченная коллекция уникальных hashable-элементов; `frozenset` — её неизменяемый hashable-вариант.",
        "Membership, добавление и удаление работают в среднем за O(1) благодаря hashing. Объединение `|`, пересечение `&` и разность `-` выражают стандартные операции множеств.",
        "Порядок обхода set не является контрактом. Когда порядок результата важен, его задают отдельно; преобразование в set также удаляет повторы.",
        "Set естественно подходит для проверки permissions или удаления дублей, когда исходный порядок не нужен.",
        "Возврат `list(set(values))` из API молча уничтожает детерминированный порядок.",
    ),
    "2.6": (
        "Comprehension создаёт list, dict или set из выражения, исходного iterable и необязательного фильтра; generator expression остаётся ленивым.",
        "Выражение выполняется по одному разу для каждого выбранного элемента. В Python 3 переменная цикла comprehension имеет собственную область видимости.",
        "Обычный цикл лучше, когда есть несколько ветвей, побочные эффекты или вложенная трансформация, скрывающая смысл.",
        None,
        "Плотный вложенный comprehension может быть корректным, но заметно сложнее для чтения и отладки, чем короткий цикл.",
    ),
    "3.5": (
        "`*args` собирает дополнительные позиционные аргументы в tuple, а `**kwargs` — именованные аргументы в dict; те же звёздочки распаковывают значения при вызове.",
        "Привязка аргументов всё равно проверяет сигнатуру. Wrapper обычно передаёт вызов как `fn(*args, **kwargs)`, а двойная передача одного параметра вызывает `TypeError`.",
        "Не заменяй понятную публичную сигнатуру неограниченным `**kwargs`: явные keyword-only параметры дают лучшую типизацию и понятные ошибки API.",
        None,
        "Вызов `fn(value, **{'value': other})` передаёт один параметр дважды и завершается `TypeError`.",
    ),
    "3.7": (
        "LEGB — порядок поиска имени в Python: Local, Enclosing, Global, Builtins.",
        "Чтение имени проходит эти области по порядку. Присваивание внутри функции делает имя локальным без `global` или `nonlocal`, поэтому чтение до присваивания может вызвать `UnboundLocalError`.",
        "Имена `list`, `id` и других builtins можно затенить, но последующие вызовы станут запутанными или сломаются.",
        None,
        "Ожидание, что присваивание изменит global, хотя Python создал local binding, приводит к неверному состоянию и `UnboundLocalError`.",
    ),
    "3.9": (
        "Closure — внутренняя функция, сохраняющая доступ к свободным именам enclosing scope после завершения внешней функции.",
        "Функция хранит ссылки на enclosing cells, а не замороженную копию каждого значения. Factory может захватить конфигурацию или намеренно сохранить изменяемое состояние.",
        "Closures, созданные в цикле, используют late binding; текущее значение фиксируют через factory, default argument или `partial`.",
        "Factory валидаторов или callback может захватить неизменяемую конфигурацию без глобального состояния.",
        "Ожидание, что каждая lambda из цикла запомнит свою итерацию, обычно даёт последнее значение цикла во всех callback.",
    ),
    "4.1": (
        "Iterable умеет создать iterator, а iterator — stateful-объект, который последовательно выдаёт значения и расходуется.",
        "`iter(obj)` получает iterator, `next(it)` запрашивает один элемент. List создаёт новый iterator для каждого обхода, а generator object обычно сам является одноразовым iterator.",
        "После исчерпания iterator остаётся исчерпанным; для нового обхода нужен новый iterator, если исходный iterable позволяет его создать.",
        None,
        "Повторный обход сохранённого generator даёт пустой результат, в отличие от повторного обхода исходного list.",
    ),
    "4.2": (
        "Iterator protocol состоит из `__iter__`, возвращающего iterator, и `__next__`, возвращающего элемент либо поднимающего `StopIteration`.",
        "Пользовательский iterator хранит текущую позицию. Цикл `for` вызывает `iter`, повторяет `next` и самостоятельно перехватывает `StopIteration`.",
        "`StopIteration` — служебный сигнал завершения protocol, а не обычная ошибка для вывода или широкого перехвата в consumer-коде.",
        None,
        "Возврат `None` вместо `StopIteration` создаёт бесконечную последовательность `None`, а не завершает обход.",
    ),
    "4.3": (
        "Generator function содержит `yield`; её вызов возвращает generator object и не запускает тело немедленно.",
        "Каждый `next` продолжает выполнение до следующего `yield`, сохраняя локальные переменные и позицию. `return` или конец функции превращается для consumer в `StopIteration`.",
        "Ленивость уменьшает пиковую память, но generator одноразовый, а исключения откладываются до достижения проблемной строки.",
        "Generators позволяют потоково отдавать строки или chunks, не собирая весь результат в памяти.",
        "Преобразование generator в list ради логирования расходует его до основного использования.",
    ),
    "4.7": (
        "Exceptions — объекты иерархии; прикладные ошибки обычно наследуют `Exception`, а `BaseException` также включает сигналы управления процессом вроде `KeyboardInterrupt`.",
        "Python проверяет except-блоки сверху вниз и раскручивает stack frames до подходящего обработчика; без обработчика traceback возвращается вызывающему коду.",
        "Перехватывай узкий тип ошибки, которую можешь обработать. Широкий catch обычно должен добавить контекст и повторно поднять исключение.",
        "Domain exception можно преобразовать в стабильную HTTP-ошибку на границе API.",
        "Bare `except:` способен поглотить отмену, завершение процесса и программные ошибки.",
    ),
    "4.8": (
        "`try/except/else/finally` разделяет рискованную операцию, восстановление, действия только при успехе и обязательный cleanup.",
        "`except` выполняется для подходящего исключения, `else` — только без ошибки в try, а `finally` — перед любым выходом по успеху, return или exception.",
        "Делай try-блок узким, чтобы несвязанные ошибки не выглядели как ожидаемый failure.",
        None,
        "`return` внутри finally перекрывает предыдущий return или exception и может уничтожить диагностическую информацию.",
    ),
    "4.12": (
        "Context manager задаёт надёжную границу acquire/use/release для оператора `with`.",
        "`__enter__` возвращает значение после `as`; `__exit__` получает данные об исключении, а cleanup выполняется даже при ошибке. Truthy-результат `__exit__` подавляет исключение.",
        "Подавляй только ошибки, которые context manager действительно умеет обработать; случайный `True` скрывает сбой.",
        "Файлы, locks, DB transactions и clients используют context managers для явного управления ресурсом.",
        "Ручные open/close без finally оставляют ресурс открытым при исключении.",
    ),
    "5.1": (
        "Class — объект, описывающий поведение и class attributes; instance имеет собственную identity и instance namespace.",
        "Поиск атрибута начинается в instance, затем идёт по MRO класса; function на классе при чтении через instance превращается в bound method.",
        "Изменяемый class attribute разделяется между экземплярами, пока конкретный instance не затенит имя.",
        None,
        "`items = []` на классе для данных отдельного объекта переносит мутации между всеми instances.",
    ),
    "5.5": (
        "Encapsulation объединяет состояние и поведение, abstraction показывает значимый контракт, а polymorphism позволяет разным объектам удовлетворять этому контракту.",
        "Python часто использует duck typing: caller зависит от доступного поведения, а не от конкретного дерева наследования. ABC и Protocol делают договор явным, когда это нужно.",
        "Начальный underscore обозначает непубличный API, но не является контролем доступа; invariants всё равно защищают методами, properties и тестами.",
        "Service может принять любой notifier с методом `send`: в тесте передаётся fake, а в production — реальный provider.",
        "Проверка `type(obj) is ConcreteClass` запрещает корректные замены и ломает polymorphism.",
    ),
    "5.6": (
        "Inheritance моделирует отношение «является», composition — отношение «содержит», передавая объекту явные collaborators.",
        "Inheritance переиспользует и переопределяет поведение через MRO. Composition делегирует внедрённым объектам, снижая coupling и упрощая замену.",
        "Для services и repositories обычно лучше composition. Inheritance оправдано стабильной взаимозаменяемой иерархией или framework contract, а не только повторным использованием кода.",
        "Notification service с внедрённым email provider тестируется проще глубокой иерархии сервисов.",
        "Подкласс для каждой комбинации поведения создаёт хрупкую иерархию и неочевидный MRO.",
    ),
    "5.10": (
        "`@dataclass` генерирует `__init__`, `__repr__`, equality и другие методы по объявленным fields.",
        "Fields обрабатываются по порядку; `field(default_factory=list)` создаёт новый mutable default для каждого instance. `frozen=True` запрещает обычное присваивание полям, но не даёт глубокой неизменяемости.",
        "Dataclass подходит для внутренних data/value objects; Pydantic валидирует недоверенный input, а ORM models отвечают за persistence.",
        None,
        "Mutable default нужно задавать через `default_factory`, иначе instances получат общее состояние или dataclass отклонит объявление.",
    ),
    "6.1": (
        "Type hints описывают контракт для static checker, IDE и читателя; Python остаётся динамически типизированным во время выполнения.",
        "Annotations хранятся как metadata и сами не добавляют проверки типов. FastAPI и Pydantic отдельно читают их для schema и validation.",
        "Успешная статическая проверка не заменяет input validation, а допустимое runtime-преобразование может нарушать domain rule.",
        "Типизированные границы service находят ошибки до тестов, а Pydantic валидирует входящие request data.",
        "Аннотация `value: int` сама по себе не запрещает caller передать строку.",
    ),
    "7.5": (
        "GIL в CPython позволяет только одному thread выполнять Python bytecode в процессе в конкретный момент.",
        "Threads всё равно перекрывают ожидание I/O, потому что GIL освобождается вокруг многих blocking/native операций. Для CPU-bound Python обычно нужны processes, native code без GIL или внешние workers.",
        "GIL не является lock для приложения: многошаговые операции с общим состоянием и database invariants всё равно подвержены race conditions.",
        None,
        "Утверждение, что из-за GIL в threads нет races, смешивает планирование bytecode с атомарностью бизнес-операции.",
    ),
    "8.1": (
        "Последовательный код выполняет операции одну за другой; concurrency позволяет нескольким задачам продвигаться, а parallelism выполняет работу одновременно.",
        "Async и threads обычно дают concurrency для ожидания I/O, а processes способны дать parallel execution для CPU-bound Python.",
        "Concurrency уменьшает простой, но добавляет вопросы порядка, cancellation и shared state; одна CPU-операция сама по себе быстрее не становится.",
        None,
        "Выбор async для CPU-heavy работы без выноса из event loop увеличивает latency всех requests.",
    ),
    "8.2": (
        "Coroutine function объявляется через `async def`; вызов создаёт coroutine object, а не выполняет тело до конца.",
        "Объект запускается через `await` или scheduling как Task. Потерянная coroutine обычно приводит к warning `coroutine was never awaited`.",
        "Coroutine object одноразовый: после завершения его нельзя await повторно.",
        None,
        "Возврат coroutine object из кода, обещавшего готовое значение, переносит async boundary не тому caller.",
    ),
    "8.4": (
        "Event loop планирует готовые callbacks/tasks и ждёт I/O readiness или timers, когда готовой работы нет.",
        "Task кооперативно выполняется до `await`; затем loop запускает другую готовую task и возвращается к приостановленной после готовности awaitable.",
        "Одна blocking function в event-loop thread задерживает все остальные tasks этого loop.",
        "ASGI server выполняет application coroutines на event loop, поэтому endpoint dependencies обязаны соблюдать ту же границу.",
        "Blocking network или DB call внутри async endpoint останавливает обслуживание несвязанных requests.",
    ),
    "8.5": (
        "Asyncio Task планирует одну coroutine и хранит её состояние завершения, result, exception или cancellation.",
        "`create_task` делает coroutine готовой к выполнению; caller должен сохранить reference и затем дождаться результата либо явно обработать outcome.",
        "Fire-and-forget внутри web process не является durable: shutdown может потерять task, а необработанное исключение останется только в logs.",
        None,
        "Создание task без сохранения reference скрывает сбои и не гарантирует завершение до остановки request или process.",
    ),
    "9.1": (
        "Thread выполняется внутри одного process и разделяет память, file descriptors и module state с другими threads.",
        "Threads удобны для blocking I/O libraries. Shared mutable state требует Lock или другой синхронизации; `join` ожидает завершения.",
        "GIL ограничивает CPU-bound parallelism Python-кода, но не предотвращает race conditions в многошаговых операциях.",
        None,
        "Check-then-act над общим состоянием без lock может потерять изменение, даже если отдельные операции кажутся атомарными.",
    ),
    "9.2": (
        "Multiprocessing запускает работу в отдельных processes с изолированной памятью и отдельными Python interpreters.",
        "Входы и результаты пересекают границу процесса через serialization и IPC. Это даёт CPU parallelism ценой startup, памяти и передачи данных.",
        "Targets и arguments обычно должны быть pickleable, а поведение запуска процесса различается между платформами.",
        None,
        "Передача живой Session, клиента с locks или локального closure в process часто ломает serialization или создаёт некорректную копию состояния.",
    ),
    "10.2": (
        "`SELECT` выбирает result columns и expressions; aliases задают имена результата, не меняя stored schema.",
        "Expressions вычисляются для rows после FROM/JOIN/filter/group. `SELECT *` связывает caller с изменениями schema и передаёт ненужные данные.",
        "Порядок SQL-результата не определён без `ORDER BY`, даже если локальный тест кажется стабильным.",
        "Repository для API выбирает только поля, необходимые response DTO.",
        "Неявный порядок или одинаковые имена columns делают pagination и mapping нестабильными.",
    ),
    "10.3": (
        "`WHERE` фильтрует исходные rows по boolean predicates до grouping и aggregation.",
        "AND имеет более высокий приоритет, чем OR, поэтому parentheses фиксируют намерение. Сравнения с NULL дают UNKNOWN и требуют `IS NULL` или `IS NOT NULL`.",
        "Функция вокруг indexed column может помешать простому index access path; решение проверяют через EXPLAIN.",
        None,
        "`status = 'paid' OR status = 'new' AND active` часто означает не ту группировку, которую читатель предполагает визуально.",
    ),
    "10.5": (
        "`ORDER BY` задаёт порядок результата, `LIMIT` ограничивает rows, а `OFFSET` пропускает строки для простой pagination.",
        "Несколько полей сортировки применяются слева направо. Уникальный tie-breaker вроде id нужен для детерминированных страниц при одинаковом основном значении.",
        "Большой OFFSET заставляет БД просмотреть и отбросить предыдущие rows, а concurrent inserts сдвигают границы страниц; keyset pagination масштабируется лучше.",
        None,
        "LIMIT/OFFSET без стабильного уникального ordering возвращает пропущенные или повторные rows между страницами.",
    ),
    "10.8": (
        "`GROUP BY` формирует группы rows и возвращает одну result row для каждого уникального grouping key.",
        "Aggregate functions считают значения внутри группы. Выбранные неагрегированные columns обычно должны находиться в GROUP BY.",
        "Сначала назови grain результата, например «одна строка на `user_id`», и только потом добавляй joins, способные размножить source rows.",
        None,
        "Grouping после one-to-many join может посчитать сумму дважды, если grain join мельче измеряемого показателя.",
    ),
    "10.9": (
        "`HAVING` фильтрует группы после aggregation, а `WHERE` отбирает исходные rows до формирования групп.",
        "Условие на обычные rows относится к WHERE; условие вроде `COUNT(*) >= 2` — к HAVING.",
        "Перенос фильтра через границу aggregation способен изменить и состав групп, и набор surviving groups.",
        None,
        "`WHERE COUNT(*) > 1` некорректен, потому что aggregate на этом этапе ещё не вычислен.",
    ),
    "10.11": (
        "`LEFT JOIN` сохраняет каждую row левой таблицы и подставляет NULL в columns правой стороны при отсутствии совпадения.",
        "Фильтр правой таблицы в ON влияет на присоединяемые совпадения; тот же фильтр в WHERE удаляет NULL-rows и фактически превращает результат в INNER JOIN.",
        "Для числа связанных rows считай nullable primary key правой таблицы, а не `COUNT(*)`.",
        None,
        "Условие `right.active = true` в WHERE неожиданно удаляет left rows без активной связи.",
    ),
    "10.14": (
        "Subquery — запрос, используемый как expression или table source внутри другого SQL statement.",
        "Scalar subquery должен вернуть не больше одной row; `IN` сравнивает с набором values; subquery в FROM создаёт derived table с alias.",
        "Выбирай форму по ясности смысла. Производительность зависит от planner и данных, поэтому универсального правила «JOIN всегда быстрее» нет.",
        None,
        "Scalar subquery с несколькими rows вызывает ошибку, а `NOT IN` при наличии NULL может дать неожиданный UNKNOWN.",
    ),
    "10.21": (
        "Window function вычисляет значение по связанным rows, сохраняя каждую исходную row, в отличие от GROUP BY.",
        "`OVER` задаёт partition, order и frame. Типичные случаи — ranking, running total и сравнение с предыдущей row.",
        "Ordering внутри OVER управляет window calculation; финальный порядок результата всё равно требует отдельного ORDER BY.",
        "Report может добавить накопительную сумму по customer, не теряя отдельные transactions.",
        "Отсутствие tie-breaker в window ordering делает `row_number` недетерминированным при равных значениях.",
    ),
    "11.2": (
        "Database constraints защищают invariants для всех writers: NOT NULL, UNIQUE, CHECK, primary key и foreign key.",
        "База проверяет constraints во время write или завершения transaction и отклоняет неверное состояние; приложение преобразует конкретный conflict в понятную ошибку.",
        "Application validation улучшает UX, но не заменяет DB constraint при конкурентных requests.",
        None,
        "Проверка уникальности через SELECT перед INSERT подвержена race; окончательной гарантией должен быть UNIQUE constraint.",
    ),
    "11.3": (
        "Normalization организует relations так, чтобы уменьшить дублирование фактов и update anomalies; для Junior важна практическая идея 1NF–3NF.",
        "Сущности разделяют и связывают keys, чтобы у факта был один source of truth. Denormalization намеренно дублирует данные ради измеренной задачи чтения.",
        "Normalization не означает максимальное число tables: границы определяются смыслом данных и зависимостями обновления.",
        None,
        "Копирование email пользователя во множество order rows создаёт противоречия при обновлении и размывает source of truth.",
    ),
    "11.4": (
        "Database index — вспомогательная структура, позволяющая находить упорядоченные ranges ключей без полного table scan.",
        "Index ускоряет подходящий access path, но занимает место и добавляет работу INSERT/UPDATE/DELETE. Planner может выбрать sequential scan, когда совпадает большая часть rows.",
        "Проектируй indexes по реальным WHERE/JOIN/ORDER patterns и проверяй `EXPLAIN ANALYZE`; index на каждую column вреден.",
        None,
        "Index без конкретного query shape и selectivity увеличивает стоимость writes и может никогда не использоваться.",
    ),
    "11.8": (
        "`EXPLAIN` показывает план и estimates, а `EXPLAIN ANALYZE` действительно выполняет statement и добавляет actual rows и timing.",
        "Plan читают от дочерних nodes вверх, сравнивая estimated и actual rows, loops, scan type и buffers.",
        "ANALYZE реально выполняет изменяющий statement; такую проверку делают безопасно, например внутри transaction с rollback.",
        None,
        "Просмотр только общего времени скрывает ошибку оценки rows или большое число loops, которое станет дорогим на реальных данных.",
    ),
    "11.9": (
        "Transaction объединяет операции в одну атомарную границу; ACID означает atomicity, consistency, isolation и durability.",
        "Commit фиксирует изменения, rollback отменяет их. Consistency обеспечивается правильным кодом и constraints, а не буквой C автоматически.",
        "Transactions держат короткими и по возможности не выполняют внутри них сетевые вызовы, пока заняты locks и connection.",
        "Создание заказа и резервирование остатка должны входить в одну transaction, если этого требует invariant.",
        "Commit внутри каждого repository call способен сохранить половину use case после ошибки следующего шага.",
    ),
    "11.10": (
        "Isolation levels определяют, какие эффекты concurrent transactions могут наблюдать друг у друга.",
        "PostgreSQL Read Committed использует snapshot на statement, Repeatable Read сохраняет snapshot transaction, а Serializable может отменить transaction ради последовательной семантики.",
        "Более строгая isolation не бесплатна, а serialization failure требует retry всей transaction.",
        None,
        "Повышение isolation без названной anomaly увеличивает contention и может не защитить реальный invariant.",
    ),
    "12.1": (
        "HTTP — request/response protocol: request содержит method, target, headers и необязательное body, response — status, headers и необязательное body.",
        "Server разбирает request, выбирает route, выполняет application logic и сериализует response. HTTP semantics отделены от JSON и framework implementation.",
        "Успешная передача по сети не означает успех бизнес-операции: результат выражают status и body.",
        None,
        "Ответ 200 с ошибкой внутри JSON ломает clients, monitoring и стандартную retry/cache semantics.",
    ),
    "12.3": (
        "HTTP methods выражают намерение: GET читает, POST отправляет или создаёт, PUT заменяет ресурс по известному адресу, PATCH частично меняет, DELETE удаляет.",
        "Safety означает отсутствие запрошенного изменения состояния, idempotency — одинаковый целевой эффект повторного request. Framework не обеспечивает эти свойства автоматически.",
        "POST можно сделать безопасным для retry через idempotency key, а плохо спроектированный PUT всё равно способен иметь лишние side effects.",
        None,
        "Выбор method только по наличию body игнорирует cache, retry и ожидания clients.",
    ),
    "12.7": (
        "HTTP status code сообщает категорию и конкретный результат обработки request.",
        "Частые API-коды: 200, 201, 204 без body, 400 для некорректного request, 401 без authentication, 403 без права, 404, 409 conflict, 422 validation и 500 для неожиданной server error.",
        "Используй единый error body с machine-readable code и не раскрывай stack trace.",
        None,
        "Ответ 200 на любую ошибку заставляет client угадывать успех по тексту response.",
    ),
    "12.10": (
        "`Content-Type` описывает representation отправленного body, а `Accept` — форматы, которые client готов получить.",
        "Для JSON API отправитель обычно указывает `application/json`; charset важен для текстовых форматов, а parser следует объявленному media type.",
        "Строка, похожая на JSON, с неверным Content-Type не является тем же protocol contract.",
        None,
        "Смешение Accept и Content-Type приводит к ошибкам 415/406 или неверному parsing.",
    ),
    "12.11": (
        "Cookie — пара name/value, которую response устанавливает header-ом, а browser автоматически возвращает с учётом domain, path, срока и security attributes.",
        "HttpOnly запрещает чтение из JavaScript, Secure ограничивает передачу HTTPS, SameSite ограничивает cross-site отправку; ни один атрибут не заменяет server-side authorization.",
        "Cookie authentication требует защиты от CSRF, потому что browser прикрепляет cookies автоматически.",
        None,
        "Session cookie без HttpOnly, Secure и подходящего SameSite неоправданно расширяет поверхность атаки.",
    ),
    "12.13": (
        "HTTPS — HTTP поверх TLS, который даёт encryption в пути, integrity и authentication сервера по certificate.",
        "TLS handshake согласует keys и проверяет certificate chain; reverse proxy может завершить TLS и передать request приложению по доверенной сети.",
        "HTTPS не проверяет business permissions и не шифрует данные at rest.",
        None,
        "Безусловное доверие forwarded headers позволяет внешнему client выдать insecure request за HTTPS.",
    ),
    "12.20": (
        "API error contract — стабильная форма failure response с machine code, понятным message и необязательными field details.",
        "Domain и infrastructure exceptions переводятся на границе в подходящий status и безопасный payload; trace и secrets остаются в защищённых logs.",
        "Clients должны ветвиться по стабильному code/status, а не по точному человеческому тексту.",
        None,
        "Возврат raw exception string раскрывает детали реализации и создаёт нестабильный публичный contract.",
    ),
    "13.1": (
        "Authentication устанавливает личность requester, authorization решает, может ли эта identity выполнить действие над конкретным resource.",
        "Сначала проверяется credential, token или session, затем policy проверяет role, permission, ownership или attributes для операции.",
        "Авторизованный вход в систему не даёт автоматического права читать чужой объект.",
        None,
        "Скрытая admin-кнопка во frontend не является ни authentication, ни authorization: правило обязан проверять API.",
    ),
    "13.4": (
        "JWT — формат подписанного token с header, payload claims и signature; обычно он закодирован, но не зашифрован.",
        "Server проверяет signature, разрешённый algorithm, issuer, audience и time claims до доверия identity и permissions.",
        "Revocation и refresh lifecycle всё равно нужно проектировать; долгоживущий access JWT не становится безопасным автоматически.",
        None,
        "Декодирование payload без проверки signature и claims позволяет attacker подставить произвольную identity.",
    ),
    "13.13": (
        "CORS — browser policy, управляющая чтением responses JavaScript-кодом из другого origin.",
        "Для несimple request browser сначала отправляет preflight OPTIONS; server отвечает разрешёнными origins, methods, headers и credentials policy.",
        "CORS не является authentication и не блокирует curl или server-to-server clients.",
        None,
        "Wildcard origin вместе с credentials недопустим или опасен; разрешённые origins задают явно.",
    ),
    "14.1": (
        "FastAPI application — ASGI callable, участвующий в асинхронном request lifecycle.",
        "ASGI server принимает события соединения, FastAPI выбирает route, валидирует input, разрешает dependencies, вызывает endpoint и сериализует response.",
        "Endpoint лучше оставлять adapter-ом, а business rules и transaction boundary тестировать без framework request objects.",
        None,
        "Создание DB session и domain logic прямо в каждом route дублирует lifecycle и error handling.",
    ),
    "14.3": (
        "Path parameter идентифицирует часть resource path и преобразуется из текста по annotation endpoint.",
        "`/users/{user_id}` связывает segment с параметром; constraints отклоняют значение до handler. Static routes не должны случайно затеняться широким dynamic route.",
        "Path parameter обязателен для совпавшего route; необязательные filters относятся к query parameters.",
        None,
        "Конфликт `/users/{user_id}` и `/users/me` может отправить `me` в int validation вместо нужного handler.",
    ),
    "14.4": (
        "Query parameters описывают обязательные или необязательные modifiers после `?`: pagination, filtering и sorting.",
        "FastAPI читает annotations и defaults, применяет `Query` constraints и отражает contract в OpenAPI.",
        "Ограничивай максимальный page size и разрешённые sort fields вместо подстановки произвольного input в SQL.",
        None,
        "`limit: int | None` без default всё равно остаётся обязательным параметром.",
    ),
    "14.5": (
        "Request body переносит структурированный input; FastAPI обычно валидирует JSON через Pydantic model.",
        "Body bytes декодируются по media type, разбираются как JSON и рекурсивно валидируются до передачи typed model в endpoint.",
        "Schema validation проверяет форму и ranges; business invariants, зависящие от БД, относятся к service logic и constraints.",
        None,
        "Raw dict повсюду лишает код generated schema, typed access и точных field errors.",
    ),
    "14.6": (
        "Response model задаёт публичную output schema и фильтрует или сериализует результат endpoint.",
        "FastAPI проверяет returned value по model и публикует representation в OpenAPI.",
        "Отдельная public schema не позволяет password hash и внутренним flags случайно попасть из ORM object в response.",
        None,
        "Возврат ORM `__dict__` или неограниченной model способен раскрыть secret и internal fields.",
    ),
    "14.12": (
        "Exception handler преобразует определённый тип исключения в единый HTTP response на границе application или router.",
        "Domain code поднимает domain exception, а FastAPI handler сопоставляет его со status и безопасным payload; неожиданные ошибки остаются server failures.",
        "Не преобразуй любой Exception в 400: так programming bugs маскируются под ошибку client.",
        None,
        "Передача `str(database_error)` клиенту раскрывает SQL/schema details и создаёт нестабильный contract.",
    ),
    "14.13": (
        "Middleware оборачивает request/response flow для cross-cutting задач: request ID, timing или security headers.",
        "Каждый middleware выполняется до внутреннего app и после его response; порядок влияет на наблюдение и обработку ошибок.",
        "Domain authorization обычно требует resolved user/resource и относится к dependencies или services, а не к общему middleware.",
        None,
        "Чтение streaming request body в middleware без восстановления потока может оставить endpoint без body.",
    ),
    "14.14": (
        "FastAPI lifespan управляет ресурсами уровня application process: connection pools и общими HTTP clients.",
        "Async context manager выполняет setup до `yield` и cleanup после него при shutdown; tests тоже должны входить в lifespan.",
        "Application resources могут быть общими, но request-specific Session и user state хранить в них нельзя.",
        None,
        "Новый дорогой client на каждый request разрушает pooling, а незакрытый общий client оставляет ресурсы при shutdown.",
    ),
    "14.15": (
        "FastAPI поддерживает sync и async endpoints; async полезен, когда весь dependency stack выполняет awaitable I/O.",
        "Async endpoint работает на event loop, а sync endpoint обычно отправляется в thread pool, чтобы blocking work не останавливал loop напрямую.",
        "`async def` не превращает sync driver в неблокирующий: нужен async driver/client или явный offload.",
        None,
        "`requests` или sync DB driver внутри async endpoint блокирует loop несмотря на объявление async function.",
    ),
    "14.16": (
        "FastAPI `BackgroundTasks` запускает небольшую in-process работу после отправки response.",
        "Task работает в том же application process и не имеет гарантий durable delivery, distributed retry или восстановления после crash.",
        "Используй механизм для небольших некритичных действий; durable jobs требуют queue/worker и idempotency.",
        None,
        "Критическое письмо или payment только через BackgroundTasks может потеряться при restart process.",
    ),
    "14.20": (
        "Практичная структура FastAPI отделяет HTTP routers и schemas от use-case services и деталей data access.",
        "Routers адаптируют request/response, services содержат business workflow и transaction decisions, repositories или query modules изолируют persistence, когда добавляют реальную ценность.",
        "Не создавай pass-through layers без поведения: boundary должна соответствовать изменению или test seam.",
        None,
        "Все concerns внутри routes усложняют transaction tests и проверку business logic без framework.",
    ),
    "16.1": (
        "SQLAlchemy Engine владеет SQL dialect и connection pool; это долгоживущая application-level factory, а не ORM Session.",
        "Session получает connection, когда нужен SQL, и возвращает его согласно transaction и session lifecycle.",
        "Pool size согласуют с возможностями БД и workload; новый Engine на каждый request уничтожает пользу pooling.",
        None,
        "Незакрытая Session удерживает transaction или connection, пока pool не исчерпается.",
    ),
    "16.2": (
        "Declarative ORM models сопоставляют Python classes и attributes с tables и columns через `Mapped` и `mapped_column` в SQLAlchemy 2.x.",
        "Class metadata формирует описание schema для ORM statements и migration tooling; instances представляют rows в состоянии Session.",
        "Изменение model code не мигрирует существующую production database: schema transition выполняет Alembic revision.",
        None,
        "`create_all` как production migration strategy не даёт versioned и reviewable истории schema.",
    ),
    "16.3": (
        "Relationship описывает ORM-навигацию между entities; foreign key column остаётся источником referential truth в БД.",
        "`back_populates` связывает направления; one-to-many, many-to-one и many-to-many определяют collection/scalar форму и loading behavior.",
        "Relationship не выбирает автоматически эффективный eager loading и безопасную cascade semantics.",
        None,
        "Смешение ORM relationship и ownership в БД может настроить delete cascade, удаляющий лишние данные.",
    ),
    "16.5": (
        "Session lifecycle: создать, использовать в одном unit of work, выполнить commit или rollback и закрыть.",
        "FastAPI yield-dependency может владеть одной Session на request; service решает исход transaction, а cleanup всегда закрывает Session.",
        "Одну AsyncSession нельзя одновременно использовать в нескольких tasks: она содержит mutable transaction и identity state.",
        None,
        "Module-global Session переносит tracked objects и transaction failures между requests.",
    ),
    "16.6": (
        "SQLAlchemy 2.x `select()` строит явное SQL expression, выполняемое через Session.",
        "`where` добавляет predicates; `session.scalars(statement)` возвращает первую выбранную entity или value column; `one_or_none` требует не больше одной row, а `first` просто берёт одну.",
        "Result method выбирают по ожидаемой cardinality, а не скрывают duplicate rows.",
        None,
        "`.first()` там, где требуется уникальность, скрывает duplicate-data bug, который показал бы `.one_or_none()`.",
    ),
    "16.8": (
        "`add` присоединяет новую entity, `flush` отправляет pending SQL внутри transaction, `commit` фиксирует её, `refresh` перечитывает значения из БД.",
        "Autoflush может сработать перед query; generated primary key часто доступен после flush без commit.",
        "После commit objects могут стать expired в зависимости от configuration; refresh не заменяет правильного transaction ownership.",
        None,
        "Commit только ради получения id ломает атомарный use case; внутри открытой transaction достаточно flush.",
    ),
    "16.9": (
        "Rollback отменяет текущую database transaction и обязателен перед повторным использованием Session после flush или commit error.",
        "SQLAlchemy помечает transaction как failed; перехват `IntegrityError` без rollback оставляет дальнейшие операции нерабочими.",
        "После rollback известный constraint conflict переводят в domain error, а неожиданный сбой поднимают с исходной причиной.",
        None,
        "Query сразу после IntegrityError без rollback вызывает pending-rollback error и скрывает исходный conflict.",
    ),
    "16.10": (
        "Explicit transaction boundary объединяет все database changes одного use case в одно решение commit или rollback.",
        "`with session.begin()` делает commit при normal exit и rollback при exception; repositories не должны незаметно фиксировать отдельные части.",
        "External network calls по возможности выносят за transaction, чтобы не удерживать locks и connection.",
        None,
        "Несколько скрытых commits в repository оставляют частичные данные после ошибки позднего шага.",
    ),
    "16.13": (
        "N+1 — один query для parent rows и затем отдельный relationship query для каждого parent.",
        "Lazy loading запускает повторные queries; проблему находят по SQL logs или query-count test и выбирают `selectinload`, `joinedload` либо explicit projection по cardinality.",
        "Eager load должен загружать только нужные use case данные; огромный joined graph размножает rows и расходует память.",
        "Список users с roles часто создаёт N+1, когда serialization обращается к каждой lazy relationship.",
        "Cache не исправляет ORM query shape, который делает сотни лишних round trips.",
    ),
    "16.17": (
        "AsyncEngine и AsyncSession используют async DB driver, поэтому SQL I/O можно await без остановки event loop.",
        "ORM state и transaction semantics сохраняются: одна AsyncSession на request или task, явный await для I/O и понятный владелец commit/rollback.",
        "Не разделяй одну AsyncSession между tasks в `gather`: каждой concurrent единице нужна своя session и transaction.",
        None,
        "Переход на AsyncSession без async driver или с blocking data path не делает работу асинхронной.",
    ),
    "17.1": (
        "Migration — versioned и reviewable переход существующей database schema или данных; изменение ORM model само не обновляет deployed database.",
        "Alembic revisions определяют upgrade и downgrade steps и образуют ordered history, одинаково применяемую в окружениях.",
        "Schema changes должны оставаться совместимыми со старой и новой версиями application во время rolling deploy.",
        None,
        "`create_all` при startup не умеет безопасно выразить rename, backfill или поэтапное добавление constraint.",
    ),
}

# Не публикуем англоязычные черновики выше: генератор использует только
# проверенную русскую таблицу.
COMPACT = COMPACT_RU


def compact_dossier(lesson: dict, values: tuple[str, str, str, str | None, str]) -> LessonDossier:
    what, mechanism, nuance, backend, mistake = values
    outline = tuple(str(item).rstrip(".") for item in lesson.get("outline", [])) or (lesson["title"],)
    must = outline[:4]
    return LessonDossier(
        what=what,
        mechanism=mechanism,
        nuance=nuance,
        backend=backend,
        mistakes=(mistake,),
        required=must,
        useful=outline[4:6] or ("один короткий пример кода с результатом",),
        skip_deep=("внутренние детали реализации за пределами обычных Junior follow-up",),
        practices=(
            f"**A · Предсказание результата.** Измени один input в примере `{outline[0]}` и предскажи результат до запуска.",
            f"**B · Найди ошибку.** Найди код, нарушающий `{outline[min(1, len(outline) - 1)]}`, и объясни конкретное последствие.",
            f"**D · Небольшая задача.** Реализуй минимальную функцию или query, демонстрирующие `{outline[0]}`, и добавь один edge-case test.",
            f"**E · Ответ на собеседовании.** Объясни {lesson['title']} за 45–60 секунд и назови одно ограничение.",
        ),
        question=f"Что такое {lesson['title']} и как это работает?",
        short_answer=what,
        junior_answer=f"{what} {mechanism} Важное ограничение: {nuance}",
        follow_up_question=f"Какая типичная ошибка связана с {lesson['title']}?",
        follow_up_answer=mistake,
        rubric=must,
    )


STAGE_WHAT = {
    0: "Тема помогает построить точный ответ: определение, механизм, короткий пример и честное ограничение.",
    1: "Это часть Python object model: код работает с объектами, namespaces и bindings, а не с независимыми «коробками значений».",
    2: "Это операция или гарантия стандартной коллекции Python; выбор структуры зависит от порядка, уникальности и стоимости основных операций.",
    3: "Это часть контракта Python function: важно различать definition time, call time, signature и разрешение имён.",
    4: "Это протокол управления потоком: consumer и объект договариваются о шагах, завершении и обработке ошибок.",
    5: "Это элемент Python object model, который определяет состояние объекта, поиск поведения или способ композиции типов.",
    6: "Это статический контракт для checker и IDE; runtime-поведение Python и validation остаются отдельными слоями.",
    7: "Это практическая модель CPython для lifetime, памяти или конкурентности; детали реализации нужно отделять от спецификации языка.",
    8: "Это часть asyncio: event loop кооперативно планирует coroutines/tasks вокруг await points.",
    9: "Это модель выполнения работы с разной ценой shared memory, serialization и startup.",
    10: "Это SQL-конструкция, преобразующая набор строк; корректность начинается с grain, cardinality, NULL и явного ordering.",
    11: "Это механизм PostgreSQL, который защищает данные или выбирает access path при конкурентной работе.",
    12: "Это часть наблюдаемого HTTP contract: method/target/headers/body на входе и status/headers/body на выходе.",
    13: "Это security boundary: сервер проверяет утверждение и безопасно отказывает, не доверяя клиентскому UI.",
    14: "Это часть FastAPI request lifecycle между routing, validation, dependencies, handler и response serialization.",
    15: "Это часть Pydantic v2 boundary между недоверенным input, validated model и serialized output.",
    16: "Это часть SQLAlchemy 2.x data-access flow: statement, Session, identity map и transaction lifecycle.",
    17: "Это версионированный переход schema, который должен безопасно работать с кодом во время deploy.",
    18: "Это инструмент проверки observable contract с контролируемым setup, failure и cleanup.",
}


STAGE_MECHANISM = {
    0: "Сначала классифицируй вопрос, затем восстанови mental model и только после этого формулируй ответ.",
    1: "Проследи конкретный объект: какой у него type и identity, какие имена на него ссылаются и меняется object или binding.",
    2: "Сравни порядок, duplicates, mutability, lookup/membership и стоимость изменения; затем проверь edge cases коротким кодом.",
    3: "Отдели выполнение `def`, связывание arguments при вызове и разрешение names по LEGB.",
    4: "Определи инициатора шага, сохраняемое state, сигнал нормального завершения и cleanup при exception.",
    5: "Проследи instance/class namespaces, attribute lookup и направление зависимости между объектами.",
    6: "Покажи, что проверит static analyzer, что произойдёт runtime и где boundary должна добавить validation.",
    7: "Сначала измерь lifetime, allocations или contention и только затем связывай symptom с особенностью CPython.",
    8: "Проследи coroutine от создания через scheduling и await points до result, cancellation и cleanup.",
    9: "Определи workload: blocking I/O, CPU-bound Python или изолированная задача; затем оцени memory sharing и IPC.",
    10: "Мысленно выполняй FROM/JOIN → WHERE → GROUP/HAVING → SELECT → ORDER/LIMIT и считай строки после каждого этапа.",
    11: "Назови invariant и concurrent scenario, затем проверь constraint, transaction boundary и фактический query plan.",
    12: "Опиши один request и один response, включая поведение retry, cache и error contract только там, где они относятся к теме.",
    13: "Назови asset, threat, trust boundary, server-side verification и безопасный failure result.",
    14: "Проследи request через router, Pydantic validation, dependency graph, service и response model.",
    15: "Проверь четыре состояния: missing, explicit null, invalid type/value и сериализованный результат.",
    16: "Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback.",
    17: "Раздели upgrade, совместимость старого/нового кода, backfill и rollback; autogenerate обязательно review.",
    18: "Сформулируй observable behavior, выбери isolation boundary и добавь case, который падает при реальном regression.",
}


STAGE_MISTAKE = {
    0: "Заменить ответ списком терминов без механизма и примера.",
    1: "Смешать mutation объекта с rebinding имени и неверно предсказать alias.",
    2: "Выбрать collection по привычке и не проверить duplicates, order или lookup cost.",
    3: "Смешать definition time и call time либо скрыть неясную signature за `**kwargs`.",
    4: "Забыть состояние protocol, сигнал завершения или cleanup при exception.",
    5: "Добавить inheritance ради нескольких строк переиспользования и получить жёсткую связь типов.",
    6: "Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.",
    7: "Принять деталь CPython за гарантию языка или оптимизировать без измерения.",
    8: "Выполнить blocking call в event loop или создать coroutine и не await/schedule её.",
    9: "Разделить mutable state без synchronization или отправить несериализуемый object в process.",
    10: "Не определить cardinality результата и замаскировать неверный query через DISTINCT.",
    11: "Добавить index/lock без конкретного query или invariant и не проверить план/конкурентный case.",
    12: "Возвращать 200 для любой ошибки или проектировать retry без понимания idempotency.",
    13: "Перенести security check в UI либо считать CORS/JWT самостоятельной авторизацией.",
    14: "Открыть глобальный request resource или спрятать domain logic в framework hook.",
    15: "Смешать missing и explicit null либо считать coercion бизнес-валидацией.",
    16: "Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.",
    17: "Принять autogenerate без review или выпустить несовместимые schema/code изменения одним шагом.",
    18: "Mock-нуть реализацию вместо внешней границы и получить тест, не проверяющий observable behavior.",
}


def fallback_dossier(lesson: dict, stage_number: int, explain_point) -> LessonDossier:
    outline = [str(item).rstrip(".") for item in lesson.get("outline", [])] or [lesson["title"]]
    explanations: list[str] = []
    for point in outline[:6]:
        explanation = explain_point(point)
        explanations.append(f"**{point}.** {explanation}")
    mechanism = STAGE_MECHANISM.get(
        stage_number,
        "Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.",
    )
    if explanations:
        mechanism += "\n\n" + "\n\n".join(explanations)
    first = outline[0]
    second = outline[1] if len(outline) > 1 else lesson["title"]
    answer = (
        f"{lesson['title']} — тема, в которой я сначала фиксирую `{first}`, затем объясняю `{second}` на коротком примере. "
        f"Ключевой механизм: {STAGE_MECHANISM.get(stage_number, 'вход преобразуется в наблюдаемый результат по явному контракту')} "
        f"Главная практическая ошибка — {STAGE_MISTAKE.get(stage_number, 'игнорировать ограничение механизма')}"
    )
    return LessonDossier(
        what=STAGE_WHAT.get(stage_number, f"Тема **{lesson['title']}** описывает отдельный контракт backend-разработки."),
        mechanism=mechanism,
        nuance=f"Граница Junior: уверенно объясняй `{first}` и `{second}` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.",
        backend=None if stage_number in {1, 2, 3, 4, 5, 6, 7, 9, 28} else f"В backend эта тема важна в том месте, где применяется `{first}`; проверяй именно наблюдаемый contract, а не название инструмента.",
        mistakes=(STAGE_MISTAKE.get(stage_number, "Игнорировать ограничение механизма и проверять только happy path."),),
        required=tuple(outline[:4]),
        useful=tuple(outline[4:6]) or (f"связать {lesson['title']} с коротким рабочим примером",),
        skip_deep=("implementation internals, не влияющие на Junior-код и типичный interview follow-up",),
        practices=(
            f"**A · Prediction/reasoning.** Предскажи результат минимального примера для `{first}` до запуска.",
            f"**B · Find the bug.** Найди нарушение `{second}` и объясни конкретное последствие.",
            f"**E · Interview explanation.** Дай ответ про {lesson['title']} за 60 секунд: определение, механизм, пример, ограничение.",
        ),
        question=f"Что такое {lesson['title']} и какой механизм здесь важно понимать Junior-разработчику?",
        short_answer=f"{lesson['title']}: {STAGE_WHAT.get(stage_number, 'это отдельный технический контракт')}",
        junior_answer=answer,
        follow_up_question=f"Какое ограничение или типичная ошибка относится именно к теме {lesson['title']}?",
        follow_up_answer=STAGE_MISTAKE.get(stage_number, "Нужно назвать конкретный failure path и способ его проверить."),
        rubric=tuple(outline[:4]),
    )


def dossier_for(lesson: dict, stage_number: int, explain_point) -> LessonDossier:
    if lesson["number"] in CURATED:
        dossier = CURATED[lesson["number"]]
    elif lesson["number"] in COMPACT:
        dossier = compact_dossier(lesson, COMPACT[lesson["number"]])
    else:
        dossier = fallback_dossier(lesson, stage_number, explain_point)
    return russianize_dossier(dossier)
