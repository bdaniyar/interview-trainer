# Источники и версии

Проверено 2026-11-24.

| Источник и раздел | Применение |
| --- | --- |
| [OpenAI · Function calling](https://developers.openai.com/api/docs/guides/function-calling) | JSON schema, несколько вызовов, item ID и call ID, отправка function-call outputs и исходных reasoning items. |
| [OpenAI · Conversation state](https://developers.openai.com/api/docs/guides/conversation-state) | История и повторная передача элементов для stateless продолжения. В P3 владелец истории проверяется приложением. |
| [Python 3.12 · asyncio tasks](https://docs.python.org/3.12/library/asyncio-task.html) | TaskGroup, timeout и propagation of cancellation. |
| [FastAPI · Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) и [Lifespan](https://fastapi.tiangolo.com/advanced/events/) | Серверная инъекция principal и жизненный цикл адаптера. |
| [Pydantic · Strict Mode](https://pydantic.dev/docs/validation/latest/concepts/strict_mode/) | Строгие DTO и запрет дополнительных полей. |
| [OWASP GenAI · LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) и [OWASP API1 · BOLA](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/) | Ограничение capabilities и проверка владения перед чтением payload. |

Протестировано с CPython 3.12.13, FastAPI 0.116.1, Pydantic 2.11.7, Starlette 0.47.3, httpx 0.28.1, Uvicorn 0.35.0 и pytest 8.4.1. Полный набор зависимостей и хешей находится в `requirements.txt`. Отдельный SDK lock содержит OpenAI 3.57.0 и httpx2 2.16.2. SDK обмен проверен через MockTransport, включая отдельную проверку OpenAI 3.58.0. P3 использует прикладную модель бюджета и синтетический principal. Live совместимость с конкретной моделью не проверялась.
