# Session mental model

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Session mental model**, а не только запомнить термин;
- прочитать и изменить короткий пример для `unit of work`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

SQLAlchemy `Session` — рабочая область ORM: она отслеживает entities, хранит identity map, собирает изменения как unit of work и управляет transaction. Это не просто один connection.

### Как работает

Новая entity после `add` становится pending; при flush INSERT/UPDATE/DELETE уходят в текущую transaction, а объект становится persistent. Identity map гарантирует один Python object на пару `(mapped class, primary key)` внутри Session. После close/expunge объект detached и lazy loading больше не имеет активного Session context.


### Пример

```python
with Session(engine) as session:
    first = session.get(User, 1)
    second = session.get(User, 1)

    print(first is second)  # True: identity map
```

### Важный нюанс / limitation

Session получает connection по необходимости. `flush` отправляет SQL, но не делает commit; после flush error нужен rollback. Обычно один request/use case владеет одной Session. AsyncSession нельзя одновременно использовать из нескольких tasks.

### Где используется в backend

FastAPI yield-dependency создаёт Session на request, service задаёт transaction boundary, а cleanup закрывает Session.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- identity map
- unit of work
- основные entity states
- flush vs commit
- request scope

### Полезно

- expire/refresh
- autoflush
- transaction context manager

### Можно не учить глубоко

- внутренние события unit-of-work sorter

## Code examples

### Session mental model: отдельный пример

```python
def load_twice(session, model, object_id):
    raise NotImplementedError
```

Это публичный starter contract практики «Session identity map». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Common mistakes

### Ошибка 1

Создать глобальную Session для всего приложения — state и transaction начнут протекать между requests.

### Ошибка 2

Коммитить внутри каждого repository method и разрушать атомарность use case.

### Ошибка 3

Продолжить работу после IntegrityError без `rollback()`.

## Practice

**A · Code prediction.** Два `session.get(User, 1)` — сравни identity результатов.

**B · Find the bug.** Найди global Session и commit в repository.

**C · Rewrite.** Перенеси commit на service/use-case boundary.

**D · Small task.** Реализуй `load_twice` и пройди hidden identity-map test.

## Interview questions

### Основной вопрос

Что такое SQLAlchemy Session и зачем ей identity map?

### Follow-up

Чем `flush` отличается от `commit`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Session — unit of work + identity map + transaction state; в одной Session одна DB row представлена одним Python object.

### Нормальный Junior answer

> Session отслеживает ORM objects и их изменения, объединяет их в unit of work и владеет transaction state. Identity map хранит уже загруженные объекты по class и primary key, поэтому повторный `get` в той же Session обычно возвращает тот же Python object. Flush отправляет SQL внутри transaction, а commit завершает её. Для web request обычно создают отдельную Session.

### Углубление / follow-up

**Чем `flush` отличается от `commit`?**

Flush синхронизирует ORM state с БД внутри открытой transaction и может получить generated id; commit фиксирует transaction. После rollback результат flush не сохраняется.

## Expected answer rubric

### Must mention

- identity map
- unit of work
- основные entity states
- flush vs commit

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Создать глобальную Session для всего приложения — state и transaction начнут протекать между requests.
- пересказ одного определения без механизма или примера.

### Follow-up

- Чем `flush` отличается от `commit`?

## Задача

### Session identity map

load_twice делает два Session.get и возвращает tuple; не закрывает и не commit session.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Session — unit of work + identity map + transaction state; в одной Session одна DB row представлена одним Python object.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Создать глобальную Session для всего приложения — state и transaction начнут протекать между requests.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
