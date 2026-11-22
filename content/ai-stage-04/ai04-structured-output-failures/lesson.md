# Отказ, обрыв и границы восстановления

Провайдер дал обрезанный ответ. Второй вызов может вернуть данные, потратить средства или повторить сбой. Приложению нужна конечная политика, сохраняющая исходный запрос и смысл ошибки.

## Учебные цели

- Различить refusal, incomplete, malformed, invalid domain и ошибки транспорта.
- Ограничить восстановление одной разрешённой попыткой.
- Сохранить correlation ID и неизвестные значения.

## Теория

**Refusal** — модель отклонила запрос. **Incomplete** — генерация оборвана, например по лимиту. **Malformed** — payload нарушил wire schema. **Domain invalid** — форма принята, но нарушено правило приложения. Checkout до checkin может быть корректной строкой JSON и ошибкой интервала. Транспортная ошибка может быть временной, постоянной или с неизвестным исходом. Timeout оставляет неизвестным внешний эффект и стоимость.

Repair — дополнительный запрос для исправления класса результата. Он требует разрешения конфигурацией. Для incomplete, malformed и подтверждённого временного отказа до обработки в учебном контракте сверху есть одна попытка. Refusal, permanent и неизвестный timeout завершают работу. Если DTO уже валиден и в нём неизвестный год, исправлять нечего. Верни needs_clarification. Догадка о годе нарушила бы контракт исходных данных.

**Correlation ID** связывает попытки. Его получаем один раз. Счётчик живёт вокруг вызовов и не сбрасывается после перехода к новому типу ошибки. Исходный текст неизменяем. Разбирая ошибки, записывай категорию и идентификатор. Текст запроса, исключение поставщика и свободный вывод не нужны в журнале.

## Модель понимания

Проверь три перехода. Первый incomplete без разрешения завершает запрос. С разрешением запускается repair. Если вторая попытка malformed, состояние становится terminal. Отдельная политика для этого статуса не даёт третью попытку.

## Что нужно знать на Junior

Отмена вызывающей задачи отличается от локального таймаута. Не подавляй CancelledError. У state machine должен быть конечный максимум, независимо от ответов провайдера.

## Примеры кода

```python
attempts=[]
for number,status in enumerate(["truncated","invalid"],1):
    attempts.append((number,status))
    if status=="ready" or number==2:
        break
assert attempts==[(1,"truncated"),(2,"invalid")]
assert len(attempts)==2
assert attempts[-1][1]!="ready"
print(attempts[-1])
```

Вывод `(2, 'invalid')`. Второй вызов сохранил свой исход. Публичный пример иллюстрирует только общий счётчик.

## Типичные ошибки

- Повторять refusal.
- Сбрасывать budget при новом типе ошибки.
- Принимать partial output за completed.
- Логировать raw payload.

## Практика

Запрос «Рига в июле» вернул `incomplete`. После repair пришёл валидный город и null для дат. Что ответить с разрешением и без него?

<details>
<summary>Сверить ход рассуждения</summary>

С разрешением будет needs_clarification и сохранённый город. Без него останется первый incomplete.
</details>

## Вопросы с собеседований

1. Чем invalid domain отличается от malformed?
2. Что гарантирует timeout?

## Хорошие ответы

**Чем invalid domain отличается от malformed?**

Например, две даты имеют правильный тип, но checkout предшествует checkin. Просить уточнение и хранить null.

**Что гарантирует timeout?**

Он оставляет внешний эффект неизвестным. Повторы требуют отдельной политики. Исходный request, общий счётчик и correlation ID.

## Критерии хорошего ответа

Покажи переход для двух различных сбоев, объясни границу авторизации и точное поведение unknown.

## Задача

Напиши `async recover(send, request, *, allow_repair=False) -> Result`. Request неизменяемый с correlation_id. Send возвращает Outcome(kind, trip=None) или поднимает TimeoutError. Первая попытка с repair=False. Вторую можно сделать с True только при allow_repair и kind incomplete, malformed или retryable. Refusal и permanent завершают запрос. TimeoutError переведи в timeout, отмену пропусти. Completed проверяется `validate_trip`; ValueError становится invalid_domain, валидный DTO с null — needs_clarification. Например, два incomplete с разрешением дают итог incomplete, attempts=2 и исходный ID. Check подставляет другие порядки, виды ошибок, отмену и частичные данные.

## Шпаргалка

### Краткий конспект

Разделяй тип неуспеха и политику повторов. Attempt 1 + максимум 1 repair. Null сохраняется. Refusal и timeout terminal. Correlation ID и input одинаковы для обеих отправок.

1. Что ограничивает repair?
2. Как вернуть неизвестный город?
3. Означает ли timeout отсутствие вызова?

<details>
<summary>Сверить конспект</summary>

Явное разрешение и вид первого сбоя. Null и needs_clarification. Timeout оставляет эффект неизвестным.
</details>

## Источники

- OpenAI Structured Outputs, schema and refusals. Responses API и ограниченное подмножество JSON Schema. Проверено 2026-11-22. [A2](https://developers.openai.com/api/docs/guides/structured-outputs)
- OpenAI API, Error codes. Сетевые ошибки, timeout и статусы. Проверено 2026-11-22. [A7](https://developers.openai.com/api/docs/guides/error-codes)
