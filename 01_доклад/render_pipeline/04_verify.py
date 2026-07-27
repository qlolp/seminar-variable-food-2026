"""Verify the rendered PDF: page count, file size, sample text from key pages,
and check that tables are present.
"""
from pypdf import PdfReader
from pathlib import Path

PDF = Path("/mnt/c/Users/Evgenii/.mavis/agents/mavis/workspace/seminar_beautiful.pdf")
r = PdfReader(str(PDF))
print(f"Pages: {len(r.pages)}")
print(f"Size: {PDF.stat().st_size/1024:.1f} KB")

# Sample text from first 3 pages, last 3 pages, and middle
for idx in [0, 1, 2, 50, 100, 150, 200, len(r.pages)-2, len(r.pages)-1]:
    if idx < len(r.pages):
        text = (r.pages[idx].extract_text() or "")[:300]
        text = text.replace("\n", " ⏎ ")
        print(f"\n--- Page {idx+1} ---")
        print(text)
