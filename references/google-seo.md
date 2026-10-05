# Google: обязательный второй слой

Google не заменяет Яндекс в RU-first аудите. Используй GSC, PageSpeed Insights, CrUX и Rich Results Test при наличии доступа или публичной проверки.

## Проверяемые данные

- GSC: clicks, impressions, CTR, average position, query → page, index coverage и период выгрузки;
- PageSpeed/CrUX: field-data отдельно от lab-data, URL/шаблон и дату проверки;
- публичный web: indexable content, canonical, robots, schema и SERP pattern.

## Stop conditions и fallback

- Не называй среднюю позицию «позицией сайта» без GSC и периода.
- Не делай вывод об index coverage без GSC или URL Inspection.
- Если GSC нет, используй public SERP только для intent/конкурентов и занеси отсутствие performance/index data в limitation log.
- Любое изменяемое правило Google проверяй по записи в `references/source-registry.md`.
