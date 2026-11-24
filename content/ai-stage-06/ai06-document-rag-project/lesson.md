# Document Knowledge Assistant: жизненный цикл RAG

У базы знаний есть жизненный цикл. Документ можно загрузить, заменить или удалить, пока поисковые и генеративные запросы уже идут. Проект P5 показывает, какие данные видит каждый шаг.

## Учебные цели

- Собрать ingest, retrieval и типизированное подтверждение источников.
- Заблокировать частичную активацию, устаревшую цитату и выдачу чужого фрагмента.
- Связать результаты с вложенными OpenTelemetry spans.

## Теория

При ingest валидация и хеширование предшествуют chunking и embedding. Провайдер работает до DB transaction. Готовые fragments записываются под новой версией, и active pointer меняется только после полного набора. При сбое читатель видит старую версию. Повтор того же ingest идемпотентен, другой текст с тем же номером конфликтует, а tombstone запрещает повторную активацию.

Поиск применяет tenant, scopes, owner или grant, active version и embedding space. Rank выдаёт ссылки на выбранные chunks. Отдельный scoped запрос получает их protected payload. Перед ответом приложение повторяет проверку всех использованных источников. Exact reference включает версию и access epoch; epoch меняется при изменении права или активации, поэтому revoke→grant не оживляет старый snapshot. Успех проверки относится к её DB snapshot: изменение после неё может сделать уже отправленный ответ устаревшим. P5 читает БД при каждом запросе, без retrieval cache.

Trace — цепочка временных интервалов одного запроса. SDK понимает родителя и дочерние spans ingest/chunk/embed или request/retrieve/rank/rerank/generate/validate. В attributes остаются request ID, ревизии, размеры, длительности и безопасный outcome. Prompt, body, private principal и сырые exception туда не пишутся.

## Модель понимания

Запрос прочитал document v7 при epoch=12. Пока generator ждал, владелец отозвал grant и выдал его снова. Текущий epoch=14, поэтому законченный ответ со старым evidence получает stale_evidence. Следующий запрос заново прочитает текущие источники.

## Что нужно знать на Junior

Чтобы отладить пустой ответ, смотри retrieval candidates, затем сколько блоков поместилось, потом status generation и validation. Для production с внешним cache нужна invalidation, привязанная к tenant, версии и ACL; она не заменяет проверку перед выдачей.

## Примеры кода

```python
active = {"guide": (2, 7)}
snapshot = ("guide", 2, 7)
for epoch in (7, 8):
    active["guide"] = (2, epoch)
    print(snapshot[1:] == active[snapshot[0]])
```

Вывод `True False`. Версия не менялась, но revision доступа изменилась. Реальное состояние проверяет PostgreSQL, а в упражнении это одна запись словаря.

## Типичные ошибки

- Включить новую версию до последней успешной строки embeddings.
- Держать SQL-транзакцию во время генерации.
- Проверить доступ только перед поиском и забыть о завершении long request.
- Записать документы или exceptions в trace.

## Практика

Вход: v3 активна, для v4 подготовилось два из трёх chunks, а потом пользователь запускает поиск. Какую версию он увидит? Что если следующий полный ingest активирует v4, пока генератор ещё отвечает по v3?

<details>
<summary>Сверить разбор упражнения</summary>

Первый поиск может использовать v3. Частичный набор v4 не активируется. После полной активации итоговая проверка отклонит источники v3. Новый запрос строит контекст в текущем состоянии.

</details>

## Вопросы с собеседований

1. Что видно при частичном batch?
2. Для чего access epoch?
3. Что покажет безопасный trace?

## Хорошие ответы

**Что видно при частичном batch?**

Последняя целиком активированная версия. Сбой подготовки не переключает pointer.

**Для чего access epoch?**

Он обнаруживает изменение прав даже при неизменной версии. Revoke→grant не делает старый snapshot текущим.

**Что покажет безопасный trace?**

Имена стадий, порядок, outcome, ревизии, размеры и задержку. Private identity и raw payload не нужны для корреляции.

## Критерии хорошего ответа

Нарисуй границу транзакции. Покажи revoke→grant во время генерации и два безопасных поля span для диагностики.

## Задача

Реализуй `activate(state,actor,key,version,text,build)`, `revise_access(state,actor,key,reader=None,delete=False)` и `answer(state,actor,question,retrieve,generate)`. State отображает (tenant,key) в Document, DTO в contracts.py. Для изменения нужен write и owner существующей записи. activate отвергает пустые данные и нецелую/неположительную version как invalid, чужой/удалённый документ или отсутствующий scope как forbidden. Совпавшая текущая версия и SHA-256 текста дают replayed без build, другая запись со старым номером conflict. Build обязан вернуть непустую последовательность Chunk с индексами от нуля, без пустых частей, их конкатенация равна тексту. Ошибка или неполнота дают incomplete без изменения состояния. Успех activated, увеличь epoch и сохрани grants. revise_access отзывает reader либо ставит tombstone, увеличивая epoch только при изменении, идемпотентный статус updated. answer проверяет read, вызывает retrieve(actor,question), проверяет tenant/owner-or-reader/tombstone/version/epoch/index и передаёт уникальные пары (ref,text) генератору. None или пустой context дают insufficient_evidence. Невыданный ref даёт invalid_citation. Повторная проверка всех supplied после generation даёт stale_evidence при изменении. Успех возвращает answered с исходным текстом и ref. Исключения зависимостей дают retrieval_error или generation_error. Пример Run активирует карту и цитирует текст. Check меняет источники во время генерации, пробует повтор и частичный набор. Реальная практика P5 запускается отдельно по [README](https://github.com/bdaniyar/interview-trainer/tree/main/projects/document_rag).

## Шпаргалка

### Краткий конспект

Ingest строит целый новый набор и активирует версию атомарно. Retrieval берёт только разрешённые фрагменты; final recheck убирает устаревшие цитаты. При snapshot (v2,epoch 7) смена epoch на 8 требует нового поиска. Trace фиксирует границы, исходы и длительность.

- Можно ли повторить ingest?
- Где проверяется финальная цитата?
- Какая гарантия остаётся при update после финального SELECT?

<details>
<summary>Ответы для самопроверки</summary>

**Можно ли повторить ingest?**

Да, при тех же version и fingerprint он идемпотентен.

**Где проверяется финальная цитата?**

После generation, перед формированием ответа.

**Какая гарантия остаётся при update после финального SELECT?**

Проверка относится к snapshot SELECT и не отзывает уже отправленный ответ.

</details>

## Источники

- Querying, HNSW, filtering. PG17 + pgvector 0.8.2. Проверено 2026-11-24. [PGV](https://github.com/pgvector/pgvector/tree/v0.8.2)
- Creating nested spans. Локальный SDK, безопасные атрибуты. Проверено 2026-11-24. [OTEL](https://opentelemetry.io/docs/languages/python/instrumentation/)
- Dependencies. Внедрение доверенного principal. Проверено 2026-11-24. [FAST](https://fastapi.tiangolo.com/tutorial/dependencies/)
- Object-level authorization. Проверка прав перед чтением. Проверено 2026-11-24. [BOLA](https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/)
