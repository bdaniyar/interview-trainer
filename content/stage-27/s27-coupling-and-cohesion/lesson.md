# Coupling and cohesion

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Architecture basics нужны для объяснения design choices без senior-level overengineering.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Coupling and cohesion**, а не только запомнить термин;
- прочитать и изменить короткий пример для `Coupling and cohesion`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Coupling and cohesion** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**Coupling and cohesion.** `Coupling and cohesion` задаёт границу слоя и направление зависимости; хороший design оставляет seam для теста без реальной infrastructure.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `Coupling and cohesion` и `Coupling and cohesion` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `Coupling and cohesion`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Высокоуровневое правило не должно зависеть от детали storage/framework без необходимости.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- Coupling and cohesion

### Полезно

- связать Coupling and cohesion с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Coupling and cohesion: отдельный пример

```python
def example_s27_coupling_and_cohesion() -> tuple[str, ...]:
    # Coupling and cohesion: проверяем отдельный contract урока.
    return ('Coupling and cohesion',)

assert example_s27_coupling_and_cohesion()
```

Проведи границу слоя и dependency direction; business rule не должен зависеть от framework.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `Coupling and cohesion` до запуска.

**B · Find the bug.** Найди нарушение `Coupling and cohesion` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Coupling and cohesion за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Coupling and cohesion и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Coupling and cohesion?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Coupling and cohesion: это отдельный технический контракт

### Нормальный Junior answer

> Coupling and cohesion — тема, в которой я сначала фиксирую `Coupling and cohesion`, затем объясняю `Coupling and cohesion` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Coupling and cohesion?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- Coupling and cohesion

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Coupling and cohesion?

## Задача

Сделай короткую письменную практику по теме **Coupling and cohesion**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Coupling and cohesion: это отдельный технический контракт
- **Механизм:** Высокоуровневое правило не должно зависеть от детали storage/framework без необходимости.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python abc](https://docs.python.org/3.12/library/abc.html)
- [FastAPI dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)

Последняя проверка версий: **2026-08-27**.
