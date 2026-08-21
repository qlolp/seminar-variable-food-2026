# -*- coding: utf-8 -*-
"""Собрать HTML трёх версий и PDF через WeasyPrint; второй проход оглавления."""
import json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
SCRIPTS = ROOT / "scripts"
WIN_BASE = "BASE = 'C:/Users/Evgenii/AppData/Local/Temp/seminar-food/проект'"
LOCAL_BASE = f"BASE = {str(ROOT)!r}"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PLAYFAIR_FACES = """
@font-face { font-family:'Playfair Lat'; src:url('fonts/playfair-400-lat.woff2') format('woff2'); font-weight:400; }
@font-face { font-family:'Playfair Cyr'; src:url('fonts/playfair-400-cyr.woff2') format('woff2'); font-weight:400; }
@font-face { font-family:'Playfair Lat'; src:url('fonts/playfair-700-lat.woff2') format('woff2'); font-weight:700; }
@font-face { font-family:'Playfair Cyr'; src:url('fonts/playfair-700-cyr.woff2') format('woff2'); font-weight:700; }
@font-face { font-family:'Playfair Lat'; src:url('fonts/playfair-800-lat.woff2') format('woff2'); font-weight:800; }
@font-face { font-family:'Playfair Cyr'; src:url('fonts/playfair-800-cyr.woff2') format('woff2'); font-weight:800; }
@font-face { font-family:'Playfair Lat'; src:url('fonts/playfair-900-lat.woff2') format('woff2'); font-weight:900; }
@font-face { font-family:'Playfair Cyr'; src:url('fonts/playfair-900-cyr.woff2') format('woff2'); font-weight:900; }
@font-face { font-family:'Playfair Lat'; src:url('fonts/playfair-600i-lat.woff2') format('woff2'); font-weight:600; font-style:italic; }
@font-face { font-family:'Playfair Cyr'; src:url('fonts/playfair-600i-cyr.woff2') format('woff2'); font-weight:600; font-style:italic; }
"""

COLOR_FACES = """
@font-face { font-family:'PT Serif'; src:url('fonts/PTSerif-Regular.ttf'); }
@font-face { font-family:'PT Serif'; src:url('fonts/PTSerif-Bold.ttf'); font-weight:bold; }
@font-face { font-family:'PT Serif'; src:url('fonts/PTSerif-Italic.ttf'); font-style:italic; }
@font-face { font-family:'PT Sans'; src:url('fonts/PTSans-Regular.ttf'); }
@font-face { font-family:'PT Sans'; src:url('fonts/PTSans-Bold.ttf'); font-weight:bold; }
@font-face { font-family:'Noto Sans'; src:url('fonts/NotoSans-variable.ttf'); font-weight:100 900; }
"""


def run_builder(name):
    path = SCRIPTS / name
    src = path.read_text(encoding="utf-8").replace(WIN_BASE, LOCAL_BASE)
    ns = {"__name__": "__main__", "__file__": str(path)}
    os.chdir(ROOT)
    exec(compile(src, str(path), "exec"), ns)


def inject_css(html_path, extra):
    html = html_path.read_text(encoding="utf-8")
    if extra.strip() in html:
        return
    html = html.replace("<style>", "<style>\n" + extra, 1)
    html_path.write_text(html, encoding="utf-8")


def weasy(html, pdf):
    env = dict(os.environ)
    env["LANG"] = "C.UTF-8"
    print(f"weasyprint {html.name} → {pdf.name}", flush=True)
    r = subprocess.run(
        ["weasyprint", str(html), str(pdf)],
        cwd=str(OUT),
        env=env,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        print(r.stderr[-4000:], file=sys.stderr)
        raise SystemExit(f"weasyprint failed: {pdf}")
    from pypdf import PdfReader
    n = len(PdfReader(str(pdf)).pages)
    print(f"  {pdf.name}: {n} стр.", flush=True)
    return n


def headings_from_html(html_path):
    html = html_path.read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r'<h1 id="([^"]+)"[^>]*>(.*?)</h1>', html, re.S):
        aid = m.group(1)
        title = re.sub(r"<[^>]+>", "", m.group(2)).strip()
        title = re.sub(r"\s+", " ", title)
        if title and title != "НЕ ПРОСТО НАКОРМИТЬ":
            out.append((aid, title))
    return out


