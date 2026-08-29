# Cascade and delete-orphan

> [!IMPORTANT]
> **P1 · вероятность на интервью: medium · 10 минут.** ORM/SQLAlchemy явно встречались в 4/18, но Session/transaction знание фундаментально для FastAPI backend.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Cascade and delete-orphan**, а не только запомнить термин;
- прочитать и изменить короткий пример для `ORM cascade vs DB cascade`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это часть SQLAlchemy 2.x data-access flow: statement, Session, identity map и transaction lifecycle.

### Как работает

Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback.

**ORM cascade vs DB cascade.** `ORM cascade vs DB cascade` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.

**ownership.** `ownership` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.

**dangerous deletes.** `dangerous deletes` влияет на SQLAlchemy Session/transaction state, момент фактического SQL I/O и поведение rollback или relationship loading.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `ORM cascade vs DB cascade` и `ownership` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `ORM cascade vs DB cascade`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Один request/use case обычно владеет одной Session и явно завершает commit или rollback.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- ORM cascade vs DB cascade
- ownership
- dangerous deletes

### Полезно

- связать Cascade and delete-orphan с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Cascade and delete-orphan: отдельный пример

```text
Сценарий: Удаление parent неожиданно удалило shared children.

Проверка:
Настроить cascade по ownership и DB FK semantics; тестировать delete/replace relationship на реальной БД.
```

Это отдельный debugging example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `ORM cascade vs DB cascade` до запуска.

**B · Find the bug.** Найди нарушение `ownership` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Cascade and delete-orphan за 60 секунд: определение, механизм, пример, ограничение.

## Debugging practice

### Wrong cascade

**Сценарий:** Удаление parent неожиданно удалило shared children.

**Rubric:** Настроить cascade по ownership и DB FK semantics; тестировать delete/replace relationship на реальной БД.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Cascade and delete-orphan и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Cascade and delete-orphan?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Cascade and delete-orphan: Это часть SQLAlchemy 2.x data-access flow: statement, Session, identity map и transaction lifecycle.

### Нормальный Junior answer

> Cascade and delete-orphan — тема, в которой я сначала фиксирую `ORM cascade vs DB cascade`, затем объясняю `ownership` на коротком примере. Ключевой механизм: Укажи владельца Session/transaction, момент SQL I/O и state entity до и после flush/commit/rollback. Главная практическая ошибка — Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Cascade and delete-orphan?**

Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.

## Expected answer rubric

### Must mention

- ORM cascade vs DB cascade
- ownership
- dangerous deletes

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Cascade and delete-orphan?

## Задача

Сделай короткую письменную практику по теме **Cascade and delete-orphan**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Cascade and delete-orphan: Это часть SQLAlchemy 2.x data-access flow: statement, Session, identity map и transaction lifecycle.
- **Механизм:** Один request/use case обычно владеет одной Session и явно завершает commit или rollback.
- **Ограничение:** Скрыть commit внутри repository, допустить N+1 или продолжить Session без rollback после ошибки.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [SQLAlchemy 2.0 Session](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [ORM Querying Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html)

Последняя проверка версий: **2026-08-27**.
