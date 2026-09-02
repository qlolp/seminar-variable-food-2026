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
