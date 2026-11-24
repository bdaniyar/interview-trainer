# P5 · источники и версии

Источники сверены 2026-11-24. Фактически протестированы CPython 3.12.13, PostgreSQL 17.10, pgvector 0.8.2, psycopg/binary 3.2.13, FastAPI 0.116.1, Pydantic 2.11.7, OTel SDK/API 1.45.2 и semantic-conventions 0.66b2, pytest 8.4.1. Полный lock сохраняет зависимости и хеши. Образ PostgreSQL закреплён в [P4](../vector_search/SOURCES.md). В trace используются прикладные имена `rag.*`, без заявления о совместимости с незакреплёнными экспериментальными GenAI attributes.

- `plainto_tsquery`, ранжирование FTS; PostgreSQL baseline использует `ts_rank_cd`. [PostgreSQL 17 text search](https://www.postgresql.org/docs/17/textsearch-controls.html)
- Сложение обратных рангов; небольшое top-N окно добавляет прикладной scorer. [Оригинальная работа RRF](https://cormack.uwaterloo.ca/cormack/cormacksigir09-rrf.pdf)
- Насыщение TF, IDF и нормализация длины проверяются в отдельной Python задаче. [Robertson и Zaragoza, BM25](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf)
- Поиск перед генерацией; у P5 собственные scoped data, schema и failure policy. [Lewis и соавторы, RAG](https://arxiv.org/abs/2005.11401)
- Объектные права и indirect prompt injection. [OWASP API1](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/), [OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- Границы DTO и DI. [FastAPI](https://fastapi.tiangolo.com/tutorial/dependencies/), [Pydantic Strict Mode](https://pydantic.dev/docs/validation/latest/concepts/strict_mode/)
- Вложенные spans, status и SDK local export. [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/instrumentation/), [закреплённый пакет](https://pypi.org/project/opentelemetry-sdk/1.45.2/)

API-образ устанавливает hashed lock через uv 0.11.24 из образа, закреплённого по digest. [Официальная Docker-инструкция uv](https://docs.astral.sh/uv/guides/integration/docker/).

Фиксированные признаки и генератор проверяют контракт, включая смешанные языки. Утверждения о качестве реальной embedding модели или преимуществах hybrid на других корпусах требуют отдельного эксперимента.
