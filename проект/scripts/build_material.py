# -*- coding: utf-8 -*-
"""Материал к сессии (2 стр. A4): chapters/../material_sessii.md → HTML (стиль claude) → PDF (WeasyPrint).
CSS переиспользуется из build_claude.py. Запуск из корня репозитория:
    python3 проект/scripts/build_material.py
Итог: проект/output/Материал_к_сессии_26_08.pdf"""
import os, re, subprocess, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'output')
SRC = os.path.join(BASE, 'material_sessii.md')

md = open(SRC, encoding='utf-8').read()
md = re.sub(r'^# .*\n', '', md, count=1)  # заголовок даём своим блоком

env = dict(os.environ); env['LANG'] = 'C.UTF-8'
frag = subprocess.run(
    ['pandoc', '-f', 'markdown+superscript+autolink_bare_uris', '-t', 'html', '--wrap=none'],
    input=md, capture_output=True, text=True, env=env).stdout

# CSS из build_claude.py (между 'CSS = """' и закрывающим '"""')
claude_src = open(os.path.join(BASE, 'scripts', 'build_claude.py'), encoding='utf-8').read()
a = claude_src.index('CSS = """') + len('CSS = """')
b = claude_src.index('"""', a)
css = claude_src[a:b]
# 2-страничная раздатка: A4, компактные поля, корпус крупнее, заголовки не с новой страницы
css = css.replace('</style>',
                  '\n@page { size: A4; margin: 12mm 14mm; }'
                  '\nhtml { font-size: 9.6pt; }'
                  '\nh2 { page-break-before: auto; margin: 9pt 0 4pt; }'
                  '\nh1 { margin: 0 0 4pt; }\nul, ol { margin: 3pt 0; }\nli { margin: 1.5pt 0; }\n</style>')

TITLE = '''
<div style="border-bottom:2.5pt solid #C15F3C; padding-bottom:6pt; margin-bottom:8pt;">
  <div style="font-family:'PT Sans'; font-size:8pt; letter-spacing:2.5pt; color:#87867F;">ПРОСТРАНСТВО НОВЫХ ИДЕЙ 2.0 · СЕМИНАР 25–27.08.2026</div>
  <div style="font-family:'Playfair Display'; font-weight:800; font-size:22pt; line-height:1.05; color:#141413; margin-top:3pt;">Не просто накормить — материал к сессии</div>
</div>
'''

html = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<title>Материал к сессии 26.08</title>' + css + '</head><body>'
        + TITLE + frag + '</body></html>')

html_path = os.path.join(OUT, '_material.html')
open(html_path, 'w', encoding='utf-8').write(html)
print('material HTML written:', len(html), 'chars')

pdf_path = os.path.join(OUT, 'Материал_к_сессии_26_08.pdf')
r = subprocess.run(['weasyprint', html_path, pdf_path], cwd=OUT, env=env,
                   capture_output=True, text=True)
if r.returncode != 0:
    sys.stderr.write((r.stderr or r.stdout or 'weasyprint failed')[-3000:])
    raise SystemExit('weasyprint failed on material')
try:
    from pypdf import PdfReader
    n = len(PdfReader(pdf_path).pages)
    print(f'PDF: {pdf_path} — {n} стр.')
except Exception:
    print(f'PDF: {pdf_path}')
