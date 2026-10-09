---
title: Журнал wiki
type: log
tags: [log]
sources: []
updated: 2026-09-13
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

## [2026-09-02] ingest | Вариативное меню, НПА и регионы

Иммутабельный PDF 82 стр. + PPTX 28 слайдов уже на `main` (`1bab521`, PR #20). Ingest только wiki: `wiki/sources/variativnoe-menu-npa-2026.md`, сущность СПб № 1284, правки понятий и домов. Канон «Не просто накормить» не затирался. Автор на титуле не назван. Противоречия (дефиниция, СанПиН 3590-20 vs 4282-26, пять моделей vs М0–М5, Болотнинский) — в `wiki/gaps.md`.

## [2026-09-02] lint | После ingest НПА и регионов

`python3 .github/check_wiki.py`: OK, 43 wiki md, frontmatter и wikilinks живые. `raw/` не тронут. PPTX/PDF остаются только в `raw/sources/variativnoe-menu-npa-2026/`.

## [2026-09-13] query | Пачка типовых ответов для РГ

Семь страниц в `wiki/queries/`: СанПиН с 1 сентября; две лестницы; комплект проверяющему; что не норма; слои кейса Болотнинского; 223 vs 44; определение вариативности. Каталог — `wiki/queries/README.md` и секция Queries в `wiki/index.md`. Сырьё `raw/` не трогали.

## [2026-09-13] lint | gaps: убрать удалённые соседние репо

В `wiki/gaps.md` таблица «что положить следующим» больше не предлагает удалённые remote (`-variabelnoe-menu-pni`, `academic-redesign-report`, `social-nutrition-reports`, `seminar-materials-2026`, `vault`) как живые GitHub. Содержание первых трёх — в `raw/sources/related/`. Опционально позже: `seminar-mental-health-cost-2026`, `seminar-ai-social-care-2026`, `glm-quiz`. Фраза «репо на GitHub не удалять» снята.

## [2026-10-09] ingest | Поиск 2026-10: дисфагия

По просьбе автора начата вторая редакция доклада в `doklad-v2/` (канон в `raw/` не тронут). Новый каталог `raw/sources/poisk-2026-10-disfagiya/` — реестр 14 источников с переводами (распространённость, удушье, гигиена рта, свободная вода, IDDSI по-русски). Wiki: `wiki/sources/poisk-2026-10-disfagiya.md`, дополнение в `concepts/disfagiya.md`, `gaps.md` (п. 21, частичное закрытие «30–50 %»), index. Пилотная глава — `doklad-v2/10_disfagiya.md`.

## [2026-10-09] ingest | Поиск 2026-10: вторая редакция доклада

Вторая редакция всех 44 глав в `doklad-v2/` (около 98 тыс. слов против 40 тыс.), сборка `ne-prosto-nakormit-v2.md` и PDF. Девять реестров `raw/sources/poisk-2026-10-blok-a…i/` (канон в `raw/` не тронут). Wiki: `sources/poisk-2026-10-vtoraya-redakciya.md`; исправлены `entities/irkutskaya-oblast.md` (четыре учреждения), `concepts/lestnica-modelej.md` (Nijs без деменции), `concepts/pravo-na-vybor.md` (п. 3 ст. 36 ГК); `gaps.md` п. 22–25; index.

## [2026-10-09] ingest | Поиск 2026-10: кейсы и приложения второй редакции

Переписаны 22 учебных кейса и 45 приложений-шаблонов в `doklad-v2/кейсы/` и `doklad-v2/приложения/`. Новые реестры: `raw/sources/poisk-2026-10-kejsy-a`, `-kejsy-b`, `-pril-a`, `-pril-b`, `-pril-c`; 18 источников сведены в раздел 44.5. Исправлены ошибки первой редакции в кейсах: гуманное отношение — ч. 2 ст. 5 Закона № 3185-1; прокурорский контур опирается на `S111` и `S135`, а не на дела ФАС; удалено неподтверждённое «80 %». Сборка и PDF теперь включают кейсы и приложения.
