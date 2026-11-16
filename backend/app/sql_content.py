"""Explicit lesson capabilities; only the public projection leaves the server."""
from dataclasses import dataclass
import json
from types import MappingProxyType

from fastapi import HTTPException

from .content import content_repo
from .sql_schemas import SqlLesson

DATASET_ID = "shop-v1"
DATASET_CHECKSUM = "a1de3973eb4a2febc818c026def43716109e7ffde6b0bc46721e11d1b2fa4b97"


@dataclass(frozen=True)
class Registration:
    lesson_id: str
    task_id: str
    revision: int
    grader_revision: str
    expected_columns: tuple[str, ...]
    tests_total: int
    prompt: str
    starter_sql: str
    rows_feedback: str
    column_hint: str = ""
    dataset_id: str = DATASET_ID
    dataset_checksum: str = DATASET_CHECKSUM
    comparison: str = "unordered"


def build_registry(entries):
    lessons, tasks = {}, set()
    for entry in entries:
        if entry.lesson_id in lessons or entry.task_id in tasks:
            raise ValueError("Duplicate SQL lesson/task registration")
        if entry.revision < 1 or not 1 <= entry.tests_total <= 16 or not entry.expected_columns:
            raise ValueError("Invalid SQL task registration")
        lessons[entry.lesson_id] = entry
        tasks.add(entry.task_id)
    return MappingProxyType(lessons)


