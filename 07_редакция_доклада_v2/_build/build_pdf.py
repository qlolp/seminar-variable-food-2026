# -*- coding: utf-8 -*-
"""
build_pdf.py - Сборка PDF через Chrome/Edge headless
Используется, когда weasyprint не работает (отсутствует libgobject-2.0-0.dll)

Использование: python build_pdf.py
"""

import os
import sys
import subprocess
import time
from pathlib import Path

BASE = Path(r"C:/Users/Evgenii/OneDrive/Desktop/seminar/seminar-variable-food-2026/07_редакция_доклада_v2")
OUT = BASE / "_build"
HTML_DIR = OUT / "html"
PDF_DIR = OUT / "pdf"
CSS_FILE = OUT / "style.css"

# Найдём Chrome
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]

CHROME = None
for p in CHROME_PATHS:
    if Path(p).exists():
        CHROME = p
        break

if not CHROME:
    print("ОШИБКА: Chrome или Edge не найден.")
    sys.exit(1)

print(f"Браузер: {CHROME}")

# Те же файлы, что и в build.py
FILES = [
    ("07_полная_версия/Не_просто_накормить_редакция_v2.md", "01_Не_просто_накормить_редакция_v2", "Не просто накормить — редакция v2 (227 стр.)", "Чистяков Е. В."),
    ("08_версии/01_управленческое_резюме.md", "02_управленческое_резюме", "Управленческое резюме (5-7 стр.)", "Чистяков Е. В."),
    ("08_версии/02_методические_рекомендации.md", "03_методические_рекомендации", "Методические рекомендации (50-70 стр.)", "Чистяков Е. В."),
    ("08_версии/03_статья_для_публикации.md", "04_статья_для_публикации", "Статья для публикации (8 000-12 000 слов)", "Чистяков Е. В."),
    ("08_версии/04_выступление_20_минут.md", "05_выступление_20_минут", "Устное выступление 18-20 минут", "Чистяков Е. В."),
    ("08_версии/05_выступление_40_минут.md", "06_выступление_40_минут", "Расширенное выступление 30-40 минут", "Чистяков Е. В."),
    ("08_версии/06_тезисы.md", "07_тезисы", "Тезисы доклада (2-4 стр.)", "Чистяков Е. В."),
    ("08_версии/07_QA.md", "08_QA", "Q&A - 22 вопроса для спикера", "Чистяков Е. В."),
    ("08_версии/памятка_26.08_обновлённая.md", "09_памятка_26.08", "Памятка 26.08 - обновлённая", "Чистяков Е. В."),
    ("09_инструменты/паспорт_пилота_90_дней.md", "10_паспорт_пилота_90_дней", "Паспорт пилота 90 дней", "Чистяков Е. В."),
    ("09_инструменты/форма_базового_замера.md", "11_форма_базового_замера", "Форма базового замера", "Чистяков Е. В."),
    ("10_источники/библиография_v2.md", "12_библиография_v2", "Библиография v2 (134 источника)", "Чистяков Е. В."),
    ("11_этика/этическая_рецензия.md", "13_этическая_рецензия", "Этическая рецензия", "Редакционная группа"),
    ("11_этика/словарь_предпочтительных_формулировок.md", "14_словарь_формулировок", "Словарь предпочтительных формулировок", "Редакционная группа"),
    ("12_QA/финальный_отчёт.md", "15_финальный_отчёт", "Финальный отчёт (4 прохода QA)", "Редакционная группа"),
    ("12_QA/оставшиеся_риски.md", "16_оставшиеся_риски", "Оставшиеся риски", "Редакционная группа"),
]

