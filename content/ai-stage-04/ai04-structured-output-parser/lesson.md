# Как разобрать ответ Structured Outputs

Провайдер вернул объект поездки, номер модели и статус генерации. Запрос также может закончиться отказом или оборваться на середине. Адаптер сохраняет смысл этих различий для backend.

## Учебные цели

- Объяснить область гарантий выдачи по схеме.
- Прочитать typed parsed object и явные статусы.
- Разнести model ID, prompt version и schema version.

## Теория

**Structured Outputs** ограничивают форму успешного ответа по заявленной JSON Schema. В Responses API Python SDK метод responses.parse с аргументом text_format строит схему из Pydantic и десериализует текст ответа в типизированный объект. В проверенной версии 3.57.0 его извлекает свойство output_parsed. Статус генерации и части сообщения читаются независимо. Отказ имеет собственный content item refusal, а incomplete означает незавершённый ответ, например по лимиту вывода. Одно только значение None у output_parsed не объясняет причину.

Для внешней схемы выбери закрытые объекты с обязательными полями и явным null для неизвестного. Вложенный trip отделяет поля поездки от остальных данных. Домен проверяет календарь и интервал. Факт сверяют с исходным запросом отдельно. Если в запросе стоит «Бишкек», schema validator пропустит корректно написанное «Алматы».

**Provenance** — происхождение результата. Model обозначает выбранную версию модели, prompt_version — набор инструкций, schema_version — контракт результата. Допустимые сочетания задаёт сервер. В лаборатории wire revision передаётся в scripted fake, а ожидаемая версия приходит из прикладной конфигурации. В реальном адаптере schema_version можно фиксировать той же конфигурацией, которая послала схему.

Разбор typed результата иногда завершается исключением SDK до получения объекта. SDK-тест покрывает этот путь отдельно. Не вырезай подстроку между первой и последней скобкой. Ответ может содержать вложенный JSON, а сама строка может содержать скобки. В лаборатории Pydantic проверяет целую структуру, для SDK используется закрытый MockTransport.

## Модель понимания

Сначала читаем envelope и явные refusal/incomplete. Только completed пробует проверить provenance и разобрать payload. Не переносим случайные фрагменты и сырые исключения в прикладной DTO.

## Что нужно знать на Junior

Раздели десериализацию и доменные правила. Fake демонстрирует порядок обработки. SDK mock подтверждает транспортный контракт, выводы о живой модели требуют отдельной оценки.

## Примеры кода

```python
from pydantic import BaseModel, StrictInt, ValidationError
class Reading(BaseModel):
    count: StrictInt | None
assert Reading.model_validate({"count":None}).count is None
assert Reading.model_validate({"count":0}).count == 0
try:
    Reading.model_validate({"count":"0"})
except ValidationError:
    print("Строка отклонена, null остаётся неизвестным")
else:
    raise AssertionError("strict int accepted a string")
```

Вывод подтверждает отказ на строке. Целый ноль и неизвестное представлены разными значениями. Это пример одного свойства схемы без обращения к провайдеру.

## Типичные ошибки

- Искать JSON подстрокой.
- Принимать incomplete с удачным фрагментом.
- Передавать константу schema revision из сгенерированного текста.
- Считать parsed фактами.

## Практика

Первый ответ имеет completed и part `refusal`. Второй incomplete, но содержит целый parsed. Какая структура может попасть в домен?

<details>
<summary>Сверить ход рассуждения</summary>

Refusal и incomplete оба остаются самостоятельными статусами без trip. Только completed без refusal может пройти shape и revision.
</details>

## Вопросы с собеседований

1. Зачем отдельный refusal?
2. Что доказывает output_parsed?

## Хорошие ответы

**Зачем отдельный refusal?**

Отказ не следует объяснять битым JSON или заменять новым фактом. Безопасный статус и provenance.

**Что доказывает output_parsed?**

После парсинга остаются доменная и фактическая проверки. Версия промпта и политика приложения, а схема задаёт форму.

## Критерии хорошего ответа

Объясни порядок состояний и приведи один неверный факт, который проходит форму. Назови владельца применённой схемы.

## Задача

Реализуй `parse_response(response, prompt_version, expected_revision="trip.schema.v1") -> ExtractionResult`. Fake содержит status, model, schema_version, output и output_parsed. В output есть message items с content parts. Part refusal даёт refusal даже при status=incomplete. Затем incomplete даёт неполный исход. Completed нужной версии принимает объект Envelope или вложенный dict. Например, trip с city=Костанай, обеими датами null и guests=1 проходит. Отсутствующий parsed, raw string, extra, несовместимая revision или повреждённый envelope дают invalid. У неуспеха trip отсутствует. Укажи model (None при повреждении ID), переданный prompt_version и ожидаемую schema_version. Check использует другие города, версии, типы и порядок вложенных элементов.

## Шпаргалка

### Краткий конспект

Прочитай status, отказ и typed payload по документированным полям. Версии model/prompt/schema фиксируй отдельно. Completed без parsed — invalid. Даты и факты проверяются после разбора.

1. У чего приоритет перед parsed?
2. Что хранит provenance?
3. По чему проверяют факты?

<details>
<summary>Сверить конспект</summary>

У явных failure states. Provenance связывает результат с моделью, промптом и схемой. Факты требуют отдельного источника.
</details>

## Источники

- OpenAI Structured Outputs, schema and refusals. Responses API и ограниченное подмножество JSON Schema. Проверено 2026-11-22. [A2](https://developers.openai.com/api/docs/guides/structured-outputs)
- OpenAI Responses, инструкции и вход. Формат Responses API. Проверено 2026-11-22. [A1](https://developers.openai.com/api/docs/guides/text)
- Pydantic Validators. Model validator и post-validation. Проверено 2026-11-22. [VALIDATORS](https://docs.pydantic.dev/latest/concepts/validators/)
