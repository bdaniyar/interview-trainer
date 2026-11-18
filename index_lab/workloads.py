"""Server-owned synthetic workload shapes and independent expected results."""
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from index_lab.policy import Index, Key

DAY = date(2026, 11, 8)
LOWER_SQL = "SELECT id, email FROM users WHERE lower(email)='person7@example.test' ORDER BY id"
HOTEL_SQL = ("SELECT id, arrival FROM orders WHERE hotel_id=7 "
             "AND arrival >= DATE '2026-11-08' AND arrival < DATE '2026-11-11' "
             "ORDER BY arrival,id LIMIT 7")
NEW_SQL = "SELECT id, created_at FROM orders WHERE status='new' ORDER BY created_at DESC,id DESC LIMIT 6"
OWNER_SQL = "SELECT id, created_at FROM orders WHERE user_id=9 ORDER BY created_at DESC,id DESC LIMIT 6"
PLAN_SQL = ("SELECT o.id,u.email FROM orders o JOIN users u ON u.id=o.user_id "
            "WHERE o.hotel_id=7 AND o.status='new' ORDER BY o.id LIMIT 12")
QUERY_SQL = ("SELECT id, created_at FROM orders WHERE created_at::date = DATE '2026-11-08' "
             "ORDER BY created_at,id LIMIT 30")


@dataclass(frozen=True)
class Workload:
    title: str
    slug: str
    subject: str
    queries: tuple[str, ...]
    designs: tuple[Index, ...]


def design(table, *columns, active_only=False):
    return Index(table, tuple(Key(name) for name in columns), (), active_only)


TASKS = {
    "pg.index.11.4.expression-v1": Workload("Поиск email без учёта регистра",
        "s11-index-mental-model", "index", (LOWER_SQL,),
        (Index("users", (Key("email", expression="lower"),), (), False),)),
    "pg.index.11.6.composite-v1": Workload("Диапазон дат одного отеля",
        "s11-composite-indexes-and-column-order", "index", (HOTEL_SQL,),
        (design("orders", "hotel_id", "arrival", "id"),)),
    "pg.index.11.7.partial-v1": Workload("Лента новых заказов",
        "s11-selectivity", "index", (NEW_SQL,),
        (design("orders", "created_at", "id", active_only=True),)),
    "pg.index.11.5.workload-v1": Workload("Два индекса на горячие выдачи",
        "s11-postgresql-b-tree", "index", (OWNER_SQL, NEW_SQL),
        (design("orders", "user_id", "created_at", "id"),
         design("orders", "created_at", "id", active_only=True))),
    "pg.plan.11.8.analysis-v1": Workload("План соединения с фактическими строками",
        "s11-explain-and-explain-analyze", "plan", (PLAN_SQL,), ()),
    "pg.plan.11.15.range-v1": Workload("Выборка дня по индексируемому диапазону",
        "s11-pagination", "optimize", (QUERY_SQL,), ()),
}

# Includes no match, repeated projected values, tied timestamps, large IDs,
# hot/cold distribution and shifted date boundaries.
CASES = (
    (0, 20000, 100, 31, 97, 1, 0),
    (1, 16000, 113, 27, 67, 0, 1),
    (2, 19000, 121, 31, 47, 2, -2),
    (3, 12100, 83, 11, 80, 1, 3),
    (4, 18500, 127, 13, 11, 3, -9),
    (9007199254740993, 22000, 137, 37, 101, 4, 5),
)


def fixture(case):
    offset, rows, users, hotels, new_every, days_offset, minute_offset = CASES[case]
    people = [(offset+i, ("PERSON7" if i in (7, 24) and case % 2 == 0 else "person7" if i == 7
                else f"person{i}") + "@example.test", "north" if i % 2 else "south")
              for i in range(1, users+1)]
    start = datetime.combine(DAY - timedelta(days=days_offset), datetime.min.time())
    orders = []
    for i in range(1, rows+1):
        # Floor creates timestamp ties. Separate arrival dates preserve ordering edge cases.
        clock = start + timedelta(minutes=i//4 + minute_offset)
        if case == 4:
            # Sparse target day and rows exactly at the exclusive upper bound.
            if i <= 6:
                clock = datetime.combine(DAY, datetime.min.time())
            elif i <= 40:
                clock = datetime.combine(DAY + timedelta(days=1), datetime.min.time())
            else:
                clock = start + timedelta(minutes=i % 1200)
        orders.append((offset+i, offset+1+i%users, 1+i%hotels, clock.date(), clock,
                       "new" if i % new_every == 0 else "archived", (i % 39) + 1))
    if case == 1:
        people[6] = (offset+7, "nobody@example.test", "north")
    return people, orders


def truth(query, case):
    people, orders = fixture(case)
    if query == LOWER_SQL:
        return ["id", "email"], [(str(id_), email) for id_, email, _ in people
                                 if email.lower() == "person7@example.test"]
    if query == HOTEL_SQL:
        subset = sorted((arrival, id_) for id_, _, hotel, arrival, *_ in orders
                        if hotel == 7 and DAY <= arrival < DAY + timedelta(days=3))[:7]
        return ["id", "arrival"], [(str(id_), arrival.isoformat()) for arrival, id_ in subset]
    if query == PLAN_SQL:
        emails = {id_: email for id_, email, _ in people}
        subset = [(str(id_), emails[person]) for id_, person, hotel, _, _, status, _ in orders
                  if hotel == 7 and status == "new"][:12]
        return ["id", "email"], subset
    if query == QUERY_SQL:
        subset = sorted((clock, id_) for id_, _, _, _, clock, _, _ in orders if clock.date() == DAY)[:30]
    else:
        subset = sorted(((clock, id_) for id_, person, _, _, clock, status, _ in orders
                         if (status == "new" if query == NEW_SQL else person == 9)),
                        reverse=True)[:6]
    return ["id", "created_at"], [(str(id_), clock.isoformat()) for clock, id_ in subset]
