# Замороженная оценка P5

В корпусе 25 синтетических документов и 26 Markdown-версий на русском, казахском и английском. North и south имеют раздельный доступ. Каталог включает текущее и старое расписание, tombstone, выданные и отозванные grants, похожие посторонние сведения и текст с поддельной инструкцией. Оригинальные вопросы и разметка хранятся рядом. Казахский язык помечен кодом `kk`. Языковой редактор казахского отдельно не привлекался.

Разбиение 18 dev и 12 holdout, по 6 и 4 на язык. Один `group` удерживает близкие вопросы в одном split. В holdout есть cross-language вопрос о пароме с исходным документом на русском и казахско-английский вопрос о library code. Источники размечены на уровне (document ID, version), фрагменты этой версии сворачиваются с сохранением первого ранга. Разметка Claim включает отрицательные строки для проверки поддержки при формально допустимой ссылке.

## Воспроизведение

На свежей базе P5 из корня repository:

```sh
python -m projects.document_rag.evaluate seed
python -m projects.document_rag.evaluate dev --output-dir /tmp/p5-eval
python -m projects.document_rag.evaluate holdout --output-dir /tmp/p5-eval
cmp projects/document_rag/data/dev-report.json /tmp/p5-eval/dev-report.json
cmp projects/document_rag/data/holdout-report.json /tmp/p5-eval/holdout-report.json
```

Порядок выбора зафиксирован в `selection.json`: максимальный dev Recall@6, затем MRR, затем порядок FTS/dense/hybrid/rerank. Для ответа выбрана exact dense. Dense, hybrid и rerank получили одинаковый recall и MRR на dev, поэтому tie-break сохранил dense. Выбор закоммичен до прогона holdout. Данные, qrels, настройки и конфигурация не менялись на holdout.

Метрики имеют отдельные знаменатели. Recall и RR получают null при пустом qrels. Precision делится на фактически возвращённые уникальные document/version в пределах шести, при пустом результате null. Сводка указывает число определённых cases. Support, текущая цитата, abstention/conflict и task correctness считаются отдельно. Счётчики forbidden/stale и отрицательных support controls блокируют успешный результат независимо от средних метрик. Скрипт использует отдельный ACL-oracle по манифесту fixtures.

Корпус и энкодер учебные. Вектор кодирует наличие токенов из малого трёхъязычного словаря. Генератор извлекает документированные строки Fact из переданного контекста. Он никогда не получает qrels или gold labels. Измеренные задержки отдельно от детерминированного JSON записаны как loopback p50/p95/N. Способ измерения не претендует на холодный cache или производительность рабочего сервиса.

[Конфигурация](data/selection.json), [dev](data/dev-report.json), [holdout](data/holdout-report.json), [dev timings](data/dev-timings.json), [holdout timings](data/holdout-timings.json).
