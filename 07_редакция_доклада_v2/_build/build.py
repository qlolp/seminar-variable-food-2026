# -*- coding: utf-8 -*-
"""
build.py - Сборка DOCX и PDF для редакции v2
Автор: Mavis, 22.08.2026
Правовая сверка и фактчекинг: 22.08.2026

Использование:
  python build.py docx      # только DOCX
  python build.py pdf       # только PDF
  python build.py all       # всё (по умолчанию)
"""

import os
import sys
import subprocess
from pathlib import Path

BASE = Path(r"C:/Users/Evgenii/OneDrive/Desktop/seminar/seminar-variable-food-2026/07_редакция_доклада_v2")
OUT = BASE / "_build"
DOCX_DIR = OUT / "docx"
PDF_DIR = OUT / "pdf"
CSS_FILE = OUT / "style.css"

# Карта файлов: исходник -> (имя, заголовок, автор)
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

def run_pandoc(args, capture=True):
    """Запустить pandoc."""
    cmd = ["pandoc"] + args
    result = subprocess.run(cmd, capture_output=capture, text=True, encoding="utf-8")
    if result.returncode != 0 and capture:
        return False, result.stderr
    return True, result.stdout

def build_docx():
    print("[DOCX]")
    DOCX_DIR.mkdir(parents=True, exist_ok=True)
    ok_count = 0
    for src_rel, name, title, author in FILES:
        src = BASE / src_rel
        if not src.exists():
            print(f"  ПРОПУСК: {src_rel} (нет файла)")
            continue
        out = DOCX_DIR / f"{name}.docx"
        args = [
            str(src),
            "-o", str(out),
            "--from=gfm+yaml_metadata_block+pipe_tables",
            "--to=docx",
            "--toc",
            "--toc-depth=3",
            f"--metadata=title:{title}",
            f"--metadata=author:{author}",
            f"--metadata=date:22.08.2026",
            "--metadata=lang:ru",
            "--wrap=preserve",
        ]
        ok, msg = run_pandoc(args, capture=True)
        if ok and out.exists():
            size_kb = round(out.stat().st_size / 1024, 1)
            print(f"  OK: {name}.docx ({size_kb} КБ)")
            ok_count += 1
        else:
            print(f"  FAIL: {name}.docx — {msg[:200] if msg else 'unknown'}")
    return ok_count

def build_pdf():
    print("[PDF]")
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    CSS_FILE.write_text(CSS, encoding="utf-8")
    ok_count = 0
    for src_rel, name, title, author in FILES:
        src = BASE / src_rel
        if not src.exists():
            print(f"  ПРОПУСК: {src_rel} (нет файла)")
            continue
        out = PDF_DIR / f"{name}.pdf"
        tmp_html = OUT / f"_{name}.html"
        # Этап 1: markdown -> html
        args_html = [
            str(src),
            "-o", str(tmp_html),
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
        ok, msg = run_pandoc(args_html, capture=True)
        if not ok:
            print(f"  HTML FAIL: {name} — {msg[:200] if msg else 'unknown'}")
            continue
        # Этап 2: html -> pdf
        try:
            from weasyprint import HTML
            HTML(string=tmp_html.read_text(encoding="utf-8")).write_pdf(str(out))
            tmp_html.unlink(missing_ok=True)
            if out.exists():
                size_kb = round(out.stat().st_size / 1024, 1)
                print(f"  OK: {name}.pdf ({size_kb} КБ)")
                ok_count += 1
            else:
                print(f"  PDF FAIL: {name}.pdf — не создан")
        except Exception as e:
            print(f"  PDF FAIL: {name}.pdf — {str(e)[:200]}")
    return ok_count

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    print(f"=== Сборка редакции v2 (target={target}) ===")
    print(f"Источник: {BASE}")
    print(f"Выход:    {OUT}")
    print()

    OUT.mkdir(parents=True, exist_ok=True)
    DOCX_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)

    docx_ok = pdf_ok = 0
    if target in ("all", "docx"):
        docx_ok = build_docx()
    if target in ("all", "pdf"):
        print()
        pdf_ok = build_pdf()

    print()
    print(f"=== Готово: DOCX {docx_ok}/{len(FILES)}, PDF {pdf_ok}/{len(FILES)} ===")
    print(f"DOCX: {DOCX_DIR}")
    print(f"PDF:  {PDF_DIR}")

if __name__ == "__main__":
    main()
