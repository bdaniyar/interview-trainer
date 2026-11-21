# Проверка OpenAI Python SDK для авторов курса

Совместимость проверяется с Python 3.12, OpenAI SDK 3.57.0 и HTTPX2 2.16.2. Этот SDK принимает HTTPX2-клиент в `http_client`. В `requirements.txt` закреплены транзитивные версии и хеши. Среда отделена от Pythoria Runner.

```sh
uv venv --python 3.12 /tmp/pythoria-sdk-check
uv pip sync --python /tmp/pythoria-sdk-check/bin/python --require-hashes tools/ai_sdk_verify/requirements.txt
/tmp/pythoria-sdk-check/bin/python -m pytest tools/ai_sdk_verify
```

Первичная установка требует доступных пакетов или локального кэша. Тесты используют in-process MockTransport и блокируют подключение через обычные сокеты. Проверяются запрос POST /v1/responses, несколько элементов в выходе, aggregate output_text, usage, неполный ответ, 401, 429 и timeout. `max_retries=0` оставляет один вызов. Модель и ключ в тесте вымышленные.

Основной пример находится в `example.py`; жизненным циклом клиента управляет вызывающий код. Урок использует SDK-shaped fake, совместимый с networkless Runner. Совместимость с живой моделью и её качество этими тестами не измеряются.

Проверка AI3.5 дополнительно подаёт SSE-кадры через MockTransport. Она проверяет тип события, Unicode delta, final response и закрытие HTTPX2 stream.
