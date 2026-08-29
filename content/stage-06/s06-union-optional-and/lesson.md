# Union, Optional and `|`

> [!IMPORTANT]
> **P0 · вероятность на интервью: high · 12 минут.** Python указан в 18/18; typing повышает надёжность API contracts.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Union, Optional and `|`**, а не только запомнить термин;
- прочитать и изменить короткий пример для `optional value`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Это статический контракт для checker и IDE; runtime-поведение Python и validation остаются отдельными слоями.

### Как работает

Покажи, что проверит static analyzer, что произойдёт runtime и где boundary должна добавить validation.

**optional value.** `T | None` разрешает значение `None`, но не делает аргумент или поле необязательным без default; missing и explicit null — разные состояния.

**required nullable field distinction.** `NULL` означает отсутствие известного значения; сравнение с ним делают через `IS NULL`, а многие выражения дают `UNKNOWN`.

**narrowing.** `narrowing` описывает статическую часть type contract; runtime остаётся динамическим, а недоверенные данные требуют отдельной validation.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `optional value` и `required nullable field distinction` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

## Mental model

Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- optional value
- required nullable field distinction
- narrowing

### Полезно

- связать Union, Optional and `|` с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Union, Optional and `|`: отдельный пример

```python
def normalize(value: str | None) -> str:
    return value.strip() if value is not None else ""

print(normalize(None))
try:
    normalize()
except TypeError:
    print("argument is still required")
```

Nullable type разрешает `None`, но отсутствие default не делает argument optional при вызове.

## Common mistakes

### Ошибка 1

Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `optional value` до запуска.

**B · Find the bug.** Найди нарушение `required nullable field distinction` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Union, Optional and `|` за 60 секунд: определение, механизм, пример, ограничение.

## Code prediction

### Optional не создаёт default

```python
def parse(value: str | None):
    return value is None
try:
    parse()
except TypeError:
    print('missing')
```

**Вопрос:** Что выведет код и почему? Сначала ответь без запуска.

<details><summary>Показать ответ</summary>

Expected:

```text
missing
```

Union с None разрешает значение None, но параметр остаётся обязательным без default.

Misconception: `optional-vs-default`.

</details>

## Interview questions

### Основной вопрос

Что такое Union, Optional and `|` и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Union, Optional and `|`?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Union, Optional and `|`: Это статический контракт для checker и IDE; runtime-поведение Python и validation остаются отдельными слоями.

### Нормальный Junior answer

> Union, Optional and `|` — тема, в которой я сначала фиксирую `optional value`, затем объясняю `required nullable field distinction` на коротком примере. Ключевой механизм: Покажи, что проверит static analyzer, что произойдёт runtime и где boundary должна добавить validation. Главная практическая ошибка — Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Union, Optional and `|`?**

Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.

## Expected answer rubric

### Must mention

- optional value
- required nullable field distinction
- narrowing

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Union, Optional and `|`?

## Задача

Сделай короткую письменную практику по теме **Union, Optional and `|`**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Union, Optional and `|`: Это статический контракт для checker и IDE; runtime-поведение Python и validation остаются отдельными слоями.
- **Механизм:** Аннотация — описание для инструментов; runtime validation выполняет отдельный код или библиотека.
- **Ограничение:** Считать type hint runtime validation или использовать `Any`, скрывая ошибку contract.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [typing](https://docs.python.org/3.12/library/typing.html)

Последняя проверка версий: **2026-08-27**.
