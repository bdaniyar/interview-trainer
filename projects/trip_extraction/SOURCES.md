# Источники, версии и fixtures

Проверено 2026-11-22. Исполняемое окружение проекта закреплено в `requirements.txt`.

| Источник | Использовано |
| --- | --- |
| [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) | Подмена провайдера. FastAPI 0.116.1 |
| [Pydantic fields](https://docs.pydantic.dev/latest/concepts/fields/), [validators](https://docs.pydantic.dev/latest/concepts/validators/) | Обязательные nullable поля, strict int и межполевое правило. Pydantic 2.11.7 |
| [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) | Responses parser, strict shape и отказ. Отдельно проверены OpenAI SDK 3.57.0, HTTPX2 2.16.2 и Pydantic 2.14.4 под Python 3.12.13 |
| [OpenAI Evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices) | Разделение метрик, фиксированные кейсы и проверка регрессий |
| [OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) | Недоверенный контекст и проверка прав вне промпта |

`data/cases.jsonl` — замороженные входы и ожидаемые исходы. `provider-fixtures.jsonl` содержит только scripted provider behavior. SHA-256 обоих файлов фиксирует `evaluation-report.json`. Few-shot из `prompt.py` проверяются на отсутствие текстов dev и holdout.
