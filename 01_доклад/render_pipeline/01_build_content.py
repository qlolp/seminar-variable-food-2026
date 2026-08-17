"""Smart parser v2 — handles multi-line chapter titles, skips TOC, filters false positives."""
from __future__ import annotations

import json
import re
from pathlib import Path

SRC = Path("data/seminar_text.md")
OUT = Path("data/seminar_content.json")

# Skip the first 8 pages (cover + 2 TOC pages + 4 intro pages + 1 extra intro)
SKIP_PAGES = 8

# Patterns
PART_RE      = re.compile(r"^ЧАСТЬ\s+([IVX]+)\.\s*(.*)$")
CHAPTER_RE   = re.compile(r"^Глава\s+(\d+)\.\s*(.*)$")
APPENDIX_RE  = re.compile(r"^Приложение\s+([А-ЯA-Z]\d+)\.\s*(.*)$")
CASE_RE      = re.compile(r"^Кейс\s+(\d+)\.\s*(.*)$")
SUBSECTION_RE = re.compile(r"^(\d+\.\d+)\.?\s+(.+)$")
NAMED_SECTION_RE = re.compile(
    r"^(Конфликт|Уровень|Шаг|Этап|Принцип|Правило|Раздел|Модель|Мера|Рекомендация|Вариант)\s+(\d+(?:\.\d+)?)\.?\s+(.*)$"
)
PAGE_MARKER_RE = re.compile(r"^=+\s*PAGE\s+\d+/\d+\s*=+\s*$")


