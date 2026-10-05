# Русская семантика и кластеризация

## Цель
Построить карту спроса → страниц → бизнес-ценности.

## Seed sources
Услуги/товары, категории сайта, запросы Вебмастера/GSC, внутренний поиск, отдел продаж, CRM, отзывы, Wordstat associations, SERP competitors.

## Русские формы
Учитывай склонения, число, разговорные синонимы, слитное/раздельное написание, транслит, бренды, аббревиатуры, жаргон, города и коммерческие модификаторы.

## Intent taxonomy
- Transactional
- Commercial investigation
- Local
- Informational
- Navigational/brand
- Support/post-purchase
- Employment/education
- DIY/accessory

## Intent validation
Для важного запроса:
1. Посмотри Яндекс SERP в целевом регионе.
2. Определи доминирующий page type.
3. Определи действие пользователя.
4. Проверь, может ли бизнес удовлетворить intent.
5. Назначь target page.

## Кластеризация
Приоритет:
1. SERP overlap.
2. Одинаковый intent.
3. Одинаковый page type.
4. Семантическая близость.

Не объединяй запросы только по общим словам.

## Keyword map
Поля:
cluster_id, cluster_name, primary_keyword, secondary_keywords, region, intent, funnel_stage, page_type, target_url, status, impressions, clicks, conversion evidence, business_value, priority, notes.

## Упущенный спрос
Ищи:
- спрос без страницы;
- неверный page type;
- query → wrong URL;
- высокий показ + низкий CTR;
- 8–30 позиции с хорошей конверсией;
- растущие запросы;
- сезонность;
- города/категории с доказанным спросом.

## Stop reasons
jobs, free, DIY, definition, unrelated brand, repair/support, used/avito, B2B/B2C mismatch, wrong geography, low business value. Не удаляй автоматически — маркируй.
