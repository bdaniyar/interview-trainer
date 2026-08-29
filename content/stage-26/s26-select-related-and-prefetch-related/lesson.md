# `select_related` and `prefetch_related`

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Django/DRF встречался в 7/18 и расширяет Казахстанскую junior-воронку.

## Learning objectives

После урока ты сможешь:

- объяснить `N+1` своими словами и связать с backend-сценарием;
- объяснить `FK/one-to-one vs collections.` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

Django/DRF предоставляет batteries-included стек: ORM, migrations, admin, auth и API abstractions.

В теме **`select_related` and `prefetch_related`** важно уверенно объяснять следующие части:

### N+1

N+1 возникает, когда список загружается одним query, а relationship каждого объекта — отдельным; query-count test и eager-loading делают проблему видимой.

### FK/one-to-one vs collections

Для `FK/one-to-one vs collections` сопоставь Django/DRF abstraction с request, ORM query count, validation и permissions.

## Mental model

Django project содержит configuration, apps группируют domain capability, DRF serializer задаёт API boundary.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### `select_related` and `prefetch_related`: отдельный пример

```python
def example_s26_select_related_and_prefetch_related() -> tuple[str, ...]:
    # `select_related` and `prefetch_related`: проверяем отдельный contract урока.
    return ('N+1', 'FK/one-to-one vs collections',)

assert example_s26_select_related_and_prefetch_related()
```

Проследи Django/DRF request, ORM query count, validation, permission и response.

## Common mistakes

**Ошибка:** Путать select_related и prefetch_related или переносить FastAPI patterns дословно.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **`select_related` and `prefetch_related`** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Сравни request flow и data access одного endpoint в DRF и FastAPI. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- N+1
- FK/one-to-one vs collections.
- Django project содержит configuration, apps группируют domain capability, DRF serializer задаёт API boundary.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Путать select_related и prefetch_related или переносить FastAPI patterns дословно.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- N+1
- FK/one-to-one vs collections.

## Задача

Разбери backend-сценарий: **Сравни request flow и data access одного endpoint в DRF и FastAPI.**

Запиши решение в формате: assumptions → mechanism → edge cases → test/verification. Для этого урока автоматическая coding-проверка не нужна; ответ сверяется с rubric interview-вопроса.

## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **`select_related` and `prefetch_related`**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Django documentation](https://docs.djangoproject.com/en/5.2/)
- [Django REST Framework guide](https://www.django-rest-framework.org/)

Последняя проверка версий: **2026-08-27**.