def parse_table_block(text: str) -> list | None:
    """Parse a [TABLES_DETECTED] block. Returns list of {headers, rows}."""
    parts = re.split(r"\nTable\s+(\d+):\n", "\n" + text)
    if len(parts) < 3:
        return None
    tables = []
    for i in range(1, len(parts), 2):
        body = parts[i + 1] if i + 1 < len(parts) else ""
        rows = []
        for line in body.splitlines():
            line = line.strip()
            if not line:
                continue
            cells = [c.strip() for c in line.split(" | ")]
            rows.append(cells)
        if len(rows) < 2:
            continue
        # Find a real header row (one that doesn't have many empty cells)
        header_idx = 0
        for ri, r in enumerate(rows[:3]):
            non_empty = sum(1 for c in r if c)
            if non_empty >= max(1, len(r) // 2):
                header_idx = ri
                break
        headers = rows[header_idx]
        data_rows = rows[header_idx + 1:]
        if not data_rows:
            continue
        ncols = max(len(headers), max((len(r) for r in data_rows), default=0))
        if ncols == 0:
            continue
        if len(headers) < ncols:
            headers = headers + [""] * (ncols - len(headers))
        data_rows = [r + [""] * (ncols - len(r)) if len(r) < ncols else r[:ncols] for r in data_rows]
        # Drop completely-empty rows
        data_rows = [r for r in data_rows if any(c.strip() for c in r)]
        if not data_rows:
            continue
        tables.append({"headers": headers, "rows": data_rows})
    return tables or None


def is_chapter_title_line(text: str) -> bool:
    """A standalone line is a chapter title if it starts with Глава N. and
    isn't a parenthetical reference inside another sentence."""
    m = CHAPTER_RE.match(text)
    if not m:
        return False
    # Filter out references like "Глава 30 (дисциплина труда)"
    if "(" in text and ")" in text:
        return False
    # Filter out "...см. Главу 5" type references — these are body text
    if text.endswith((",", ";", "—", "-")):
        return False
    if len(text) > 200:
        return False
    return True


def main() -> int:
    raw = SRC.read_text(encoding="utf-8")
    page_chunks = re.split(r"\n=+\s*PAGE\s+\d+/\d+\s*=+\s*\n", raw)
    body_chunks = page_chunks[SKIP_PAGES:]
    if not body_chunks:
        print("FAIL: no body pages found", file=sys.stderr)
        return 1

    blocks: list[dict] = []

    # Build a flat list of (line, source_page) for sequential processing
    flat_lines: list[tuple[str, int]] = []
    for page_idx, chunk in enumerate(body_chunks, start=SKIP_PAGES + 1):
        for ln in chunk.splitlines():
            ln = ln.strip()
            if not ln:
                continue
            flat_lines.append((ln, page_idx))

    # Walk lines; assemble into blocks
    i = 0
    n = len(flat_lines)
    while i < n:
        line, page = flat_lines[i]

        # Skip page markers if any leaked in
        if PAGE_MARKER_RE.match(line):
            i += 1
            continue

        # Skip pdfplumber's [TABLES_DETECTED] separator
        if line.strip() in ("[TABLES_DETECTED]", "[TABLES_DETECTED]."):
            i += 1
            continue

        # PART
        m = PART_RE.match(line)
        if m and not line.endswith((",", ";", ".", "—")):
            blocks.append({"type": "pagebreak"})
            blocks.append({"type": "h1", "text": f"ЧАСТЬ {m.group(1)}. {m.group(2).strip().upper() if m.group(2).strip() else m.group(1)}".rstrip(" .")})
            i += 1
            continue

        # Глава (chapter) — handle multi-line title
        m = CHAPTER_RE.match(line)
        if m and is_chapter_title_line(line):
            num = m.group(1)
            name = m.group(2).strip()
            # Look ahead for continuation lines (lines that don't end with period and are short
            # and aren't a new section marker)
            j = i + 1
            continuation_words = []
            while j < n:
                next_line, _ = flat_lines[j]
                if PAGE_MARKER_RE.match(next_line):
                    break
                if (PART_RE.match(next_line) or CHAPTER_RE.match(next_line) or
                    APPENDIX_RE.match(next_line) or CASE_RE.match(next_line) or
                    SUBSECTION_RE.match(next_line) or NAMED_SECTION_RE.match(next_line)):
                    break
                # Continuation heuristic: short, no terminal punctuation, not bullet, not body
                # Body lines tend to be > 60 chars; chapter title continuations are very short
                if (len(next_line) < 60 and
                    not next_line.endswith((".", "!", "?", ":", ";")) and
                    not next_line.startswith(("  ", "•", "-", "*")) and
                    not next_line.startswith("Table ") and
                    "==" not in next_line and
                    not next_line.startswith("[") and
                    # Body lines often have lots of words; continuations usually 1-3 words
                    len(next_line.split()) <= 5):
                    continuation_words.append(next_line)
                    j += 1
                else:
                    break
            full_title = name
            if continuation_words:
                full_title = (name + " " + " ".join(continuation_words)).strip()
            blocks.append({"type": "pagebreak"})
            blocks.append({"type": "h1", "text": f"Глава {num}. {full_title}"})
            i = j
            continue

        # Приложение (multi-line possible)
        m = APPENDIX_RE.match(line)
        if m:
            code = m.group(1)
            name = m.group(2).strip()
            j = i + 1
            continuation_words = []
            while j < n:
                next_line, _ = flat_lines[j]
                if (PART_RE.match(next_line) or CHAPTER_RE.match(next_line) or
                    APPENDIX_RE.match(next_line) or CASE_RE.match(next_line) or
                    SUBSECTION_RE.match(next_line) or NAMED_SECTION_RE.match(next_line)):
                    break
                # Skip bracket markers and [TABLES_DETECTED] in continuations
                if next_line.startswith("[") or next_line.strip() in ("[TABLES_DETECTED]", "[TABLES_DETECTED]."):
                    j += 1
                    continue
                if (len(next_line) < 60 and
                    not next_line.endswith((".", "!", "?", ":", ";")) and
                    not next_line.startswith(("  ", "•", "-", "*")) and
                    "==" not in next_line and
                    len(next_line.split()) <= 5):
                    continuation_words.append(next_line)
                    j += 1
                else:
                    break
            full_title = name + (" " + " ".join(continuation_words) if continuation_words else "")
            full_title = full_title.strip()
            blocks.append({"type": "pagebreak"})
            blocks.append({"type": "h1", "text": f"Приложение {code}. {full_title}"})
            i = j
            continue

        # Кейс (with possible multi-line)
        m = CASE_RE.match(line)
        if m:
            num = m.group(1)
            name = m.group(2).strip()
            j = i + 1
            continuation_words = []
            while j < n:
                next_line, _ = flat_lines[j]
                if (PART_RE.match(next_line) or CHAPTER_RE.match(next_line) or
                    APPENDIX_RE.match(next_line) or CASE_RE.match(next_line) or
                    SUBSECTION_RE.match(next_line) or NAMED_SECTION_RE.match(next_line)):
                    break
                if (len(next_line) < 100 and
                    not next_line.startswith(("  ", "•", "-", "*")) and
                    "==" not in next_line and
                    not next_line.endswith((".", "!", "?", ":", ";")) and
                    len(next_line.split()) <= 8):
                    continuation_words.append(next_line)
                    j += 1
                else:
                    break
            full_title = name + (" " + " ".join(continuation_words) if continuation_words else "")
            full_title = full_title.strip()
            blocks.append({"type": "h2", "text": f"Кейс {num}. {full_title}"})
            i = j
            continue

        # N.M. subsection
        m = SUBSECTION_RE.match(line)
        if m and len(line) < 120 and not line.endswith((",", ";")):
            blocks.append({"type": "h2", "text": f"{m.group(1)}. {m.group(2).strip()}"})
            i += 1
            continue

        # Named section
        m = NAMED_SECTION_RE.match(line)
        if m and len(line) < 120 and not line.endswith((",", ";")):
            blocks.append({"type": "h2", "text": line})
            i += 1
            continue

        # Inline tables — the [TABLES_DETECTED] markers are placed AFTER a paragraph
        # in the extracted text. We handle them by joining adjacent lines.
        # For now, just emit line as body or part of table.

        # Bullet?
        if line.startswith(("  ", "•", "-", "*")):
            text_part = re.sub(r"^[\s•\-*]+", "", line).strip()
            if text_part:
                blocks.append({"type": "bullet", "text": text_part})
            i += 1
            continue

        # Table line?
        if line.startswith("Table "):
            # Start a table block — collect following lines until blank/non-table
            table_lines = [line]
            j = i + 1
            while j < n:
                nl, _ = flat_lines[j]
                if (PAGE_MARKER_RE.match(nl) or PART_RE.match(nl) or
                    CHAPTER_RE.match(nl) or APPENDIX_RE.match(nl) or
                    CASE_RE.match(nl) or SUBSECTION_RE.match(nl) or
                    NAMED_SECTION_RE.match(nl)):
                    break
                # Stop at next "Table N:" — each table is parsed independently
                if nl.startswith("Table "):
                    break
                # Skip standalone [TABLES_DETECTED] markers if they leak in
                if nl.strip() in ("[TABLES_DETECTED]", "[TABLES_DETECTED]."):
                    j += 1
                    continue
                if " | " in nl or len(nl.split()) < 12:
                    table_lines.append(nl)
                    j += 1
                else:
                    break
            # Convert table_lines into a single [TABLES_DETECTED] synthetic block
            synth = "\n".join(table_lines)
            tables = parse_table_block(synth)
            if tables:
                for t in tables:
                    blocks.append({"type": "table", "headers": t["headers"], "rows": t["rows"]})
            else:
                # Fallback: emit as body
                blocks.append({"type": "body", "text": " ".join(table_lines)})
            i = j
            continue

        # Default: body — but strip [TABLES_DETECTED] if it's a suffix
        clean_line = re.sub(r"\s*\[TABLES_DETECTED\]\s*\.?\s*$", "", line)
        if clean_line:
            blocks.append({"type": "body", "text": clean_line})
        i += 1

    # Final pass: merge adjacent body blocks into single paragraphs
    # Also collapse adjacent pagebreaks
    merged: list[dict] = []
    body_buf: list[str] = []
    last_was_pagebreak = False
    for b in blocks:
        if b.get("type") == "body":
            body_buf.append(b.get("text", ""))
            last_was_pagebreak = False
        elif b.get("type") == "pagebreak":
            if not last_was_pagebreak:
                merged.append(b)
            last_was_pagebreak = True
        else:
            if body_buf:
                merged.append({"type": "body", "text": " ".join(body_buf)})
                body_buf = []
            merged.append(b)
            last_was_pagebreak = False
    if body_buf:
        merged.append({"type": "body", "text": " ".join(body_buf)})

    # Strip leading pagebreak(s) — the body should start with content, not a blank page
    while merged and merged[0].get("type") == "pagebreak":
        merged.pop(0)

    OUT.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")

    type_counts: dict[str, int] = {}
    for b in merged:
        t = b.get("type", "?")
        type_counts[t] = type_counts.get(t, 0) + 1
    print(f"Wrote {OUT} ({OUT.stat().st_size//1024} KB)")
    print(f"Total blocks: {len(merged)}")
    for t, n in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {t:12} × {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
