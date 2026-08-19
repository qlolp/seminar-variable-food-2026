# -*- coding: utf-8 -*-
"""Собрать 3 PDF версии доклада через Edge headless (обход WeasyPrint).
Использует build.py + build_html.py + build_color.py + build_beautiful.py,
затем рендерит HTML→PDF через msedge.exe --headless --print-to-pdf."""
import os, re, sys, json, subprocess, time, shutil
from pathlib import Path

ROOT = Path(r"C:\Users\Evgenii\OneDrive\Desktop\seminar\seminar-variable-food-2026\проект")
OUT  = ROOT / "output"
SCRIPTS = ROOT / "scripts"
WIN_BASE = "BASE = 'C:/Users/Evgenii/AppData/Local/Temp/seminar-food/проект'"
LOCAL_BASE = f"BASE = {str(ROOT)!r}"

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
TARGETS = {
    "_report.html":            (ROOT.parent / "01_доклад" / "Не_просто_накормить_доклад_официальный.pdf"),
    "_report_color.html":      (ROOT.parent / "01_доклад" / "Не_просто_накормить_доклад_журнальный.pdf"),
    "_report_beautiful.html":  (ROOT.parent / "01_доклад" / "Не_просто_накормить_доклад_красивая_версия.pdf"),
}


def run_builder(name):
    """Запустить build-скрипт с подменой путей."""
    path = SCRIPTS / name
    src = path.read_text(encoding="utf-8").replace(WIN_BASE, LOCAL_BASE)
    ns = {"__name__": "__main__", "__file__": str(path)}
    os.chdir(ROOT)
    print(f"  → {name}", flush=True)
    exec(compile(src, str(path), "exec"), ns)


def headless_render(html_path: Path, pdf_path: Path):
    """Render HTML→PDF via Edge headless."""
    if not Path(EDGE).exists():
        raise FileNotFoundError(f"Edge not found: {EDGE}")
    file_url = "file:///" + str(html_path).replace("\\", "/").lstrip("/")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    if pdf_path.exists():
        pdf_path.unlink()
    cmd = [
        EDGE,
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--no-sandbox",
        f"--print-to-pdf={pdf_path}",
        file_url,
    ]
    print(f"  Edge → {pdf_path.name}", flush=True)
    r = subprocess.run(cmd, capture_output=True, timeout=120)
    if r.returncode != 0:
        print(f"    stderr: {r.stderr.decode('utf-8', errors='replace')[-2000:]}", file=sys.stderr)
        raise SystemExit(f"Edge failed for {html_path.name}")
    time.sleep(0.3)
    if pdf_path.exists() and pdf_path.stat().st_size > 5000:
        size_kb = round(pdf_path.stat().st_size / 1024, 1)
        print(f"    OK ({size_kb} KB)", flush=True)
    else:
        raise SystemExit(f"PDF not produced: {pdf_path}")


def main():
    print("=" * 60, flush=True)
    print("Пересборка doklad (3 PDF версии) через Edge headless", flush=True)
    print("=" * 60, flush=True)

    print("\n[1/2] Сборка MD и HTML (4 стадии):", flush=True)
    run_builder("build.py")
    run_builder("build_html.py")
    run_builder("build_color.py")
    run_builder("build_beautiful.py")

    print("\n[2/2] Edge headless рендер HTML → PDF:", flush=True)
    for html_name, pdf_path in TARGETS.items():
        html_path = OUT / html_name
        if not html_path.exists():
            print(f"  MISSING: {html_name}", flush=True)
            continue
        headless_render(html_path, pdf_path)

    print("\n" + "=" * 60, flush=True)
    print("Готово. PDF:", flush=True)
    for html_name, pdf_path in TARGETS.items():
        if pdf_path.exists():
            size_mb = round(pdf_path.stat().st_size / 1024 / 1024, 2)
            print(f"  {pdf_path.name}: {size_mb} MB", flush=True)
    print("=" * 60, flush=True)


if __name__ == "__main__":
    main()
