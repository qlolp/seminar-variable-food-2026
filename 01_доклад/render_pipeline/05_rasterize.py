"""Rasterize a few pages of the new PDF for visual inspection."""
import sys
from pathlib import Path

try:
    import pypdfium2 as pdfium
except ImportError:
    print("pypdfium2 not installed", file=sys.stderr)
    sys.exit(1)

PDF = Path("/mnt/c/Users/Evgenii/.mavis/agents/mavis/workspace/seminar_beautiful.pdf")
OUT_DIR = Path("/mnt/c/Users/Evgenii/.mavis/agents/mavis/workspace/preview")
OUT_DIR.mkdir(parents=True, exist_ok=True)

pdf = pdfium.PdfDocument(str(PDF))
# Render cover, table of contents-like area, mid-content, and last
for label, idx in [("cover", 0), ("chapter1", 1), ("chapter2-start", 16), ("mid", 100), ("appendix", 200), ("last", len(pdf)-1)]:
    if idx >= len(pdf):
        continue
    page = pdf[idx]
    img = page.render(scale=1.5).to_pil()
    out = OUT_DIR / f"page_{label}_{idx+1:03d}.png"
    img.save(out)
    print(f"  rendered {label} → {out}  ({img.size[0]}x{img.size[1]})")
