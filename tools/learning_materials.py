"""Topic-specific learning copy for the curriculum publisher.

The module deliberately separates teaching material from taxonomy metadata.
Every published lesson gets a Learn flow; high-frequency Junior topics can
override the generic stage-aware material with a reviewed dossier below.
"""

from __future__ import annotations

from dataclasses import dataclass, field


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
            "`dict` — изменяемое отображение пар key-value. Ключи уникальны и должны быть hashable; значения могут быть "
            "любыми. С Python 3.7 insertion order гарантирован языком."
        ),
        mechanism=(
            "Dict использует hash table: по hash ключа ищется позиция, затем equality подтверждает совпадение. Lookup, insert "
            "и delete в среднем O(1). `keys()`, `values()` и `items()` возвращают динамические views. Обновление существующего "
            "ключа меняет value, но не перемещает ключ в порядке."
        ),
        nuance=(
            "`data[key]` поднимает `KeyError`, `.get(key)` возвращает `None`, `.get(key, default)` — default и не меняет dict. "
            "`.setdefault(key, default)` при отсутствии вставляет default и всегда возвращает итоговое значение. Для накопления "
            "многих групп часто яснее `defaultdict(list)`."
        ),
        backend="Dict удобен для индексирования ORM/DTO объектов по id и для чтения необязательных HTTP headers или JSON fields.",
        mistakes=(
            "`user['email']` падает с `KeyError`, если поле действительно необязательное; используй `.get` только когда отсутствие допустимо.",
            "`data[[1, 2]] = 'value'` падает с `TypeError: unhashable type: 'list'`.",
            "`bucket = data.setdefault('roles', [])` изменяет dict при отсутствующем ключе — в отличие от `.get`.",
        ),
        required=("hashable и уникальные keys", "`.get` vs `[]`", "`.setdefault`", "insertion order", "средняя O(1) lookup"),
        useful=("merge через `|` и `update`", "views и безопасная итерация", "когда выбрать defaultdict"),
        skip_deep=("размер таблицы, perturb algorithm и layout CPython",),
        practices=(
            "**A · Code prediction.** Обнови существующий ключ и предскажи `list(data)`.",
            "**B · Find the bug.** Исправь чтение необязательного `Authorization` без сокрытия обязательных полей.",
            "**C · Rewrite.** Перепиши ручное группирование сначала с `setdefault`, затем сравни с `defaultdict(list)`.",
            "**D · Small task.** Построй индекс пользователей по id и отклони дубликаты.",
            "**F · Backend scenario.** Выбери структуру для ответа API, где важны порядок и lookup по id.",
        ),
        question="Что такое `dict`, как работает lookup и чем `.get()` отличается от `[]` и `.setdefault()`?",
        short_answer="Dict — mutable mapping на hash table; lookup в среднем O(1), keys hashable. `[]` даёт KeyError, `.get` не меняет dict, `setdefault` может вставить default.",
        junior_answer=(
            "`dict` хранит пары key-value; keys уникальны и hashable. В среднем lookup работает за O(1), потому что сначала "
            "используется hash, а затем equality. `data[key]` нужен, когда ключ обязателен, и поднимет `KeyError` при ошибке. "
            "`.get` удобен для допустимо отсутствующего значения и не меняет dict. `.setdefault` возвращает значение, но при "
            "отсутствии ещё и вставляет default. Dict сохраняет insertion order, а замена value не перемещает ключ."
        ),
        follow_up_question="Когда `.setdefault()` лучше заменить на `defaultdict(list)`?",
        follow_up_answer="Когда код систематически группирует много значений по keys: defaultdict убирает повторяющееся создание bucket. Для единичной вставки setdefault проще и не меняет тип mapping.",
        example="""```python
user = {"id": 1, "name": "Daniyar"}

print(user.get("name"))              # Daniyar
print(user.get("email"))             # None
print(user.get("email", "unknown"))  # unknown

roles = user.setdefault("roles", [])
roles.append("reader")
print(user["roles"])                 # ['reader']
```""",
        rubric=("mutable mapping", "hashable unique keys", "average O(1)", "insertion order", "get/setdefault semantics"),
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
            "Dependency Injection — передача нужной зависимости извне вместо создания её внутри handler. В FastAPI `Depends` "
            "описывает dependency graph, который framework разрешает для каждого request."
        ),
        mechanism=(
            "FastAPI читает signature endpoint и dependencies, вызывает их в правильном порядке и передаёт результаты дальше. "
            "Одинаковая dependency по умолчанию кэшируется один раз в рамках request. Dependency может зависеть от другой dependency; "
            "yield-вариант выполняет setup до handler и cleanup после response/error."
        ),
        nuance=(
            "Request-scoped cache не является глобальным cache. Не храни request-specific Session или user в module global. "
            "Dependencies удобны для границ framework — auth, session, settings — но сложные business rules лучше оставить service."
        ),
        backend="`get_current_user` может зависеть от token parser, а endpoint получает уже проверенного user; dependency override упрощает тест.",
        mistakes=(
            "Вызвать dependency вручную как обычную функцию и ожидать, что FastAPI разрешит её sub-dependencies.",
            "Создать глобальную SQLAlchemy Session и возвращать её всем requests.",
            "Поместить всю бизнес-логику в огромную dependency graph, которую трудно тестировать отдельно.",
        ),
        required=("зачем DI", "dependency graph", "per-request cache", "yield cleanup", "test overrides"),
        useful=("`Annotated` aliases", "`use_cache=False`", "граница dependency/service"),
        skip_deep=("внутренние классы решения dependency graph FastAPI",),
        practices=(
            "**A · Flow prediction.** Расположи вызовы parent dependency, child dependency, endpoint и cleanup.",
            "**B · Find the bug.** Найди глобальную Session в dependency module.",
            "**C · Rewrite.** Вынеси чтение X-Role в `require_admin`.",
            "**D · Small task.** Реализуй защищённый `/admin` endpoint с hidden tests.",
        ),
        question="Как работает `Depends` в FastAPI и каков lifecycle dependency?",
        short_answer="Depends объявляет dependency graph; FastAPI разрешает его на request, кэширует одинаковые dependencies и выполняет cleanup yield-dependency.",
        junior_answer=(
            "`Depends` позволяет endpoint явно объявить, что ему нужны user, Session или settings. FastAPI строит graph по signatures, "
            "вызывает dependencies и передаёт результаты в handler. Внутри одного request одинаковая dependency обычно выполняется один "
            "раз. Если dependency использует `yield`, код после yield работает как cleanup. В тестах dependency можно override-нуть."
        ),
        follow_up_question="Чем request cache dependency отличается от singleton?",
        follow_up_answer="Результат переиспользуется только внутри одного request; следующий request разрешает dependency заново. Singleton живёт между requests на уровне приложения.",
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
            "SQLAlchemy `Session` — рабочая область ORM: она отслеживает entities, хранит identity map, собирает изменения "
            "как unit of work и управляет transaction. Это не просто один connection."
        ),
        mechanism=(
            "Новая entity после `add` становится pending; при flush INSERT/UPDATE/DELETE уходят в текущую transaction, а объект "
            "становится persistent. Identity map гарантирует один Python object на пару `(mapped class, primary key)` внутри Session. "
            "После close/expunge объект detached и lazy loading больше не имеет активного Session context."
        ),
        nuance=(
            "Session получает connection по необходимости. `flush` отправляет SQL, но не делает commit; после flush error нужен rollback. "
            "Обычно один request/use case владеет одной Session. AsyncSession нельзя одновременно использовать из нескольких tasks."
        ),
        backend="FastAPI yield-dependency создаёт Session на request, service задаёт transaction boundary, а cleanup закрывает Session.",
        mistakes=(
            "Создать глобальную Session для всего приложения — state и transaction начнут протекать между requests.",
            "Коммитить внутри каждого repository method и разрушать атомарность use case.",
            "Продолжить работу после IntegrityError без `rollback()`.",
        ),
        required=("identity map", "unit of work", "основные entity states", "flush vs commit", "request scope"),
        useful=("expire/refresh", "autoflush", "transaction context manager"),
        skip_deep=("внутренние события unit-of-work sorter",),
        practices=(
            "**A · Code prediction.** Два `session.get(User, 1)` — сравни identity результатов.",
            "**B · Find the bug.** Найди global Session и commit в repository.",
            "**C · Rewrite.** Перенеси commit на service/use-case boundary.",
            "**D · Small task.** Реализуй `load_twice` и пройди hidden identity-map test.",
        ),
        question="Что такое SQLAlchemy Session и зачем ей identity map?",
        short_answer="Session — unit of work + identity map + transaction state; в одной Session одна DB row представлена одним Python object.",
        junior_answer=(
            "Session отслеживает ORM objects и их изменения, объединяет их в unit of work и владеет transaction state. Identity map "
            "хранит уже загруженные объекты по class и primary key, поэтому повторный `get` в той же Session обычно возвращает тот же "
            "Python object. Flush отправляет SQL внутри transaction, а commit завершает её. Для web request обычно создают отдельную Session."
        ),
        follow_up_question="Чем `flush` отличается от `commit`?",
        follow_up_answer="Flush синхронизирует ORM state с БД внутри открытой transaction и может получить generated id; commit фиксирует transaction. После rollback результат flush не сохраняется.",
        example="""```python
with Session(engine) as session:
    first = session.get(User, 1)
    second = session.get(User, 1)

    print(first is second)  # True: identity map
```""",
    ),
}


