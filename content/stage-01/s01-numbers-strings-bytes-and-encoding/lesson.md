# Numbers, strings, bytes and encoding

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Python указан в 18/18 primary вакансий; object model — базовый screening foundation.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Numbers, strings, bytes and encoding**, а не только запомнить термин;
- прочитать и изменить короткий пример для `int/float/Decimal basics`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

`int`, `float` и `Decimal` представляют числа с разными гарантиями. `str` хранит Unicode-текст, а `bytes` — последовательность байтов. Между текстом и байтами всегда есть явная граница encoding.

### Как работает

Обычный `float` следует IEEE 754 и хранит число в двоичной форме; многие десятичные дроби не представимы точно. `Decimal` хранит десятичное представление и управляемый контекст точности. `text.encode('utf-8')` создаёт bytes, а `raw.decode('utf-8')` восстанавливает str при совпадающей кодировке.


### Пример

```python
from decimal import Decimal

print(0.1 + 0.2 == 0.3)                 # False
print(Decimal("0.1") + Decimal("0.2"))  # 0.3

raw = "Алматы".encode("utf-8")
print(raw.decode("utf-8"))              # Алматы
```

### Важный нюанс / limitation

`0.1 + 0.2 == 0.3` даёт `False` из-за округления binary float. Для денег обычно используют `Decimal` в Python и `NUMERIC/DECIMAL` в БД; вход для `Decimal` лучше брать из строки, а не из уже неточного float.

### Где используется в backend

HTTP/JSON приносит текст, файлы и сокеты — bytes, а база должна хранить деньги типом с десятичной точностью.

## Mental model

Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- объяснить погрешность float
- различать str/bytes
- уметь encode/decode
- выбрать Decimal для денег

### Полезно

- знать про `math.isclose` для приближённых сравнений

### Можно не учить глубоко

- битовая раскладка IEEE 754 и Unicode normalization algorithms

## Code examples

### Numbers, strings, bytes and encoding: отдельный пример

```python
text = "Алматы"
payload = text.encode("utf-8")
restored = payload.decode("utf-8")

print(type(text).__name__, type(payload).__name__)
print(restored == text)
```

`str` — Unicode text, `bytes` — закодированное представление на I/O-границе.

## Common mistakes

### Ошибка 1

Создать `Decimal(0.1)` и ожидать точное `0.1`; лучше `Decimal('0.1')`.

### Ошибка 2

Декодировать произвольные bytes без согласованной encoding/error policy.

## Practice

**A · Code prediction.** Проверь `0.1 + 0.2 == 0.3` и объясни результат.

**B · Find the bug.** Найди потерю точности в `Decimal(0.1)`.

**D · Small task.** Преобразуй UTF-8 bytes в str и корректно обработай ошибочную последовательность.

## Interview questions

### Основной вопрос

Почему float не подходит для точных денежных расчётов и чем `str` отличается от `bytes`?

### Follow-up

Как корректно сравнивать результаты обычных scientific float-вычислений?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Float хранит двоичное приближение; для денег нужен Decimal/NUMERIC. `str` — Unicode, `bytes` — конкретные байты.

### Нормальный Junior answer

> Многие десятичные дроби нельзя точно записать в двоичном float, поэтому операции накапливают небольшую погрешность. Для денег используют `Decimal` и SQL `NUMERIC`, создавая Decimal из строки. `str` представляет Unicode-текст, а `bytes` — данные на границе файла или сети; переход выполняют явными `encode` и `decode` с одной кодировкой.

### Углубление / follow-up

**Как корректно сравнивать результаты обычных scientific float-вычислений?**

Обычно через допустимую абсолютную/относительную погрешность, например `math.isclose`, а не прямое `==`.

## Expected answer rubric

### Must mention

- объяснить погрешность float
- различать str/bytes
- уметь encode/decode
- выбрать Decimal для денег

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Создать `Decimal(0.1)` и ожидать точное `0.1`; лучше `Decimal('0.1')`.
- пересказ одного определения без механизма или примера.

### Follow-up

- Как корректно сравнивать результаты обычных scientific float-вычислений?

## Задача

Сделай короткую письменную практику по теме **Numbers, strings, bytes and encoding**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Float хранит двоичное приближение; для денег нужен Decimal/NUMERIC. `str` — Unicode, `bytes` — конкретные байты.
- **Механизм:** Отделяй identity объекта, его value и binding имени. Assignment обычно создаёт новую связь, а не копию.
- **Ограничение:** Создать `Decimal(0.1)` и ожидать точное `0.1`; лучше `Decimal('0.1')`.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [Python Data Model](https://docs.python.org/3.12/reference/datamodel.html)
- [Python execution model](https://docs.python.org/3.12/reference/executionmodel.html)

Последняя проверка версий: **2026-08-27**.
