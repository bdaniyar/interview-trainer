# HTTP API поездки и происхождение результата

Локальная форма ручного уточнения получает результат извлечения. Ей нужны известные поля, версия контракта и точная причина остановки. Сырое сообщение провайдера для этого не подходит.

## Учебные цели

- Спроектировать HTTP DTO для запроса и ответа.
- Сохранить идентичность операции и provenance без утечки.
- Доказать независимость конкурентных запросов.

## Теория

FastAPI на входе проверяет форму и предел запроса. **Dependency injection** передаёт выбранный сервером provider. Отправляем текст один раз и ограничиваем таймаут. Статус transport показывает доставку, extraction status — качество и полноту операции. HTTP 200 с needs_clarification означает, что пришёл допустимый объект с неизвестными полями. При provider refusal и incomplete тоже возвращаем явный outcome без DTO поездки. Malformed или domain invalid даёт 502. Timeout даёт 504, invalid request 422.

DTO ответа содержит request_id, status, trip, model, prompt_version, schema_version и category. Request ID создаётся для каждого HTTP-входа, чтобы соединить сырые метрики и события без текста. Версия схемы задаёт значение каждого поля, версия промпта объясняет, какие факты заполнялись. Сырые provider exceptions могут содержать текст, authorization header или сведения о клиенте. Переводи ожидаемые ошибки в безопасные категории. При логировании оставляй поля allowlist. FastAPI валидацию 422 можно переопределить, иначе details могут содержать отклонённый input.

Конкурентные запросы могут делить HTTP-клиент и неизменяемую конфигурацию. Переменная текущего текста или ответа должна быть локальной для вызова. Тест отправляет два разных обращения через ASGITransport и проверяет соответствие каждого DTO исходному запросу. Тест таймаута использует отменяемое ожидание Event. Проверка контракта не требует порта, а отдельный loopback smoke проверяет запуск Uvicorn.

## Модель понимания

Границы идут так: DTO → provider с timeout → domain validation → typed result. Никакая ветка не возвращает raw. Результат с неверной датой не попадает в сохранённый список заявок.

## Что нужно знать на Junior

Сопоставляй HTTP и status явно. Проверь отсутствие журналирования оригинального текста при плохом вводе и provider exception. Схема ответа не фильтрует секрет, уже помещённый в разрешённое строковое поле.

## Примеры кода

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

class View(BaseModel):
    request_id: str
    status: str
app = FastAPI()
@app.get("/probe", response_model=View)
def probe():
    return {"request_id":"r-5","status":"ready","raw":"private"}
with TestClient(app) as client:
    response=client.get("/probe")
    assert response.status_code==200
    assert response.json()=={"request_id":"r-5","status":"ready"}
    assert "private" not in response.text
print("Результат прошёл через схему")
```

Вывод подтверждает фильтрацию дополнительного ключа. Секрет, случайно записанный в статус, требовал бы проверки значения до формирования DTO.

## Типичные ошибки

- Использовать общий изменяемый storage для текущего результата.
- Возвращать raw provider объект.
- Считать валидный JSON разрешением на бронь.
- Ретранслировать отклонённый запрос в error details.

## Практика

Подумай о двух запросах `Астана, двое` и `Алматы, четверо`, которые завершаются в обратном порядке. Какие assertions отличат гонку данных от нормального поведения?

<details>
<summary>Сверить ход рассуждения</summary>

Сравни каждому вызову ожидаемый город и гостей, проверь уникальные request IDs и число вызовов провайдера. Порядок завершения не обязан совпадать с порядком отправки.
</details>

## Вопросы с собеседований

1. Какие поля должны попасть в лог?
2. Как проверить параллельность?

## Хорошие ответы

**Какие поля должны попасть в лог?**

Для диагностики достаточно request ID, статуса, безопасной категории ошибки и времени обработки. ID связывает запись с ответом, а категория отличает timeout от ошибки DTO. Сырые запросы, ключи и исключения провайдера могут содержать приватные данные.

**Как проверить параллельность?**

Отправь два запроса с разными данными и задержи первый внутри fake-адаптера. Проверь, что каждый ответ содержит ожидаемые город и гостей и что ID различаются. В одном кейсе оставь дату неизвестной и проверь, что `null` и `needs_clarification` принадлежат только этому ответу.

## Критерии хорошего ответа

Покажи независимость DTO, timeout, защиту от лишнего поля и provenance на любой ветке.

## Задача

Реализуй `create_app(provider, *, timeout=0.5)`. POST /extract-trip принимает JSON с единственным text длиной 1–500 после strip. Неизвестные ключи и неверный ввод дают HTTP 422, status=invalid_request, без исходного текста. `provider.extract(text)` возвращает `Raw(status, data)` или поднимает TimeoutError/ProviderFailure. Completed принимает словарь четырёх nullable полей. Даты — ISO YYYY-MM-DD и выезд строго позже въезда; guests — положительный strict int; city — непустой str; extra запрещены. Пример валидного результата с city=Рига и датами null даёт needs_clarification. Refusal/incomplete возвращаем отдельно с trip=null. Неверный completed даёт invalid_trip/502; TimeoutError — timeout/504; ProviderFailure — unavailable/503. Ответ содержит request_id UUID, status, trip, model из provider.identity, версии из fixtures и category (None при completed, иначе равную status). В неверном DTO провайдер не вызван; ошибки и исходный текст не попадают в ответ или лог. Check использует другое содержимое и конкурентные запросы.

## Шпаргалка

### Краткий конспект

Клиент диктует текст, сервер выбирает provider. Схема проверяет вход и выход. Nullable trip сообщает о неизвестности, refusal и incomplete не имеют trip. ID и версии сопровождают исход. Проверяй параллельность ASGI запросами.

1. Какие статусы следует отличать?
2. За что отвечает model field?
3. Почему no raw logs?

<details>
<summary>Сверить конспект</summary>

Полный и частичный успех, отказ, обрыв, ошибку и timeout. Model фиксирует происхождение. Сырые данные могут содержать ключи и приватный текст.
</details>

## Источники

- FastAPI Dependencies. FastAPI 0.116.1 и подмена зависимостей. Проверено 2026-11-22. [FASTAPI](https://fastapi.tiangolo.com/tutorial/dependencies/)
- OpenAI Structured Outputs, schema and refusals. Responses API и ограниченное подмножество JSON Schema. Проверено 2026-11-22. [A2](https://developers.openai.com/api/docs/guides/structured-outputs)
- OWASP LLM01, Prompt Injection. Граница доверия приложения. Проверено 2026-11-22. [S1](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
