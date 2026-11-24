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

## Phase 11 и Structured Outputs

`structured.py` показывает `AsyncOpenAI.responses.parse(..., text_format=WireExtraction)`. С тем же lock-файлом Python 3.12.13, OpenAI 3.57.0, HTTPX2 2.16.2 и Pydantic 2.14.4 выполнены 6 новых MockTransport cases. Они проверяют вложенную строгую схему, обязательные nullable поля, typed `output_parsed`, refusal, incomplete и ошибки разбора. В частности, оборванная JSON-строка в incomplete item поднимает Pydantic ValidationError до возврата ответа SDK. Если приложение должно различать incomplete и malformed во всех таких случаях, сначала прочитай статус ответа, полученного без автопарсинга, затем валидируй полный payload.

Проверки SDK выполняются в среде авторов. В Runner остаются отдельные offline fixtures. Сверка образцов и источников выполнена 2026-11-22.

## Phase 12 · вызов функций

`tools_roundtrip.py` показывает два сообщения Responses. В первом запросе две strict tool schemas. Адаптер читает typed `function_call`, проверяет `id`, `call_id`, имя и JSON. Прикладной callback выполняет разрешённое действие. Второй запрос передаёт исходный вход, все output items, в том числе opaque reasoning item, и `function_call_output` по `call_id`. Для ограниченного примера continuation просит финальный ответ с `tool_choice="none"`. OpenAI client принадлежит вызывающему коду, повторы выключены в тесте.

Сверка 2026-11-24 подтвердила wire-запросы на OpenAI 3.57.0, HTTPX2 2.16.2, Pydantic 2.14.4 и Python 3.12.13. В отдельной временной среде заменён только OpenAI на 3.58.0, затем прошли `uv pip check` и тот же набор из 22 MockTransport-тестов. Основной SDK lock сохранён. Новые 10 сценариев покрывают несколько calls, continuation, различие ID, невалидные поля и отсутствие повтора после timeout/503. MockTransport подтверждает сериализацию и поведение установленного SDK на этих сценариях.

В Claude Messages `tool_use.id` связывается с `tool_result.tool_use_id`. В Gemini Interactions ответ `function_result` использует `call_id` исходного шага. Сверены [OpenAI Function Calling](https://developers.openai.com/api/docs/guides/function-calling), [Claude Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) и [Gemini Function Calling](https://aistudio.google.com/docs/function-calling).