# Compact dossiers cover the rest of the high-frequency Junior core. They are
# intentionally factual topic notes, not stage prompts. Rich dossiers above
# override them for the lessons used in the manual acceptance pass.
COMPACT: dict[str, tuple[str, str, str, str | None, str]] = {
    "1.1": (
        "Python name is a label in a namespace bound to an object; assignment binds a name and normally does not copy the object.",
        "Each object has a type, identity and value. `a = b` makes both names refer to the same object; later rebinding `a = ...` changes only name `a`, while mutation is visible through every alias.",
        "Function arguments use the same object-reference model: a function can mutate a passed list, but rebinding its local parameter does not rebind the caller's name.",
        None,
        "Treating a variable as an independent box leads to wrong predictions for aliases and function arguments.",
    ),
    "1.3": (
        "Mutable objects can change while keeping identity; immutable objects cannot be changed in place and an apparent update creates or binds another object.",
        "Lists, dicts and sets expose mutating operations. Integers, strings, bytes and tuples do not. A tuple itself is immutable but may contain a mutable element.",
        "Mutability matters more than the syntax: `name += value` may mutate a list but creates a new string object.",
        "Shared mutable request/config defaults can leak state between calls.",
        "Confusing mutation with rebinding makes a caller's data change unexpectedly through an alias.",
    ),
    "1.4": (
        "A hashable object has a stable hash and equality behavior, so it can be a dict key or set element.",
        "A hash table uses `hash(key)` to find candidates and `==` to confirm a match. Objects that compare equal must have equal hashes; state involved in equality must not change while used as a key.",
        "A tuple is hashable only when all elements are hashable. Custom equality often requires an explicit, consistent `__hash__` decision.",
        None,
        "Using list or dict as a key raises `TypeError: unhashable type`; making mutable state hashable can corrupt lookup semantics.",
    ),
    "1.5": (
        "Truthiness is Python's protocol for converting an object to boolean context such as `if value`.",
        "Python calls `__bool__`; if absent, it uses `__len__`; without both, an object is truthy. `None`, numeric zero and empty standard collections are falsy.",
        "`if value` merges several states. Use `is None` when zero, empty string or empty list is valid data rather than absence.",
        "Pagination offset `0` and an empty JSON array may be valid values and must not be confused with missing input.",
        "Replacing `if limit is None` with `if not limit` incorrectly rejects a valid zero when the contract permits it.",
    ),
    "1.6": (
        "Aliases are multiple names or container slots referring to one object; nested mutation through any alias changes that same object.",
        "Assignment and sequence repetition copy references. `[[]] * 3` repeats one inner-list reference three times, so mutating one visible row changes all three positions.",
        "Build independent nested values with a comprehension such as `[[] for _ in range(3)]`.",
        None,
        "Using multiplication for mutable nested defaults creates shared state that is difficult to notice in tests with one element.",
    ),
    "2.4": (
        "`set` is a mutable unordered collection of unique hashable elements; `frozenset` is its immutable hashable variant.",
        "Membership, add and remove are average O(1) through hashing. Union `|`, intersection `&` and difference `-` express standard set operations.",
        "Set iteration order is not a business contract. Sorting is required when output order matters; converting to set also discards duplicates.",
        "Sets are useful for permission membership or deduplication when original order is not required.",
        "Returning `list(set(values))` from an API silently loses deterministic ordering.",
    ),
    "2.6": (
        "A comprehension builds a list, dict or set from an expression, source iterable and optional filters; a generator expression stays lazy.",
        "The expression runs once per selected input item. Comprehension loop variables have their own scope in Python 3, while referenced outer names are read normally.",
        "Prefer a regular loop when there are several branches, side effects or nested transformations that hide intent.",
        None,
        "A dense nested comprehension can be syntactically valid but harder to review and debug than a four-line loop.",
    ),
    "3.5": (
        "`*args` collects extra positional arguments into a tuple, `**kwargs` collects extra keyword arguments into a dict; the same stars unpack values at a call site.",
        "Argument binding still enforces the signature. Forwarding wrappers commonly call `fn(*args, **kwargs)`, and duplicate values for one parameter raise `TypeError`.",
        "Do not replace a clear public signature with unlimited kwargs. Explicit keyword-only parameters produce better typing and API errors.",
        None,
        "Forwarding `fn(value, **{'value': other})` passes the same parameter twice and raises `TypeError`.",
    ),
    "3.7": (
        "LEGB is Python's name lookup order: Local, Enclosing, Global, Builtins.",
        "A read searches those scopes in order. Assignment inside a function makes the name local unless declared `global` or `nonlocal`, which can cause `UnboundLocalError` when the name is read before local assignment.",
        "Shadowing `list`, `id` or another builtin works but makes later calls confusing or broken.",
        None,
        "Assuming assignment updates a global while Python created a new local binding causes wrong state and `UnboundLocalError`.",
    ),
    "3.9": (
        "A closure is an inner function that retains access to free variables from its enclosing scope after the outer function returns.",
        "The function stores references to enclosing cells, not a frozen copy of every value. A factory can therefore capture configuration or deliberately retain mutable state.",
        "Closures created in a loop exhibit late binding unless the current value is bound through a factory, default argument or `partial`.",
        "A validator or callback factory can capture immutable configuration without global state.",
        "Expecting each loop-created lambda to remember its loop iteration usually produces the final loop value for all callbacks.",
    ),
    "4.1": (
        "An iterable can produce an iterator; an iterator is a stateful object that yields next values and is consumed.",
        "`iter(obj)` obtains the iterator and `next(it)` asks for one item. A list can create a fresh iterator for each loop, while a generator object is typically its own single-pass iterator.",
        "After exhaustion, an iterator stays exhausted; call the iterable again to obtain a new traversal when supported.",
        None,
        "Storing one generator and iterating it twice gives an empty second pass, unlike iterating the original list twice.",
    ),
    "4.2": (
        "The iterator protocol consists of `__iter__` returning an iterator and `__next__` returning an item or raising `StopIteration`.",
        "A custom iterator stores its current position. A `for` loop calls `iter`, repeatedly calls `next` and catches `StopIteration` internally.",
        "`StopIteration` is a control signal for the protocol, not an ordinary error to print or broadly catch in consumer code.",
        None,
        "Returning `None` instead of raising `StopIteration` creates an endless stream of None values instead of ending iteration.",
    ),
    "4.3": (
        "A generator function contains `yield`; calling it returns a generator object without running the body immediately.",
        "Each `next` resumes execution until the next `yield`, preserving local variables and instruction position. Return or falling off the end raises `StopIteration` to the consumer.",
        "Laziness reduces peak memory but generators are single-use and defer exceptions until iteration reaches the failing line.",
        "Generators naturally stream rows or chunks instead of collecting the entire result in memory.",
        "Converting a generator to list for logging before real use accidentally exhausts it.",
    ),
    "4.7": (
        "Exceptions are objects in a hierarchy; application errors usually derive from `Exception`, while `BaseException` also includes process-control signals such as `KeyboardInterrupt`.",
        "Python searches matching except clauses from top to bottom and unwinds stack frames until a handler is found; otherwise the traceback reaches the caller.",
        "Catch the narrow type you can handle. A broad catch must normally log context and re-raise rather than report false success.",
        "Domain exceptions can be translated to stable HTTP errors at the API boundary.",
        "Bare `except:` can swallow cancellation or shutdown signals and hide programming bugs.",
    ),
    "4.8": (
        "`try/except/else/finally` separates risky work, recovery, success-only work and unconditional cleanup.",
        "`except` runs for a matching exception, `else` only when the try block succeeds, and `finally` runs before control leaves by success, return or exception.",
        "Keep the try block narrow so unrelated bugs are not mistaken for the expected failure.",
        None,
        "A return inside finally overrides an earlier return or exception and can silently destroy diagnostic information.",
    ),
    "4.12": (
        "A context manager defines a reliable acquire/use/release boundary used by the `with` statement.",
        "`__enter__` returns the value bound after `as`; `__exit__` receives exception information and cleanup runs even when the body fails. A truthy `__exit__` return suppresses the exception.",
        "Suppress only errors the context manager intentionally handles; returning True accidentally can hide real failures.",
        "Files, locks, DB transactions and clients use context managers to make resource lifetime visible.",
        "Manual open/close without finally leaks resources on an exception path.",
    ),
    "5.1": (
        "A class is an object describing behavior and class attributes; an instance has its own identity and instance namespace.",
        "Attribute lookup starts on the instance, then follows the class MRO; methods found on the class become bound methods when read through an instance.",
        "A mutable class attribute is shared by instances until an instance shadows the name.",
        None,
        "Defining `items = []` on the class for per-instance data leaks mutations between all instances.",
    ),
    "5.5": (
        "Encapsulation groups state and behavior, abstraction exposes a relevant contract, and polymorphism lets different objects satisfy that contract.",
        "Python often uses duck typing: caller depends on available behavior rather than a concrete inheritance tree. ABC and Protocol can make the contract explicit when useful.",
        "Leading underscores communicate non-public API but are not access control; invariants still need methods/properties and tests.",
        "A service can accept any notifier implementing `send`, allowing a fake in tests and different providers in production.",
        "Checking `type(obj) is ConcreteClass` blocks valid substitutes and defeats polymorphism.",
    ),
    "5.6": (
        "Inheritance models an is-a relationship; composition models has-a by giving an object explicit collaborators.",
        "Inheritance reuses and overrides behavior through MRO. Composition delegates to injected objects, reducing coupling and making substitutions local.",
        "Prefer composition for services/repositories. Inheritance is justified for a stable substitutable hierarchy or framework contract, not only code reuse.",
        "A notification service composed with an email provider is easier to test than a deep service subclass tree.",
        "Adding subclasses for every combination of behavior creates a fragile hierarchy and unclear MRO.",
    ),
    "5.10": (
        "`@dataclass` generates methods such as `__init__`, `__repr__` and equality from declared fields.",
        "Fields are processed in order; `field(default_factory=list)` creates a fresh mutable default per instance. `frozen=True` blocks normal field assignment but is not deep immutability.",
        "Dataclass is good for internal data/value objects; Pydantic handles untrusted validation and ORM models handle persistence.",
        None,
        "Using `items: list = []` is rejected/unsafe; mutable defaults need `default_factory`.",
    ),
    "6.1": (
        "Type hints describe contracts for static checkers, IDEs and readers; Python remains dynamically typed at runtime.",
        "Annotations are stored as metadata and do not automatically insert type checks. Frameworks such as FastAPI/Pydantic explicitly inspect them to build validation/schema behavior.",
        "A passing type check is not input validation, and a runtime-valid coercion may still be undesirable for a domain rule.",
        "Typed service boundaries catch many mistakes before tests while Pydantic validates incoming request data.",
        "Assuming `value: int` prevents a caller from passing a string leads to runtime surprises.",
    ),
    "7.5": (
        "The CPython GIL allows one thread at a time to execute Python bytecode in a process.",
        "Threads can still overlap waiting I/O because the GIL is released around many blocking/native operations. CPU-bound pure Python usually needs processes, native code that releases the GIL or external workers.",
        "The GIL is not an application lock: multi-step shared-state operations and database invariants still race.",
        None,
        "Claiming that threads cannot race because of the GIL confuses bytecode scheduling with atomic business operations.",
    ),
    "8.1": (
        "Sequential code does one operation after another; concurrency makes progress on multiple tasks; parallelism executes work simultaneously.",
        "Async and threads often provide concurrency for I/O waits, while processes can provide parallel execution for CPU-bound Python.",
        "Concurrency can reduce idle time but adds ordering, cancellation and shared-state concerns; it does not make a single CPU calculation faster by itself.",
        None,
        "Selecting async for CPU-heavy work without moving it off the event loop increases latency for every request.",
    ),
    "8.2": (
        "A coroutine function is declared with `async def`; calling it creates a coroutine object rather than executing the body to completion.",
        "The object runs when awaited or scheduled as a Task. Dropping it without either usually produces a 'coroutine was never awaited' warning.",
        "A coroutine object is single-use and cannot be awaited again after completion.",
        None,
        "Returning a coroutine object from code that promised a final value leaks the async boundary to the wrong caller.",
    ),
    "8.4": (
        "The event loop schedules ready callbacks/tasks and waits for I/O readiness or timers when nothing is ready.",
        "A task runs cooperatively until it awaits. The loop then resumes another ready task and later returns to the suspended one.",
        "One blocking function in the event-loop thread delays every other task on that loop.",
        "ASGI servers run application coroutines on event loops, so endpoint dependencies must respect the same boundary.",
        "Calling blocking network/DB code directly from an async endpoint stalls unrelated requests.",
    ),
    "8.5": (
        "An asyncio Task schedules one coroutine and stores its completion, result, exception or cancellation state.",
        "`create_task` makes a coroutine eligible to run; the caller should keep a reference and eventually await it or otherwise handle its outcome.",
        "Fire-and-forget inside a web process is not durable: process shutdown can lose the task, and unobserved exceptions may surface only in logs.",
        None,
        "Creating a task and dropping the reference hides failures and does not guarantee completion before request/process shutdown.",
    ),
    "9.1": (
        "A thread executes within one process and shares its memory, file descriptors and module state with other threads.",
        "Threads are useful for blocking I/O libraries. Shared mutable state needs Lock or another synchronization design; `join` waits for completion.",
        "The GIL limits CPU-bound Python parallelism but does not prevent race conditions between multi-step operations.",
        None,
        "Updating shared state with check-then-act logic without a lock can lose changes even when individual operations appear atomic.",
    ),
    "9.2": (
        "Multiprocessing runs work in separate processes with isolated memory and separate Python interpreters.",
        "Inputs/results cross process boundaries through serialization and IPC. This enables CPU parallelism but adds startup, memory and communication cost.",
        "Worker targets and arguments generally must be pickleable, and process startup behavior differs by platform.",
        None,
        "Passing a live Session, lock-bound client or local closure to a process often fails serialization or creates invalid copied state.",
    ),
    "10.2": (
        "`SELECT` chooses result columns or expressions; aliases name output fields without changing stored schema.",
        "Expressions are evaluated for rows produced by FROM/JOIN/filter/group stages. `SELECT *` couples callers to schema changes and transfers unused data.",
        "SQL result order is undefined without `ORDER BY`, even when a local test appears stable.",
        "API repositories project only fields needed for response DTOs.",
        "Relying on implicit row order or ambiguous duplicate column names makes pagination and mapping unstable.",
    ),
    "10.3": (
        "`WHERE` filters source rows using boolean predicates before grouping and aggregation.",
        "AND binds tighter than OR, so parentheses make intended logic explicit. NULL comparisons yield UNKNOWN and require `IS NULL`/`IS NOT NULL`.",
        "Functions applied to an indexed column can prevent a simple index access path; confirm with EXPLAIN rather than guessing.",
        None,
        "`status = 'paid' OR status = 'new' AND active` usually means something different from the visually assumed grouping.",
    ),
    "10.5": (
        "`ORDER BY` defines result order; `LIMIT` bounds rows and `OFFSET` skips rows for simple pagination.",
        "Multiple order columns are evaluated left to right. A unique tie-breaker such as id is needed for deterministic pages when primary sort values tie.",
        "Large OFFSET makes the database scan/discard earlier rows and concurrent inserts can shift page boundaries; keyset pagination scales better.",
        None,
        "Using LIMIT/OFFSET without a stable unique ordering returns duplicated or missing rows across pages.",
    ),
    "10.8": (
        "`GROUP BY` forms groups of rows and returns one result row per unique grouping key.",
        "Aggregate functions compute inside each group. Selected non-aggregate columns must normally appear in GROUP BY or be functionally determined under DB rules.",
        "Always state the grain, such as one row per `user_id`, before adding joins that may multiply source rows.",
        None,
        "Grouping after a one-to-many join can double-count totals if the join has a finer grain than the measure.",
    ),
    "10.9": (
        "`HAVING` filters groups after aggregation, while `WHERE` filters source rows before groups exist.",
        "A condition on ordinary rows belongs in WHERE; a condition such as `COUNT(*) >= 2` belongs in HAVING.",
        "Moving a filter across aggregation can change both which rows contribute and which groups survive.",
        None,
        "Writing `WHERE COUNT(*) > 1` is invalid because the aggregate has not been computed at that stage.",
    ),
    "10.11": (
        "`LEFT JOIN` preserves every left row and fills right-side columns with NULL when no match exists.",
        "Right-table filters in ON affect which matches attach; the same filter in WHERE can remove NULL-extended rows and effectively turn the result into INNER JOIN.",
        "Count a nullable right primary key, not `COUNT(*)`, when measuring related rows per left entity.",
        None,
        "Putting `right.active = true` in WHERE unexpectedly removes left rows with no active relation.",
    ),
    "10.14": (
        "A subquery is a query used as an expression or table source inside another statement.",
        "A scalar subquery must return at most one row; `IN` compares against a set of values; a FROM subquery exposes a derived table with an alias.",
        "Prefer the form that expresses intent clearly. Performance depends on the planner and data, not a universal 'JOIN is faster' rule.",
        None,
        "A scalar subquery returning multiple rows raises an error; `NOT IN` with NULL can also produce surprising UNKNOWN results.",
    ),
    "10.21": (
        "A window function computes across related rows while keeping each original row visible, unlike GROUP BY.",
        "`OVER` defines partition, order and frame. Ranking, running totals and comparisons to previous rows are common uses.",
        "Ordering inside OVER controls the window calculation; final output order still requires a separate ORDER BY.",
        "Reports can add per-customer running totals without losing individual transactions.",
        "Omitting a tie-breaker from window ordering can make row_number results nondeterministic.",
    ),
    "11.2": (
        "Database constraints enforce invariants for every writer: NOT NULL, UNIQUE, CHECK, primary/foreign keys.",
        "The database evaluates constraints during writes/transaction completion and rejects invalid state; application code translates the specific conflict.",
        "Validation improves UX but cannot replace a DB constraint under concurrent requests.",
        None,
        "Checking uniqueness only with SELECT then INSERT races; a UNIQUE constraint must be the final authority.",
    ),
    "11.3": (
        "Normalization structures relations to reduce duplicated facts and update anomalies; Junior depth focuses on practical 1NF–3NF intuition.",
        "Separate entities and connect them by keys so one fact has one authoritative storage location. Denormalization intentionally duplicates derived/read data for a measured need.",
        "Normalization is not maximum table count; boundaries follow data meaning and update dependencies.",
        None,
        "Storing the same user email in many order rows makes updates inconsistent and obscures the source of truth.",
    ),
    "11.4": (
        "A database index is an auxiliary structure that can find ordered key ranges without scanning every table row.",
        "It speeds matching access paths but consumes storage and adds work to INSERT/UPDATE/DELETE. The planner may choose a sequential scan when many rows match.",
        "Design indexes from actual WHERE/JOIN/ORDER patterns and inspect EXPLAIN ANALYZE; an index on every column is harmful.",
        None,
        "Adding an index without the query shape or selectivity can increase write cost while never being selected.",
    ),
    "11.8": (
        "`EXPLAIN` shows the planned operations and estimates; `EXPLAIN ANALYZE` executes the statement and adds actual rows/timing.",
        "Read plan nodes from children upward and compare estimated vs actual rows, loops, scan type and buffers when requested.",
        "ANALYZE really executes data-changing statements unless wrapped and rolled back; test safely.",
        None,
        "Looking only at total time misses a severe estimate error or loop count that becomes expensive on larger data.",
    ),
    "11.9": (
        "A transaction groups operations into one atomic boundary; ACID describes atomicity, consistency, isolation and durability.",
        "Commit makes the transaction's changes durable/visible under DB rules; rollback discards them. Consistency comes from correct code plus constraints, not the letter C automatically.",
        "Keep transactions short and avoid network calls while locks/resources are held.",
        "A service operation that creates an order and reserves inventory should commit or rollback as one unit where invariants require it.",
        "Committing inside each repository call can leave half a use case saved after a later failure.",
    ),
    "11.10": (
        "Isolation levels define which effects of concurrent transactions can be observed.",
        "PostgreSQL commonly uses Read Committed per statement; Repeatable Read keeps a transaction snapshot; Serializable may abort a transaction to preserve serial behavior.",
        "Higher isolation is not free and serialization failures require retry of the entire transaction.",
        None,
        "Changing isolation without identifying the anomaly often adds contention while leaving the actual invariant unprotected.",
    ),
    "12.1": (
        "HTTP is a request/response application protocol: a request contains method, target, headers and optional body; a response contains status, headers and optional body.",
        "The server parses the request, routes it, applies application logic and serializes a response. HTTP semantics remain distinct from JSON and framework implementation.",
        "Transport success does not mean business success; status and body must describe the application result.",
        None,
        "Returning 200 with an error hidden in JSON breaks clients, monitoring and standard retry/cache behavior.",
    ),
    "12.3": (
        "HTTP methods express intent: GET reads, POST submits/creates/actions, PUT replaces at a known target, PATCH partially changes and DELETE removes.",
        "Safety means no requested state change; idempotency means repeating the same request has the same intended effect. These are semantics, not automatic framework enforcement.",
        "POST can be made retry-safe with an idempotency key, while a badly designed PUT can still have extra side effects.",
        None,
        "Choosing a method only by whether it has a body ignores caching, retries and client expectations.",
    ),
    "12.7": (
        "HTTP status codes communicate the outcome category and specific result of processing a request.",
        "Typical API codes include 200, 201 with Location where useful, 204 without body, 400 malformed request, 401 unauthenticated, 403 forbidden, 404, 409 conflict, 422 validation and 500 unexpected server error.",
        "Use one consistent error body with a machine-readable code; do not leak stack traces.",
        None,
        "Returning 200 for every error forces clients to reverse-engineer success from response text.",
    ),
    "12.10": (
        "`Content-Type` describes the representation sent in a body; `Accept` describes representations the client can receive.",
        "For JSON APIs the sender normally uses `application/json`; charset matters for textual formats and body parsing follows the declared media type.",
        "A JSON-looking string with the wrong Content-Type is not the same protocol contract.",
        None,
        "Confusing Accept with Content-Type produces 415/406 behavior or incorrect parsing.",
    ),
    "12.11": (
        "A cookie is a name/value set by response header and automatically returned by a browser according to domain, path, expiry and security attributes.",
        "HttpOnly blocks JavaScript reads, Secure restricts HTTPS transport and SameSite limits cross-site sending; none replaces server-side authorization.",
        "Cookie authentication needs CSRF considerations because the browser attaches cookies automatically.",
        None,
        "Putting a session cookie without HttpOnly/Secure/SameSite defaults unnecessarily expands the attack surface.",
    ),
    "12.13": (
        "HTTPS is HTTP carried through TLS, providing encryption in transit, integrity and server authentication through certificates.",
        "A TLS handshake negotiates keys and verifies the certificate chain; a reverse proxy may terminate TLS before forwarding to the app on a trusted network.",
        "HTTPS does not validate business permissions or encrypt data at rest.",
        None,
        "Trusting forwarded scheme/client headers from arbitrary peers can make an app believe an insecure request was HTTPS.",
    ),
    "12.20": (
        "An API error contract is a stable response shape for failures, usually containing a machine code, human message and optional field details.",
        "Domain/infrastructure exceptions are translated at the boundary to an appropriate status and safe payload; internal trace and secrets remain in protected logs.",
        "Clients should branch on stable code/status, not exact human wording.",
        None,
        "Returning raw exception strings leaks implementation details and creates an unstable public contract.",
    ),
    "13.1": (
        "Authentication establishes who the requester is; authorization decides whether that identity may perform an action on a resource.",
        "Credentials/token/session are verified first, then policy checks roles, permissions, ownership or attributes for the concrete operation.",
        "A logged-in user is not automatically allowed to read another user's object.",
        None,
        "Hiding an admin button in the frontend is neither authentication nor authorization; the API must enforce the rule.",
    ),
    "13.4": (
        "JWT is a signed token format with header, payload claims and signature; it is normally encoded, not encrypted.",
        "The server verifies signature, allowed algorithm, issuer, audience and time claims before trusting identity/permissions.",
        "Revocation and refresh lifecycle still need design; a long-lived access JWT is not automatically secure or stateless in the operational sense.",
        None,
        "Decoding payload without signature/claim verification lets an attacker supply arbitrary identity data.",
    ),
    "13.13": (
        "CORS is a browser policy controlling whether frontend JavaScript from one origin may read responses from another origin.",
        "For non-simple requests the browser sends a preflight OPTIONS request; the server returns allowed origins, methods, headers and credentials policy.",
        "CORS is not authentication and does not block curl or server-to-server clients.",
        None,
        "Using wildcard origin with credentials is invalid/unsafe; allowed origins should be explicit.",
    ),
    "14.1": (
        "A FastAPI application is an ASGI callable that participates in an asynchronous request lifecycle.",
        "The ASGI server receives connection events, FastAPI matches a route, validates inputs, resolves dependencies, calls the endpoint and serializes a response.",
        "The endpoint should be an adapter; business rules and transaction boundaries remain testable outside framework request objects.",
        None,
        "Putting DB session creation and domain logic directly in every route duplicates lifecycle and error handling.",
    ),
    "14.3": (
        "A path parameter identifies part of the routed resource path and is converted/validated from text using the endpoint annotation.",
        "`/users/{user_id}` binds the segment; constraints can reject invalid values before handler execution. Static routes must not be accidentally shadowed by a broad dynamic route.",
        "Path parameters are required by the matched path; optional filters belong in query parameters.",
        None,
        "Registering `/users/{user_id}` before a conflicting `/users/me` design can route `me` into integer validation instead of the intended handler.",
    ),
    "14.4": (
        "Query parameters describe optional or required modifiers such as pagination, filtering and sorting after `?`.",
        "FastAPI reads annotations/defaults and applies `Query` constraints; the resulting contract appears in OpenAPI.",
        "Set maximum page sizes and allowlist sort fields rather than interpolating arbitrary user input into SQL.",
        None,
        "Treating `limit: int | None` as optional without a default still leaves it required.",
    ),
    "14.5": (
        "A request body carries structured input; FastAPI commonly validates JSON through a Pydantic model.",
        "Body bytes are decoded by media type, parsed as JSON and validated recursively before the endpoint receives a typed model.",
        "Schema validation handles shape/ranges; database-dependent business invariants belong in service logic/constraints.",
        None,
        "Using a raw dict everywhere loses generated schema, typed access and precise field errors.",
    ),
    "14.6": (
        "A response model defines the public output schema and filters/serializes endpoint results.",
        "FastAPI validates the returned value against the model and emits the declared representation in OpenAPI.",
        "Use a separate public schema so password hashes and internal flags cannot leak from an ORM object.",
        None,
        "Returning ORM `__dict__` or an unrestricted model can expose secret/internal fields.",
    ),
    "14.12": (
        "An exception handler translates an exception type into a consistent HTTP response at an application/router boundary.",
        "Domain code raises a meaningful domain exception; FastAPI handler maps it to status and safe payload while unexpected errors remain server failures.",
        "Do not catch every exception and convert programming bugs into 400 responses.",
        None,
        "Leaking `str(database_error)` to clients exposes schema/SQL details and creates an unstable contract.",
    ),
    "14.13": (
        "Middleware wraps the request/response flow for cross-cutting behavior such as request IDs, timing or security headers.",
        "Each middleware runs before the inner app and after it returns; order therefore changes observation and error behavior.",
        "Domain authorization usually needs resolved user/resource context and belongs in dependencies/services, not generic middleware.",
        None,
        "Reading a streaming request body in middleware without replaying it can leave the endpoint with no body.",
    ),
    "14.14": (
        "FastAPI lifespan manages resources that live for the application process, such as connection pools and shared HTTP clients.",
        "An async context manager runs setup before yield and cleanup after yield during shutdown; tests should enter lifespan too.",
        "Application-level resources are shared, but request-specific Session/user state must not be stored in them.",
        None,
        "Creating a new expensive client per request wastes pools, while never closing a shared client leaks resources at shutdown.",
    ),
    "14.15": (
        "FastAPI supports sync and async endpoints; async is useful when the dependency stack performs awaitable I/O.",
        "Async endpoints run on the event loop, while sync endpoints are normally dispatched through a thread pool so blocking work does not directly block the loop.",
        "Declaring `async def` does not make sync drivers non-blocking; use an async driver/client or deliberately offload work.",
        None,
        "Calling `requests` or a sync DB driver inside async endpoint blocks the loop despite the async function declaration.",
    ),
    "14.16": (
        "FastAPI `BackgroundTasks` schedules small in-process work after the response is sent.",
        "The task runs in the same application process and has no durable delivery, distributed retry or crash recovery guarantee.",
        "Use it for small non-critical actions; use a queue/worker and idempotency for durable jobs.",
        None,
        "Sending a critical payment/email only via BackgroundTasks can lose it on process restart.",
    ),
    "14.20": (
        "A practical FastAPI structure separates HTTP routers/schemas from use-case services and data-access details.",
        "Routers adapt request/response, services hold business workflows/transaction decisions, repositories or query modules isolate persistence when they add value.",
        "Avoid pass-through layers with no behavior; boundaries should correspond to change/test seams.",
        None,
        "Putting every concern into routes makes transaction testing and framework-independent business tests difficult.",
    ),
    "16.1": (
        "SQLAlchemy Engine owns the SQL dialect and connection pool; it is a long-lived application-level factory, not an ORM Session.",
        "A Session checks out a connection when SQL is needed and returns it according to transaction/session lifecycle.",
        "Pool size must match database capacity and workload; creating an engine per request defeats pooling.",
        None,
        "A leaked Session can keep a transaction/connection checked out until the pool is exhausted.",
    ),
    "16.2": (
        "Declarative ORM models map Python classes/attributes to tables/columns using `Mapped` and `mapped_column` in SQLAlchemy 2.x.",
        "Class metadata builds a SQL schema description used by ORM statements and migrations tooling; instances represent rows within Session state.",
        "Changing model code does not migrate an existing production database; Alembic revision must apply the schema transition.",
        None,
        "Calling `create_all` as a production migration strategy loses versioned, reviewable schema history.",
    ),
    "16.3": (
        "A relationship describes ORM navigation between entities; the foreign key column remains the database source of referential truth.",
        "`back_populates` connects both directions; one-to-many, many-to-one and many-to-many determine collection/scalar shape and loading behavior.",
        "Relationship does not automatically choose efficient eager loading or safe cascade semantics.",
        None,
        "Confusing ORM relationship with database ownership can configure delete cascade that removes more data than intended.",
    ),
    "16.5": (
        "Session lifecycle is create → use within one unit of work → commit or rollback → close.",
        "A FastAPI yield-dependency can own one Session per request; service code decides the transaction outcome and cleanup always closes it.",
        "One AsyncSession must not be used concurrently by multiple tasks because it carries mutable transaction/identity state.",
        None,
        "A module-global Session leaks tracked objects and transaction failures across requests.",
    ),
    "16.6": (
        "SQLAlchemy 2.x `select()` builds an explicit SQL expression executed through Session.",
        "`where` adds predicates; `session.scalars(statement)` returns the first selected entity/value column; `one_or_none` enforces at most one row while `first` merely takes one.",
        "Choose result method according to cardinality instead of silently ignoring duplicate rows.",
        None,
        "Using `.first()` where uniqueness is required hides duplicate-data bugs that `.one_or_none()` would expose.",
    ),
    "16.8": (
        "`add` attaches a new entity, `flush` emits pending SQL inside the transaction, `commit` finalizes it and `refresh` reloads current DB values.",
        "Autoflush may run before a query; generated primary keys often become available after flush without commit.",
        "After commit objects may be expired depending on configuration; refresh is not a substitute for correct transaction ownership.",
        None,
        "Committing only to obtain an id breaks atomic use cases; flush is sufficient inside the still-open transaction.",
    ),
    "16.9": (
        "Rollback cancels the current database transaction and is required before reusing a Session after a flush/commit error.",
        "SQLAlchemy marks the failed transaction state; catching IntegrityError without rollback leaves later operations failing.",
        "Translate known constraint conflicts after rollback and re-raise unexpected failures with their cause/context.",
        None,
        "Continuing queries immediately after IntegrityError produces a pending-rollback error and obscures the original conflict.",
    ),
    "16.10": (
        "An explicit transaction boundary groups all database changes of one use case into one commit/rollback decision.",
        "`with session.begin()` commits on normal exit and rolls back on exception; repositories should not secretly finalize independent parts.",
        "Keep external network calls outside the transaction when possible to reduce lock/connection time.",
        None,
        "Multiple hidden repository commits make partial data durable when a later step fails.",
    ),
    "16.13": (
        "N+1 is one query for parent rows followed by one relationship query per parent.",
        "Lazy loading triggers the repeated queries; detect it in SQL logs or a query-count test and choose `selectinload`, `joinedload` or explicit projection based on cardinality.",
        "Eager-load only data the use case needs; a giant joined graph can create row multiplication and memory cost.",
        "Listing users with roles is a common N+1 path when serialization touches each lazy relationship.",
        "Adding a cache does not fix an ORM query shape that issues hundreds of avoidable round trips.",
    ),
    "16.17": (
        "AsyncEngine and AsyncSession use an async DB driver so SQL I/O can be awaited without blocking the event loop.",
        "ORM state/transaction semantics remain: one AsyncSession per request/task, explicit await for I/O and clear commit/rollback ownership.",
        "Do not share one AsyncSession across `gather` tasks; each concurrent unit needs its own session/transaction.",
        None,
        "Switching to AsyncSession without an async driver or while using blocking migrations does not create an async data path.",
    ),
    "17.1": (
        "A migration is a versioned, reviewable transition of an existing database schema/data; changing ORM model code alone does not update deployed databases.",
        "Alembic revisions define upgrade/downgrade steps and form an ordered history applied consistently across environments.",
        "Schema changes must stay compatible with old/new application versions during rolling deploys.",
        None,
        "Running `create_all` on startup cannot safely express rename, backfill or staged constraint changes.",
    ),
}


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
        useful=outline[4:6] or ("one short code/result example",),
        skip_deep=("internal implementation details beyond common Junior follow-ups",),
        practices=(
            f"**A · Code/result prediction.** Change one input in the `{outline[0]}` example and predict the result before running it.",
            f"**B · Find the bug.** Find code that violates `{outline[min(1, len(outline) - 1)]}` and explain the concrete consequence.",
            f"**D · Small task.** Implement the smallest function/query that demonstrates `{outline[0]}` and add one edge-case test.",
            f"**E · Interview explanation.** Explain {lesson['title']} in 45–60 seconds and include one limitation.",
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
        return CURATED[lesson["number"]]
    if lesson["number"] in COMPACT:
        return compact_dossier(lesson, COMPACT[lesson["number"]])
    return fallback_dossier(lesson, stage_number, explain_point)
