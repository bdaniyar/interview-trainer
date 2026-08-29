# Ports and network diagnostics

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Linux basics явно встречались в 5/18 и часто подразумеваются для backend debugging.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Ports and network diagnostics**, а не только запомнить термин;
- прочитать и изменить короткий пример для `curl`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Ports and network diagnostics** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**curl.** `curl` связывает shell command с конкретным process, file, permission, environment или network state.

**listening port.** `list` — ordered mutable sequence: индекс и append удобны, а поиск значения и вставка в начало линейны; aliases видят общие mutations.

**localhost.** `localhost` связывает shell command с конкретным process, file, permission, environment или network state.

**DNS.** `DNS` связывает shell command с конкретным process, file, permission, environment или network state.

**service unavailable.** `service unavailable` связывает shell command с конкретным process, file, permission, environment или network state.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `curl` и `listening port` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `curl`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Процесс видит filesystem, env, user permissions, descriptors и network namespace.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- curl
- listening port
- localhost
- DNS

### Полезно

- service unavailable

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Ports and network diagnostics: отдельный пример

```text
Сценарий: API не bind 8000.

Проверка:
ss/lsof, stop owner или change mapping.
```

Это отдельный operations example для данного subtopic, а не общий пример stage.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `curl` до запуска.

**B · Find the bug.** Найди нарушение `listening port` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Ports and network diagnostics за 60 секунд: определение, механизм, пример, ограничение.

## Operations practice

### Port occupied

**Сценарий:** API не bind 8000.

**Rubric:** ss/lsof, stop owner или change mapping.

**Слабый ответ:** Сразу назвать инструмент без symptom, boundary и verification.

## Interview questions

### Основной вопрос

Что такое Ports and network diagnostics и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Ports and network diagnostics?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Ports and network diagnostics: это отдельный технический контракт

### Нормальный Junior answer

> Ports and network diagnostics — тема, в которой я сначала фиксирую `curl`, затем объясняю `listening port` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Ports and network diagnostics?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- curl
- listening port
- localhost
- DNS

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Ports and network diagnostics?

## Задача

Сделай короткую письменную практику по теме **Ports and network diagnostics**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Ports and network diagnostics: это отдельный технический контракт
- **Механизм:** Процесс видит filesystem, env, user permissions, descriptors и network namespace.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GNU Coreutils manual](https://www.gnu.org/software/coreutils/manual/coreutils.html)
- [Bash manual](https://www.gnu.org/software/bash/manual/)

Последняя проверка версий: **2026-08-27**.
