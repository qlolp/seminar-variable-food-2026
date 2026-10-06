---
title: Журнал wiki
type: log
tags: [log]
sources: []
updated: 2026-10-06
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

## [2026-10-06] ingest | Доклад v2 «Вариативное меню: право, данные, практика»

Источник: `raw/sources/variativnoe-menu-doklad-2026-v2/` (doklad md/pdf/docx, README, прил. Г 47–48а) — вторая редакция правового обзора, 05.10.2026, шесть проходов, draft PR #23. Решение автора («почини там все») — ingest в той же ветке. `raw/` не трогали.

Создано: `wiki/sources/variativnoe-menu-doklad-2026-v2.md`; сущности `wiki/entities/prikaz-305n.md`, `wiki/entities/rostrud-kontrol.md`. ПП СПб № 507 — внутри страницы № 1284, отдельной страницы нет.

Обновлено: `gaps.md` (п. 1, 2, 4–11, 13–17, 20 — след «закрыто в v2, п. X» без удаления истории; новые закрытия п. 21–34; открытое после v2 п. 35–45; дыры данных и «что положить»); сущности № 1284, Серафимовский, приказ № 124, Иркутская обл., Болотнинский, Успенский, Усть-Илимский, ДДСОЛ, СанПиН 4282-26, 520н; понятия переход СанПиН, модели М0–М5, ступени участия, вариативность, каналы воли, три отказа, аутсорсинг, 223/44, комплект проверяющему, пары эквивалентов; queries `sanpin-s-1-sentyabrya`, `dve-lestnicy`, `223-i-44`, `chto-ne-norma`, `komplekt-proveryayushchemu`, `variativnost-opredelenie`, `sloi-kejsov-bolotninskiy`; `pni-vs-dso` (Усть-Илимский не ПНИ, 19РВ-32); источник обзора НПА (ссылка на v2); `overview.md`; `index.md`.

Главное: аутсорсинг — один кейс (Серафимовский), условия договора не проверены; № 1284 с 01.01.2026 в ред. ПП № 507; № 124 — правила внутреннего распорядка с одной фразой о «зале заказного питания»; порядок каналов воли и протокол трёх отказов — рекомендация, не норма; Роструд проверяет государственные дома субъекта. Классы утверждений сохранены; ранние слои не затёрты. Приватного нет: без ksp-путей, номеров документооборота, имён, кроме автора и со-модератора.

## [2026-10-06] lint | После ingest доклада v2

Снят дрейф: «публичных кейсов на аутсорсинге нет» (index, концепт, query 223/44); «субсидия на госзадание нередко в 44-ФЗ» (концепт и query 223/44); «19РВ-32 — мостик» (ДДСОЛ, index, gaps); «Иркутск — заявка на региональный М2» (index, overview, модели); живая ссылка на приказ № 124 (sdso-spb.ru вместо мёртвого pni9.ru). Новые страницы внесены в index. `python3 .github/check_wiki.py` — в коммите ingest.

