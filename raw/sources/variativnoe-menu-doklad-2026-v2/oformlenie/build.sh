#!/bin/bash
# Сборка оформленных PDF/DOCX из неизменённого doklad.md (pandoc 3.6.4, WeasyPrint)
set -e; cd "$(dirname "$0")"; SRC=${1:-../doklad.md}
pandoc "$SRC" -s --toc --toc-depth=3 -N --lua-filter oformlenie.lua -c oformlenie.css -o doklad.html
weasyprint -q doklad.html doklad.pdf
pandoc "$SRC" --toc --toc-depth=3 -N --lua-filter oformlenie.lua --reference-doc reference.docx -o doklad.docx
