# -*- coding: utf-8 -*-
"""Создать PDF без резерва (только 18 основных страниц)."""
import os
import pypdfium2 as pdfium

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "Презентация_v6_Не_просто_накормить.pdf")
DST = os.path.join(os.path.dirname(HERE), "Презентация_v6_Не_просто_накормить_без_резерва.pdf")

pdf = pdfium.PdfDocument(SRC)
out = pdfium.PdfDocument.new()
out.import_pages(pdf, list(range(18)))
out.save(DST)
print(f"PDF без резерва: {DST}")
