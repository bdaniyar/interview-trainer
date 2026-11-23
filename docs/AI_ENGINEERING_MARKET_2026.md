# AI Engineering и рынок труда · ноябрь 2026

## 1. Вывод

Для Python backend-разработчика ближайший профиль — **Applied AI Engineer / AI Backend Engineer**. Умение довести LLM-функцию до рабочего сервиса связывает уже знакомые API, схемы, PostgreSQL, очереди и тесты с новыми задачами. На входе полезны стажировки по интеграции LLM, а также обычные Python Backend позиции с AI-функциями. Примеры в выборке показывают разные планки от учебного проекта до опыта эксплуатации. [ITX](https://astanahub.com/ru/vacancy/7180), [Sia](https://jobs.smartrecruiters.com/sia/744000158718389), [EPAM](https://careers.epam.com/en/vacancy/bltdae092523b87c979).

Из 30 отобранных вакансий 28 упоминают Python, включая вакансии с альтернативным языком, 23 — RAG, 21 — оценку качества или регрессий. Пять из семи входных позиций упоминают RAG. Для основной программы приоритет получают прямой вызов инструментов, RAG с доступом по владельцу, проверка качества, восстановление после сбоя и воспроизводимая поставка. LangChain, MCP и LangGraph вводятся на уже понятных контрактах. Qdrant добавляется как сравнительный практикум; основной векторный проект остаётся на PostgreSQL и pgvector.

Все 29 опубликованных AI-уроков и 370 уроков Backend остаются в прежнем составе. План содержит 72 урока, 10 этапов, 9 проектов. Изменения распределены внутри AI5–AI10 и P3–P9. Конкретные требования для реализации включены в [учебный план](AI_CURRICULUM_PLAN.md#рыночная-сверка-112026).

## 2. Дата, охват и методика

Срез сделан **23.11.2026, Asia/Almaty**. Казахстанская часть охватывает Алматы, Астану и вакансии с явной привязкой к Казахстану. Международная часть включает Европу с Великобританией, США, одну вакансию с пометкой Worldwide и одну с международным наймом без списка стран. Работодатели представляют продуктовые IT-компании, банки и финтех, индустриальные продукты, консалтинг и аутсорсинг.

1. Искали AI Engineer, Applied/Generative AI Engineer, AI Software/Backend/Integration Engineer, LLM Engineer, junior/intern, ML Engineer, AI Platform и Forward Deployed Engineer. Сочетали названия с `Almaty`, `Astana`, `Казахстан`, `RAG`, `Python`, `early career`, `US remote` и `worldwide`. Просматривали Astana Hub, выдачу HeadHunter, LinkedIn, страницы работодателей, их ATS, а также публичные агрегаторы и указатели на профессиональные публикации.
2. Включали индивидуальную карточку с читаемыми задачами и требованиями. Ключ дедупликации — работодатель, роль и совпадающий объём работы; ID заявки и локация помогают различить роли. Повторы Documentolog, Itransition, Freedom и KOZ сведены к одной записи на роль. Географические копии одинаковой роли Graphcore не суммировались. У Kimchi две самостоятельные позиции с разными обязанностями и ID.
3. `Открыта` означает, что работодатель, его ATS или его объявление на Astana Hub показывает отклик без признака закрытия на дату проверки. `Архив` включает явный архив и истёкший опубликованный дедлайн. `Не подтверждена` означает, что требования прочитаны в копии, а исходный отклик не проверен. Отклики не отправлялись. Дефис в дате означает, что точная дата публикации отсутствует в проверенном тексте. Даты копий помечены.
4. `Вход` объединяет вакансии с явным Junior, Intern или Graduate. Сюда входят прикладные стажировки и исследовательская PhD-стажировка I05. Middle/Senior определялись по названию работодателя, а Senior также назначался при явном минимуме 5+ лет применимого опыта. Диапазоны площадки 1–3 и 3–6 лет сами по себе уровня не задают. Стаж, требования к образованию, язык и право на работу оцениваются отдельно.
5. В таблице подсчётов каждое объявление даёт максимум одно попадание на строку. Для этой строки приоритет поля `требования → преимущества → задачи/стек`, поэтому три числа суммируются в общее. Стек, приведённый через «или» и «например», учитывается как именованная альтернатива. Это подсчёт упоминаний, обязательность конкретного бренда видна в исходной выдержке. Технологии кодировались по названиям и указанным в строке синонимам. Для групп объединялись связанные термины: backend/API/БД; LLM API и structured output/tool calling; retrieval/RAG и vector DB; агенты и инструменты; eval/tracing/latency; Docker/CI/cloud; обучение и serving. Coding assistants учитывались отдельно от навыка работы над агентным продуктом. Общие unit tests сами по себе не засчитывались как AI eval.

**Пределы среза.** Это целевая выборка вакансий под программу, без случайного отбора, весов или оценки доли рынка. Срез читает доступные в ноябре карточки. Первую публикацию I08 и I09 ATS относит к 2025 году. Открытая форма не показывает очередность найма или наличие свободного места на конкретную дату. Запросы с RAG и агентами повышают частоту этих тем. По части HH URL инструмент получил отказ, LinkedIn ограничил выдачу, а Ashby для Sierra потребовал JavaScript. Полный текст копии и статус исходного объявления в таком случае имеют разное качество. Перепосты с пустыми описаниями, Telegram-сводки без исходной карточки и объявления о продаже курсов исключены. Нулевое число означает отсутствие упоминания в закодированных выдержках. Работодатели редко перечисляют все библиотеки, а статус вакансии меняется.

Для контекста hh.kz сообщает, что в III квартале 2026 года 38,7% всех вакансий платформы в Казахстане пришлись на Алматы и 21,9% на Астану. Это статистика площадки по всем профессиям. Antal Kazakhstan опросил 3 923 специалистов и руководителей об условиях труда и использовании AI. Stanford AI Index 2026, гл. 4, отдельно анализирует объявления на основе Lightcast за 2025 год. Эти источники описывают общий фон, а прямые сравнения в этом отчёте привязаны к 30 карточкам. [hh.kz, 14.10.2026](https://hh.kz/article/34483), [Antal, 09.10.2026](https://antalkazakhstan.kz/en/antal-kazakhstan-key-findings-from-the-annual-labour-market-and-salary-survey/), [Stanford HAI, Economy](https://hai.stanford.edu/ai-index/2026-ai-index-report/economy).

## 3. Вакансии

**Каждая строка проверена 23.11.2026.** Первые две таблицы соединяются по ID. Требования ниже пересказаны по видимому тексту, включая различие между навыком кандидата и будущей задачей.

| ID | Работодатель · точное название | География и формат | Доступ из-за рубежа | Уровень · опыт | Публикация · статус | Источник и ограничение |
| --- | --- | --- | --- | --- | --- | --- |
| K01 | ITX (Айтикс) · AI-разработчик (Python) | Алматы, удалённо | Международный найм не указан | Вход · Без стажа, старшие курсы или выпускник | — · Открыта | Astana Hub, объявление работодателя. [Карточка](https://astanahub.com/ru/vacancy/7180) |
| K02 | АЛАТАУ ИННОВАЦИЯ · Стажёр ML-инженер (NLP/LLM) | Алматы, удалённо | Международный найм не указан | Вход · Учебные проекты достаточны, коммерческий стаж не назван | — · Открыта | Astana Hub, стек обучения в колонке задач. [Карточка](https://astanahub.com/ru/vacancy/7025) |
| K03 | iKapitalist Ltd · AI Engineer/AI-инженер | Астана, формат не уточнён | Удалённый найм не указан | Не указан · 1–3 года по карточке | — · Открыта | Astana Hub, объявление работодателя. [Карточка](https://astanahub.com/ru/vacancy/6893) |
| K04 | ASTANA CLOUD LTD. · LLM-инженер | Астана, формат не уточнён | Удалённый найм не указан | Не указан · 3–6 лет по карточке | — · Открыта | Astana Hub, использована одна карточка. [Карточка](https://astanahub.com/ru/vacancy/7162) |
| K05 | WhiteList & Co Ltd. · Инженер больших языковых моделей (LLM Engineer) | Астана, гибкий график, формат не уточнён | Удалённый найм не указан | Не указан · 3–6 лет по карточке | — · Открыта | Astana Hub, объявление работодателя. [Карточка](https://astanahub.com/ru/vacancy/6917) |
| K06 | KAZDEVLAB · AI инженер | Астана, упомянут офис | Удалённый найм не указан | Не указан · 1–3 года по карточке | — · Открыта | Astana Hub, Python прямо не требуется. [Карточка](https://astanahub.com/ru/vacancy/6896) |
| K07 | АКВЕЛОН-КАЗАХСТАН · Middle AI Engineer | Алматы, гибрид или удалённо | Международный найм не указан | Middle · 1–3 года по карточке | — · Открыта | Astana Hub, языки и облака перечислены как варианты. [Карточка](https://astanahub.com/ru/vacancy/7089) |
| K08 | COGNIVE KZ · LLM Специалист | Алматы, удалённо | Международный найм не указан | Не указан · Python от 3 лет, NLP/LLM от 2 лет | — · Открыта | Astana Hub, смешанная application/model роль. [Карточка](https://astanahub.com/ru/vacancy/7037) |
| K09 | Bultech · AI Engineer / Python Backend Developer | Астана, формат не уточнён | Удалённый найм не указан | Не указан · Коммерческий backend от 2 лет | — · Архив | Явный статус Astana Hub, история требований. [Карточка](https://astanahub.com/ru/vacancy/6536) |
| K10 | EPAM · Cloud Native Python Engineer with AI Integration Focus | Казахстан, гибрид, город не указан | Нанимают в Казахстане, мировой remote не заявлен | Не указан · Значимый опыт, число лет не указано | — · Открыта | Карьерная страница EPAM. [Карточка](https://careers.epam.com/en/vacancy/bltdae092523b87c979) |
| K11 | Documentolog · AI Engineer (LLM-агенты, RAG) | Астана, офис | Требуется офис в Астане | Не указан · Python от 2 лет, production LLM от 1 года | — · Не подтверждена | Hirify, текст копии; прямую карточку HH прочитать не удалось, более ранняя копия дедуплицирована. [Карточка](https://hirify.me/jobs/1273616-ai-engineer-llm-rag-python) |
| K12 | Itransition · AI Agent Developer | Астана, удалённо | Публикация для Казахстана, worldwide не указан | Не указан · 1–3 года в копии и выдаче, требуется production опыт | 18.09.2026 (Finder); виден повтор в ноябре · Не подтверждена | Finder + свежая выдача HH; один профиль проекта из всех копий. [Карточка](https://kz.finder.work/vacancy/244069699) |
| K13 | Dreamlab Technologies Ltd · LLM-инженер / AI-разработчик | Астана, офис | Указан офис и трудоустройство по ТК РК | Не указан · Python от 3 лет, production LLM от 1,5 года | — · Не подтверждена | Taylor, видна карточка зеркала. [Карточка](https://taylor.kz/jobs/llm-inzener-ai-razrabotcik-at-dreamlab-technologies-ltd) |
| K14 | Банк ЦентрКредит · Middle+ AI/ML Engineer | Алматы, гибрид по Taylor | Удалённый найм не указан | Middle · 3–6 лет по выдаче HH | — · Не подтверждена | Taylor + выдача HH, используется текст вакансии без оценки зарплаты. [Карточка](https://taylor.kz/jobs/middle-aiml-engineer-at-bank-centrkredit) |
| K15 | Freedom Holding Operations · Senior Python / AI Developer | Алматы, гибрид | Локальный гибрид, мировой remote не заявлен | Senior · Python от 6 лет в описании, рубрика площадки 3–6 | 19.11.2026 (Finder) · Не подтверждена | Полное зеркало Finder, дата зеркала; совпадает с выдачей HH. [Карточка](https://kz.finder.work/vacancy/408363440) |
| K16 | KOZ AI · Forward Deployed Engineer (Python / AI) — KOZ AI | Алматы, офис | Требуется офис в Алматы | Не указан · Рубрика 3–6 лет; описание допускает учебные/личные проекты | 10.11.2026 (Finder) · Не подтверждена | Finder, не объединялась с отдельной Fullstack вакансией; повторные публикации FDE исключены. [Карточка](https://kz.finder.work/vacancy/368823985) |
| K17 | Kaspi.kz · NLP Engineer (AI) | Алматы, офис | Офис, гибрид и удалёнка исключены в копии | Не указан · 1–3 года production NLP/ML; junior только метка агрегатора | — · Не подтверждена | Hirify, заголовок зеркала; выдача HH показывает NLP Engineer. [Карточка](https://hirify.me/jobs/1419110-nlp-engineer-ai-ml) |
| I01 | Sia · Junior Forward Deployed Engineer | Амстердам, Нидерланды, гибрид | Work permit не предоставляют, гибрид в Нидерландах | Вход · 0–2 года, включая практику/учёбу; Master’s | 23.11.2026 (SmartRecruiters API) · Открыта | ATS работодателя SmartRecruiters. [Карточка](https://jobs.smartrecruiters.com/sia/744000158718389) |
| I02 | M3 USA · AI Engineering Intern (Remote) | Форт-Вашингтон, Пенсильвания, США, удалённо | Worldwide и работа из РК не заявлены | Вход · Студент или недавний выпускник, достаточно учебного проекта | 08.09.2026 (SmartRecruiters API) · Открыта | ATS работодателя, требования к RAG отсутствуют. [Карточка](https://jobs.smartrecruiters.com/m3usa/744000148244649-ai-engineering-intern-remote-) |
| I03 | Sierra · Software Engineer Intern, Agent (London 2027) | Лондон, Великобритания, in-person по описанию | Лондон; разрешение на работу и sponsorship не уточнены в просмотренном тексте | Вход · Студент, коммерческие годы не указаны | 20.10.2026 (зеркало) · Открыта | Карьерная доска Sierra содержит позицию; Ashby требует JS, текст сверен по индексу/зеркалу. [Карточка](https://jobs.ashbyhq.com/Sierra/7af8aa4e-ba84-49ba-bc53-19358f4564ff) |
| I04 | Google · Forward Deployed Engineering Intern, BS/MS, Summer 2027 | Саннивейл, Нью-Йорк, Рестон, требуется присутствие в США | Нужно находиться в США во время программы | Вход · BS/MS, целевой предпоследний курс, численного стажа нет, требуется опыт AI delivery | —; дедлайн 20.11.2026 · Архив | Google Careers, срок подачи прошёл при доступной странице. [Карточка](https://www.google.com/about/careers/applications/jobs/results/75665705386549958-forward-deployed-engineering-intern-bsms-summer-2027) |
| I05 | Graphcore · AI Technology PhD Research Internship | Бристоль, Кембридж или Лондон, Великобритания; офис упомянут | UK work rights, спонсорства нет | Вход · PhD по AI/ML, промышленный стаж не требуется | 20.10.2026 (Greenhouse first_published) · Открыта | ATS работодателя Greenhouse; исследовательская стажировка. [Карточка](https://job-boards.greenhouse.io/graphcore/jobs/8894738002) |
| I06 | Graphcore · AI Research Engineer | Лондон, Великобритания, формат не уточнён | Требуется право работы в UK, спонсорства нет | Не указан · Master’s/PhD или эквивалент, лет не задано | 14.07.2026 (Greenhouse first_published) · Открыта | ATS работодателя; использована только лондонская карточка из географических дублей. [Карточка](https://job-boards.greenhouse.io/graphcore/jobs/8632581002) |
| I07 | Capco · Mid Level AI Engineer | Орландо, США, гибрид | Локальный гибрид, форма спрашивает о праве работы | Middle · 2–3 года в software/AI engineering | 04.09.2026 (Greenhouse first_published) · Открыта | ATS работодателя Greenhouse. [Карточка](https://job-boards.greenhouse.io/capco/jobs/8178266) |
| I08 | CoreStory · AI Engineer | США, удалённо | Явно Remote US | Senior · 7+ лет engineering, из них 3+ в AI/ML/NLP | 18.11.2025 (Greenhouse first_published) · Открыта | ATS работодателя, Senior по правилу порога; в заголовке грейда нет. [Карточка](https://job-boards.greenhouse.io/corestory/jobs/4984207007) |
| I09 | apiphani · Senior Software Engineer (AI / LLMs) | Удалённо, города и перечень стран не указаны | Явно есть найм за пределами США через EoR, Казахстан не назван | Senior · 6+ лет production backend | 23.10.2025 (Greenhouse first_published) · Открыта | ATS работодателя, международность по условиям найма. [Карточка](https://job-boards.greenhouse.io/apiphani/jobs/4893893007) |
| I10 | Appsilon · Applied AI Engineer | Worldwide, полностью удалённо | Карточка явно Worldwide, B2B, Казахстан отдельно не перечислен | Не указан · Production agents, число лет не задано | — · Открыта | ATS работодателя Teamtailor. [Карточка](https://appsilon-1739358905.teamtailor.com/jobs/7750183-applied-ai-engineer) |
| I11 | Kimchi / Cast AI · Senior ML Engineer \| Kimchi (Inference Stack Optimization) | Remote-first, список стран Европы + UK | Перечень стран Europe/UK, Казахстан не указан | Senior · 5+ лет ML systems | 15.10.2026 (Greenhouse first_published) · Открыта | ATS работодателя; в точном заголовке разделитель вертикальная черта. [Карточка](https://job-boards.greenhouse.io/kimchi/jobs/4451244009) |
| I12 | Kimchi / Cast AI · Senior Applied ML Engineer \| Kimchi (Model Router) | Remote-first, ЕС/UK по списку карточки | Перечень стран/ЕС и UK, Казахстан не указан | Senior · 5+ лет applied ML/research | 15.10.2026 (Greenhouse first_published) · Открыта | ATS работодателя, самостоятельная заявка; в точном заголовке разделитель вертикальная черта. [Карточка](https://job-boards.greenhouse.io/kimchi/jobs/4451281009) |
| I13 | Novartis · Forward Deployed Engineer – AWS Stack | Барселона, Испания, гибрид | Требуется гибрид в Барселоне | Не указан · Существенный production/delivery опыт, численного минимума нет | 13.11.2026 · Открыта | Карьерная страница, REQ-10090384. [Карточка](https://www.novartis.com/cz-cs/careers/career-search/job/details/req-10090384-forward-deployed-engineer-aws-stack) |

### Требования, предпочтения и задачи

| ID | Требования и допустимые альтернативы | Преимущества | Задачи или рабочий стек |
| --- | --- | --- | --- |
| K01 | Python, HTTPX или requests, JSON, API, LLM, embeddings, RAG, русский, чтение документации на английском | Git, FastAPI, LangChain, казахский | OpenAI / Anthropic API, RAG-прототипы по документам, тестирование и eval ответов |
| K02 | Python, Git, основы ML/NLP/LLM, знакомство с NumPy, pandas, PyTorch | — | RAG, prompt experiments, локальный inference и eval; знакомство со стеком Hugging Face, LangChain, Qdrant, Docker, FastAPI и tool calling |
| K03 | Python, LLM, API, JSON, Git, SQL, RAG, vector search, eval, конфиденциальность | — | Извлечение из документов, интеграция LLM API, поиск по внутренним данным и сопровождение |
| K04 | Python, REST, LLM API (OpenAI, Claude, локальные модели), RAG (LangChain/LlamaIndex, Qdrant/Pinecone/pgvector), n8n/Make/Power Automate | — | Корпоративные ассистенты, документы, Service Desk, RBAC, eval, коннекторы 1С, CRM, ERP и Microsoft 365 |
| K05 | Python, LLM API, prompts, RAG, embeddings, semantic search, REST, БД, Git | — | OpenAI / Claude / Gemini, ассистенты, vector search, eval, latency/cost |
| K06 | LLM, API, RAG, embeddings, eval, Docker, Git, контекст и tools | — | Агенты и tool calling для интеграций, локальный inference, измерение галлюцинаций и наблюдаемость |
| K07 | Python или TypeScript/JavaScript, API, БД, Git, CI/CD, RAG, tool calling, MCP, state/recovery, eval, approval, AWS/Azure/GCP | — | Клиентские интеграции, оркестрация субагентов, автоматизированные тесты, развертывание, ACL |
| K08 | Python, ML, Transformers, LangChain и LlamaIndex, RAG, fine-tuning, Git, CI/CD | PyTorch предпочтителен в работе с нейросетями; Docker, MLflow | Адаптация моделей, оптимизация inference, агенты и интеграция в продукты |
| K09 | Python, async, FastAPI, Pydantic, PostgreSQL, REST, OAuth/JWT, очереди, дедупликация, Git, Docker, LLM API, RAG, embeddings, structured output, tool calling, eval, тестирование | — | Агенты для CRM и поддержки, фоновые события, оптимизация latency/cost, релизы |
| K10 | Python, cloud (AWS/Azure/GCP), LLM, RAG | Kubernetes, Docker и микросервисы | Интеграция AI в обычные Python-проекты; Django/Flask/FastAPI как варианты реализации |
| K11 | Python, asyncio, FastAPI, Pydantic, SQLAlchemy, pytest, function calling, RAG, агентный framework (LangGraph/LangChain/ADK/CrewAI), SSE или WebSocket, PostgreSQL, Redis, Docker, Git | MCP, Langfuse, RAGAS, real-time/queues, vLLM, LoRA, классический ML | Корпоративный поиск, OpenAI-compatible API, self-hosted модели, eval, traces, маскирование данных, защита от prompt injection; RU/KK в более ранней копии |
| K12 | Python, structured output, tool calling, MCP или аналог, eval и regression, traces, управление стоимостью, permission boundaries, retrieval кода | Java/C#, тестовая автоматизация, игровой домен | Интеграция агентного сервиса с Java-тестами; queues/state, индексирование исходников, review gate |
| K13 | Python, FastAPI, Pydantic, async, SQL, Docker, фоновые задачи, OpenAI-compatible API, structured output, production RAG или агент, eval | Казахский или low-resource NLP/LoRA, vLLM/SGLang, quantization, Qdrant, Elasticsearch, Neo4j, Langfuse, MCP, OCR | Document pipelines, LangGraph, dense + BM25, reranking, citations, eval precision/recall, on-prem |
| K14 | Python, PyTorch, Hugging Face, fine-tuning, GPU inference, RAG, embeddings, vector search, agent context | LangGraph, LangChain, high-load | Поддерживать банковские AI-сервисы, обучать/развёртывать модели, улучшать скорость, качество и стоимость |
| K15 | Python, FastAPI/Flask/Django, PostgreSQL, Redis, Docker, REST, RAG, embeddings, vLLM или Ollama, AI coding tools | — | Backend, ассистенты, LLM API и локальный inference, микросервисы |
| K16 | Python, техническая подготовка, проектная защита, коммуникация с пользователями | AI agents, LLM applications, API/SQL, Docker/cloud, eval и monitoring | Доводить клиентские интеграции от понимания задачи до пилота, сопровождения и повторного использования компонентов |
| K17 | Python, SQL, BERT/Sentence-BERT/T5/FastText/Word2Vec или аналог, LLM, RAG, AI agents, Docker, Kubernetes, CI/CD и анализ качества | — | Подготовка данных, обучение/выкладка NLP-моделей, мониторинг, A/B и продуктовые метрики |
| I01 | Python, API, LLM, RAG, базовые agents, eval/tests; Dutch и English | LangChain/LlamaIndex, OpenAI/Anthropic SDK, cloud AWS/Azure/GCP, vector DB/embeddings, prompt versioning и monitoring; German | Клиентский discovery, prototyping и deployment; pgvector назван как инструмент практики |
| I02 | Python или TypeScript/аналог, Git, AI coding agent, чтение документации | Web development, устройство LLM, проект с пользователями | Внутренний сервис от общения с пользователем до демо и сопровождения |
| I03 | BS/MS CS/смежная область, технические задачи и коммуникация; выпуск 12.2027–06.2028 | Production AI/LLM, eval frameworks, agent tooling, RAG, prompting, React/TypeScript/Go | Работа над клиентскими production-агентами, тестирование и внедрение |
| I04 | Python или аналог, cloud (GCP как пример), vector databases, RAG | LangGraph/CrewAI/ADK и multi-agent, tracing, token/cost metrics | Клиентские интеграции, tool/agent workflows, MCP, eval, latency и наблюдаемость |
| I05 | Python или C++, PyTorch как пример ML framework, дизайн экспериментов | — | Исследовать ML-алгоритмы и аппаратные ограничения, воспроизводить эксперименты |
| I06 | Python, PyTorch или JAX, C++/CUDA/Triton, обучение/инференс, компиляция и эксперименты | Математика, submissions в научные издания | Эксперименты и eval для аппаратной платформы, доклады и совместная работа с research и silicon инженерами |
| I07 | Python, REST, RAG, LLM APIs (OpenAI/Anthropic/Gemini), Git, CI/CD, тесты, AWS/Azure/GCP, vector DB (Pinecone/Weaviate/Chroma/Qdrant/FAISS) | LangChain/LangGraph/CrewAI/AutoGen, MCP, LangSmith/Langfuse, Docker/Kubernetes | AI-сервисы и tool calling для финансовых клиентов, интеграция корпоративных знаний |
| I08 | Python, FastAPI/pandas/NumPy как примеры, LLM API, RAG, embeddings, tool calling, LangChain/LlamaIndex, vector DB (Pinecone/FAISS/Weaviate и др.) | Docker, Azure/AWS, LangGraph, hybrid retrieval | Индексирование кода, retrieval и генерация, eval, latency/cost; Chroma/Azure Cognitive Search в задачах |
| I09 | Python и TypeScript, AWS ECS/Bedrock/S3, SQL и migrations (PostgreSQL или аналог), Docker, GitHub Actions, CI/CD, RAG, embeddings, Terraform/CDK | LangChain, OpenAI/Anthropic API, agent frameworks, Datadog/Dynatrace | AI platform backend, event pipeline, vector DB (pgvector/Pinecone/Qdrant), мониторинг и деплой |
| I10 | Python/backend, LLM API (OpenAI/Anthropic/Google/open-source), RAG, tool calling, LangChain/LangGraph/CrewAI/AutoGen или аналог, eval, tracing | AWS/Azure/GCP, Docker/Kubernetes, pgvector/Qdrant/Pinecone/Weaviate, LangSmith/Langfuse, scikit-learn/PyTorch | Разработка и эксплуатация AI-агентов в корпоративной фарме |
| I11 | Python, vLLM/SGLang/TensorRT-LLM, quantization, multi-GPU/multi-node inference | LLM routing eval, calibration, A/B drift | Serving stack PyTorch/Kubernetes, OpenTelemetry/Grafana/Prometheus/GitLab CI, throughput, TTFT, профилирование и KV cache |
| I12 | Python, SQL, eval, production ranking/decision models, serving и latency | Model routing, calibration, online A/B/drift | PyTorch, ClickHouse, OpenAI-/Anthropic-compatible API, GitLab CI, оценки quality/cost/TTFT для выбора модели |
| I13 | Python или Java, LLM/RAG/tool calling как варианты опыта, AWS Bedrock/SageMaker/OpenSearch/Lambda/API Gateway/S3/DynamoDB, API интеграции | AWS certification, Azure AI, Claude, enterprise governance | Клиентский discovery, безопасное развёртывание и adoption сервисов в регулируемой среде |

Дополнительные источники для сверки сложных случаев. [Documentolog в выдаче HH](https://hh.kz/vacancy/138010571) и [ранняя копия с RU/KK](https://astana.cataloxy-kz.ru/rabota/vacancy1067364505_ai-engineer-llm-agenty-rag.htm), [ноябрьский повтор Itransition](https://dreamjob.ru/employers/57097/vakansii), [карточка Freedom на HH](https://hh.kz/vacancy/139640794), [KOZ AI на HH](https://hh.kz/vacancy/139305567), [карточка Kaspi на HH](https://hh.kz/vacancy/139535640), [открытые роли Sierra](https://sierra.ai/careers) и [читаемая копия текста](https://jobs.evolc.com/job/sierra-software-engineer-intern-agent-london-2027-riwvi). Прямые ссылки HH здесь служат ключами происхождения, поскольку инструмент не смог получить эти карточки. Даты Greenhouse взяты из поля `first_published` публичного Job Board API, даты SmartRecruiters — из `releasedDate` публичного Postings API. Времена пересчитаны в Asia/Almaty. [Пример ответа Greenhouse I08](https://boards-api.greenhouse.io/v1/boards/corestory/jobs/4984207007), [SmartRecruiters I01](https://api.smartrecruiters.com/v1/companies/sia/postings/744000158718389), [SmartRecruiters I02](https://api.smartrecruiters.com/v1/companies/m3usa/postings/744000148244649).

## 4. Частоты и сравнение

В Казахстане 8/17 объявлений привязаны к Алматы, 8/17 к Астане и 1/17 к стране без города. В международной выборке 7/13 относятся к Европе и UK, 4/13 к США, 1/13 к Worldwide и 1/13 к международному remote с неуточнённым списком стран. Статус и уровень ниже посчитаны отдельно. Колонка «Открыта / 21» позволяет сравнить частоту признака после исключения архивов и объявлений с неопределённым статусом.

| Выборка | Всего | Вход | Middle | Senior | Грейд не указан | Открыта | Архив | Статус не подтверждён |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Казахстан | 17 | 2 | 2 | 1 | 12 | 9 | 1 | 7 |
| Международные | 13 | 5 | 1 | 4 | 3 | 12 | 1 | 0 |
| Всего | 30 | 7 | 3 | 5 | 15 | 21 | 2 | 7 |

| Технология или группа | Треб. / плюс / задачи | Всего / 30 | KZ / 17 | Intl / 13 | Вход / 7 | Senior / 5 | Открыта / 21 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Backend/API и данные | 16/1/3 | 20 | 13 | 7 | 3 | 4 | 15 |
| Прикладная интеграция LLM | 11/2/6 | 19 | 12 | 7 | 3 | 4 | 14 |
| Retrieval / RAG | 21/1/1 | 23 | 15 | 8 | 5 | 3 | 16 |
| Агенты и исполнение инструментов | 11/5/3 | 19 | 11 | 8 | 4 | 2 | 11 |
| Оценка и операционные измерения | 9/4/9 | 22 | 13 | 9 | 5 | 4 | 15 |
| Deployment / инфраструктура | 13/4/3 | 20 | 11 | 9 | 3 | 5 | 13 |
| Обучение / serving моделей | 7/3/1 | 11 | 6 | 5 | 2 | 3 | 7 |
| Python | 28/0/0 | 28 | 16 | 12 | 6 | 5 | 19 |
| Async Python / asyncio | 3/0/0 | 3 | 3 | 0 | 0 | 0 | 0 |
| FastAPI | 5/1/2 | 8 | 7 | 1 | 2 | 2 | 4 |
| Pydantic | 3/0/0 | 3 | 3 | 0 | 0 | 0 | 0 |
| SQLAlchemy | 1/0/0 | 1 | 1 | 0 | 0 | 0 | 0 |
| SQL | 5/1/0 | 6 | 4 | 2 | 0 | 2 | 3 |
| PostgreSQL | 4/0/0 | 4 | 3 | 1 | 0 | 2 | 1 |
| Redis | 2/0/0 | 2 | 2 | 0 | 0 | 1 | 0 |
| Celery | 0/0/0 | 0 | 0 | 0 | 0 | 0 | 0 |
| REST | 5/0/0 | 5 | 4 | 1 | 0 | 1 | 3 |
| HTTPX | 1/0/0 | 1 | 1 | 0 | 1 | 0 | 1 |
| pytest | 1/0/0 | 1 | 1 | 0 | 0 | 0 | 0 |
| Git | 10/1/0 | 11 | 9 | 2 | 3 | 0 | 9 |
| CI/CD или именованный CI | 5/0/2 | 7 | 3 | 4 | 0 | 3 | 6 |
| GitHub Actions | 1/0/0 | 1 | 0 | 1 | 0 | 1 | 1 |
| Docker | 7/6/1 | 14 | 10 | 4 | 1 | 3 | 8 |
| Docker Compose | 0/0/0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Kubernetes | 1/3/1 | 5 | 2 | 3 | 0 | 1 | 4 |
| OpenAI Responses API (явно) | 0/0/0 | 0 | 0 | 0 | 0 | 0 | 0 |
| OpenAI (включая совместимый API) | 4/2/4 | 10 | 5 | 5 | 2 | 2 | 8 |
| Anthropic / Claude | 3/3/3 | 9 | 3 | 6 | 2 | 2 | 9 |
| Google Gemini | 1/0/1 | 2 | 1 | 1 | 0 | 0 | 2 |
| OpenAI-compatible endpoint | 1/0/2 | 3 | 2 | 1 | 0 | 1 | 1 |
| Streaming / SSE / WebSocket | 1/0/0 | 1 | 1 | 0 | 0 | 0 | 0 |
| Structured output | 3/0/0 | 3 | 3 | 0 | 0 | 0 | 0 |
| Tool calling / tools integration | 7/0/3 | 10 | 6 | 4 | 1 | 1 | 7 |
| Model routing | 0/2/0 | 2 | 0 | 2 | 0 | 2 | 2 |
| RAG | 21/1/1 | 23 | 15 | 8 | 5 | 3 | 16 |
| Embeddings | 8/1/0 | 9 | 6 | 3 | 2 | 3 | 6 |
| pgvector | 1/1/2 | 4 | 1 | 3 | 1 | 1 | 4 |
| Qdrant | 2/2/2 | 6 | 3 | 3 | 1 | 1 | 5 |
| Chroma | 1/0/1 | 2 | 0 | 2 | 0 | 1 | 2 |
| Pinecone | 3/1/1 | 5 | 1 | 4 | 0 | 2 | 5 |
| Weaviate | 2/1/0 | 3 | 0 | 3 | 0 | 1 | 3 |
| Elasticsearch / OpenSearch | 1/1/0 | 2 | 1 | 1 | 0 | 0 | 1 |
| BM25 | 0/0/1 | 1 | 1 | 0 | 0 | 0 | 0 |
| Hybrid retrieval | 0/1/1 | 2 | 1 | 1 | 0 | 1 | 1 |
| RRF | 0/0/0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Reranking | 0/0/1 | 1 | 1 | 0 | 0 | 0 | 0 |
| Citations | 0/0/1 | 1 | 1 | 0 | 0 | 0 | 0 |
| LangChain | 5/5/1 | 11 | 6 | 5 | 3 | 2 | 9 |
| LangGraph | 2/4/1 | 7 | 3 | 4 | 1 | 1 | 3 |
| LlamaIndex | 3/1/0 | 4 | 2 | 2 | 1 | 1 | 4 |
| MCP | 2/3/1 | 6 | 4 | 2 | 1 | 0 | 2 |
| CrewAI | 2/2/0 | 4 | 1 | 3 | 1 | 0 | 2 |
| AutoGen | 1/1/0 | 2 | 0 | 2 | 0 | 0 | 2 |
| Google ADK / ADK | 1/1/0 | 2 | 1 | 1 | 1 | 0 | 0 |
| OpenAI Agents SDK | 0/0/0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Human approval / review gate | 1/0/1 | 2 | 2 | 0 | 0 | 0 | 1 |
| Eval качества / регрессии | 10/3/8 | 21 | 13 | 8 | 5 | 3 | 14 |
| Наблюдаемость / tracing / monitoring | 2/3/5 | 10 | 5 | 5 | 2 | 2 | 5 |
| Latency / cost / TTFT | 2/1/5 | 8 | 4 | 4 | 1 | 3 | 4 |
| LangSmith | 0/2/0 | 2 | 0 | 2 | 0 | 0 | 2 |
| Langfuse | 0/4/0 | 4 | 2 | 2 | 0 | 0 | 2 |
| OpenTelemetry | 0/0/1 | 1 | 0 | 1 | 0 | 1 | 1 |
| RAGAS | 0/1/0 | 1 | 1 | 0 | 0 | 0 | 0 |
| DeepEval | 0/0/0 | 0 | 0 | 0 | 0 | 0 | 0 |
| MLflow | 0/1/0 | 1 | 1 | 0 | 0 | 0 | 1 |
| NumPy | 2/0/0 | 2 | 1 | 1 | 1 | 1 | 2 |
| pandas | 2/0/0 | 2 | 1 | 1 | 1 | 1 | 2 |
| scikit-learn | 0/1/0 | 1 | 0 | 1 | 0 | 0 | 1 |
| PyTorch | 4/2/2 | 8 | 3 | 5 | 2 | 2 | 7 |
| Hugging Face | 1/0/1 | 2 | 2 | 0 | 1 | 0 | 1 |
| Fine-tuning / адаптация моделей | 2/0/0 | 2 | 2 | 0 | 0 | 0 | 1 |
| LoRA / PEFT | 0/2/0 | 2 | 2 | 0 | 0 | 0 | 0 |
| Квантизация | 1/1/0 | 2 | 1 | 1 | 0 | 1 | 1 |
| Ollama | 1/0/0 | 1 | 1 | 0 | 0 | 1 | 0 |
| vLLM | 2/2/0 | 4 | 3 | 1 | 0 | 2 | 1 |
| AWS | 5/3/0 | 8 | 2 | 6 | 1 | 2 | 8 |
| Azure | 3/4/0 | 7 | 2 | 5 | 1 | 1 | 7 |
| GCP | 4/2/0 | 6 | 2 | 4 | 2 | 0 | 5 |
| Secrets / ACL / RBAC / privacy / permissions | 3/1/3 | 7 | 6 | 1 | 0 | 0 | 4 |
| RU/KK, казахский или low-resource NLP | 0/2/1 | 3 | 3 | 0 | 1 | 0 | 1 |

**Казахстан.** RAG упомянут в 15/17 карточках. В этой выборке он привязан к документообороту, корпоративной базе знаний, работе с клиентами и внутренним автоматизациям (K03–K07, K09–K11, K13). Требования включают FastAPI/Pydantic, SQL/Redis, интеграции с внутренними системами, актуальность и доступ к документам. K11, K13 и K01 дают конкретные сигналы о RU/KK и low-resource NLP. Это 3/17, причём K11 и K13 опираются на вторичные источники. RU/KZ/EN имеет смысл как портфельное отличие за счёт воспроизводимого сравнения, с отдельной языковой разбивкой и code-switching. Для региона в целом долю спроса этот срез не определяет.

**Международный рынок.** Среди 13 карточек 8 упоминают RAG и 8 — оценку качества в широком смысле из таблицы. Консалтинг и FDE добавляют discovery, внедрение и объяснение решения пользователям (I01, I04, I07, I13). Платформенные и ML-роли добавляют опыт эксплуатации, производительность и ресурсы (I09, I11, I12). I08 ограничена США, I11–I12 ограничены перечисленными странами/регионами. I09 допускает международный найм через EoR, а конкретная страна остаётся предметом проверки. Лишь I10 прямо публикуется как Worldwide. Даже у неё право заключить договор из Казахстана нужно подтвердить для конкретного кандидата. I01 и I05 показывают явные ограничения по работе в стране.

**Вход и Senior.** Входные объявления указывают Python или аналог в 6/7, RAG в 5/7 и Docker в 1/7. ITX принимает учебную подготовку, Sia засчитывает 0–2 года практики или учёбы, M3 принимает проекты из вуза или хакатона. Sierra ограничивает окно выпуска, Google требует delivery-опыт при статусе стажировки, Graphcore I05 требует PhD. В группе Senior Docker встречается в 3/5, а развёртывание или инфраструктурные навыки в 5/5. K15 совмещает AI с 6+ годами Python; I09 требует backend и AWS; у I11–I12 нужны GPU serving или real-time ML. Эти различия связаны также с составом ролей. Двенадцать казахстанских объявлений имеют неизвестный грейд, и часть принимает проектные работы при формальном опыте 1–3 или 3–6 лет. Их полезно читать по требованиям и обсуждать стаж напрямую с работодателем.

## 5. Специализации и точки входа

Название вакансии не определяет задачу. K14 совмещает Applied AI и ML, I09 называет backend-роль работой над AI platform, а I12 обучает модель выбора модели. Адаптация резюме начинается с ожидаемого результата работы.

| Путь | Работа, код и инфраструктура | Математика и артефакты | Доступность на входе в этом срезе |
| --- | --- | --- | --- |
| **Applied AI / LLM Engineer** | Python, HTTP и adapters, structured output, RAG, tool calling, тестирование модели и прикладного контракта; Docker и один cloud на уровне деплоя | Вероятность, векторы и метрики. Сервис извлечения или ассистент с размеченной оценкой, источниками и отказами | K01/K02 дают вход через синтетические или учебные проекты. K13 уже требует опыт production LLM |
| **AI Backend Engineer** | Async FastAPI/аналог, PostgreSQL, транзакции, cache/queue, API и авторизация. Провайдер — внешняя зависимость с deadline, version и cost | Численная грамотность для бюджета и retrieval, concurrency и состояние. API с реальными integration tests, миграциями и аудитом | K09 — пример роли от 2 лет backend, K10 — Python-роль с AI, K15 — Senior. Навыки переносятся из обычного backend |
| **ML Engineer** | Данные, обучение, валидация, выкладка и мониторинг моделей. Python/SQL, numpy/pandas, scikit-learn или PyTorch/HF, Docker и инфраструктура по нагрузке | Статистика, loss, leakage, метрики и деградация. Пайплайн данных, baseline и отчёт о модели | K02 — учебный вход. K17 требует production NLP от года, K14 и I12 — обучение, эксплуатация и измерения |
| **AI Platform Engineer** | Serving, routing, quotas, batch/cache, OpenTelemetry, cloud/Kubernetes, CI и права доступа. Python/Go/TypeScript по команде | Capacity, tail latency, профилирование, стоимость, SLO. Платформа inference или шлюз с нагрузочным и incident отчётом | I09 и I11 показывают высокую планку эксплуатации. Реалистичный путь для backend — владение одним сервисом, затем platform |
| **Research Engineer** | Реализация и проверка алгоритмов, PyTorch/JAX, в части вакансий CUDA/C++/Triton и доступ к ускорителям | Линейная алгебра, вероятность, оптимизация, анализ эксперимента и масштабирования. Воспроизводимые эксперименты, результаты и отчёт | I05 принимает без промышленного стажа при наличии PhD. I06 допускает Master’s/PhD или эквивалент с системной и ML-подготовкой |
| **AI Solutions / Forward Deployed** | Discovery, интеграции API и данных, быстрый прототип, внедрение в контуре заказчика и передача решения. Python/Java/TS, cloud по клиенту | Достаточно понимать retrieval/eval и считать качество, latency и стоимость. Демо с метрикой, runbook и обсуждением trade-off | I01 и I03–I04 дают входные примеры. K16 принимает проектные артефакты, I13 ожидает опыт поставки. Язык и on-site могут быть обязательными |

Основная траектория — взять уже знакомый FastAPI, async, SQLAlchemy, PostgreSQL, Redis и Docker, добавить один самостоятельный LLM-сервис и одно retrieval-решение. Для отклика подходят вакансии Python Backend с AI-интеграцией и вакансии без слова Junior, если опыт в тексте совместим. K10 демонстрирует такое название. Решение проверяется по опыту кандидата, продукту, формату и праву работать в указанной локации. Подход распространяется и на FDE, если есть интерес к работе с пользователями. [EPAM](https://careers.epam.com/en/vacancy/bltdae092523b87c979), [KOZ AI, копия](https://kz.finder.work/vacancy/368823985).

## 6. Матрица навыков и аудит Pythoria

База аудита — `main` `5694b7b6010167f05aed7e99b459a65f629e2392`, [учебный план](AI_CURRICULUM_PLAN.md), [манифест R1](../content/ai_curriculum.json) и [отчёт R1](AI_R1_VERIFICATION.md). Уровни покрытия в таблице относятся к артефакту курса. **Объяснение** даёт понятие, **пример** запускается, **Check** оценивает самостоятельный код, **интеграция** проверяет реальный компонент, **проект** собирает путь запроса, **live** отдельно проверяет реальную модель. У AI1–AI4 есть теория и runnable practice, 20 лабораторий с Check. [P1](../projects/chat_api/README.md) и [P2](../projects/trip_extraction/README.md) выполнены как офлайн-проекты с HTTP-контрактами. SDK MockTransport проверяет транспорт и парсинг. Качество ответов реального провайдера остаётся за рамками этой проверки.

**Статус baseline** в таблице отражает план до этой сверки. «Усилить» означает уже запланированный навык с конкретным недостатком практики. «Пробел» означает отсутствие отдельного обязательного упражнения. P0 — основной прикладной навык, P1 — практическое преимущество, P2 — специализация или обзор.

| Категория и навык | Наблюдение и роль технологии | Глубина Junior → Middle | Покрытие baseline и действие |
| --- | --- | --- | --- |
| **A. Python 3, async, REST, FastAPI, Pydantic, HTTPX** | Python 28/30, FastAPI и альтернативы Flask/Django в K10/K15/I08. Python и HTTP переносятся между стеками, framework и HTTP-клиент закрепляют конкретную реализацию | Собрать bounded async HTTP и typed DTO, отменить запрос → управлять lifecycle, backpressure и деградацией | **Готово** AI1.1, AI3.1–3.5/3.7, AI4.2/4.6, P1/P2, Check и интеграционные тесты. P0 перенести контракты в P3, с одним тестом отсутствия DB-транзакции при ожидании модели |
| **A. PostgreSQL, SQLAlchemy, Redis, Celery, очереди** | K09/K11/K13/K15 показывают базы, владельца или фоновые работы. PostgreSQL/SQLAlchemy — данные и транзакции, Redis — короткое состояние/лимит, Celery — исполнение задач; название Celery не встречается в срезе | Составить query/migration, повторить задачу безопасно → объяснить race, ack/commit, cache invalidation и reconciliation | **Готово** SQL/Transaction/Index и Worker labs для основ с реальным PostgreSQL. **Усилить** AI6.4, AI10.2–10.3/P9 для действующих ACL, batch ingest и атомарной квоты; Celery выбран как перенос знакомого backend опыта |
| **A. pytest, Git, Docker, CI/CD** | pytest назван в K11, тесты и CI в K07/I07/I09. Эти понятия переносятся, GitHub Actions — конкретная реализация | Зафиксировать зависимости, написать негативный тест → собрать release artifact, миграцию и rollback по CI | **Готово** runnable tests P1/P2 и labs. **Пробел** цельный gate AI10.5–10.6/P9 с GitHub Actions, отрицательным candidate и доказательством отката |
| **B. LLM API, OpenAI Responses, Anthropic, Google Gemini, совместимые endpoints** | K01/K04/K05/K11/K13/I07/I10. В вакансиях есть провайдеры и совместимые endpoints, конкретный Responses API не назван. Wire protocol, lifecycle и capability различаются | Реализовать один adapter и прочитать чужой wire example → матрица возможностей, контрактные тесты совместимости, безопасная миграция | **Готово** AI3.1/3.7, P1 и mock SDK. **Усилить** AI10.5/P9 двумя scripted adapters и отчётом. OpenAI Responses — основной пример. Anthropic Messages, Gemini Interactions и совместимый endpoint сравнить по tool/stream/error/usage; второй live SDK остаётся P2 |
| **B. Streaming, structured output, timeout/retry, контекст, token/cost и routing** | K09/K11/K12/K13 — отдельные протоколы и ошибки; I12 — специальная работа над routing. Schema, отказ, cancellation и budget — переносимые навыки | Проследить SSE/typed output, посчитать бюджет, выделить timeout/refusal → различать неизвестную оплату, агрегировать usage и выбирать из двух совместимых моделей по измерениям | **Готово** AI2.8, AI3.3–3.6 и AI4.1–4.7, P1/P2. **Усилить** AI5.1–5.5 и AI10.1/10.3/10.5. Policy routing на двух scripted вариантах P1-приоритет, обучение router остаётся P2 |
| **C. Embeddings, ingestion, chunking, версии, metadata filters** | K03/K05/K11/K13/K14/I08/I09 показывают необходимость поиска по данным. Качество зависит от модели, границ фрагмента, языка и доступа | Построить replay-safe ingest и qrels → staging версии индекса, re-embed, ACL/deletion и профилировать фильтры | **Готово** AI2.9 объяснение и Check на synthetic vectors. **Усилить** AI6.2–6.5/6.10 P4/P5 настоящей PG-проверкой повторов, смены версии и отзыва доступа |
| **C. PostgreSQL+pgvector, Qdrant и альтернативы** | Qdrant 6/30, pgvector 4/30; K04 перечисляет альтернативы. pgvector даёт SQL joins и транзакцию с метаданными; Qdrant даёт отдельную vector service/collection с payload filters и sparse/dense retrieval | Спроектировать PG schema и exact/ANN query, прочитать Qdrant API → сравнить recall, индексацию, обновления, backup и ownership на одном наборе | **Запланировано** AI6.4–6.5/P4 — pgvector, P0. **Пробел** сравнение с Qdrant. P1 — соседний локальный профиль по желанию, с общими qrels. Chroma — локальный vector store; Pinecone/Weaviate — сравнение интерфейсов и эксплуатации. Elasticsearch/OpenSearch — поисковый стек с inverted index и hybrid возможностями, обзор P2 |
| **C. Lexical/BM25, hybrid, RRF, reranking и cross-encoder** | K13 описывает dense+BM25 и reranker; I08 даёт hybrid как плюс. BM25 — лексическая функция, RRF объединяет ранги, cross-encoder пересчитывает пару query/document на малом top-N | Сравнить lexical, dense и hybrid на одном запросе, реализовать RRF → зафиксировать candidate budget, recall/latency и эффект reranking | **Усилить** AI6.6/P5. PostgreSQL FTS остаётся baseline; отдельный tiny BM25 пример. Обязателен scripted reranker, локальный cross-encoder — P1 эксперимент |
| **C. Citations, access-controlled retrieval и RAG eval** | K04 RBAC и K13 ссылки на источники; K11 корпоративные данные. ACL и provenance — кодовые свойства. Верность утверждения проверяется размеченным evidence | Реализовать prefilter, проверить chunk/version, вернуть abstain → document lifecycle, multilingual cohort и диагностика retrieval/answer отдельно | **Усилить** AI6.7–6.10/P5. Межтенантный тест, stale-source test и RU/KZ/EN frozen split; 0 запрещённых фрагментов на заявленном corpus |
| **D. Tool calling, bounded loop, state, checkpoints и approvals** | K07/K09/K11/K12 и I07/I10. Протокол и state machine переносятся. Авторизация и подтверждение действия остаются в коде приложения | Исполнить allowlisted read tool, связать IDs, ограничить шаги → восстановиться при crash, replay, stale approval и uncertain result | **Усилить** AI5.1–5.7/P3, AI8.2/8.5/P7, AI9.2–9.4/P8. Один моделируемый write после approval впервые в P7. P3 выдаёт proposal |
| **D. LangChain, LangGraph, MCP и альтернативы** | LangChain 11/30, LangGraph 7/30, MCP 6/30. LangChain — app/model/tool integrations; LangGraph — stateful runtime; MCP — protocol. K11/I07 перечисляют другие framework варианты | Собрать plain Python реализацию, сравнить adapter/trace, подключить local MCP client → обосновать checkpoint, replay и transport authz | **Запланировано** AI7–AI9/P6–P8. **Усилить** gate реальным SDK и parity. CrewAI/AutoGen/Google ADK/OpenAI Agents SDK рассматриваются в ADR без обязательной установки. Multi-agent — **вне core**: multi-tool одного агента покрывает нужные контракты |
| **E. Golden set, retrieval/answer eval, prompt/model versions и human/judge** | Eval 21/30; K13 считает precision/recall, K11 и I07 называют инструменты. Golden cases фиксируют expected outcome. Judge даёт отдельный сигнал, требующий калибровки | Считать знаменатели и per-case ошибки → калибровать judge на ручной разметке, проверять invariants отдельно и стопорить релиз при регрессии | **Готово** AI4.5/4.7/P2, офлайн-оценка extraction. **Усилить** AI6.9, AI9.5, AI10.5/P5/P8/P9. RAGAS и DeepEval — обзор peer APIs, для core достаточно собственного scorer |
| **E. OpenTelemetry, traces, latency/cost; Langfuse, LangSmith, MLflow** | K11/K12/K13 и I07/I10/I11. OTel стандартизует spans и экспорт; Langfuse/LangSmith добавляют AI UI/experiments; MLflow ведёт эксперименты/артефакты, K08 считает плюсом | Прочитать redacted trace и p50/p95 с размером выборки → instrument queue, TTFT, retries, token/cost и проверить redaction/cancellation | **Пробел** единый переносимый стек. P0 OpenTelemetry Python + локальный InMemorySpanExporter и redacted JSON, с локальным Collector debug как расширением. AI6.7/P5 — минимум этапов, AI9.7/P8 — recovery, AI10.4/P9 — полный отчёт. SaaS и второе хранилище — **вне core** |
| **F. NumPy, pandas, scikit-learn, PyTorch, HF Transformers/Datasets/Tokenizers** | PyTorch 8/30, в том числе исследовательские и serving роли; K02 просит знакомство. NumPy/tensors — вычисления, pandas/Datasets — данные, scikit-learn — baseline, HF/PyTorch — model inference/обучение | Основной путь объясняет shapes/split/loss/tokenizer и проходит CPU Check → специализация сравнивает sklearn baseline и tiny torch training, фиксирует dataset/model revision | **Готово** AI2.1–2.10, численные и token exercises. Практику с библиотеками вынести в **optional** M1–M2. Связать оставшееся core с AI6.1 и AI6.9 без нового пакета |
| **F. Fine-tuning, PEFT/LoRA/QLoRA, quantization, Ollama, vLLM и serving eval** | K08/K14 дообучают модели; K13 даёт vLLM и LoRA как плюс; K15 требует vLLM или Ollama, I11 — GPU-serving. LoRA меняет малый набор обучаемых параметров, QLoRA сочетает adapters с quantized base | Объяснить различие RAG/retrieval и изменения weights; отдельно замерить опциональную локальную модель → оценить serving throughput, GPU/RAM и quality loss, совместимость artifacts | **Optional** M3–M6 для соответствующего профиля. Core фиксирует capability и usage в AI10.1/10.5. Ollama — локальная демонстрация inference, vLLM — отдельный обзор serving, Docker/Compose для core обходятся без весов |
| **G. Deploy, cloud и эксплуатация** | I09/I13 — конкретный AWS стек; K07/K10/I07 принимают облачные альтернативы. Docker/CI/IAM и monitoring переносятся между облаками | Fresh-clone Compose, secret injection, CI и один безопасный deploy → масштабирование, queues, quota, incident, rollback и cost attribution | **Усилить** AI10.1–10.7/P9 новой поставкой. AWS ECR/ECS Fargate с GitHub Actions OIDC — один opt-in маршрут. AWS S3 для учебного export, очереди Redis/Celery локально; Azure/GCP/managed AI services и Kubernetes — обзор сопоставления ролей. Зафиксировать cleanup и стоимость |
| **H. Security, privacy, RBAC и языки** | K04/K07/K11/K12 — права, approval/PII; K01/K11/K13 — локальный язык/low-resource. Локальный inference может уменьшить передачу наружу, чувствительные данные всё равно требуют storage и logs policy | Запретить tool action и межтенантный доступ, собрать RU/KZ/EN тесты → threat model, revoke/cache/retention, secret rotation, отдельный live privacy review | **Готово** AI1.1/3.2/4.1/4.6, fixtures P1/P2; **усилить** AI5.3/5.6, AI6.8–6.10, AI8.5, AI9.6, AI10.3/10.6. Добавить code-switch, abstention, небезопасный документ/response и независимые policy asserts |

### Выбор хранилища и трассировки

- **pgvector в core.** Тот же SQL объединяет tenant/version/ACL с топом кандидатов. Exact запрос — эталон для ANN. При HNSW-фильтрации число полученных кандидатов может измениться, поэтому нужен реальный `EXPLAIN` и recall на тех же допустимых данных. Обновление документа делает Postgres удобным для транзакционной активации версии. [pgvector, Indexing и Filtering](https://github.com/pgvector/pgvector).
- **Qdrant на уровне интеграции.** Адаптер вызывает collection query с собственным payload filter; фильтр формирует приложение из trusted principal. Сопоставимый тест загружает те же ID, vectors, модель и ACL, задаёт тот же k, сверяет отозванные документы, recall@k и latency. Qdrant добавляет независимый lifecycle хранилища, payload indexes и согласование с application DB. Нужен отдельный замер при реальной потребности в другой нагрузке. [Qdrant Hybrid Queries](https://qdrant.tech/documentation/search/hybrid-queries/), [Multitenancy](https://qdrant.tech/documentation/manage-data/multitenancy/).
- **От одного span до incident trace.** Обязательные spans `ingest`, `retrieve`, `generate`, `tool`, `queue` используют request/trace ID и ограниченные attributes, например outcome и revisions. User/tenant ID и raw payload не становятся labels. В core экспорт идёт в локальную память и redacted JSON. Для P9 добавить отдельную проверку OTLP с локальным Collector, без внешнего SaaS. Закрепить версию GenAI conventions и собственных attributes, поскольку схема развивается. [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/instrumentation/), [GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai), [Collector](https://github.com/open-telemetry/opentelemetry-collector).

## 7. Изменения по приоритету

Для локальных профилей ниже указаны **проектные бюджеты**, а фактические RAM/CPU и время стартов фиксируются будущим PR на ARM64/macOS и Linux. Локальный Runner сохраняет действующие лимиты. Профили Compose используют только собственные контейнеры и synthetic fixtures. Первичная загрузка lock-зависимостей и образов требует сети или готового кэша. Offline suites связываются только с собственными локальными сервисами.

| Приоритет · сигнал | Старое покрытие и пробел | Точная цель и практикум | Проверка и зависимости · ресурс | Core |
| --- | --- | --- | --- | --- |
| **P0 · K01/K07/K09/K11/I10**, безопасные tools | AI4 умеет валидировать ответ, AI5 уже описывает registry; нужен интегрированный результат в цикле | AI5.1–5.7/P3. Выполнить два read tools через FastAPI с trusted principal, сквозным call ID и бюджетом. История хранит пары, риск даёт proposal | ≥12 deterministic cases, параллельные owners, duplicate/unknown ID, отмена и auth spy. Python/Pydantic/TestClient, 1 CPU/≤512 MiB локально, без сети в Check | +0 |
| **P0 · K04/K11/K13/I09**, проверяемый vector retrieval | AI2.9 покрывает косинус, AI6 уже планирует PG; не хватает отчёта о выборке и поведении фильтра | AI6.2–6.5/P4. Новый digest, replay/change/tombstone, real exact vs HNSW на одинаковом corpus и фильтре | Fresh PG17+pgvector, real migration и pytest, планы EXPLAIN, recall и latency. 2 CPU, до 2 GiB на профиль, isolated Compose | +0 |
| **P1 · K04/K13/I07/I09**, Qdrant | Qdrant отсутствовал как сравнимая интеграция | AI6.5/P4. ADR на те же фильтры и lifecycle. Opt-in адаптер к локальному Qdrant с payload indexes | Общие qrels/ACL и сравнимый k; отдельный отчёт если запускался. Qdrant + locked client, 2 CPU и до 3 GiB на обе БД в optional прогоне | +0 |
| **P0 · K11/K13/K01**, прикладной гибрид и языки | AI6.6 уже планирует RRF, AI6.9 — RU/EN; нужны KZ, защита версий и единый protocol измерений | AI6.6–6.10/P5. FTS и tiny BM25, dense→RRF→top-N rerank; 30 RU/KZ/EN cases, один корпус и замороженный split; delete/update/revoke | Recall@k/MRR отдельно от answer support/citation/abstain. 0 leakage на adversarial cases, mutation отбрасывается. Стек P4 + scripted generator, 2 CPU/до 3 GiB. Optional CPU model отдельно | +0 |
| **P1 · K11/K14/I07/I10**, framework отладка | AI7 планирует миграцию; нужен одинаковый endpoint contract и измеримая граница полезности | AI7.1–7.6/P6. Подключить LangChain `create_agent`/middleware к готовым tools и retriever. Сохранить прямой путь, проверить usage/retry | Один parametrized suite для обоих путей, один turn trace, negative control на auth/retry. Локальный lock, 1–2 CPU/до 1 GiB сверх P5 | +0 |
| **P0 · K07/K12**, ошибки протокола и approval | AI8 планирует MCP и approval; нужно разделить transport identity и ресурсные права | AI8.1–8.6/P7. Один bounded coordinator, read-only MCP local server и synthetic approved effect; сравнить deterministic path с agent loop | ≥12 scenarios и реальные in-memory + stdio SDK tests; unsupported revision, no scope, replay и stale approval. Python SDK v2 lock, локальный pipe, 1 CPU/до 1 GiB | +0 |
| **P0 · K07/K11/K12/I04**, recovery и безопасность | AI9 планирует checkpoint, replay и threats; нужен наблюдаемый реальный restart | AI9.2–9.7/P8. Положить checkpoint в отдельную SQLite, убить worker после synthetic эффекта и продолжить с тем же key в новом процессе | ≥20 graph scenarios, matrix crash windows, состояние effect store, revoked approval и cross-thread. LangGraph + persistent plugin, 2 CPU/до 1 GiB, без внешней сети | +0 |
| **P0 · K12/I08/I09/I11**, измерение и release eval | P2 даёт offline counters. AI10.4 предусматривал optional exporter; нет сквозного gate | AI6.7/AI9.7/AI10.3–10.5/P5/P8/P9. OTel spans на реальных code boundaries, запуск плохого scripted candidate через GitHub Actions | Красная регрессия и сохранённый предыдущий release; metadata-only tracing, p50/p95/TTFT с N, no raw texts, wrong provider accounting. OTel SDK/Collector и CI, локальный профиль P9 до 6 GiB | +0 |
| **P0 local / P1 cloud · K07/K10/I09/I13**, поставка | Docker/worker уже знакомы; требуется release и incident evidence | AI10.2/10.5–10.7/P9. Fresh clone Compose, queue/DB/ACL restore, rollback, ограниченный local load; отдельный маршрут ECR→ECS Fargate с OIDC | 2–4 CPU, целевой Compose ≤6 GiB, local integration. AWS optional по смете, IAM/cleanup, synthetic smoke и rollback по immutable digest. Отдельно отражать результаты local и cloud | +0 |
| **P2 · K02/K08/K14/K15/I06/I11**, model engineering | AI2 объясняет основы, план уже допускает отдельную ML-ветку | Модули M1–M6. От NumPy и sklearn baseline до tiny torch/PEFT и измерения локального inference | Метрики на frozen split, seed и model card, lock и ресурсный отчёт. CPU default, тяжёлые GPU варианты только по явному opt-in | +0 |

## 8. Портфолио и готовность к отклику

Для каждой ступени используется rubric, а учащийся объясняет границу ответственности и выполняет одно самостоятельное изменение, которого не видел в эталоне. Для README указывать, где применялся AI-assisted код, какие тесты написаны самостоятельно и какой результат подтвердил тест.

| Проект | Что проверяется на защите |
| --- | --- |
| **P1 LLM Chat API** | HTTP и SSE под scripted provider, deadline/refusal и cleanup. Покажи typed результат и причину закрытия потока. Уже есть локальный runnable проект. |
| **P2 Structured Trip Extraction** | Разделение schema/domain/facts, неизвестный год, replay 20-case dev/holdout отчёта и отказ от regression candidate. Уже есть runnable отчет. |
| **P3 Controlled Booking Assistant** | 12+ cases, настоящий read tool, запрещённый вызов даёт 0 чтений ресурса, межтенантный тест, bounded loop и безопасный trace. На защите добавить один разрешённый read tool. |
| **P4 PostgreSQL Vector Search** | Fresh Compose/миграция, exact IDs, известная граница ANN recall, replay версии и фактический план. На защите объяснить другой фильтр. |
| **P5 Document Knowledge Assistant** | Двухтенантный корпус и frozen RU/KZ/EN оценка, доказательство ACL и актуальной ссылки, сравнение поисковых baseline и отдельный answer report. На защите разобрать кейс retrieval и кейс generation. |
| **P6 LangChain Refactoring Comparison** | Один test corpus для direct и framework, отказ/usage/permissions сохраняются, ADR об издержках, trace до provider. На защите исправить несовместимый вызов без смены контракта. |
| **P7 Multi-tool Assistant + MCP** | Реальные in-memory и stdio вызовы SDK, bounded coordinator, safe failure, matching approval и отказ при истечении срока. На защите объяснить смену версии протокола. |
| **P8 Durable LangGraph Workflow** | ≥20 cases, restart и повтор resume без дублирования эффекта, durable checkpoint, frozen regressions, trace инцидента. На защите разобрать crash window. |
| **P9 Study Materials AI Backend** | Fresh-clone Compose, real PG+queue, CI reject regression, редактирование/отзыв документа, отчёт latency/cost и работающий local rollback. На защите сменить policy или provider config и показать заблокированный плохой релиз. |

Три основных артефакта для профиля Applied AI / AI Backend — **P3, P5 и P9**. P3 покажет границы полномочий и ответственность backend при вызове инструмента. P5 покажет владение RAG, измерение поиска и применимость к многоязычным корпоративным данным. P9 покажет выпуск, наблюдаемость, реакцию на сбой и восстановление. Для собеседования в ML-команду отчёт из M2/M4 можно приложить отдельно. Завершение учебной программы даёт материалы для оценки и объяснения, результат найма зависит от требований, самостоятельно продемонстрированного навыка и географии.

### Опциональное реальное измерение

Офлайн suite обязателен и проверяет контракт. Live experiment запускается отдельно при явном согласии. Ему нужны зафиксированные model ID/snapshot, SDK и prompt/index version, frozen synthetic cases, request cap и бюджет. Начальный потолок проекта — до **20 запросов и 1 USD** или меньший пользовательский лимит; это потолок эксперимента, а не оценка тарифа. До запуска сверить актуальный тариф и доступность, учесть retries, общий deadline/cancellation и обработку неопределённого usage. Ключ поступает оператору через секрет окружения, отчёт содержит только агрегаты, безопасные ID и статус. Live результаты с фактической моделью, датой, выборкой и ограничениями публикуются отдельным файлом. Для казахского текста оценка семантики требует редактора, владеющего языком. LLM-as-judge сравнивается с человеческой разметкой на небольшой выборке и не используется для разрешения действий.

### Стоимость опционального облачного smoke

Для P9 ограничить пробу одним Linux/ARM task на 0,5 vCPU и 1 GiB RAM на 60 минут.
По примеру AWS для `us-east-1` стоимость CPU+RAM составляет около **0,02 USD за task-час**
(`3600 × (0.5 × 0.0000089944 + 1 × 0.0000009889)`). Учитывать отдельно хранение образа ECR,
CloudWatch logs, публичный IPv4, traffic, а при их использовании также ALB/NAT/S3 и дополнительный
task во время rollout. Перед запуском проверить ставки региона и способ закрытия доступа,
записать смету, время остановки и ответственную команду очистки. Сценарий завершает service
и задачи, удаляет выделенные тестовые артефакты и проверяет остатки по тегу эксперимента.
OIDC даёт короткоживущую роль только нужному GitHub environment/ref. Опыт локального Docker
отражается отдельно от фактически выполненного cloud smoke. [Пример тарифа AWS Linux/ARM](https://aws.amazon.com/fargate/pricing/), [GitHub OIDC для AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws).

## 9. Дополнительная ветка ML / Model Engineering

Core сохраняет CPU-математику, loss, train/test, attention, tokenization и embedding mismatch в AI2 и AI6. Издержки GPU, model artifacts и training изучаются параллельно после AI2.

| Модуль · результат | Практика и подтверждение | Проектный бюджет |
| --- | --- | --- |
| M1 · NumPy и PyTorch CPU | Покажи broadcast/shapes, autograd и конечную разность на том же tiny примере, сравни со stdlib | 1–2 CPU, до 2 GiB, малые arrays, Python lock |
| M2 · Данные и scikit-learn baseline | pandas или HF Datasets, group split без leakage, sklearn baseline, per-class метрики, seed и train/dev/test | 2 CPU, до 2 GiB, synthetic набор до 50 MiB |
| M3 · HF Transformers, Tokenizers и tiny training | Закрепи модель и tokenizer, измерь исходное CPU inference. Дообучи маленький encoder на искусственных данных, сравни замороженный тест | 2–4 CPU, до 4 GiB RAM, до 2 GiB диска с кэшем; больший training optional |
| M4 · PEFT/LoRA | Сравни число параметров, размер артефакта и score до/после. QLoRA объяснить и проверять отдельно только на совместимом устройстве | Tiny LoRA с ограничениями M3; GPU experiment по отдельной смете RAM/VRAM и лицензии |
| M5 · Локальный inference и serving | Ollama, одна 1–3B quantized модель. Измерь latency/TTFT, tok/s и RAM на фиксированном prompt set, сравни profiles. vLLM — batching/KV/throughput design и optional smoke на совместимой среде | Для Ollama ориентир 16 GiB RAM хоста, 4–6 GiB свободного диска и короткий context, одна model copy. На 8 GiB использовать tiny CPU fixture или ограничиться чтением отчёта. vLLM checks зависят от backend/ОС, ARM64 совместимость сверить до установки |
| M6 · Артефакты, drift и reproducibility | Версионировать модель, split, конфиг и lock, обнаружить известный drift; MLflow как optional tracking adapter | 1–2 CPU, до 2 GiB, локальные artifacts |

Это проектные оценки, которые будут измерены при реализации ветки. Доступ, лицензия, тип квантизации, размер весов, context и cache влияют на реальный ресурс.

## 10. Актуальность технических источников

Проверка страниц и registry **23.11.2026**. Указанные версии доступны в источнике, совместимый lock и runtime verification относятся к будущим implementation PR.

| Источник | Что подтверждает |
| --- | --- |
| [OpenAI Function Calling](https://developers.openai.com/api/docs/guides/function-calling), [Anthropic Messages](https://platform.claude.com/docs/en/api/messages), [Gemini Interactions](https://aistudio.google.com/docs/interactions-overview) | Provider-specific wire families и tool-result mapping. Совместимый HTTP endpoint сверяется по фактическим capabilities |
| [LangChain v1 migration](https://docs.langchain.com/oss/python/migrate/langchain-v1), [PyPI 1.5.2](https://pypi.org/project/langchain/1.5.2/) | `langchain.agents.create_agent`, новые пространства имён, components в `langchain-classic`. 1.5.2 опубликован 18.11 UTC |
| [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence), [PyPI 1.2.24](https://pypi.org/project/langgraph/1.2.24/) | Checkpoints и threads, `StateGraph`, сохранение состояния между вызовами. 1.2.24 опубликован 20.11 UTC |
| [MCP 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28), [Python SDK v2.3.0](https://github.com/modelcontextprotocol/python-sdk/releases/tag/v2.3.0), [Protocol versions](https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/protocol-versions.md) | Текущая ревизия, per-request metadata, `server/discover`, in-memory/stdio и legacy fallback, требующий отдельного теста. 2.3.0 опубликован 02.10 UTC |
| [PostgreSQL 17 FTS](https://www.postgresql.org/docs/17/textsearch-controls.html), [pgvector](https://github.com/pgvector/pgvector), [Qdrant Hybrid Queries](https://qdrant.tech/documentation/search/hybrid-queries/), [RRF](https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking), [OpenSearch BM25](https://docs.opensearch.org/latest/search-plugins/keyword-search/) | `ts_rank` и `ts_rank_cd`, exact/ANN и filters, lexical/dense fusion по рангу. Сравнение хранит одинаковые candidate sets и labels |
| [OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/), [OpenTelemetry GenAI conventions](https://github.com/open-telemetry/semantic-conventions-genai) | Прямой и косвенный prompt injection, минимальные полномочия, versioned instrumentation и content capture controls |
| [GitHub AWS OIDC](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws), [ECS Fargate](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html), [Fargate pricing](https://aws.amazon.com/fargate/pricing/), [AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html) | Короткоживущие credentials, task deployment, региональные цены на ресурсы, сигналы о расходах. Cloud budget alert может запаздывать |
| [Hugging Face Transformers](https://huggingface.co/docs/transformers/index), [PEFT LoRA](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora), [Ollama](https://docs.ollama.com/), [vLLM CPU requirements](https://docs.vllm.ai/en/latest/getting_started/installation/cpu/) | Model/tokenizer artifacts, adapters, local inference и ограничения serving backend. Замеры выполняются на выбранном оборудовании |

Вакансии и ограничения открываемости перечислены в §3. Тот же market snapshot нужно перечитать перед следующей серьёзной корректировкой программы. Для очередного implementation PR проверяются конкретные SDK/протоколы и зависимости из затронутых уроков.
