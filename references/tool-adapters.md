# Tool adapters

Skill не зависит от одного провайдера.

## Yandex MCP
Желательный data layer:
- Wordstat;
- Yandex Search;
- Webmaster;
- Metrika.

Ожидаемая логика credentials:
- Search + Wordstat: API key + folder ID;
- Webmaster: OAuth token;
- Metrika: OAuth token.

Не проси токены в чат — используй environment/secrets.

| Данные | Tool |
|---|---|
| спрос | Wordstat top requests |
| сезонность | Wordstat dynamics |
| география | Wordstat regions |
| SERP intent | Yandex Search |
| запросы/индексация | Webmaster |
| organic landings/conversions | Metrika |

Если установлены `yandex-wordstat`, `yandex-metrika`, `yandex-webmaster`, `crawl4ai-seo`, используй их как execution backend, а этот skill — как оркестратор.

## Crawl
Подойдут Crawl4AI, Firecrawl, Screaming Frog export и аналоги. Сохраняй полный inventory в файл, а в контекст загружай summaries/chunks.

Минимальные поля: url,status,title,description,h1,canonical,robots,word_count,internal_inlinks,internal_outlinks,depth.

## Google
Если доступны GSC/PageSpeed/CrUX, используй их как primary sources Google performance.

Сохраняй период и параметры выгрузки; field-data и lab-data не смешивай. Контракт и fallback: `references/google-seo.md`.

## No API fallback
Exports → public web → manual SERP sample → hypotheses. Для public web/SERP сохраняй параметры из evidence protocol. Никогда не изображай API-данные, которых не получал.
