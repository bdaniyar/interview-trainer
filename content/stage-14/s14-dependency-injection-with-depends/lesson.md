# Dependency injection with `Depends`

> [!IMPORTANT]
> **P0 · вероятность на интервью: very_high · 12 минут.** FastAPI явно встречался в 9/18, любой Python web framework — в 16/18.

## Learning objectives

После урока ты сможешь:

- объяснить `dependency graph` своими словами и связать с backend-сценарием;
- объяснить `request-scoped lifecycle` своими словами и связать с backend-сценарием;
- объяснить `auth/session/settings` своими словами и связать с backend-сценарием;
- распознать типичную ошибку и предложить проверяемое исправление.

## Theory

FastAPI связывает ASGI request lifecycle, routing, validation, dependency graph и response serialization.

В теме **Dependency injection with `Depends`** важно уверенно объяснять следующие части:

### dependency graph

Dependency объявляет вход handler/service явно; FastAPI разрешает graph зависимостей на request, cache-ит результат в его рамках и выполняет cleanup yield-dependency.

### request-scoped lifecycle

LEGB ищет имя в local, enclosing, global и builtins; assignment делает имя local, если не объявлены `global` или `nonlocal`.

### auth/session/settings

Session владеет identity map и transaction state; после ошибки flush требуется rollback до дальнейшей работы.

### caching per request

Для `caching per request` проследи request через router, validation/dependencies, handler/service и response serialization.

## Mental model

Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

Проверь модель вопросами: кто владеет состоянием, где проходит граница операции, что увидит вызывающий код и как выглядит безопасный отказ.

## Code examples

### Dependency injection with `Depends`: отдельный пример

```python
from fastapi import FastAPI

app = FastAPI()
# Добавь dependency и endpoint.
```

Это публичный starter contract практики «Authorization dependency». Реализация и hidden assertions в lesson Markdown не раскрываются.

## Common mistakes

**Ошибка:** Открывать Session глобально или выполнять blocking I/O в async route.

**Симптом:** код проходит простой happy path, но ломается при повторном вызове, конкурентном запросе, ошибке зависимости или изменении данных.

**Причина:** механизм и границы ответственности не были проговорены до реализации.

**Исправление:** зафиксируй контракт, сделай state/transaction boundary явной и добавь тест на failure path.

## Interview questions

1. Объясни **Dependency injection with `Depends`** по схеме «определение → механизм → пример → ограничение».
2. Сценарий: Проследи request от router через dependency и service до response model. Какие уточнения ты задашь и как проверишь решение?
3. Какой слабый ответ по этой теме создаст риск в первой backend-задаче?

## Expected answer rubric

### Must mention

- dependency graph
- request-scoped lifecycle
- auth/session/settings
- caching per request.
- Path operation — внешний адаптер; бизнес-правила лучше держать в сервисе, а ресурсы закрывать в lifespan/yield dependency.

### Good additions

- назвать конкретный trade-off, а не только API;
- привести короткий пример из FastAPI/PostgreSQL/Redis, когда он действительно уместен;
- обозначить границу Junior: что нужно проверить в документации или измерить.

### Common wrong answers

- Открывать Session глобально или выполнять blocking I/O в async route.
- ответ из одного определения без механизма и failure mode.

### Follow-up

- Как изменится решение при повторном запросе, ошибке dependency или двух одновременных операциях?
- Какой unit/integration test подтвердит ключевой контракт?

## Что нужно уметь перед практикой

- dependency graph
- request-scoped lifecycle
- auth/session/settings
- caching per request.

## Задача

### Authorization dependency

require_admin читает X-Role: не admin → 403; GET /admin использует Depends.

Работай в main.py. Не меняй публичные имена и сигнатуры: hidden tests импортируют их напрямую. Проверь happy path, boundary values, повторные вызовы и propagation ошибок.
## Cheat sheet

Перед собеседованием запомни:

- дай точное определение **Dependency injection with `Depends`**;
- объясни механизм, а не только синтаксис;
- назови один realistic backend example;
- проговори failure mode и trade-off;
- заверши ответ способом проверки: test, constraint, log или metric.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
