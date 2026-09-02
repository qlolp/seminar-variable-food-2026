---
title: Журнал wiki
type: log
tags: [log]
sources: []
updated: 2026-09-02
confidence: high
---

# log

Append-only. Формат заголовка не менять: `## [YYYY-MM-DD] ingest|query|lint | title`

## [2026-09-02] ingest | Не просто накормить (литературная редакция + пакет)

Первый ingest. Сырьё перенесено в `raw/sources/ne-prosto-nakormit/` (доклад md/PDF, главы 1–44, 22 кейса, 45 приложений, колода, семинарский пакет, листовки, викторина). Собраны страницы понятий, домов, законов, практик; `overview.md`; `gaps.md`. Канон текста — литературный markdown с ветки `cursor/literary-report-rewrite-f019`, не только академический PDF 69 стр.

## [2026-09-02] ingest | -variabelnoe-menu-pni (лёгкий снимок)

Скопированы README, STATUS, `output/executive_summary.md`, `key_findings.md`, `director_memo.md`. Полный report.md не копировался. Страница источника: `wiki/sources/variabelnoe-menu-pni.md`. Расхождения с семинарским докладом занесены в `gaps.md`.

## [2026-09-02] lint | Каркас Karpathy

Проверка: `AGENTS.md`, `wiki/index.md`, живые пути `raw/`, frontmatter, запрет писать в `raw/` после ingest. Соседние репо кроме снимка ПНИ — stubs pending.

## [2026-09-02] lint | Wiki-first: убрана печатная раздатка

Семинар прошёл. Из `raw/` удалены викторина, листовки Canva, академический PDF 69 стр., краткая версия 19 стр., колода PDF/PPTX, xlsx-калькулятор и дублирующие PDF пакета. Канон сырья — литературный markdown + один PDF редакции + markdown-бланки. CI: `.github/check_wiki.py` (каркас wiki, не список печати). Как класть новое — `HOW_TO_ADD.md`.

## [2026-09-02] ingest | -variabelnoe-menu-pni (полный корпус)

Заменён лёгкий снимок. Скопированы `output/report.md`, все `output/*.md`, `chapters/*.md`, `appendices/*.md`, семь CSV-реестров, README/STATUS upstream, `PRINT_INSTRUCTIONS.md` (ссылка из `output/README.md`). Скрипты, HTML-печать, SVG не брали. Страница: `wiki/sources/variabelnoe-menu-pni.md`. Сверка 22 глав с 44 главами канона и противоречия — в `wiki/gaps.md`. GitHub-репо не удаляли.

## [2026-09-02] ingest | academic-redesign-report (аудиты)

Скопированы CONTENT_GAP_AUDIT, FACT_CHECK_LOG, SOURCE_FILE_AUDIT, LINK_VALIDATION, STATUS, README.upstream. Без DOCX/PDF/`full_text.txt`. Страница: `wiki/sources/academic-redesign-report.md`. 8 экспертных остатков аудита не закрывали.

## [2026-09-02] ingest | social-nutrition-reports (карта + уникальное)

Скопированы корневой README.upstream, AUDIT_OLD_REPORTS, каркас `report_international_nutrition/` без скриптов. Дубли ПНИ и академического слоя не копировали: после ingest 1+2 репо в основном избыточен. Страница: `wiki/sources/social-nutrition-reports.md`. GitHub-репо не удаляли.

## [2026-09-02] lint | После ingest трёх соседних репо

`python3 .github/check_wiki.py`: каркас, frontmatter, wikilinks, пути `raw/`. Три новые/обновлённые страницы источников в index. Печатную HTML/скрипты не клали.