def extract_toc(pdf_path, headings):
    from pypdf import PdfReader
    reader = PdfReader(str(pdf_path))
    pages = []
    for i, p in enumerate(reader.pages):
        t = (p.extract_text() or "").replace("\n", " ")
        t = re.sub(r"\s+", " ", t)
        pages.append(t)
    # вариант без пробелов: WeasyPrint иногда извлекает заголовки с лишними
    # пробелами (например, «Часть IV . Одностраничные…»), что ломало поиск
    pages_n = [re.sub(r"\s+", "", t) for t in pages]
    # skip cover + TOC: pages that mention «Содержание» densely
    start = 0
    for i, t in enumerate(pages[:12]):
        if "Содержание" in t or t.count("Часть ") >= 3:
            start = i + 1
    result = {}
    cursor = start
    for aid, title in headings:
        needle = title[:36]
        needle_n = re.sub(r"\s+", "", needle)
        found = None
        for i in range(cursor, len(pages)):
            if needle in pages[i] or title[:24] in pages[i] or needle_n in pages_n[i]:
                found = i + 1
                cursor = i
                break
        if found:
            result[aid] = found
    print(f"  TOC matched {len(result)}/{len(headings)}", flush=True)
    return result


def main():
    print("1. markdown + official HTML", flush=True)
    run_builder("build.py")
    run_builder("build_html.py")
    print("2. color + beautiful HTML", flush=True)
    run_builder("build_color.py")
    run_builder("build_beautiful.py")

    inject_css(OUT / "_report_color.html", COLOR_FACES)
    inject_css(OUT / "_report_beautiful.html", PLAYFAIR_FACES)

    print("3. first-pass PDFs", flush=True)
    weasy(OUT / "_report.html", OUT / "_report.pdf")
    weasy(OUT / "_report_color.html", OUT / "_report_color.pdf")
    weasy(OUT / "_report_beautiful.html", OUT / "_report_beautiful.pdf")

    print("4. TOC from first pass", flush=True)
    toc = extract_toc(OUT / "_report.pdf", headings_from_html(OUT / "_report.html"))
    (OUT / "toc_pages.json").write_text(json.dumps(toc, ensure_ascii=False, indent=1), encoding="utf-8")
    toc_c = extract_toc(OUT / "_report_color.pdf", headings_from_html(OUT / "_report_color.html"))
    (OUT / "toc_pages_color.json").write_text(json.dumps(toc_c, ensure_ascii=False, indent=1), encoding="utf-8")

    print("5. rebuild HTML with TOC pages", flush=True)
    run_builder("build_html.py")
    run_builder("build_color.py")
    run_builder("build_beautiful.py")
    run_builder("build_claude.py")
    inject_css(OUT / "_report_color.html", COLOR_FACES)
    inject_css(OUT / "_report_beautiful.html", PLAYFAIR_FACES)

    print("6. final PDFs", flush=True)
    n_off = weasy(OUT / "_report.html", OUT / "Не_просто_накормить_доклад.pdf")
    n_col = weasy(OUT / "_report_color.html", OUT / "Не_просто_накормить_доклад_журнальный.pdf")
    n_bea = weasy(OUT / "_report_beautiful.html", OUT / "Не_просто_накормить_доклад_красивая_версия.pdf")
    n_claude = weasy(OUT / "_report_claude.html", OUT / "Не_просто_накормить_доклад_стиль_claude.pdf")
    # keep underscored aliases
    import shutil
    shutil.copy(OUT / "Не_просто_накормить_доклад.pdf", OUT / "_report.pdf")
    shutil.copy(OUT / "Не_просто_накормить_доклад_журнальный.pdf", OUT / "_report_color.pdf")
    shutil.copy(OUT / "Не_просто_накормить_доклад_красивая_версия.pdf", OUT / "_report_beautiful.pdf")
    print(json.dumps({"official": n_off, "journal": n_col, "beautiful": n_bea, "claude": n_claude}))


if __name__ == "__main__":
    main()