CSS = """
@page { size: A4; margin: 2cm 1.8cm; @bottom-center { content: counter(page); font-family: 'PT Sans', sans-serif; font-size: 9pt; color: #888; } }
body { font-family: 'PT Sans', 'Helvetica', 'Arial', sans-serif; font-size: 10.5pt; line-height: 1.45; color: #222; max-width: 16cm; }
h1 { font-family: 'Playfair Display', 'Times New Roman', serif; font-size: 22pt; font-weight: 700; color: #2a2a2a; margin-top: 0; border-bottom: 1.5pt solid #b8624d; padding-bottom: 4pt; }
h2 { font-family: 'Playfair Display', 'Times New Roman', serif; font-size: 15pt; font-weight: 700; color: #b8624d; margin-top: 18pt; border-bottom: 0.5pt solid #ddd; padding-bottom: 2pt; }
h3 { font-family: 'PT Sans', sans-serif; font-size: 12pt; font-weight: 700; color: #444; margin-top: 14pt; }
h4 { font-size: 11pt; font-weight: 600; color: #555; margin-top: 10pt; }
p { text-align: justify; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; font-size: 9.5pt; }
th, td { border: 0.5pt solid #bbb; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { background: #f4ede4; font-weight: 600; }
code { font-family: 'Consolas', monospace; font-size: 9.5pt; background: #f8f8f8; padding: 1pt 3pt; }
pre { font-family: 'Consolas', monospace; font-size: 9pt; background: #f8f8f8; padding: 6pt; border-left: 2pt solid #b8624d; }
blockquote { border-left: 3pt solid #b8624d; padding-left: 8pt; color: #555; font-style: italic; }
hr { border: 0.5pt solid #b8624d; margin: 14pt 0; }
sup { font-size: 7pt; color: #b8624d; }
"""

def run_pandoc(args):
    cmd = ["pandoc"] + args
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return result.returncode == 0, result.stdout, result.stderr

def md_to_html():
    """Сначала markdown -> HTML."""
    print("[Шаг 1: markdown -> HTML]")
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    CSS_FILE.write_text(CSS, encoding="utf-8")
    ok_count = 0
    for src_rel, name, title, author in FILES:
        src = BASE / src_rel
        if not src.exists():
            print(f"  ПРОПУСК: {src_rel}")
            continue
        out = HTML_DIR / f"{name}.html"
        args = [
            str(src),
            "-o", str(out),
            "--from=gfm+yaml_metadata_block+pipe_tables",
            "--to=html5",
            "--toc",
            "--toc-depth=3",
            "--standalone",
            f"--metadata=title:{title}",
            f"--metadata=author:{author}",
            f"--metadata=date:22.08.2026",
            f"--metadata=lang:ru",
            f"--css={CSS_FILE}",
            "--wrap=preserve",
        ]
        ok, _, err = run_pandoc(args)
        if ok and out.exists():
            size_kb = round(out.stat().st_size / 1024, 1)
            print(f"  HTML OK: {name}.html ({size_kb} КБ)")
            ok_count += 1
        else:
            print(f"  HTML FAIL: {name} — {err[:200] if err else 'unknown'}")
    return ok_count

def html_to_pdf():
    """Затем HTML -> PDF через headless Chrome/Edge."""
    print()
    print(f"[Шаг 2: HTML -> PDF через {Path(CHROME).name}]")
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    ok_count = 0
    for html_file in HTML_DIR.glob("*.html"):
        name = html_file.stem
        pdf_file = PDF_DIR / f"{name}.pdf"
        # Chrome headless: --headless --no-sandbox --disable-gpu --print-to-pdf
        cmd = [
            CHROME,
            "--headless=new",
            "--no-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--virtual-time-budget=10000",
            "--no-pdf-header-footer",
            f"--print-to-pdf={pdf_file}",
            f"file://{html_file}",
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            if pdf_file.exists():
                size_kb = round(pdf_file.stat().st_size / 1024, 1)
                print(f"  PDF OK: {name}.pdf ({size_kb} КБ)")
                ok_count += 1
            else:
                print(f"  PDF FAIL: {name} (файл не создан)")
        except subprocess.TimeoutExpired:
            print(f"  PDF TIMEOUT: {name}")
        except Exception as e:
            print(f"  PDF FAIL: {name} — {str(e)[:150]}")
    return ok_count

def main():
    print("=== Сборка PDF через Chrome/Edge headless ===")
    print(f"Источник: {BASE}")
    print(f"Выход:    {PDF_DIR}")
    print()
    OUT.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    
    html_ok = md_to_html()
    print()
    if html_ok == 0:
        print("HTML сборка не удалась, PDF не будет собран.")
        return
    
    pdf_ok = html_to_pdf()
    print()
    print(f"=== Готово: HTML {html_ok}/{len(FILES)}, PDF {pdf_ok}/{len(FILES)} ===")
    print(f"PDF: {PDF_DIR}")

if __name__ == "__main__":
    main()
