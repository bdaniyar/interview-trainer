"""Create structured SQL, debugging, testing and system-design practice banks."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
OUTPUT = CONTENT / "practice_banks.json"

SHOP_SCHEMA = """CREATE TABLE users (
    id bigint PRIMARY KEY,
    email text NOT NULL UNIQUE,
    country text,
    active boolean NOT NULL DEFAULT true,
    manager_id bigint REFERENCES users(id),
    created_at timestamptz NOT NULL
);
CREATE TABLE orders (
    id bigint PRIMARY KEY,
    user_id bigint NOT NULL REFERENCES users(id),
    status text NOT NULL,
    total numeric(12, 2) NOT NULL,
    created_at timestamptz NOT NULL
);
CREATE TABLE products (
    id bigint PRIMARY KEY,
    name text NOT NULL,
    category text NOT NULL,
    price numeric(12, 2) NOT NULL
);
CREATE TABLE order_items (
    order_id bigint REFERENCES orders(id),
    product_id bigint REFERENCES products(id),
    quantity integer NOT NULL CHECK (quantity > 0),
    PRIMARY KEY (order_id, product_id)
);"""

SHOP_SEED = """INSERT INTO users VALUES
(1,'a@example.com','KZ',true,NULL,'2026-01-01'),
(2,'b@example.com','KZ',true,1,'2026-01-02'),
(3,'c@example.com',NULL,false,1,'2026-01-03'),
(4,'d@example.com','GE',true,2,'2026-01-04');
INSERT INTO orders VALUES
(10,1,'paid',100,'2026-02-01'), (11,1,'cancelled',40,'2026-02-02'),
(12,2,'paid',200,'2026-02-03'), (13,2,'paid',50,'2026-02-04'),
(14,4,'new',80,'2026-02-05');
INSERT INTO products VALUES
(100,'Python Book','books',30), (101,'Keyboard','hardware',90), (102,'SQL Book','books',40);
INSERT INTO order_items VALUES (10,100,2),(10,101,1),(12,101,2),(13,102,1),(14,100,1);"""

BOOKING_SCHEMA = """CREATE TABLE rooms (
    id bigint PRIMARY KEY,
    hotel_id bigint NOT NULL,
    number text NOT NULL,
    UNIQUE (hotel_id, number)
);
CREATE TABLE bookings (
    id bigint PRIMARY KEY,
    room_id bigint NOT NULL REFERENCES rooms(id),
    starts_at timestamptz NOT NULL,
    ends_at timestamptz NOT NULL,
    status text NOT NULL,
    CHECK (ends_at > starts_at)
);"""

BOOKING_SEED = """INSERT INTO rooms VALUES (1,10,'101'),(2,10,'102');
INSERT INTO bookings VALUES
(1,1,'2026-09-01','2026-09-05','confirmed'),
(2,1,'2026-09-10','2026-09-12','cancelled');"""

# lesson, title, snippet, expected output, explanation, misconception tag
PYTHON_PREDICTIONS = [
    ("1.2", "Identity не равна equality", "a = [1]\nb = [1]\nprint(a == b, a is b)", "True False", "Списки равны по содержимому, но созданы как два разных объекта.", "identity-vs-equality"),
    ("1.3", "Два имени одного списка", "a = []\nb = a\nb.append(1)\nprint(a)", "[1]", "Assignment связал b с тем же mutable list; append виден через оба имени.", "aliasing"),
    ("1.6", "Повтор вложенного списка", "rows = [[0]] * 3\nrows[0].append(1)\nprint(rows)", "[[0, 1], [0, 1], [0, 1]]", "Оператор * повторил одну ссылку на внутренний список, а не создал три списка.", "nested-aliasing"),
    ("1.7", "Shallow copy", "source = {'roles': ['reader']}\ncopy = source.copy()\ncopy['roles'].append('writer')\nprint(source['roles'])", "['reader', 'writer']", "Копия отделила внешний dict, но вложенный list остался общим.", "shallow-copy"),
    ("1.5", "Truthiness пользовательского объекта", "class Queue:\n    def __len__(self):\n        return 0\n\nprint(bool(Queue()))", "False", "Если __bool__ не определён, bool использует __len__; нулевая длина означает falsy.", "truthiness"),
    ("1.4", "Равные ключи dict", "data = {True: 'yes', 1: 'one'}\nprint(len(data), data[True])", "1 one", "True == 1 и их hashes равны, поэтому второй assignment заменяет значение того же ключа.", "hash-equality-contract"),
    ("2.1", "Срез создаёт новый list", "items = [1, 2, 3]\npart = items[:]\npart.append(4)\nprint(items, part)", "[1, 2, 3] [1, 2, 3, 4]", "Срез создаёт новый внешний список; для immutable int этого достаточно для независимости.", "slice-copy"),
    ("2.4", "set удаляет дубликаты", "values = {3, 1, 3, 2}\nprint(len(values), sorted(values))", "3 [1, 2, 3]", "set хранит уникальные hashable значения; порядок вывода делают явным через sorted.", "set-order"),
    ("2.3", "dict сохраняет insertion order", "data = {'b': 2, 'a': 1}\ndata['b'] = 3\nprint(list(data))", "['b', 'a']", "Замена значения существующего ключа не переносит ключ в конец.", "dict-order"),
    ("2.1", "Unpacking со starred target", "first, *middle, last = [1, 2, 3, 4]\nprint(first, middle, last)", "1 [2, 3] 4", "Starred target собирает промежуточные элементы в новый list.", "unpacking"),
    ("3.4", "Default вычисляется один раз", "def add(value, bucket=[]):\n    bucket.append(value)\n    return bucket\n\nprint(add(1), add(2))", "[1] [1, 2]", "Mutable default создаётся при выполнении def и переиспользуется следующими вызовами.", "mutable-default"),
    ("3.7", "LEGB и локальное имя", "value = 'global'\ndef read():\n    value = 'local'\n    return value\nprint(read(), value)", "local global", "Assignment внутри функции создаёт local binding и не меняет global binding.", "legb"),
    ("3.9", "Closure хранит binding", "def make(prefix):\n    def render(value):\n        return f'{prefix}:{value}'\n    return render\nprint(make('id')(7))", "id:7", "Внутренняя функция замыкает свободное имя prefix после завершения make.", "closure"),
    ("3.10", "Late binding в цикле", "funcs = [lambda: i for i in range(3)]\nprint([fn() for fn in funcs])", "[2, 2, 2]", "Свободное имя i разрешается при вызове; после цикла оно равно 2.", "late-binding"),
    ("3.12", "Decorator меняет вызываемый объект", "def twice(fn):\n    def wrapper():\n        return fn() * 2\n    return wrapper\n\n@twice\ndef answer():\n    return 21\nprint(answer())", "42", "После декорирования имя answer связано с wrapper, который вызывает исходную функцию.", "decorator"),
    ("3.3", "Keyword-only argument", "def page(limit, *, offset=0):\n    return limit, offset\nprint(page(10, offset=20))", "(10, 20)", "Параметр после * можно передать только по имени, что делает API вызова явным.", "keyword-only"),
    ("4.2", "Iterator исчерпывается", "it = iter([1, 2])\nprint(list(it), list(it))", "[1, 2] []", "list потребил stateful iterator; повторный обход продолжается после его конца.", "iterator-exhaustion"),
    ("4.3", "Generator ленивый", "def values():\n    print('start')\n    yield 1\ng = values()\nprint('made')\nprint(next(g))", "made\nstart\n1", "Тело generator не выполняется при вызове функции, а стартует на первом next.", "generator-laziness"),
    ("4.3", "yield from передаёт значения", "def numbers():\n    yield from [1, 2]\n    yield 3\nprint(list(numbers()))", "[1, 2, 3]", "yield from делегирует итерацию вложенному iterable до его исчерпания.", "yield-from"),
    ("4.7", "finally выполняется при return", "def run():\n    try:\n        return 'result'\n    finally:\n        print('cleanup')\nprint(run())", "cleanup\nresult", "Перед фактическим выходом из функции Python выполняет finally.", "finally"),
    ("4.10", "Exception chaining", "try:\n    int('x')\nexcept ValueError as exc:\n    try:\n        raise RuntimeError('bad input') from exc\n    except RuntimeError as wrapped:\n        print(type(wrapped.__cause__).__name__)", "ValueError", "raise from записывает исходное исключение в __cause__ и делает цепочку явной.", "exception-chaining"),
    ("4.12", "Context manager получает exception", "class Guard:\n    def __enter__(self): return self\n    def __exit__(self, kind, value, tb):\n        print(kind.__name__)\n        return True\nwith Guard():\n    raise ValueError('x')\nprint('after')", "ValueError\nafter", "__exit__ получил тип ошибки и вернул True, поэтому исключение было подавлено.", "context-manager-suppression"),
    ("5.2", "Class attribute общий", "class User:\n    roles = []\na = User(); b = User()\na.roles.append('admin')\nprint(b.roles)", "['admin']", "До instance assignment оба объекта находят один mutable class attribute.", "class-attribute"),
    ("5.5", "super следует MRO", "class A:\n    def name(self): return 'A'\nclass B(A):\n    def name(self): return 'B>' + super().name()\nclass C(B): pass\nprint(C().name())", "B>A", "super в B продолжает поиск после B в MRO фактического класса C.", "mro"),
    ("5.10", "dataclass equality", "from dataclasses import dataclass\n@dataclass\nclass Point:\n    x: int\nprint(Point(1) == Point(1), Point(1) is Point(1))", "True False", "dataclass генерирует equality по полям, но каждый constructor call создаёт новый объект.", "dataclass-equality"),
    ("5.14", "Property управляет записью", "class Score:\n    def __init__(self): self._value = 0\n    @property\n    def value(self): return self._value\n    @value.setter\n    def value(self, value): self._value = max(0, value)\ns = Score(); s.value = -3\nprint(s.value)", "0", "Assignment проходит через property setter, который сохраняет нормализованное значение.", "descriptor-property"),
    ("6.1", "Type hint не валидирует runtime", "def double(value: int) -> int:\n    return value * 2\nprint(double('a'))", "aa", "Обычная annotation не вставляет runtime type check; строка использует собственный operator *.", "typing-runtime"),
    ("6.2", "Optional не создаёт default", "def parse(value: str | None):\n    return value is None\ntry:\n    parse()\nexcept TypeError:\n    print('missing')", "missing", "Union с None разрешает значение None, но параметр остаётся обязательным без default.", "optional-vs-default"),
    ("7.1", "Cycle не означает немедленное удаление", "a = []\na.append(a)\nprint(a[0] is a)", "True", "Список может ссылаться на себя; цикл обрабатывает cyclic GC, а identity сохраняется.", "reference-cycle"),
    ("8.2", "Вызов async def", "async def answer():\n    return 42\nvalue = answer()\nprint(type(value).__name__)\nvalue.close()", "coroutine", "Вызов async def создаёт coroutine object; выполнение требует await/event loop.", "coroutine-object"),
    ("8.3", "Await сохраняет порядок внутри task", "import asyncio\nasync def main():\n    print('a')\n    await asyncio.sleep(0)\n    print('b')\nasyncio.run(main())", "a\nb", "await может отдать управление loop, но эта программа содержит только одну пользовательскую task.", "await-order"),
    ("8.5", "create_task планирует работу", "import asyncio\nasync def child():\n    print('child')\nasync def main():\n    task = asyncio.create_task(child())\n    print('parent')\n    await task\nasyncio.run(main())", "parent\nchild", "create_task ставит coroutine в планирование; текущая task продолжает до await.", "task-scheduling"),
    ("8.6", "gather сохраняет порядок результатов", "import asyncio\nasync def item(value, delay):\n    await asyncio.sleep(delay)\n    return value\nasync def main():\n    print(await asyncio.gather(item('a', .01), item('b', 0)))\nasyncio.run(main())", "['a', 'b']", "Coroutines завершаются в разное время, но gather возвращает results в порядке awaitables.", "gather-order"),
    ("8.8", "Timeout преобразует ожидание в ошибку", "import asyncio\nasync def main():\n    try:\n        await asyncio.wait_for(asyncio.sleep(1), timeout=0.001)\n    except TimeoutError:\n        print('timeout')\nasyncio.run(main())", "timeout", "wait_for отменяет слишком долгий awaitable и поднимает TimeoutError вызывающему коду.", "async-timeout"),
    ("9.1", "Threads разделяют объект", "from threading import Thread\nitems = []\nt = Thread(target=items.append, args=(1,))\nt.start(); t.join()\nprint(items)", "[1]", "Thread работает в памяти процесса; join гарантирует завершение перед print.", "thread-shared-memory"),
    ("18.5", "parametrize создаёт отдельные cases", "import pytest\n@pytest.mark.parametrize('value', [1, 2, 3])\ndef test_positive(value):\n    assert value > 0", "3 passed", "pytest создаёт отдельный test case для каждого параметра; точное оформление строки зависит от verbosity.", "pytest-parametrize"),
    ("28.2", "Stable sort", "rows = [('a', 2), ('b', 1), ('c', 2)]\nprint(sorted(rows, key=lambda row: row[1]))", "[('b', 1), ('a', 2), ('c', 2)]", "При равных keys sorted сохраняет исходный относительный порядок элементов.", "stable-sort"),
    ("28.5", "Dedup с сохранением порядка", "values = [2, 1, 2, 3, 1]\nprint(list(dict.fromkeys(values)))", "[2, 1, 3]", "dict сохраняет порядок первого появления каждого hashable key.", "ordered-dedup"),
    ("28.6", "Счётчик частот", "from collections import Counter\ncounts = Counter('aba')\nprint(counts['a'], counts['x'])", "2 0", "Counter возвращает ноль для отсутствующего ключа вместо KeyError.", "counter"),
    ("27.7", "Dependency передана явно", "class Service:\n    def __init__(self, clock): self.clock = clock\n    def now(self): return self.clock()\ns = Service(lambda: 42)\nprint(s.now())", "42", "Explicit dependency делает поведение заменяемым в тесте без global patch.", "dependency-injection"),
]

# number, category, title, prompt, solution, columns, ordered
SQL_TASKS = [
    ("10.2","basic","Активные пользователи","Выбери id и email активных пользователей.","SELECT id, email FROM users WHERE active IS TRUE;",["id","email"],False),
    ("10.3","basic","Email domain","Найди email, заканчивающиеся на @example.com.","SELECT email FROM users WHERE email LIKE '%@example.com';",["email"],False),
    ("10.4","basic","Неизвестная страна","Найди пользователей, у которых country неизвестна.","SELECT id, email FROM users WHERE country IS NULL;",["id","email"],False),
    ("10.5","basic","Последние два заказа","Верни два последних заказа по created_at, при равенстве — больший id первым.","SELECT id, created_at FROM orders ORDER BY created_at DESC, id DESC LIMIT 2;",["id","created_at"],True),
    ("10.6","basic","Уникальные страны","Верни уникальные непустые country по алфавиту.","SELECT DISTINCT country FROM users WHERE country IS NOT NULL ORDER BY country;",["country"],True),
    ("10.19","basic","Label статуса","Верни id заказа и label: paid → completed, cancelled → cancelled, иначе pending.","SELECT id, CASE status WHEN 'paid' THEN 'completed' WHEN 'cancelled' THEN 'cancelled' ELSE 'pending' END AS label FROM orders;",["id","label"],False),
    ("10.3","basic","Пользователи после даты","Выбери id пользователей, созданных не раньше 2026-01-03.","SELECT id FROM users WHERE created_at >= TIMESTAMPTZ '2026-01-03';",["id"],False),
    ("10.5","basic","Вторая страница","Верни вторую страницу пользователей размера 2 с устойчивым order по id.","SELECT id, email FROM users ORDER BY id LIMIT 2 OFFSET 2;",["id","email"],True),
    ("10.7","aggregation","Количество заказов","Посчитай все строки orders.","SELECT COUNT(*) AS orders_count FROM orders;",["orders_count"],True),
    ("10.8","aggregation","Заказы по status","Посчитай заказы по status и отсортируй status.","SELECT status, COUNT(*) AS count FROM orders GROUP BY status ORDER BY status;",["status","count"],True),
    ("10.8","aggregation","Выручка по пользователю","Суммируй total только paid-заказов по user_id.","SELECT user_id, SUM(total) AS revenue FROM orders WHERE status='paid' GROUP BY user_id ORDER BY user_id;",["user_id","revenue"],True),
    ("10.8","aggregation","Средний paid-чек","Найди средний total paid-заказа.","SELECT AVG(total) AS average_total FROM orders WHERE status='paid';",["average_total"],True),
    ("10.9","aggregation","Пользователи с двумя заказами","Верни user_id с минимум двумя заказами.","SELECT user_id, COUNT(*) AS count FROM orders GROUP BY user_id HAVING COUNT(*) >= 2 ORDER BY user_id;",["user_id","count"],True),
    ("10.7","aggregation","COUNT и NULL","Верни count всех users и count известных country в одной строке.","SELECT COUNT(*) AS users_count, COUNT(country) AS known_country_count FROM users;",["users_count","known_country_count"],True),
    ("10.7","aggregation","Диапазон цен","Верни минимальную и максимальную product price.","SELECT MIN(price) AS min_price, MAX(price) AS max_price FROM products;",["min_price","max_price"],True),
    ("10.7","aggregation","Условные counts","Одной строкой посчитай paid и cancelled orders через FILTER.","SELECT COUNT(*) FILTER (WHERE status='paid') AS paid_count, COUNT(*) FILTER (WHERE status='cancelled') AS cancelled_count FROM orders;",["paid_count","cancelled_count"],True),
    ("10.10","join","Пользователь каждого заказа","INNER JOIN orders/users; верни order_id и email.","SELECT o.id AS order_id, u.email FROM orders o JOIN users u ON u.id=o.user_id;",["order_id","email"],False),
    ("10.11","join","Пользователи без заказов","LEFT JOIN и найди users без orders.","SELECT u.id, u.email FROM users u LEFT JOIN orders o ON o.user_id=u.id WHERE o.id IS NULL;",["id","email"],False),
    ("10.10","join","Товары заказа","Для order 10 верни product name и quantity.","SELECT p.name, oi.quantity FROM order_items oi JOIN products p ON p.id=oi.product_id WHERE oi.order_id=10 ORDER BY p.id;",["name","quantity"],True),
    ("10.13","join","Manager self join","Верни email пользователя и manager_email; пользователей без manager сохрани.","SELECT u.email, m.email AS manager_email FROM users u LEFT JOIN users m ON m.id=u.manager_id ORDER BY u.id;",["email","manager_email"],True),
    ("10.11","join","LEFT JOIN с условием в ON","Верни всех users и id только paid orders, не теряя users без paid-заказов.","SELECT u.id AS user_id, o.id AS order_id FROM users u LEFT JOIN orders o ON o.user_id=u.id AND o.status='paid' ORDER BY u.id,o.id;",["user_id","order_id"],True),
    ("10.10","join","Состав paid-заказов","Соедини users, orders, items, products; верни email, order_id, product и quantity для paid.","SELECT u.email,o.id AS order_id,p.name,oi.quantity FROM users u JOIN orders o ON o.user_id=u.id JOIN order_items oi ON oi.order_id=o.id JOIN products p ON p.id=oi.product_id WHERE o.status='paid';",["email","order_id","name","quantity"],False),
    ("10.11","join","Категории без продаж","Верни products, которые ни разу не встречались в order_items.","SELECT p.id,p.name FROM products p LEFT JOIN order_items oi ON oi.product_id=p.id WHERE oi.product_id IS NULL;",["id","name"],False),
    ("10.10","join","Количество товаров в заказе","Для каждого order с items верни сумму quantity.","SELECT o.id, SUM(oi.quantity) AS units FROM orders o JOIN order_items oi ON oi.order_id=o.id GROUP BY o.id ORDER BY o.id;",["id","units"],True),
    ("10.12","join","RIGHT JOIN awareness","Сохрани все products через RIGHT JOIN от items к products и верни product_id/order_id.","SELECT p.id AS product_id,oi.order_id FROM order_items oi RIGHT JOIN products p ON p.id=oi.product_id ORDER BY p.id,oi.order_id;",["product_id","order_id"],True),
    ("10.12","join","FULL OUTER reconciliation","Сопоставь users и orders по user_id, сохрани строки без пары с обеих сторон.","SELECT u.id AS user_id,o.id AS order_id FROM users u FULL OUTER JOIN orders o ON o.user_id=u.id;",["user_id","order_id"],False),
    ("10.14","subquery","Заказы выше среднего","Найди orders с total выше среднего total всех orders.","SELECT id,total FROM orders WHERE total > (SELECT AVG(total) FROM orders);",["id","total"],False),
    ("10.16","subquery","Users с paid order","Через EXISTS верни users, у которых есть paid order.","SELECT u.id,u.email FROM users u WHERE EXISTS (SELECT 1 FROM orders o WHERE o.user_id=u.id AND o.status='paid');",["id","email"],False),
    ("10.16","subquery","Users без orders","Через NOT EXISTS верни users без orders.","SELECT u.id FROM users u WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.user_id=u.id);",["id"],False),
    ("10.17","subquery","CTE revenue","CTE paid_totals считает paid revenue по user, затем оставь revenue >= 150.","WITH paid_totals AS (SELECT user_id,SUM(total) revenue FROM orders WHERE status='paid' GROUP BY user_id) SELECT user_id,revenue FROM paid_totals WHERE revenue>=150 ORDER BY user_id;",["user_id","revenue"],True),
    ("10.15","subquery","Последний заказ пользователя","Correlated subquery: верни orders, чей created_at максимален для своего user.","SELECT o.id,o.user_id FROM orders o WHERE o.created_at=(SELECT MAX(i.created_at) FROM orders i WHERE i.user_id=o.user_id) ORDER BY o.user_id;",["id","user_id"],True),
    ("10.17","subquery","Цепочка менеджеров","Recursive CTE от user 4 вверх по manager_id, верни id и depth.","WITH RECURSIVE chain AS (SELECT id,manager_id,0 depth FROM users WHERE id=4 UNION ALL SELECT u.id,u.manager_id,c.depth+1 FROM users u JOIN chain c ON u.id=c.manager_id) SELECT id,depth FROM chain ORDER BY depth;",["id","depth"],True),
    ("10.22","window","ROW_NUMBER orders","Пронумеруй orders каждого user по created_at desc, id desc.","SELECT id,user_id,ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY created_at DESC,id DESC) AS row_number FROM orders ORDER BY user_id,row_number;",["id","user_id","row_number"],True),
    ("10.22","window","RANK totals","Ранжируй orders по total desc с пропусками после ties.","SELECT id,total,RANK() OVER(ORDER BY total DESC) AS rank FROM orders ORDER BY rank,id;",["id","total","rank"],True),
    ("10.22","window","DENSE_RANK totals","Плотно ранжируй orders по total desc.","SELECT id,total,DENSE_RANK() OVER(ORDER BY total DESC) AS dense_rank FROM orders ORDER BY dense_rank,id;",["id","total","dense_rank"],True),
    ("10.23","window","Running revenue","Для каждого user посчитай накопительный total по created_at/id.","SELECT id,user_id,SUM(total) OVER(PARTITION BY user_id ORDER BY created_at,id) AS running_total FROM orders ORDER BY user_id,created_at,id;",["id","user_id","running_total"],True),
    ("10.21","window","Предыдущий order total","Добавь previous_total через LAG в рамках user.","SELECT id,user_id,total,LAG(total) OVER(PARTITION BY user_id ORDER BY created_at,id) AS previous_total FROM orders ORDER BY user_id,created_at,id;",["id","user_id","total","previous_total"],True),
    ("10.21","window","Следующий order time","Добавь next_created_at через LEAD в рамках user.","SELECT id,user_id,LEAD(created_at) OVER(PARTITION BY user_id ORDER BY created_at,id) AS next_created_at FROM orders ORDER BY user_id,created_at,id;",["id","user_id","next_created_at"],True),
]

PG_SCENARIOS = [
    ("11.4","Index для email lookup","GET /users/by-email выполняет WHERE lower(email)=lower($1), но индекс только на email. Что проверить?","EXPLAIN ANALYZE; expression index on lower(email) либо normalized stored value; цена write/storage."),
    ("11.6","Composite index order","Запрос WHERE hotel_id=$1 AND starts_at >= $2 ORDER BY starts_at. Предложи индекс.","B-tree (hotel_id, starts_at): equality prefix before range/order; проверить plan и selectivity."),
    ("11.8","Sequential scan","После роста таблицы endpoint замедлился и plan показывает Seq Scan. План диагностики?","Predicate/types/stats/selectivity; EXPLAIN ANALYZE; подходящий index; Seq Scan не всегда плох."),
    ("11.9","Atomic booking","Два запроса бронируют последний room одновременно. Где защитить инвариант?","Short transaction плюс DB constraint/lock/conditional write; separate SELECT недостаточен; вернуть 409."),
    ("11.13","Deadlock lock order","Две transaction обновляют accounts A/B в разном порядке.","Единый порядок locks, короткая transaction, retry whole transaction после deadlock."),
    ("11.5","Partial index","Большинство orders имеют status='archived', а dashboard читает только status='new'. Как оценить partial index?","Сверить точный predicate запроса, долю active rows и write cost; EXPLAIN ANALYZE; index WHERE status='new' не помогает несовместимому predicate."),
    ("11.7","Covering index","Query фильтрует user_id, сортирует created_at и возвращает total. Когда уместен INCLUDE?","B-tree (user_id, created_at DESC) INCLUDE (total); index-only scan зависит от visibility map, а INCLUDE увеличивает размер/write cost."),
    ("11.10","Isolation anomaly","Две transaction читают доступный balance и обе списывают средства. Что гарантирует Read Committed?","Каждый statement видит свой snapshot; read-then-write требует conditional UPDATE, lock либо более сильной isolation с retry."),
    ("11.11","Savepoint","В batch нужно отклонить одну строку после IntegrityError, сохранив остальные.","Использовать SAVEPOINT/nested transaction вокруг строки; после ошибки откатить savepoint, не продолжать failed transaction как будто она здорова."),
    ("11.12","Pool exhaustion","API получает timeout на connection pool при нормальном DB CPU.","Проверить leaked/long transactions, pool size/overflow/wait time, request concurrency и DB max_connections; не лечить только ростом pool."),
]

DEBUGGING = [
    ("3.4","Mutable default","Список tags растёт между независимыми вызовами.","Default создаётся при def; None/sentinel и новый list; тест на два вызова."),
    ("1.6","Nested alias","[[]] * 3 меняет все строки после append.","Повторяется одна reference; comprehension создаёт независимые lists."),
    ("1.7","Shallow copy","dict.copy не изолировал nested roles.","Outer container новый, nested object общий; selective/deep copy по ownership."),
    ("3.10","Late closure","Callbacks из цикла используют последнее id.","Free name resolved at call time; bind default/factory."),
    ("4.7","Broad exception","except Exception превращает DB outage в 404.","Перехватывать ожидаемую domain error; unexpected log/re-raise."),
    ("3.12","Missing wraps","FastAPI/introspection видит wrapper signature.","functools.wraps сохраняет metadata и __wrapped__."),
    ("5.2","Shared class state","roles=[] class attribute делится между instances.","Mutable instance state создавать в __init__/default_factory."),
    ("5.13","Broken hash","Mutable field участвует в __hash__, set не находит object.","Hash/equality contract; immutable key or unhashable entity."),
    ("8.3","Forgotten await","Endpoint возвращает coroutine object.","await coroutine; включить warnings/test serialization."),
    ("8.9","Blocking HTTP","requests.get внутри async route блокирует loop.","Async client или to_thread; timeout/cancellation."),
    ("8.9","time.sleep in async","Все concurrent requests замирают.","asyncio.sleep для cooperative wait."),
    ("8.6","Sequential awaits","Независимые I/O выполняются по очереди.","gather/TaskGroup с bounded concurrency и failure policy."),
    ("8.5","Unhandled task","create_task потерян, exception logged later.","Хранить reference, await/supervise, done callback."),
    ("8.8","Swallowed cancellation","except BaseException подавляет shutdown.","CancelledError не поглощать; cleanup finally; re-raise."),
    ("16.17","Shared AsyncSession","Две tasks используют одну AsyncSession.","Session per concurrent task/use case."),
    ("10.11","LEFT becomes INNER","WHERE right.status='paid' удалил NULL rows.","Условие правой таблицы в ON или explicit NULL semantics."),
    ("10.8","COUNT nullable","COUNT(country) меньше COUNT(*).","COUNT(expression) пропускает NULL."),
    ("16.9","Failed session","После IntegrityError новые queries падают.","Rollback failed transaction before reuse."),
    ("19.5","Stale cache","PUT commit успешен, GET отдаёт старое.","Invalidate/update after commit; key ownership, TTL, race."),
    ("21.8","Container localhost","API не видит PostgreSQL по localhost.","localhost — тот же container; Compose DNS service name + container port."),
    ("10.10","Wrong JOIN condition","JOIN orders/users размножил и сопоставил несвязанные строки.","Проверить foreign-key cardinality и ON u.id=o.user_id; сравнить row count до/после JOIN."),
    ("10.8","Incorrect GROUP BY","Запрос агрегирует по user_id, но выбирает произвольный email.","Все неагрегированные columns должны быть функционально зависимы/в GROUP BY; сначала определить grain результата."),
    ("10.5","Missing deterministic order","LIMIT 20 иногда возвращает другой набор строк.","Добавить ORDER BY с уникальным tie-breaker; без него SQL не обещает порядок."),
    ("11.4","Missing index","Lookup по уникальному external_id замедлился после роста таблицы.","Снять EXPLAIN ANALYZE, проверить predicate/type/statistics и добавить targeted unique B-tree index."),
    ("11.8","Low-selectivity index","Planner выбирает Seq Scan для boolean active, хотя index существует.","При высокой доле совпадений Seq Scan может быть дешевле; сравнить estimates/actual rows, не принуждать index вслепую."),
    ("11.9","Long transaction","Request держит transaction открытой во время HTTP-вызова.","Сетевой I/O вынести за DB transaction; короткая boundary уменьшает locks, pool pressure и stale snapshot."),
    ("11.13","Deadlock order","Два flow блокируют resources A/B в противоположном порядке.","Единый порядок lock acquisition, короткие transactions и retry всей transaction после deadlock."),
    ("11.9","Double booking race","Два SELECT видят свободный номер и создают booking.","Защитить invariant в БД constraint/lock/conditional write и проверить concurrent integration test."),
    ("16.8","Commit in repository","repository.save неожиданно commit-ит половину use case.","Transaction boundary принадлежит service/use case; repository делает add/flush, caller решает commit/rollback."),
    ("16.13","N+1","Список 100 users выполняет ещё 100 SELECT roles.","Посчитать queries и использовать selectinload/joinedload по cardinality; integration test с query counter."),
    ("16.12","Unexpected lazy load","Доступ к relationship запускает SQL в serializer.","Загрузить данные явно, запретить accidental lazy load и не прятать I/O за attribute access."),
    ("16.12","Detached instance","После закрытия Session serializer читает unloaded relationship и падает.","Сформировать DTO внутри session boundary или eager-load нужное; не возвращать live ORM entity наружу."),
    ("16.18","Serialization hits DB","Response validation выполняет queries после service return.","Map ORM to response data при открытой session; query-count test обнаруживает hidden I/O."),
    ("16.16","Wrong cascade","Удаление parent неожиданно удалило shared children.","Настроить cascade по ownership и DB FK semantics; тестировать delete/replace relationship на реальной БД."),
    ("14.15","Blocking dependency","Async route вызывает sync dependency с долгим blocking client внутри event loop.","Использовать async client/driver или thread offload; измерить event-loop lag и concurrent latency."),
    ("14.6","Secret ORM field","Endpoint возвращает ORM object вместе с password_hash.","Явная response model/DTO с allowlist полей; contract test проверяет отсутствие secret."),
    ("14.7","Wrong 401/403","API отдаёт 403 пользователю без валидной authentication.","401 — нет/невалидна authentication (с challenge), 403 — identity известна, permission недостаточно."),
    ("14.24","Dependency not overridden","FastAPI test ходит в production-like DB.","Переопределить тот же dependency key через app.dependency_overrides и очищать override после test."),
    ("14.22","Global request state","Route пишет current_user в module global.","Request-scoped dependency/context, immutable arguments; concurrent test обнаруживает утечку между запросами."),
    ("14.14","Resource not closed","HTTP client создаётся на startup, но socket остаётся после shutdown.","Lifespan async context manager с cleanup в finally; test lifespan and close state."),
    ("19.3","Missing TTL","Reset state навсегда остаётся в Redis.","Установить короткий TTL атомарно при записи и тестировать expiration policy."),
    ("19.2","Cache key collision","profile:42 разных tenants возвращает чужие данные.","Key включает namespace/version/tenant/entity; authorization остаётся server-side."),
    ("19.8","PubSub as history","Offline WebSocket client потерял события.","Pub/Sub только live fan-out; durable history/read state хранить в PostgreSQL или durable stream."),
    ("19.7","Local rate limit","Два API process дают вдвое больший лимит.","Shared Redis counter + atomic operation/Lua, window semantics, TTL и fail-open/fail-closed policy."),
    ("21.5","Wrong Docker port","API container подключается к db:5433 из-за host mapping 5433:5432.","Между containers использовать service DNS и container port 5432; host port нужен только host client."),
    ("21.13","depends_on readiness","API стартует после container DB, но раньше готовности принимать SQL.","Healthcheck/retry/backoff или entrypoint wait; start order не является readiness guarantee."),
    ("21.6","Bind mount hides files","Mount ./app:/app скрыл dependencies, созданные в image path.","Проверить mount target; отделить source и dependency paths, использовать named volume где уместно."),
    ("21.9","Secret copied into image","COPY . . сохранил .env в старом image layer.","Rotate secret, .dockerignore, runtime injection/secrets; удаление в следующем layer не очищает историю."),
    ("21.6","No database volume","После compose down/recreate PostgreSQL пуст.","Named volume и backup/restore; документировать, что down -v удаляет данные."),
    ("22.9","Reset shared branch","force push после reset удалил commits коллег.","Для published history использовать revert; recovery через reflog/remote refs и coordination."),
    ("22.7","Untested conflict resolution","Conflict markers удалены выбором одной стороны, контракт сломан.","Понять обе версии, собрать итог вручную, inspect diff и запустить tests."),
    ("22.10","Secret still active","Token удалён из Git, но им продолжают пользоваться.","Немедленно revoke/rotate, затем audit и при необходимости clean history; gitignore не лечит leak."),
    ("22.6","Rebase published commits","Коллеги получили divergent history после rebase main.","Не переписывать shared commits; merge/revert или явно координировать rare rewrite."),
    ("13.2","Fast password hash","Пароли сохранены через один SHA-256.","Argon2id/bcrypt/scrypt с индивидуальной солью и cost; тест verify и migration policy."),
    ("13.6","Unverified JWT","API декодирует payload без проверки signature/issuer/audience/exp.","Полная verification с разрешённым algorithm и claims; invalid token всегда безопасно отклоняется."),
    ("13.5","Long-lived access token","Украденный access действует месяц без возможности быстро ограничить ущерб.","Короткий access, controlled refresh session/rotation/revocation; threat-based TTL."),
    ("32.22","Reusable reset token","Один reset URL меняет пароль повторно.","Random high-entropy token, server-side hash, TTL и atomic one-time invalidation; revoke sessions по policy."),
    ("13.13","CORS as authorization","Backend разрешает действие, полагаясь на blocked browser origin.","CORS — browser read policy; authentication/authorization проверяются на сервере для каждого request."),
    ("13.10","SQL f-string","Query строится из user input через f-string.","Parameterized query/SQLAlchemy expression; test malicious input как data, не SQL syntax."),
]

TESTING = [
    ("18.1","Test boundary","Раздели booking flow на unit, integration и API tests.","Unit domain decision; integration DB constraint; API status/body."),
    ("18.2","Readable assertion","Тест падает без понятного expected/actual.","Один observable contract и plain assert."),
    ("18.3","Fixture cleanup","Resource остаётся после failed test.","yield fixture, cleanup in finally, narrow scope."),
    ("18.4","Fixture scope","Mutable session fixture течёт между tests.","Function scope или reset; scope по isolation."),
    ("18.5","Parametrization","Пять копий теста отличаются input/result.","parametrize cases с ids и boundaries."),
    ("18.6","Mock boundary","Тест mock-ает private calls.","Mock external boundary; assert outcome."),
    ("18.7","Patch namespace","patch library.client не влияет на imported symbol.","Patch имя в module under test."),
    ("18.8","Dependency override","FastAPI test ходит в real DB.","app.dependency_overrides и cleanup."),
    ("18.9","Database isolation","Порядок tests влияет на rows.","Transaction rollback/recreated schema."),
    ("18.10","Redis fake","Fake не моделирует TTL/failure.","Отдельные unit fake и integration Redis tests."),
    ("18.11","Async task leak","Test завершился, background task осталась.","Await/cancel tasks; deterministic event."),
    ("18.14","Flaky order","Test зависит от timezone/unordered SELECT.","Fixed clock и explicit ORDER BY."),
]

OPERATIONS = [
    ("21.5","Wrong port","Host открывает 5433, какой port использует API container?","service:5432; host mapping только для host client."),
    ("21.8","Service discovery","API config содержит DB_HOST=localhost.","Compose service name; shared network/DNS."),
    ("21.13","Readiness","depends_on есть, migrations падают.","Healthcheck/ready retry; start order не readiness."),
    ("21.6","Lost data","После recreate DB данные исчезли.","Named volume; backups; down -v destructive."),
    ("21.9","Secret in image","COPY . . добавил .env.","dockerignore, rotation, runtime secrets."),
    ("22.7","Conflict","Markers удалены, tests не запускались.","Понять обе стороны, stage, test."),
    ("22.9","Undo public commit","Ошибка уже в main.","git revert; не rewrite shared history."),
    ("22.10","Leaked token","Secret удалён из file.","Rotate; audit; history cleanup отдельно."),
    ("22.6","Shared rebase","Rebase опубликованных commits.","Не rebase shared; coordinate/recover refs."),
    ("22.12","Wrong branch","Commit случайно в main local.","Создать branch at commit; безопасно restore main."),
    ("23.3","Find error","Найди ERROR request_id=abc.","rg/grep + tail/context."),
    ("23.5","Process exit","Uvicorn сразу code 1.","stderr/log, command, env, permissions, port."),
    ("23.6","Permission denied","Container не читает mount.","uid/gid/mode, минимальный доступ."),
    ("23.7","Port occupied","API не bind 8000.","ss/lsof, stop owner или change mapping."),
    ("23.4","Missing env","Local works, service KeyError APP_ENV.","Runtime env source, quoting, restart."),
]

ARCHITECTURE = [
    ("29.1","Request path","Покажи путь request.","Boundaries, timeout, request id, source of truth."),
    ("29.2","Stateless API","Что мешает второму API instance?","Local state; shared DB/cache/storage."),
    ("29.3","Cache placement","Где cache profile read?","Auth-aware key; TTL/invalidation/fallback."),
    ("29.4","Background email","Email без latency/loss.","Outbox/durable queue, retry, idempotency."),
    ("29.5","DB bottleneck","p95 вырос, DB CPU высокий.","Slow queries, pool, plans, indexes, N+1."),
    ("29.6","Booking endpoint","Спроектируй POST booking.","Validation, auth, transaction, 201/409, idempotency."),
    ("29.7","Double booking","Concurrent availability.","DB conflict, lock/constraint, test."),
    ("29.8","WebSocket scale","Fan-out между processes.","Redis Pub/Sub live + PostgreSQL history."),
    ("29.9","File upload","Большой upload не через API memory.","Presigned URL, policy, finalize validation."),
    ("29.10","Outbox","Commit прошёл, publish упал.","Same transaction outbox; retry/idempotency."),
    ("29.11","Scaling order","Когда microservice?","Measure/ownership; modular monolith first."),
    ("32.1","StudyHub pitch","Проект за 60 секунд.","Problem, own role, stack, decision, verification."),
    ("32.4","Why async","Зачем async?","Concurrent I/O; not CPU speed; no blocking."),
    ("32.5","PostgreSQL plus Redis","Почему оба?","Durable truth vs cache/temp/fan-out."),
    ("32.6","WebSocket Pub/Sub","Cross-instance flow.","Persist, publish, fan-out; offline reads DB."),
    ("32.8","Outbox defense","Почему outbox?","Atomicity gap; at-least-once/idempotency."),
    ("32.11","JWT sessions","Отозвать stolen refresh.","Server session, rotation/revocation, short access."),
    ("32.14","Presigned upload","Слишком большой file.","Policy, size validation, delete/reject."),
    ("32.17","Hotel race","Не допустить double booking.","DB invariant, short transaction, concurrent test."),
    ("32.23","Honest boundary","Спросили Kafka/Kubernetes/AWS.","Не заявлять опыт; learning plan; factual stack."),
]


def indexes() -> tuple[dict[str, dict], dict[str, Path]]:
    curriculum = json.loads((CONTENT / "curriculum.json").read_text(encoding="utf-8"))
    lessons = {lesson["number"]: lesson for stage in curriculum["stages"] for lesson in stage["lessons"]}
    directories = {}
    for path in CONTENT.glob("*/*/metadata.json"):
        metadata = json.loads(path.read_text(encoding="utf-8"))
        directories[metadata["slug"]] = path.parent
    return lessons, directories


def upsert_section(markdown: str, heading: str, body: str) -> str:
    pattern = rf"\n{re.escape(heading)}\n.*?(?=\n## [^\n]+|\Z)"
    replacement = f"\n{heading}\n\n{body.rstrip()}\n"
    if re.search(pattern, markdown, re.DOTALL):
        return re.sub(pattern, replacement, markdown, flags=re.DOTALL)
    if "\n## Cheat sheet" in markdown:
        return markdown.replace("\n## Cheat sheet", replacement + "\n## Cheat sheet")
    return markdown.rstrip() + "\n" + replacement


def scenario_records(kind: str, rows: list[tuple[str, str, str, str]]) -> list[dict]:
    return [
        {
            "id": f"{kind}.{index:02d}",
            "lesson_number": number,
            "title": title,
            "prompt": prompt,
            "expected_reasoning": expected,
            "common_weak_answer": "Сразу назвать инструмент без symptom, boundary и verification.",
        }
        for index, (number, title, prompt, expected) in enumerate(rows, 1)
    ]


def main() -> None:
    lessons, directories = indexes()
    prediction_records = []
    grouped_predictions: dict[str, list[dict]] = defaultdict(list)
    for index, (number, title, snippet, expected, explanation, misconception) in enumerate(PYTHON_PREDICTIONS, 1):
        record = {
            "id": f"python.prediction.{index:02d}",
            "lesson_number": number,
            "title": title,
            "snippet": snippet,
            "prompt": "Что выведет код и почему? Сначала ответь без запуска.",
            "expected_output": expected,
            "step_by_step": explanation,
            "misconception_tag": misconception,
        }
        prediction_records.append(record)
        grouped_predictions[number].append(record)

    for number, records in grouped_predictions.items():
        directory = directories[lessons[number]["implementation_slug"]]
        body = "\n\n".join(
            f"### {record['title']}\n\n```python\n{record['snippet']}\n```\n\n"
            f"**Вопрос:** {record['prompt']}\n\n"
            f"<details><summary>Показать ответ</summary>\n\n"
            f"Expected:\n\n```text\n{record['expected_output']}\n```\n\n"
            f"{record['step_by_step']}\n\nMisconception: `{record['misconception_tag']}`.\n\n</details>"
            for record in records
        )
        lesson_path = directory / "lesson.md"
        lesson_path.write_text(
            upsert_section(lesson_path.read_text(encoding="utf-8"), "## Code prediction", body),
            encoding="utf-8",
        )

    sql_records = []
    grouped_sql: dict[str, list[dict]] = defaultdict(list)
    for index, (number, category, title, prompt, solution, columns, ordered) in enumerate(SQL_TASKS, 1):
        record = {
            "id": f"sql.{category}.{index:02d}",
            "lesson_number": number,
            "category": category,
            "title": title,
            "schema": SHOP_SCHEMA,
            "seed": SHOP_SEED,
            "prompt": prompt,
            "expected_columns": columns,
            "comparison": "ordered" if ordered else "unordered",
            "solution_sql": solution,
            "hidden_dataset_note": "Проверять additional rows, NULL, duplicates и ties.",
        }
        sql_records.append(record)
        grouped_sql[number].append(record)
    for index, (number, title, prompt, expected) in enumerate(PG_SCENARIOS, 1):
        record = {
            "id": f"sql.postgresql.{index:02d}",
            "lesson_number": number,
            "category": "postgresql_reasoning",
            "title": title,
            "schema": BOOKING_SCHEMA,
            "seed": BOOKING_SEED,
            "prompt": prompt,
            "expected_columns": [],
            "comparison": "reasoning_rubric",
            "solution_sql": None,
            "expected_reasoning": expected,
        }
        sql_records.append(record)
        grouped_sql[number].append(record)

    for number, tasks in grouped_sql.items():
        directory = directories[lessons[number]["implementation_slug"]]
        blocks = []
        for task in tasks:
            columns = ", ".join(task["expected_columns"]) or "reasoning rubric"
            blocks.append(
                f"### {task['title']}\n\n```sql\n{task['schema']}\n```\n\n"
                f"Seed:\n\n```sql\n{task['seed']}\n```\n\n"
                f"**Вопрос:** {task['prompt']}\n\n"
                f"Expected columns: {columns}. Comparison: {task['comparison']}.\n\n"
                "SQL runner пока не подключён: выполни запрос в локальном PostgreSQL и сверь result с rubric."
            )
        lesson_path = directory / "lesson.md"
        lesson_path.write_text(
            upsert_section(lesson_path.read_text(encoding="utf-8"), "## SQL practice", "\n\n".join(blocks)),
            encoding="utf-8",
        )

    banks = {
        "schema_version": 1,
        "python_prediction": prediction_records,
        "sql": sql_records,
        "testing": scenario_records("testing", TESTING),
        "operations": scenario_records("operations", OPERATIONS),
        "debugging": scenario_records("debugging", DEBUGGING),
        "architecture": scenario_records("architecture", ARCHITECTURE),
    }
    for kind in ("testing", "operations", "debugging", "architecture"):
        grouped: dict[str, list[dict]] = defaultdict(list)
        for record in banks[kind]:
            grouped[record["lesson_number"]].append(record)
        for number, records in grouped.items():
            directory = directories[lessons[number]["implementation_slug"]]
            body = "\n\n".join(
                f"### {record['title']}\n\n**Сценарий:** {record['prompt']}\n\n"
                f"**Rubric:** {record['expected_reasoning']}\n\n"
                f"**Слабый ответ:** {record['common_weak_answer']}"
                for record in records
            )
            lesson_path = directory / "lesson.md"
            lesson_path.write_text(
                upsert_section(lesson_path.read_text(encoding="utf-8"), f"## {kind.title()} practice", body),
                encoding="utf-8",
            )
    OUTPUT.write_text(json.dumps(banks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Added {len(prediction_records)} Python predictions, {len(sql_records)} SQL, "
        f"{len(TESTING)} testing, {len(OPERATIONS)} operations, "
        f"{len(DEBUGGING)} debugging and {len(ARCHITECTURE)} architecture scenarios"
    )


if __name__ == "__main__":
    main()
