#!/usr/bin/env bash
# Идемпотентная установка окружения для сборки доклада и презентаций.
# Инструментарий: pandoc (MD → HTML), WeasyPrint (HTML → PDF),
# poppler-utils (pdfunite/pdfinfo), openpyxl (реестры XLSX), pypdf (оглавление).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

# --- Системные пакеты ---
# pandoc            — markdown+superscript → HTML во всех build_*.py
# poppler-utils     — pdfunite (склейка слайдов), pdfinfo/pdftoppm (проверка)
# lib*pango/cairo/… — нативные библиотеки рендеринга WeasyPrint
# fonts-dejavu-core — базовый фолбэк-шрифт (основные шрифты лежат в fonts/)
sudo apt-get update -qq
sudo apt-get install -y --no-install-recommends \
  pandoc \
  poppler-utils \
  libpango-1.0-0 \
  libpangocairo-1.0-0 \
  libgdk-pixbuf-2.0-0 \
  libcairo2 \
  libffi-dev \
  libjpeg-dev \
  shared-mime-info \
  fonts-dejavu-core

# --- Python-пакеты ---
# Ставим системно (sudo), чтобы CLI `weasyprint` попал в /usr/local/bin (в PATH):
# build-скрипты вызывают его через subprocess.
sudo pip3 install --break-system-packages -r requirements.txt

echo "Окружение готово: доклад — python3 проект/scripts/rebuild_pdfs.py;"
echo "презентация — python3 02_презентация/презентация_v5_21_слайд/build_v5.py --pdf"
