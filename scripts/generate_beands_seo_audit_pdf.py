#!/usr/bin/env python3
"""Build a portable, static PDF audit report for beands-media.ru."""
from __future__ import annotations

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer, Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "beands-media-seo-audit-2026-08-12.pdf"
FONT = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D8E1EB"))
    canvas.line(18 * mm, 13 * mm, 192 * mm, 13 * mm)
    canvas.setFont("Arial", 8)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(18 * mm, 8 * mm, "Beands Media - SEO-аудит - read-only публичная проверка")
    canvas.drawRightString(192 * mm, 8 * mm, f"Страница {doc.page}")
    canvas.restoreState()


def make_table(rows, widths, header=True):
    table = Table(rows, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D8E1EB")),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#102A43")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Arial-Bold"),
        ]
    table.setStyle(TableStyle(style))
    return table


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdfmetrics.registerFont(TTFont("Arial", str(FONT)))
    pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONT_BOLD)))
    styles = getSampleStyleSheet()
    normal = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Arial", fontSize=9.2, leading=13, textColor=colors.HexColor("#243B53"), spaceAfter=6)
    small = ParagraphStyle("Small", parent=normal, fontSize=8, leading=10.5)
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="Arial-Bold", fontSize=24, leading=29, textColor=colors.HexColor("#102A43"), spaceAfter=9)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Arial-Bold", fontSize=14, leading=18, textColor=colors.HexColor("#0F766E"), spaceBefore=11, spaceAfter=7)
    h3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName="Arial-Bold", fontSize=10.5, leading=14, textColor=colors.HexColor("#102A43"), spaceBefore=7, spaceAfter=3)
    white = ParagraphStyle("White", parent=normal, fontName="Arial-Bold", fontSize=10, leading=14, textColor=colors.white)
    center = ParagraphStyle("Center", parent=normal, alignment=TA_CENTER, fontSize=9)
    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=19 * mm)
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates(PageTemplate(id="report", frames=[frame], onPage=footer))

    story = []
    story += [p("SEO-аудит", h1), p("beands-media.ru", ParagraphStyle("Domain", parent=h1, fontSize=17, textColor=colors.HexColor("#0F766E"))), Spacer(1, 4 * mm)]
    hero = Table([[p("READ-ONLY ПУБЛИЧНАЯ ПРОВЕРКА", white), p("Дата: 12 августа 2026", white)]], colWidths=[94 * mm, 62 * mm])
    hero.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0F766E")), ("LEFTPADDING", (0,0),(-1,-1),9), ("RIGHTPADDING", (0,0),(-1,-1),9), ("TOPPADDING", (0,0),(-1,-1),9), ("BOTTOMPADDING", (0,0),(-1,-1),9)]))
    story += [hero, Spacer(1, 7 * mm), p("Итог", h2), p("Базовая техническая подготовка хорошая: публичный sitemap содержит 35 URL, все проверенные URL отдали HTTP 200; на них присутствуют title, description, H1 и canonical. Главная отрендерена на сервере, использует русский язык документа и имеет корректные базовые метатеги.", normal)]
    story += [p("Главный риск", h3), p("robots.txt запрещает обход нескольким AI-crawler’ам, включая GPTBot, ClaudeBot, PerplexityBot и Google-Extended. Это не является проблемой обычного Google/Yandex SEO, но ограничивает видимость материалов в AI-поиске и генеративных ответах.", normal)]
    story += [p("Ограничения данных", h2), p("В отчёте нет вымышленных данных о позициях, трафике, CTR, заявках или индексации. Для точной оценки нужны доступы или экспорты из Яндекс Вебмастера, Метрики, Wordstat и Google Search Console.", normal)]
    story += [p("Что проверено", h2)]
    rows = [[p("Область", small), p("Результат", small)], [p("Robots и sitemap", small), p("robots.txt и sitemap.xml доступны; в sitemap 35 URL.", small)], [p("Crawl", small), p("35 URL из sitemap: HTTP 200; отсутствующие title/description/H1/canonical не выявлены.", small)], [p("Главная", small), p("SSR/пререндер, lang=ru, robots index/follow, canonical и OG/Twitter metadata присутствуют.", small)], [p("Разметка", small), p("На проверенных service pages JSON-LD есть; на главной JSON-LD не найден.", small)], [p("Заголовки", small), p("CSP, X-Content-Type-Options, X-Frame-Options, Referrer-Policy и Permissions-Policy присутствуют.", small)]]
    story += [make_table(rows, [48 * mm, 108 * mm]), PageBreak()]

    story += [p("Приоритетные findings", h1)]
    findings = [
        ("HIGH", "AI-crawlers заблокированы", "robots.txt закрывает GPTBot, ClaudeBot, PerplexityBot, Google-Extended и другие AI user-agent’ы.", "Принять продуктовое решение: если GEO/AEO важно, разрешить выбранные боты; если запрет осознанный, закрепить это как политику.", "SEO / business", "S", "Проверить правила robots.txt и фактическую доступность выбранному user-agent."),
        ("HIGH", "На главной нет JSON-LD", "Главная содержит бренд, услуги, контакты и кейсы, но JSON-LD не найден; на service pages разметка присутствует.", "Добавить валидируемые Organization/ProfessionalService, WebSite, WebPage и ContactPoint только с подтверждёнными фактами.", "Dev + SEO", "S", "Rich Results Test и проверка исходного HTML."),
        ("HIGH", "Неподтверждённые claims и нулевые SSR-счётчики", "На главной есть claims 50+ проектов, 95% точности, 15 экспертов и SLA 99.9%; одновременно статический HTML показывает 0+ / 0% в блоке счётчиков.", "Исправить SSR-счётчики. Для каждого числа добавить источник/методику либо смягчить формулировку. У кейсов указать согласованные доказательства.", "Business + dev", "M", "Сверка HTML, дизайна и документированного источника каждого claim."),
        ("MEDIUM", "Дубли бренда и длинные title", "У ряда страниц title заканчивается на «| Beands Media | Beands Media»; отдельные title достигают 70-89 символов.", "Убрать повтор бренда, поставить ключевой интент в начало, оставить бренд один раз.", "SEO + content", "S", "Crawl: уникальные title без повторов, оценка CTR в GSC/Вебмастере."),
        ("MEDIUM", "Размытый коммерческий фокус главной", "Главная одновременно продаёт B2B-услуги, курсы, downloads и игры; это расширяет семантику, но ослабляет главный оффер AI-разработки для бизнеса.", "Выдвинуть B2B-услуги в основной путь: AI-агенты, RAG, автоматизация продаж, MVP. Курсы и материалы оставить отдельными хабами.", "SEO + product", "M", "Проверка внутренней перелинковки и конверсии service page -> lead."),
        ("MEDIUM", "Неполный FAQ", "На главной вопросы о цене, сроках и поддержке видны, но развёрнутый публичный ответ найден только для темы безопасности.", "Заполнить все ответы фактическими условиями; добавить FAQ schema только после содержательного наполнения.", "Content + business", "S", "Проверить рендер ответов и соответствие реальной политике продаж."),
    ]
    for level, title, evidence, action, owner, effort, verification in findings:
        badge = colors.HexColor("#B42318") if level == "HIGH" else colors.HexColor("#B54708")
        head = Table([[p(level, ParagraphStyle("Badge", parent=white, fontSize=8)), p(title, ParagraphStyle("FT", parent=normal, fontName="Arial-Bold", fontSize=11, textColor=colors.HexColor("#102A43")))]], colWidths=[22 * mm, 134 * mm])
        head.setStyle(TableStyle([("BACKGROUND", (0,0),(0,0),badge), ("BACKGROUND", (1,0),(1,0),colors.HexColor("#EEF4F8")), ("VALIGN", (0,0),(-1,-1),"MIDDLE"), ("LEFTPADDING", (0,0),(-1,-1),7), ("RIGHTPADDING", (0,0),(-1,-1),7), ("TOPPADDING", (0,0),(-1,-1),6), ("BOTTOMPADDING", (0,0),(-1,-1),6)]))
        story += [head, p(f"<b>Evidence:</b> {evidence}", normal), p(f"<b>Action:</b> {action}", normal), p(f"<b>Owner / effort:</b> {owner} / {effort}. <b>Verification:</b> {verification}", small), Spacer(1, 3 * mm)]
    story += [p("План действий", h1), p("Quick wins: 7-14 дней", h2)]
    quick = [[p("1", center), p("Исправить 0+ / 0% в SSR и убрать повтор «| Beands Media» из title.", normal)], [p("2", center), p("Добавить JSON-LD на главную и проверить разметку в Rich Results Test.", normal)], [p("3", center), p("Провести ревизию цифр, отзывов, SLA и кейсов: оставить только доказуемые claims.", normal)], [p("4", center), p("Заполнить FAQ по цене, срокам, инфраструктуре и поддержке; привязать ответы к CTA.", normal)], [p("5", center), p("Зафиксировать политику для AI-crawlers в robots.txt.", normal)]]
    story += [make_table([[p("Шаг", small), p("Действие", small)]] + quick, [15 * mm, 141 * mm])]
    story += [p("Roadmap 30 / 60 / 90", h2)]
    roadmap = [[p("30 дней", small), p("Подключить/выгрузить Вебмастер, Метрику, GSC и Wordstat; собрать карту запросов для AI-агентов, RAG, автоматизации продаж и AI MVP.", small)], [p("60 дней", small), p("Усилить service pages реальными доказательствами, FAQ, интеграциями и связками «кейс -> услуга -> консультация».", small)], [p("90 дней", small), p("Развивать экспертные материалы под коммерческие вопросы и измерять non-brand visibility, CTR и органические заявки.", small)]]
    story += [make_table([[p("Период", small), p("Результат", small)]] + roadmap, [28 * mm, 128 * mm])]
    story += [p("KPI и способ проверки", h2)]
    kpis = [[p("KPI", small), p("Источник / метод", small)], [p("Клики, показы, CTR, indexed target pages", small), p("Яндекс Вебмастер и GSC.", small)], [p("Non-brand спрос и покрытие кластеров", small), p("Wordstat, SERP-проверка, keyword map.", small)], [p("Органические заявки и качество лидов", small), p("Метрика + CRM.", small)], [p("Конверсия service pages", small), p("События формы, квиза, телефона и CTA в Метрике.", small)], [p("Техническое здоровье", small), p("Регулярный crawl: status, canonical, title, schema, internal linking.", small)]]
    story += [make_table(kpis, [62 * mm, 94 * mm]), Spacer(1, 5 * mm), p("Источники: публично доступные https://beands-media.ru/, /robots.txt, /sitemap.xml и страницы из sitemap. Проверка выполнена 12.08.2026. Внешние изменения не выполнялись.", small)]
    doc.build(story)
    print(OUT)


if __name__ == "__main__":
    main()
