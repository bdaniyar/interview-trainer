# Dependency injection

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Architecture basics нужны для объяснения design choices без senior-level overengineering.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Dependency injection**, а не только запомнить термин;
- прочитать и изменить короткий пример для `explicit dependencies`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Dependency injection** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**explicit dependencies.** `explicit dependencies` задаёт границу слоя и направление зависимости; хороший design оставляет seam для теста без реальной infrastructure.

**substitution/testing.** `substitution/testing` задаёт границу слоя и направление зависимости; хороший design оставляет seam для теста без реальной infrastructure.

**framework DI vs general principle.** `framework DI vs general principle` задаёт границу слоя и направление зависимости; хороший design оставляет seam для теста без реальной infrastructure.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `explicit dependencies` и `substitution/testing` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `explicit dependencies`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Высокоуровневое правило не должно зависеть от детали storage/framework без необходимости.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- explicit dependencies
- substitution/testing
- framework DI vs general principle

### Полезно

- связать Dependency injection с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Dependency injection: отдельный пример

```python
class Service:
    def __init__(self, clock): self.clock = clock
    def now(self): return self.clock()
s = Service(lambda: 42)
print(s.now())
```

Expected: `42`. Explicit dependency делает поведение заменяемым в тесте без global patch.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `explicit dependencies` до запуска.

**B · Find the bug.** Найди нарушение `substitution/testing` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Dependency injection за 60 секунд: определение, механизм, пример, ограничение.

## Code prediction

### Dependency передана явно

```python
class Service:
    def __init__(self, clock): self.clock = clock
    def now(self): return self.clock()
s = Service(lambda: 42)
print(s.now())
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
42
```

Explicit dependency делает поведение заменяемым в тесте без global patch.

Misconception: `dependency-injection`.

</details>

## Interview questions

### Основной вопрос

Что такое Dependency injection и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Dependency injection?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Dependency injection: это отдельный технический контракт

### Нормальный Junior answer

> Dependency injection — тема, в которой я сначала фиксирую `explicit dependencies`, затем объясняю `substitution/testing` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Dependency injection?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- explicit dependencies
- substitution/testing
- framework DI vs general principle

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Dependency injection?

## Задача

Сделай короткую письменную практику по теме **Dependency injection**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Dependency injection: это отдельный технический контракт
- **Механизм:** Высокоуровневое правило не должно зависеть от детали storage/framework без необходимости.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python abc](https://docs.python.org/3.12/library/abc.html)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
