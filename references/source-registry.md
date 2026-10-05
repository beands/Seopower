# Реестр первичных источников и ревизия

Используй этот реестр перед работой с меняющимися правилами, API или поисковыми интерфейсами. Он определяет источник методологии, а не заменяет evidence register конкретного проекта.

| Module | Primary source | Scope | Owner | Last verified | Next review | Status |
|---|---|---|---|---|---|---|
| Yandex | Яндекс Справка для Вебмастера, Метрики и Search API | indexation, analytics, API | BeandsMedia | 2026-08-22 | 2026-11-22 | Active |
| Google | Google Search Central и Search Console Help | crawling, indexing, structured data, GSC | BeandsMedia | 2026-08-22 | 2026-11-22 | Active |
| Local | Справка Яндекс Бизнес, 2ГИС и Google Business Profile | profiles and factual local data | BeandsMedia | 2026-08-22 | 2026-11-22 | Active |
| Ecommerce | Google Search Central и справка Яндекса | product pages, feeds, schema | BeandsMedia | 2026-08-22 | 2026-11-22 | Active |
| GEO/AEO | первичные источники издателя и поисковых платформ | citations, entities, content facts | BeandsMedia | 2026-08-22 | 2026-11-22 | Active |
| Russian marketing channels | официальные справки Яндекс Директа, VK Рекламы, Telegram Ads, Дзена, Rutube, Ozon, Wildberries, Яндекс Маркета и Avito | campaign formats, exports, metrics, seller analytics | BeandsMedia | 2026-10-03 | 2027-01-03 | Review required |
| Reputation | официальные правила Яндекс Бизнеса, 2ГИС, маркетплейсов и публичных каталогов | reviews, profiles, responses, permitted workflows | BeandsMedia | 2026-10-03 | 2027-01-03 | Review required |
| Marketing compliance | официальный портал опубликования правовых актов, ФАС России, Роскомнадзор и актуальная документация рекламных платформ | ad labeling, advertising claims, personal-data risk indicators | BeandsMedia | 2026-10-03 | 2027-01-03 | Legal review required |
| Funnel and analytics | справки Метрики, CRM/call tracking vendors and platform export definitions | attribution, events, leads, sales, revenue/margin definitions | BeandsMedia | 2026-10-03 | 2027-01-03 | Review required |
| Agent compatibility | официальная документация каждого агента | installation and discovery | BeandsMedia | 2026-08-22 | 2026-11-22 | Pending evidence |

## Release gate

Перед квартальным релизом владелец проверяет каждую запись: ссылка доступна, правило не изменилось, связанный reference-файл актуален. Обнови `Last verified`, `Next review` и журнал изменений релиза. Если `Next review` прошла или источник недоступен, соответствующий модуль имеет статус `Review required`: не выдавай изменяемое правило как факт, используй более свежий первичный источник или пометь вывод ограничением.
