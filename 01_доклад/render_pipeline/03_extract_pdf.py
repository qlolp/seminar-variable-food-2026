"""Extract text + table structure from the source seminar PDF.

Writes two artifacts:
  C:/Users/Evgenii/.mavis/agents/mavis/workspace/seminar_text.md
  C:/Users/Evgenii/.mavis/agents/mavis/workspace/seminar_meta.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pdfplumber

SRC = Path("/mnt/c/Users/Evgenii/OneDrive/Desktop/seminar/seminar_variable_food_2026/output/Доклад_для_семинара.pdf")
OUT_MD = Path("/mnt/c/Users/Evgenii/.mavis/agents/mavis/workspace/seminar_text.md")
OUT_META = Path("/mnt/c/Users/Evgenii/.mavis/agents/mavis/workspace/seminar_meta.json")


def main() -> int:
    if not SRC.exists():
        print(f"FAIL: source not found: {SRC}", file=sys.stderr)
        return 1

    size_kb = round(SRC.stat().st_size / 1024, 1)
    pages: list[str] = []
    table_count = 0

    with pdfplumber.open(SRC) as pdf:
        page_total = len(pdf.pages)
        for idx, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            tables = page.extract_tables() or []
            if tables:
                table_count += len(tables)
                text += "\n\n[TABLES_DETECTED]\n"
                for t_idx, t in enumerate(tables, start=1):
                    text += f"\nTable {t_idx}:\n"
                    for row in t:
                        text += " | ".join((c or "").replace("\n", " ") for c in row) + "\n"
            pages.append(f"\n\n===== PAGE {idx}/{page_total} =====\n\n{text}")

    OUT_MD.write_text("\n".join(pages), encoding="utf-8")

    meta = {
        "source": str(SRC),
        "size_kb": size_kb,
        "page_count": page_total,
        "table_count": table_count,
        "text_chars": sum(len(p) for p in pages),
    }
    OUT_META.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
