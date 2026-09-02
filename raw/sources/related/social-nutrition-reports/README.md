# qlolp/social-nutrition-reports

**URL:** https://github.com/qlolp/social-nutrition-reports  
**Upstream `main`:** `13b70ae6390d16e2c90c34ee052b623867843ff6` (2026-07-24)  
**Снимок:** 2026-09-02, тонкая карта семейства + уникальные куски.

Зонтичный репозиторий докладов о вариативном питании к семинару «Пространство Новых Идей 2.0». После ingest `-variabelnoe-menu-pni` и `academic-redesign-report` этот репо **в основном избыточен**.

## Карта подкаталогов upstream (не копировать мегабайты)

| Каталог | Что это | В этом снимке |
| --- | --- | --- |
| `academic_redesign_report/` | Копия академической переработки | Не копировали: дубль `qlolp/academic-redesign-report` |
| `report_variable_menu_pni/` | Копия доклада ПНИ 22.07 | Не копировали: дубль `qlolp/-variabelnoe-menu-pni` |
| `seminar_variable_food_2026/` | Ранний корпус «Не просто накормить» + печатный пакет | Не копировали том: канон wiki — `raw/sources/ne-prosto-nakormit/`. Взяли только [`AUDIT_OLD_REPORTS.md`](AUDIT_OLD_REPORTS.md) |
| `report_international_nutrition/` | Каркас международного доклада (не содержательный текст) | Скопирован: [`report_international_nutrition/`](report_international_nutrition/) без скриптов |

## Что скопировано (как в upstream, без правки)

- [`README.upstream.md`](README.upstream.md)
- [`AUDIT_OLD_REPORTS.md`](AUDIT_OLD_REPORTS.md) (из `seminar_variable_food_2026/`)
- `report_international_nutrition/`: README, STATUS, 22 главы-каркаса, 3 приложения-каркаса, `output/report.md`, реестры CSV, `research_plan.md`, `logs/limitations.md`

## Что не копировали

Вложенные дубли ПНИ и академического доклада; DOCX/PDF/PPTX/XLSX семинарского пакета; скрипты; `data/old_report_*.md` (содержательно разобраны в AUDIT).

Wiki: [`wiki/sources/social-nutrition-reports.md`](../../../../wiki/sources/social-nutrition-reports.md).
