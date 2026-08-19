#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Собрать 30 HTML-слайдов в один PDF через Edge headless, затем склеить через pypdf."""
import os
import subprocess
import time
from pathlib import Path

ROOT = Path(r"C:\Users\Evgenii\OneDrive\Desktop\seminar\pres_v2")
SLIDES = ROOT / "slides"
TMP = ROOT / "out"
TMP.mkdir(exist_ok=True)
PDF_FINAL = ROOT / "Не_просто_накормить_презентация_v2.pdf"

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# 1. Конвертируем каждый слайд в PDF
slide_pdfs = []
for html in sorted(SLIDES.glob("slide-*.html")):
    pdf = TMP / (html.stem + ".pdf")
    file_url = "file:///" + str(html).replace("\\", "/").lstrip("/")
    cmd = [EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
           f"--print-to-pdf={pdf}", file_url]
    print(f"Converting {html.name} -> {pdf.name} ...", end=" ", flush=True)
    subprocess.run(cmd, capture_output=True, timeout=60)
    if pdf.exists() and pdf.stat().st_size > 1000:
        print(f"OK ({pdf.stat().st_size} bytes)")
        slide_pdfs.append(pdf)
    else:
        print("FAIL")
    time.sleep(0.3)  # гонка Edge

print(f"\nTotal slide PDFs: {len(slide_pdfs)}")

# 2. Склеиваем через pypdf
if len(slide_pdfs) != 30:
    print(f"WARNING: expected 30, got {len(slide_pdfs)}")

from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf in slide_pdfs:
    reader = PdfReader(str(pdf))
    for page in reader.pages:
        writer.add_page(page)

with open(PDF_FINAL, "wb") as f:
    writer.write(f)

print(f"\nFINAL PDF: {PDF_FINAL}")
print(f"Size: {PDF_FINAL.stat().st_size} bytes")
print(f"Pages: {len(slide_pdfs)}")
