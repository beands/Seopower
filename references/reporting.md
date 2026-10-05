# Reporting contract

## Evidence protocol

До findings создай evidence register. Одна строка — одно воспроизводимое наблюдение:

| Evidence ID | Label | Source | URL / query | Captured at | Region / device | Sample | Raw artifact | Confidence | Limitation |
|---|---|---|---|---|---|---|---|---|---|

`Captured at` содержит дату, время и timezone. Для экспортов указывай также период. `Raw artifact` — путь к локальному файлу, скриншоту, HTML или стабильный публичный URL; не записывай credentials, cookies и персональные данные. Если параметр неприменим, ставь `N/A`.

Факт ссылается на `Evidence ID`. Вывод связывает факты и объясняет интерпретацию. Гипотеза имеет label `INFERENCE`, содержит ограничение и следующий безопасный способ проверки. Публичная SERP-выборка не доказывает трафик, позиции, индексацию или конверсии.

## Evidence labels
LIVE_API / EXPORT / CRAWL / SERP / SITE / PUBLIC_PROFILE / CLIENT / INFERENCE

## External audit evidence

Сторонние отчёты обозначай `EXTERNAL_REPORT`. Это слабый источник: каждое утверждение должно получить статус `ПОДТВЕРЖДЕНО`, `ОПРОВЕРГНУТО`, `УСТАРЕЛО` или `НЕДОСТАТОЧНО ДАННЫХ` после проверки более сильным источником.

Не указывай общий SEO-score внешнего сервиса как оценку сайта. Для этого режима используй `assets/external-audit-review.template.md`.

## Finding
### [F-001] Название
- Severity
- Scope
- Evidence: `E-001`, `E-004`
- Fact / conclusion / hypothesis
- Why it matters
- Recommendation
- Owner
- Effort
- Dependency
- Verification
- KPI
- Confidence

## Roadmap
0–14 дней: блокеры + quick wins.
15–30: архитектура, pages, linking.
31–60: content/categories/local.
61–90: expansion + authority + GEO + iteration.

## Recommendations after findings

Заверши отчёт самостоятельным списком рекомендаций после всех evidence, limitations и findings. Не ограничивайся повторением названия finding: опиши deliverable и условие готовности.

| Recommendation ID | Type | Linked F-/E- IDs | Priority | Deliverable | Expected effect | Owner | Effort | Dependency | Acceptance criteria | Verification | KPI | Confidence | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

- `Type` - `Remediation` для подтверждённой проблемы или `Growth` для возможности.
- `Status: Ready` допустим только для доказанной проблемы с понятной зависимостью; иначе `Needs validation`.
- Для `Growth` без спроса/аналитики сначала создай recommendation на сбор доказательств, а не на массовую публикацию страниц.
- Указывай ожидаемый эффект как направление измерения, не как гарантированное изменение позиций, трафика или лидов.

## KPI
Clicks, impressions, non-brand clicks, qualified leads, conversion rates, orders, revenue and margin when available, repeat purchases, return/cancellation rate, spend, cost per qualified lead, indexed target pages, share of mapped clusters, CTR, local actions/calls and crawl health.

Для полного marketing-аудита выводи карту каналов со статусом `ACTIVE` / `PLANNED` / `NOT_USED` / `NOT_APPLICABLE` / `UNKNOWN` и покрытием `COMPLETE` / `PARTIAL` / `UNKNOWN`. Используй одинаковые периоды и определения метрик; сохраняй platform attribution отдельно от CRM/финансовых результатов. Без явно указанного полного покрытия показывай `нет данных`/observed findings вместо оценки 100. Не выдавай агрегированный marketing score.

## Compliance observations
Записывай только наблюдаемый факт, дату, официальный источник, неопределённость и вопрос для юридической проверки. Не добавляй правовую квалификацию или заключение о compliance.

## Uncertainty
Всегда указывай недоступные данные, то, что требует подтверждения, слабые samples и выводы, которые могут измениться после получения API/access.

## Limitation log

| ID | Missing or weak data | Affected conclusion | Safe next verification | Owner | Status |
|---|---|---|---|---|---|

## Saved report outputs

Для любого запроса, результатом которого является аудит или самостоятельный отчёт, сохраняй полный Markdown-источник в `output/reports/<project>-<mode>-<YYYY-MM-DD>.md` и статичный PDF в `output/pdf/<project>-<mode>-<YYYY-MM-DD>.pdf`. Это правило действует и тогда, когда пользователь просит показать отчёт в чате: дай там краткое резюме и ссылку на PDF. Исключение — явная просьба не создавать файлы или выдать другой формат.

Генерируй PDF только после завершения Markdown-отчёта с помощью `scripts/render_seo_report_pdf.py`. Сохраняй все разделы, таблицы и ссылки на источники; ссылки должны оставаться кликабельными. Проверь существование и ненулевой размер PDF, извлеки текст и сверь наличие кириллицы, findings, evidence IDs, ограничений и рекомендаций с Markdown. Отрендери все страницы в изображения и визуально проверь переносы, таблицы, заголовки, колонтитулы и нумерацию. При обнаружении дефекта исправь источник или рендерер, пересобери PDF и проверь его повторно.

Не ограничивай отчёт PDF ради экономии места. Если технически недоступен шрифт или средство рендеринга, найди доступный Unicode-шрифт и установи недостающую локальную зависимость. Если среда всё равно не позволяет создать или проверить PDF, сохрани Markdown, явно сообщи о незавершённом PDF и не называй отчёт готовым.
