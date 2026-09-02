# academic_redesign_report

Проект редакционной переработки и современного оформления доклада о вариативном питании в стационарных организациях социального обслуживания.

## Структура каталога

```
academic_redesign_report/
├── README.md                    — этот файл
├── STATUS.md                    — статус проекта
├── SOURCE_FILE_AUDIT.md         — аудит исходных файлов
├── CONTENT_GAP_AUDIT.md         — реестр пропусков и дефектов
├── EDITORIAL_PLAN.md            — редакционный план
├── DESIGN_SYSTEM.md             — визуальная система
├── CHANGELOG.md                 — реестр изменений
├── FACT_CHECK_LOG.md            — журнал проверки фактов
├── LINK_VALIDATION.md           — валидация ссылок
├── ANTI_AI_STYLE_REPORT.md      — отчёт об устранении ИИ-шаблонов
├── originals/                   — исходные файлы (не изменяются)
│   ├── Доклад_100_страниц.docx  — основной исходник (58 209 слов)
│   ├── report.md                — сокращённая версия
│   ├── chapters_md/             — 34 файла глав
│   └── appendices_md/           — 50 файлов приложений
├── scripts/                     — скрипты сборки
│   ├── build_report.py          — основной скрипт генерации DOCX
│   ├── create_xlsx.py           — генерация XLSX-реестров
│   └── generate_pdf.py          — конвертация DOCX→PDF (требует LibreOffice)
├── output/                      — итоговые файлы
│   ├── Доклад_современная_академическая_версия.docx
│   ├── Доклад_официальная_версия.docx
│   ├── chart_financial_comparison.png
│   ├── chart_staircase.png
│   ├── Реестр_устраненных_пропусков.xlsx
│   ├── Реестр_изменений.xlsx
│   └── Реестр_источников.xlsx
├── quality_control/
│   └── FINAL_LAYOUT_QA.md       — отчёт проверки верстки
├── chapters/
├── tables/
├── charts/
├── figures/
├── references/
├── drafts/
└── extracted/
```

## Быстрый старт

```bash
# Генерация DOCX (обе версии)
python3 scripts/build_report.py

# Генерация XLSX-реестров
python3 scripts/create_xlsx.py

# Конвертация в PDF (требуется LibreOffice)
python3 scripts/generate_pdf.py
```

## Требования

- Python 3.10+
- python-docx
- openpyxl
- matplotlib (для диаграмм)
- LibreOffice (для PDF, опционально)
