---
title: Источник — зонтик докладов о питании
type: source
tags: [источник, семейство, карта]
sources:
  - raw/sources/related/social-nutrition-reports/README.md
  - raw/sources/related/social-nutrition-reports/README.upstream.md
  - raw/sources/related/social-nutrition-reports/AUDIT_OLD_REPORTS.md
  - raw/sources/related/social-nutrition-reports/report_international_nutrition/README.md
  - raw/sources/related/social-nutrition-reports/report_international_nutrition/STATUS.md
  - raw/sources/related/social-nutrition-reports/report_international_nutrition/output/report.md
  - raw/sources/related/social-nutrition-reports/report_international_nutrition/logs/limitations.md
updated: 2026-09-02
confidence: low
---

# Зонтик social-nutrition-reports (qlolp/social-nutrition-reports)

Кухня-монорепо четырёх докладов к семинару «Пространство Новых Идей 2.0». Upstream: https://github.com/qlolp/social-nutrition-reports (`main` `13b70ae`, 24.07.2026).

**После ingest предшественника ПНИ и академических аудитов этот репозиторий в основном избыточен.** Соседний GitHub **не удаляли**.

Карта подкаталогов — в stub [`README.md`](../../raw/sources/related/social-nutrition-reports/README.md). В сырьё взяли только то, чего нет в снимках (1) и (2).

## Уникальное в этом снимке

1. [`AUDIT_OLD_REPORTS.md`](../../raw/sources/related/social-nutrition-reports/AUDIT_OLD_REPORTS.md) (22.07.2026). Разбор двух старых текстов (`old_report_pni.md`, `old_report_intl.md`). Верифицированы по полному тексту: IDDSI (PMID 27913916), CQC Regulation 14 (SI 2014/2936), CRPD, страница Минтруда events/1481, письмо Минтруда (PDF, О. Ю. Баталина). Итог 39 утверждений: 6 верифицировано, 26 переписать, 7 исключить. Среди «исключить / переписать»: контроль питания ПНИ Росздравнадзором; «плата не более 75%» без проверки редакции; модель СПб «35% тарифа»; Болотнинский без официального источника; «принудительное кормление запрещено» как ложное (прямого запрета не найдено).

2. [`report_international_nutrition/`](../../raw/sources/related/social-nutrition-reports/report_international_nutrition/) — **каркас**, не доклад. 4 237 слов структуры; 22 главы-заготовки; 23 источника, все «требует проверки»; 0 первоисточников открыто целиком. STATUS прямо запрещает выдумывать страны, номера и практики. `output/report.md` — оглавление и пометки «требует верификации», не сравнительная матрица.

## Внутреннее напряжение семейства

AUDIT_OLD_REPORTS на ту же дату 22.07 **верифицирует** IDDSI, CQC 14 и CRPD. Каркас международного доклада в `logs/limitations.md` пишет, что CRPD ст. 12 и актуальный IDDSI **не удалось подтвердить**, проверено источников: 0. Не склеивать. Не повышать каркас до «международного опыта».

Дубли `academic_redesign_report/` и `report_variable_menu_pni/` в wiki не клали: они уже в [[wiki/sources/academic-redesign-report]] — [академических аудитах](academic-redesign-report.md) и [[wiki/sources/variabelnoe-menu-pni]] — [докладе ПНИ](variabelnoe-menu-pni.md). Ранний `seminar_variable_food_2026/` не подменяет канон [[wiki/sources/ne-prosto-nakormit]] — [«Не просто накормить»](ne-prosto-nakormit.md).

Противоречия аудита со слоем августа — [gaps](../gaps.md).
