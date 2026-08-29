# Filesystem navigation

> [!IMPORTANT]
> **P1 · вероятность на интервью: high · 10 минут.** Linux basics явно встречались в 5/18 и часто подразумеваются для backend debugging.

## Learning objectives

После урока ты сможешь:

- восстановить mental model темы **Filesystem navigation**, а не только запомнить термин;
- прочитать и изменить короткий пример для `pwd`;
- распознать характерную ошибку и объяснить причину;
- дать реалистичный ответ уровня Junior и выдержать follow-up.

## Theory

### Что это

Тема **Filesystem navigation** описывает отдельный контракт backend-разработки.

### Как работает

Разложи механизм на вход, изменение состояния, наблюдаемый результат и специфичный для темы failure path.

**pwd.** `pwd` связывает shell command с конкретным process, file, permission, environment или network state.

**ls.** `ls` связывает shell command с конкретным process, file, permission, environment или network state.

**cd.** `cd` связывает shell command с конкретным process, file, permission, environment или network state.

**relative/absolute paths.** `relative/absolute paths` связывает shell command с конкретным process, file, permission, environment или network state.


### Важный нюанс / limitation

Граница Junior: уверенно объясняй `pwd` и `ls` на одном проверяемом примере; редкие внутренние детали сначала ищи в официальной документации.

### Где используется в backend

В backend эта тема важна в том месте, где применяется `pwd`; проверяй именно наблюдаемый contract, а не название инструмента.

## Mental model

Процесс видит filesystem, env, user permissions, descriptors и network namespace.

Используй эту модель как короткую опору, затем проверяй её конкретным примером из Theory.

## Что нужно знать на Junior

### Обязательно

- pwd
- ls
- cd
- relative/absolute paths

### Полезно

- связать Filesystem navigation с коротким рабочим примером

### Можно не учить глубоко

- implementation internals, не влияющие на Junior-код и типичный interview follow-up

## Code examples

### Filesystem navigation: отдельный пример

```bash
# 23.1 · Filesystem navigation
# Focus: pwd, ls, cd, relative/absolute paths
printf '%s
' 's23_filesystem_navigation'
```

Свяжи command с конкретным process, file, permission, environment или port symptom.

## Common mistakes

### Ошибка 1

Игнорировать ограничение механизма и проверять только happy path.

## Practice

**A · Prediction/reasoning.** Предскажи результат минимального примера для `pwd` до запуска.

**B · Find the bug.** Найди нарушение `ls` и объясни конкретное последствие.

**E · Interview explanation.** Дай ответ про Filesystem navigation за 60 секунд: определение, механизм, пример, ограничение.

## Interview questions

### Основной вопрос

Что такое Filesystem navigation и какой механизм здесь важно понимать Junior-разработчику?

### Follow-up

Какое ограничение или типичная ошибка относится именно к теме Filesystem navigation?

Сначала ответь вслух или запиши 3–5 предложений. Готовый ответ находится в следующем раскрывающемся разделе.

## Good answers

### Короткий ответ

Filesystem navigation: это отдельный технический контракт

### Нормальный Junior answer

> Filesystem navigation — тема, в которой я сначала фиксирую `pwd`, затем объясняю `ls` на коротком примере. Ключевой механизм: вход преобразуется в наблюдаемый результат по явному контракту Главная практическая ошибка — игнорировать ограничение механизма

### Углубление / follow-up

**Какое ограничение или типичная ошибка относится именно к теме Filesystem navigation?**

Нужно назвать конкретный failure path и способ его проверить.

## Expected answer rubric

### Must mention

- pwd
- ls
- cd
- relative/absolute paths

### Good additions

- один короткий пример с результатом;
- одно ограничение или характерная ошибка именно этой темы;
- backend-пример только при естественной связи.

### Common wrong answers

- Игнорировать ограничение механизма и проверять только happy path.
- пересказ одного определения без механизма или примера.

### Follow-up

- Какое ограничение или типичная ошибка относится именно к теме Filesystem navigation?

## Задача

Сделай короткую письменную практику по теме **Filesystem navigation**: реши один пункт из раздела Practice, затем сравни своё объяснение с хорошим Junior answer. Для этого урока автоматические hidden tests не требуются.

## Cheat sheet

Перед собеседованием запомни:

- **Что это:** Filesystem navigation: это отдельный технический контракт
- **Механизм:** Процесс видит filesystem, env, user permissions, descriptors и network namespace.
- **Ограничение:** Игнорировать ограничение механизма и проверять только happy path.
- **Junior depth:** знать обязательные пункты выше; implementation internals можно уточнить по документации.

## Sources

Материал написан своими словами и сверён с актуальными разделами официальной документации:

- [GNU Coreutils manual](https://www.gnu.org/software/coreutils/manual/coreutils.html)
- [Bash manual](https://www.gnu.org/software/bash/manual/)

Последняя проверка версий: **2026-08-27**.
