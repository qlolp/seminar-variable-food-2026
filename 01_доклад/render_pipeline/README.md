# Render pipeline — `minimax-pdf` для доклада «НЕ ПРОСТО НАКОРМИТЬ»

Воспроизводимая сборка «красивой» версии доклада из исходного PDF.

## Что здесь лежит

```
render_pipeline/
├── README.md                          ← этот файл
├── 01_build_content.py                ← парсер исходного PDF → content.json
├── 02_render_with_cyrillic.py         ← рендер через minimax-pdf (cover + body + merge)
├── 03_extract_pdf.py                  ← извлечение текста из исходного PDF
├── 04_verify.py                       ← проверка результата (страницы, текст, кодировка)
├── 05_rasterize.py                    ← растеризация страниц в PNG для предпросмотра
└── data/
    ├── seminar_text.md                ← сырой извлечённый текст (227 К символов)
    └── seminar_content.json           ← распарсенный контент (837 блоков: h1/h2/body/table/bullet)
```

## Воспроизведение

```bash
# 1. Сгенерировать seminar_text.md из исходного PDF
python3 03_extract_pdf.py

# 2. Распарсить текст в структурированный content.json (h1=главы, h2=подразделы, table=таблицы)
python3 01_build_content.py
# → запишет data/seminar_content.json (837 блоков: 74 h1, 337 h2, 80 таблиц)

# 3. Собрать PDF через minimax-pdf (cover + body + merge)
python3 02_render_with_cyrillic.py
# → запишет ../Не_просто_накормить_доклад_красивая_версия.pdf
```

## Зависимости

```bash
pip install pdfplumber pypdf reportlab matplotlib
pip install --break-system-packages pdfplumber   # если PEP 668
# Node 18+ + playwright для обложки
npm install -g playwright && npx playwright install chromium
```

## Параметры рендера

В `02_render_with_cyrillic.py` зашиты:

- **Тип:** `report` (fullbleed, dot-grid, Playfair Display)
- **Акцент:** `#2A5A6B` (глубокий teal)
- **Шрифты тела:** DejaVu Serif Bold (заголовки) + DejaVu Sans (тело) — для полной поддержки кириллицы
- **Токены:** `data/tokens_cyrillic.json` генерится автоматически при первом запуске

## Что важно знать

1. **Cyrillic-шрифты критичны.** Без `font_paths` в `tokens.json` весь русский текст рендерится квадратами (□). Скрипт автоматически регистрирует DejaVu из `C:\Windows\Fonts\`.

2. **PDF-извлечение теряет структуру.** Парсер делает best-effort по:
   - `ЧАСТЬ I. …` → h1 + pagebreak
   - `Глава N. …` (с возможным переносом названия) → h1 + pagebreak
   - `Приложение АN. …` → h1 + pagebreak
   - `Кейс N. …` → h2
   - `N.M. …` → h2 (нумерованные подразделы)
   - `Конфликт N`, `Уровень N`, `Модель N`, `Шаг N`, `Этап N`, `Принцип N` → h2
   - таблицы в исходнике → нативный `table` блок с чередующимися строками

3. **Известные артефакты парсинга:**
   - 2–3 таблицы в районе Глав 3 и приложений А21–А22 получили переносы строк в ячейках (выглядит читаемо, но сетка местами не идеальна)
   - Некоторые bullet-маркеры из исходника отображаются как □ в ячейках таблиц — это исходный чекбокс-символ, не баг рендера

## Если хочется пересобрать с другим дизайном

В `02_render_with_cyrillic.py` поменять:

| Параметр | Сейчас | Альтернативы |
|---|---|---|
| `--accent` | `#2A5A6B` (teal) | `#1C3A5E` (navy), `#6B2A35` (burgundy), `#2E5E3A` (forest) |
| `--type` | `report` | `academic`, `magazine`, `proposal`, `minimal` |
| Шрифт display | DejaVu Serif Bold | Cambria, Times New Roman (всё есть в `C:\Windows\Fonts\`) |
| Шрифт body | DejaVu Sans | Calibri, Segoe UI, Arial |

После правки перезапустить `02_render_with_cyrillic.py`.
