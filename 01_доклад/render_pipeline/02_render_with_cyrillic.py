"""Render the seminar PDF with proper Cyrillic fonts.

This script runs the minimax-pdf CREATE pipeline but injects Cyrillic
TTF fonts into the tokens.json before render_body.py is called.

We use DejaVu Serif (display) + DejaVu Sans (body) — both have full
Cyrillic coverage and pair well for a serious scientific report.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Source files
CONTENT_JSON = Path("/mnt/c/Users/Evgenii/.mavis/agents/mavis/workspace/seminar_content.json")
OUTPUT_PDF   = Path("/mnt/c/Users/Evgenii/.mavis/agents/mavis/workspace/seminar_beautiful.pdf")
TOKENS_JSON  = Path("/mnt/c/Users/Evgenii/.mavis/agents/mavis/workspace/tokens_cyrillic.json")

# TTF fonts (Cyrillic-supporting, on the WSL mount of Windows fonts)
WIN_FONTS = Path("/mnt/c/Windows/Fonts")
FONT_DISPLAY     = WIN_FONTS / "DejaVuSerif-Bold.ttf"        # headings
FONT_DISPLAY_IT  = WIN_FONTS / "DejaVuSerif.ttf"             # heading italic / display
FONT_BODY        = WIN_FONTS / "DejaVuSans.ttf"              # body
FONT_BODY_BOLD   = WIN_FONTS / "DejaVuSans-Bold.ttf"         # bold body
FONT_BODY_ITALIC = WIN_FONTS / "DejaVuSans-Oblique.ttf"      # italic body


def main() -> int:
    # 1. Verify all fonts exist
    for f in (FONT_DISPLAY, FONT_DISPLAY_IT, FONT_BODY, FONT_BODY_BOLD, FONT_BODY_ITALIC):
        if not f.exists():
            print(f"FAIL: font not found: {f}", file=sys.stderr)
            return 1

    # 2. Generate tokens via palette.py
    workdir = Path(tempfile.mkdtemp(prefix="pdf_work_"))
    tokens_path = workdir / "tokens.json"
    cmd = [
        "python3",
        "/mnt/c/Users/Evgenii/.minimax/skills/minimax-pdf/scripts/palette.py",
        "--title", "НЕ ПРОСТО НАКОРМИТЬ",
        "--type", "report",
        "--author", "Е. В. Чистяков, директор СПб ГАСУСОН «ДСО Серафимовский»",
        "--date", "25–27 августа 2026",
        "--accent", "#2A5A6B",
        "--out", str(tokens_path),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("palette.py failed:", res.stderr, file=sys.stderr)
        return 1

    # 3. Inject Cyrillic font configuration into tokens.json
    with open(tokens_path, encoding="utf-8") as f:
        tokens = json.load(f)
    tokens["font_paths"] = {
        "DejaVuSerif-Bold":   str(FONT_DISPLAY),
        "DejaVuSerif":        str(FONT_DISPLAY_IT),
        "DejaVuSans":         str(FONT_BODY),
        "DejaVuSans-Bold":    str(FONT_BODY_BOLD),
        "DejaVuSans-Oblique": str(FONT_BODY_ITALIC),
    }
    tokens["font_display_rl"] = "DejaVuSerif-Bold"
    tokens["font_body_rl"]    = "DejaVuSans"
    tokens["font_body_b_rl"]  = "DejaVuSans-Bold"
    # Keep the Google Fonts CSS for the cover
    with open(tokens_path, "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=2, ensure_ascii=False)
    print(f"  ✓ Tokens with Cyrillic fonts: {tokens_path}")

    # Copy tokens to a stable location for reuse
    shutil.copy(tokens_path, TOKENS_JSON)

    # 4. Render cover via cover.py + render_cover.js
    cover_html = workdir / "cover.html"
    cover_pdf  = workdir / "cover.pdf"
    subprocess.run([
        "python3",
        "/mnt/c/Users/Evgenii/.minimax/skills/minimax-pdf/scripts/cover.py",
        "--tokens", str(tokens_path),
        "--out", str(cover_html),
        "--subtitle", "Научно-аналитический доклад для межрегионального семинара «Пространство Новых Идей 2.0»",
    ], check=True)

    subprocess.run([
        "node",
        "/mnt/c/Users/Evgenii/.minimax/skills/minimax-pdf/scripts/render_cover.js",
        "--input", str(cover_html),
        "--out",   str(cover_pdf),
    ], check=True)
    print(f"  ✓ Cover rendered: {cover_pdf}")

    # 5. Render body
    body_pdf = workdir / "body.pdf"
    subprocess.run([
        "python3",
        "/mnt/c/Users/Evgenii/.minimax/skills/minimax-pdf/scripts/render_body.py",
        "--tokens",  str(tokens_path),
        "--content", str(CONTENT_JSON),
        "--out",     str(body_pdf),
    ], check=True)
    print(f"  ✓ Body rendered: {body_pdf}")

    # 6. Merge
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    if OUTPUT_PDF.exists():
        OUTPUT_PDF.unlink()
    subprocess.run([
        "python3",
        "/mnt/c/Users/Evgenii/.minimax/skills/minimax-pdf/scripts/merge.py",
        "--cover", str(cover_pdf),
        "--body",  str(body_pdf),
        "--out",   str(OUTPUT_PDF),
        "--title", "НЕ ПРОСТО НАКОРМИТЬ",
    ], check=True)

    size_kb = round(OUTPUT_PDF.stat().st_size / 1024, 1)
    print(f"\n✓ DONE — {OUTPUT_PDF} ({size_kb} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