REGISTRY = build_registry((
    Registration("backend-interview.10.2.select-aliases-and-expressions", "sql.guided.10.2.projection.v1", 1,
        "projection-v1", ("user_id", "email"), 4,
        "Выведите id и email всех пользователей из users. Назовите столбец id псевдонимом user_id. Результат должен содержать только столбцы user_id и email в этом порядке. Порядок строк несущественен.",
        "SELECT id, email FROM users;\n",
        "Результат не совпадает с условием на одном из наборов. Проверьте все строки, лишние строки и дубликаты.",
        "Для id нужен псевдоним user_id."),
    Registration("backend-interview.10.3.where-and-boolean-logic", "sql.basic.01", 1,
        "active-users-v1", ("id", "email"), 5,
        "Выведите id и email пользователей из users, у которых active = true. Только столбцы id и email в этом порядке. Порядок строк несущественен.",
        "SELECT id, email\nFROM users;\n",
        "Проверьте условие фильтрации: нужны все активные пользователи, без лишних строк и дубликатов."),
    Registration("backend-interview.10.4.null-and-three-valued-logic", "sql.basic.03", 1,
        "null-country-v1", ("id", "email"), 5,
        "Выведите id и email пользователей из users, для которых country неизвестна (NULL). Только столбцы id и email в этом порядке. Порядок строк несущественен.",
        "SELECT id, email\nFROM users;\n",
        "Проверьте работу с неизвестными значениями. SQL NULL отличается от пустой строки и обычного значения; учтите все нужные строки и дубликаты."),
    Registration("backend-interview.10.5.order-by-limit-and-offset", "sql.basic.04", 1,
        "latest-orders-v1", ("id", "created_at"), 6,
        "Верните два последних заказа по created_at. При одинаковой дате заказ с большим id должен идти первым. Только столбцы id и created_at в этом порядке. Если заказов меньше двух, верните все имеющиеся.",
        "SELECT id, created_at\nFROM orders;\n",
        "Проверьте направление сортировки, порядок заказов при одинаковой дате и ограничение количества строк.",
        comparison="ordered"),
    Registration("backend-interview.10.6.distinct", "sql.basic.05", 1,
        "distinct-countries-v1", ("country",), 6,
        "Выведите уникальные значения country из users. Исключите SQL NULL и отсортируйте страны по возрастанию. Только столбец country. Пустая строка является значением и должна остаться, если встречается в данных.",
        "SELECT country\nFROM users;\n",
        "Проверьте повторы, исключение SQL NULL и сортировку по возрастанию. Пустая строка не равна NULL.",
        comparison="ordered"),
    Registration("backend-interview.10.7.aggregates", "sql.aggregation.09", 1,
        "count-orders-v1", ("orders_count",), 6,
        "Посчитайте общее количество заказов в orders. Верните одну строку с одним столбцом orders_count. Если заказов нет, результат должен содержать число 0.",
        "SELECT id, status\nFROM orders;\n",
        "Проверьте источник подсчёта и число строк результата: нужна одна строка с количеством всех заказов, включая 0 для пустой таблицы.",
        comparison="ordered"),
    Registration("backend-interview.10.8.group-by", "sql.aggregation.10", 1,
        "orders-by-status-v1", ("status", "count"), 6,
        "Посчитайте количество заказов для каждого status. Верните status и count в этом порядке, отсортировав строки по status по возрастанию.",
        "SELECT status\nFROM orders;\n",
        "Проверьте состав групп, количество заказов в каждой группе и сортировку по status. Нужна одна строка на каждый имеющийся статус.",
        comparison="ordered"),
    Registration("backend-interview.10.9.having", "sql.aggregation.13", 1,
        "users-with-two-orders-v1", ("user_id", "count"), 6,
        "Найдите пользователей, у которых минимум два заказа. Верните user_id и количество заказов под названием count. Отсортируйте результат по user_id по возрастанию.",
        "SELECT user_id\nFROM orders;\n",
        "Проверьте количество заказов каждого пользователя и границу «минимум два»: два и больше подходят, один — нет. Учтите точный count и порядок user_id.",
        comparison="ordered"),
    Registration("backend-interview.10.10.inner-join", "sql.join.17", 1,
        "join-order-users-v1", ("order_id", "email"), 6,
        "Для каждого заказа верните order_id и email его владельца. Только эти два столбца в указанном порядке. Один пользователь может владеть несколькими заказами; порядок строк несущественен.",
        "SELECT id, user_id\nFROM orders;\n",
        "Проверьте ключ связи и число строк: каждый заказ должен встретиться один раз с email своего владельца. Сохраните все заказы одного пользователя."),
    Registration("backend-interview.10.11.left-join", "sql.join.18", 1,
        "users-without-orders-v1", ("id", "email"), 6,
        "Найдите пользователей без единого заказа. Верните только id и email в этом порядке, по одной строке на пользователя. Порядок строк несущественен.",
        "SELECT id, email\nFROM users;\n",
        "Проверьте отсутствие заказов: нужны все пользователи без совпадений и только они, без пропущенных и повторных строк."),
    Registration("backend-interview.10.12.right-and-full-outer-join", "sql.join.25", 1,
        "right-join-products-v1", ("product_id", "order_id"), 6,
        "Сохраните все товары, включая не встречающиеся в order_items. Верните product_id и order_id. Для товара без позиций order_id должен быть SQL NULL. Сортировка: product_id по возрастанию, затем order_id по возрастанию.",
        "SELECT id, name\nFROM products;\n",
        "Проверьте сохранение всех товаров, каждую связанную позицию заказа, SQL NULL для товара без пары и сортировку по product_id, order_id.",
        comparison="ordered"),
    Registration("backend-interview.10.13.self-join", "sql.join.20", 1,
        "users-managers-v1", ("email", "manager_email"), 6,
        "Верните email каждого пользователя и email его непосредственного руководителя под названием manager_email. Без руководителя нужен SQL NULL. Сохраните каждого пользователя ровно один раз; сортируйте по id исходного пользователя по возрастанию.",
        "SELECT id, email, manager_id\nFROM users;\n",
        "Проверьте направление связи пользователя с непосредственным руководителем. Сохраните пользователей без руководителя с SQL NULL и порядок по id пользователя.",
        comparison="ordered"),
    Registration("backend-interview.10.14.subqueries", 'sql.subquery.27', 1,
        'above-average-v1', ('id', 'total'), 6,
        'Заказы со строго большей, чем средняя по всем orders, суммой. Верните id,total; порядок строк несущественен.',
        'SELECT id,total FROM orders;\n',
        'Учитывайте все заказы при расчёте среднего, строгую границу и пустой набор.', comparison='unordered'),
    Registration("backend-interview.10.15.correlated-subquery", 'sql.subquery.31', 1,
        'latest-per-user-v1', ('id', 'user_id'), 6,
        'Верните id,user_id всех заказов с максимальным created_at своего пользователя. При равных максимальных timestamps нужны все такие заказы. Сортировка по user_id; внутри одного пользователя порядок свободный.',
        'SELECT id,user_id,created_at FROM orders;\n',
        'Сравнивайте дату в пределах своего пользователя; сохраните все максимальные совпадения и порядок групп user_id.', comparison='ordered'),
    Registration("backend-interview.10.16.exists-vs-in", 'sql.subquery.28', 1,
        'paid-buyers-v1', ('id', 'email'), 6,
        'Верните id,email пользователей, у которых есть хотя бы один paid-заказ. Каждый пользователь один раз; порядок строк несущественен.',
        'SELECT id,email FROM users;\n',
        'Проверьте paid-условие, связь с текущим пользователем и отсутствие умножения строк.', comparison='unordered'),
    Registration("backend-interview.10.17.cte", 'sql.subquery.30', 1,
        'paid-revenue-v1', ('user_id', 'revenue'), 6,
        'Посчитайте сумму total только paid-заказов каждого пользователя; оставьте revenue >= 150. Столбцы user_id,revenue, сортировка user_id по возрастанию.',
        'SELECT user_id,total,status FROM orders;\n',
        'Суммируйте только paid, включайте границу 150 и сортируйте по user_id.', comparison='ordered'),
    Registration("backend-interview.10.18.recursive-cte", 'sql.subquery.32', 1,
        'manager-chain-v1', ('id', 'depth'), 6,
        'От пользователя с id=4 пройдите вверх по manager_id. Верните id,depth: старт на глубине 0, далее непосредственный руководитель. Сортировка depth по возрастанию. В проверочных данных цепочка ациклична; при отсутствии id=4 результат пуст.',
        'SELECT id,manager_id FROM users;\n',
        'Нужны все предки вверх, исходная строка на depth=0 и пустой результат без стартового пользователя.', comparison='ordered'),
    Registration("backend-interview.10.19.case", 'sql.basic.06', 1,
        'status-label-v1', ('id', 'label'), 6,
        'Для каждого заказа верните id,label: paid → completed; cancelled → cancelled; любой другой статус → pending. Порядок строк несущественен.',
        'SELECT id,status FROM orders;\n',
        'Проверьте все ветки, запасной ELSE и сохранение каждой строки заказа.', comparison='unordered'),
    Registration("backend-interview.10.20.set-operations", 'sql.set.50', 1,
        'active-countries-except-paid-v1', ('country',), 6,
        'Верните уникальные страны активных пользователей, в которых нет ни одного пользователя с paid-заказом. NULL рассматривается как одно значение множества. Столбец country; по возрастанию, NULL в конце.',
        'SELECT country,active FROM users;\n',
        'Сравните множества стран, устраните повторы и учитывайте NULL как одно значение EXCEPT.', comparison='ordered'),
    Registration("backend-interview.10.21.window-functions", 'sql.window.37', 1,
        'previous-total-v1', ('id', 'user_id', 'total', 'previous_total'), 6,
        'Для каждого заказа верните id,user_id,total,previous_total — total предыдущего заказа этого пользователя. Порядок внутри окна created_at,id по возрастанию; итог по user_id,created_at,id. У первого заказа previous_total — SQL NULL.',
        'SELECT id,user_id,total,created_at FROM orders;\n',
        'Окно должно начинаться заново для каждого пользователя; учитывайте id при одинаковых датах и SQL NULL у первой строки.', comparison='ordered'),
    Registration("backend-interview.10.22.row-number-rank-dense-rank", 'sql.window.33', 1,
        'order-row-number-v1', ('id', 'user_id', 'row_number'), 6,
        'Верните id,user_id,row_number для всех заказов. Нумерация с 1 отдельно по user_id, created_at DESC,id DESC. Итог по user_id,row_number.',
        'SELECT id,user_id,created_at FROM orders;\n',
        'Проверьте PARTITION BY, обе сортировки DESC, последовательность без пропусков и итоговый порядок.', comparison='ordered'),
    Registration("backend-interview.10.23.partition-by-and-window-ordering", 'sql.window.36', 1,
        'running-revenue-v1', ('id', 'user_id', 'running_total'), 6,
        'Верните id,user_id,running_total — накопительную сумму total пользователя по created_at,id ASC. Включайте текущую строку, все статусы и все заказы; итог по user_id,created_at,id.',
        'SELECT id,user_id,total,created_at FROM orders;\n',
        'Проверьте границы partition/frame, хронологический порядок с id и нарастание суммы вместо общего итога.', comparison='ordered'),
    Registration("backend-interview.10.24.lag-and-lead", 'sql.window.38', 1,
        'next-order-time-v1', ('id', 'user_id', 'next_created_at'), 6,
        'Верните id,user_id,next_created_at — created_at следующего заказа пользователя по created_at,id ASC. У последнего SQL NULL. Итог по user_id,created_at,id.',
        'SELECT id,user_id,created_at FROM orders;\n',
        'Нужна следующая строка своего пользователя с корректным tie-breaker id и SQL NULL на конце.', comparison='ordered'),
))


