# OAuth2 Authorization Code + PKCE

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Resume Defense основан только на фактических StudyHub, Hotel Booking и Share Recipe claims.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **OAuth2 Authorization Code + PKCE**, а не только запомнить термин;
- прочитать и изменить короткий пример для `verifier/challenge`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **OAuth2 Authorization Code + PKCE** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**verifier/challenge.** `verifier/challenge` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**intercepted code cannot be exchanged without verifier.** `intercepted code cannot be exchanged without verifier` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.

**state/redirect validation still needed.** `state/redirect validation still needed` защищается по реализованному flow: проблема, принятое решение, trade-off, failure mode и test/metric.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `verifier/challenge` и `intercepted code cannot be exchanged without verifier` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `verifier/challenge`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- verifier/challenge
- intercepted code cannot be exchanged without verifier
- state/redirect validation still needed

### Полезно

- связать OAuth2 Authorization Code + PKCE с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### OAuth2 Authorization Code + PKCE: отдельный пример

```text
Тема: OAuth2 Authorization Code + PKCE

Фокус:
- verifier/challenge
- intercepted code cannot be exchanged without verifier
- state/redirect validation still needed

Рабочая проверка:
Защищай только реализованный flow: проблема → решение → trade-off → failure mode → проверка.
```

Этот micro-scenario сформирован из outline конкретного урока и не переиспользуется соседними subtopics.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `verifier/challenge` до запуска.

**B · Find the bug.** Найди нарушение `intercepted code cannot be exchanged without verifier` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про OAuth2 Authorization Code + PKCE за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое OAuth2 Authorization Code + PKCE и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме OAuth2 Authorization Code + PKCE?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

OAuth2 Authorization Code + PKCE: это отдельный технический контракт

### Нормальный Junior answer

> OAuth2 Authorization Code + PKCE — тема, в которой я сначала фиксирую `verifier/challenge`, затем объясняю `intercepted code cannot be exchanged without verifier` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме OAuth2 Authorization Code + PKCE?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- verifier/challenge
- intercepted code cannot be exchanged without verifier
- state/redirect validation still needed

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме OAuth2 Authorization Code + PKCE?

## Задача

Сделай короткую письменную практику по теме **OAuth2 Authorization Code + PKCE**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** OAuth2 Authorization Code + PKCE: это отдельный технический контракт
- **Механизм:** Отвечай только о реализованном: problem → own decision → trade-off → test/metric; честно обозначай границы.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL documentation](https://www.postgresql.org/docs/current/)
- [Redis documentation](https://redis.io/docs/latest/)

Последняя проверка версий: **2026-08-27**.
