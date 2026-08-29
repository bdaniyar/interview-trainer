# Layered architecture

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Architecture basics нужны для объяснения design choices без senior-level overengineering.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Layered architecture**, а не только запомнить термин;
- прочитать и изменить короткий пример для `API`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Layered architecture** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**API.** `API` задаёт границу слоя и направление зависимости; хороший design оставляет seam для теста без реальной infrastructure.

**service/use case.** `service/use case` задаёт границу слоя и направление зависимости; хороший design оставляет seam для теста без реальной infrastructure.

**data access.** `data access` задаёт границу слоя и направление зависимости; хороший design оставляет seam для теста без реальной infrastructure.

**infrastructure.** `infrastructure` задаёт границу слоя и направление зависимости; хороший design оставляет seam для теста без реальной infrastructure.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `API` и `service/use case` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `API`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Высокоуровневое правило не должно зависеть от детали storage/framework без необходимости.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- API
- service/use case
- data access
- infrastructure

### Полезно

- связать Layered architecture с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Layered architecture: отдельный пример

```python
def example_s27_layered_architecture() -> tuple[str, ...]:
    # Layered architecture: проверяем отдельный contract урока.
    return ('API', 'service/use case', 'data access', 'infrastructure',)

assert example_s27_layered_architecture()
```

Проведи границу слоя и dependency direction; business rule не должен зависеть от framework.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `API` до запуска.

**B · Find the bug.** Найди нарушение `service/use case` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Layered architecture за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Layered architecture и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Layered architecture?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Layered architecture: это отдельный технический контракт

### Нормальный Junior answer

> Layered architecture — тема, в которой я сначала фиксирую `API`, затем объясняю `service/use case` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Layered architecture?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- API
- service/use case
- data access
- infrastructure

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Layered architecture?

## Задача

Сделай короткую письменную практику по теме **Layered architecture**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Layered architecture: это отдельный технический контракт
- **Механизм:** Высокоуровневое правило не должно зависеть от детали storage/framework без необходимости.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python abc](https://docs.python.org/3.12/library/abc.html)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