def workspace_kind(metadata: dict) -> str:
    return "sql" if metadata.get("id") in REGISTRY and metadata.get("content_status") == "complete" else "python"


def task_record(slug: str, task_id: str) -> dict:
    metadata, _ = content_repo.lesson_dir(slug)
    spec = REGISTRY.get(metadata["id"])
    if workspace_kind(metadata) != "sql" or spec.task_id != task_id:
        raise HTTPException(404, "SQL-задание не подключено к этому уроку")
    bank = json.loads((content_repo.root / "practice_banks.json").read_text(encoding="utf-8"))
    matches = [item for item in bank["sql"] if item["id"] == spec.task_id]
    if len(matches) != 1 or (matches[0].get("expected_columns"), matches[0].get("comparison")) != (
            list(spec.expected_columns), spec.comparison):
        raise HTTPException(503, "Конфигурация SQL-задания временно недоступна")
    record = matches[0]
    # basic.01's legacy lesson_number says 10.2; this explicit capability mapping
    # enables it in 10.3 without rewriting its historical bank record. Likewise,
    # subquery.32 keeps historical 10.17 but is taught in 10.18; window.38 keeps
    # historical 10.21 but is enabled in 10.24. Capabilities own the lesson mapping.
    fields = dict(id=spec.task_id, lesson_id=spec.lesson_id, revision=spec.revision,
        grader_revision=spec.grader_revision, dataset_id=spec.dataset_id, dataset_checksum=spec.dataset_checksum,
        expected_columns=list(spec.expected_columns), comparison=spec.comparison, tests_total=spec.tests_total)
    if any(key in record and record[key] != value for key, value in fields.items()):
        raise HTTPException(503, "Конфигурация SQL-задания временно недоступна")
    return record | fields | dict(prompt=spec.prompt, starter_sql=spec.starter_sql,
                                 rows_feedback=spec.rows_feedback, column_hint=spec.column_hint)


def public_lesson(slug: str) -> SqlLesson:
    metadata, _ = content_repo.lesson_dir(slug)
    if workspace_kind(metadata) != "sql":
        raise HTTPException(404, "SQL Lab пока не подключён к этому уроку")
    task = task_record(slug, REGISTRY[metadata["id"]].task_id)
    return SqlLesson(lesson_id=metadata["id"], lesson_slug=metadata["slug"], dataset_id=task["dataset_id"],
        task_id=task["id"], task_revision=task["revision"], can_check=True,
        starter_sql=task["starter_sql"], prompt=task["prompt"], expected_columns=task["expected_columns"])
