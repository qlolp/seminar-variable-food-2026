---
title: Источник — академическая переработка (24.07.2026)
type: source
tags: [источник, редакция, аудит]
sources:
  - raw/sources/related/academic-redesign-report/README.md
  - raw/sources/related/academic-redesign-report/STATUS.md
  - raw/sources/related/academic-redesign-report/CONTENT_GAP_AUDIT.md
  - raw/sources/related/academic-redesign-report/FACT_CHECK_LOG.md
  - raw/sources/related/academic-redesign-report/SOURCE_FILE_AUDIT.md
  - raw/sources/related/academic-redesign-report/LINK_VALIDATION.md
updated: 2026-09-02
confidence: medium
---

# Академическая переработка (qlolp/academic-redesign-report)

Редакционный слой **24.07.2026** между докладом ПНИ 22.07 и литературным каноном «Не просто накормить». Upstream: https://github.com/qlolp/academic-redesign-report (`main` `206f9be`). Это аудит и перевёрстка 34-главного DOCX (~58 209 слов), не замена канона wiki.

В `raw/` — аудиты и статусы. DOCX/PDF, скрипты и `extracted/full_text.txt` не копировали: для wiki достаточно реестра пропусков.

## Что слой сам о себе говорит

Исходник: `originals/Доклад_100_страниц.docx` (34 главы, 50 приложений, 95 таблиц). Аудит 25 категорий: **47** дефектов, **39** устранено при редактировании, **8** осталось на экспертную проверку ([`CONTENT_GAP_AUDIT.md`](../../raw/sources/related/academic-redesign-report/CONTENT_GAP_AUDIT.md)). Частично открыты G12 (блоки «для руководителя»), G15 (внутренние ссылки), G46 (инструкции к формам). Приняты без правки G27 (схема документов списком) и G47 (нестабильные URL).

[`FACT_CHECK_LOG.md`](../../raw/sources/related/academic-redesign-report/FACT_CHECK_LOG.md) помечает как действующие на 24.07: 442-ФЗ, 3185-1, ГК, 48-ФЗ, 52-ФЗ, **СанПиН 2.1.3684-21**, **приказ Минтруда № 774н**. Медицина: влияние антипсихотиков на вес, литий и соль, ИМАО и тирамин, грейпфрут — «подтверждено» по инструкциям; доля дисфагии 30–50% — «требует верификации». Международные практики (protected mealtimes, IDDSI, food buddies и др.) — «существует» с разной доказательностью. Судебная практика — не найдена.

[`LINK_VALIDATION.md`](../../raw/sources/related/academic-redesign-report/LINK_VALIDATION.md): автоматической проверки URL не было. Вручную: garant.ru, consultant.ru, iddsi.org, nice.org.uk.

Ограничения STATUS: LibreOffice не стоял (PDF «ограничено»); юридическая и медицинская верификация — по общедоступным источникам; финансы иллюстративны.

## Чего этот ingest не закрывает

Не закрывать фразой «академическая редакция уже исправила». Литературный канон — другой слой (август). Расхождения с каноном — в [gaps](../gaps.md): другой номер СанПиН (G23 / fact-check: 2.1.3684-21), «11 ступеней» (G21), 774н рядом с 520н канона. Восемь экспертных остатков аудита остаются открытыми.

Связи: [[wiki/sources/ne-prosto-nakormit]] — [канон](ne-prosto-nakormit.md); [[wiki/sources/variabelnoe-menu-pni]] — [предшественник 22.07](variabelnoe-menu-pni.md); [[wiki/sources/social-nutrition-reports]] — [зонтик](social-nutrition-reports.md).
