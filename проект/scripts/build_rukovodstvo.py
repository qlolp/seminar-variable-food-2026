# -*- coding: utf-8 -*-
"""«Не просто накормить» — методическое руководство (читаемая версия ~100 стр.).
chapters источник: проект/rukovodstvo.md → HTML (стиль claude) → PDF (WeasyPrint).
Запуск из корня репозитория:
    python3 проект/scripts/build_rukovodstvo.py
Итог: проект/output/Не_просто_накормить_РУКОВОДСТВО.pdf"""
import os, re, subprocess, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'output')
SRC = os.path.join(BASE, 'rukovodstvo.md')

md = open(SRC, encoding='utf-8').read()
# первый H1 и подзаголовок отдаём своим титульным блоком
md = re.sub(r'\A# .*\n(## .*\n)?', '', md, count=1)

env = dict(os.environ); env['LANG'] = 'C.UTF-8'
frag = subprocess.run(
    ['pandoc', '-f', 'markdown+superscript+autolink_bare_uris', '-t', 'html', '--wrap=none'],
    input=md, capture_output=True, text=True, env=env).stdout

claude_src = open(os.path.join(BASE, 'scripts', 'build_claude.py'), encoding='utf-8').read()
a = claude_src.index('CSS = """') + len('CSS = """')
b = claude_src.index('"""', a)
css = claude_src[a:b]
css = css.replace('</style>',
                  '\n@page { size: A4; margin: 20mm 22mm; }'
                  '\nhtml { font-size: 11.3pt; }'
                  '\nbody { line-height: 1.5; }'
                  '\np { margin: 0 0 8pt; text-align: justify; }'
                  '\nh2 { page-break-before: always; margin: 0 0 8pt; }'
                  '\nh3 { margin: 14pt 0 5pt; }\nh1 { margin: 0 0 6pt; }\n</style>')

COVER = '''
<div style="page-break-after:always; padding:34mm 0 0;">
  <div style="font-family:'PT Sans'; font-size:9pt; letter-spacing:3pt; color:#87867F; margin-bottom:24mm;">МЕТОДИЧЕСКОЕ РУКОВОДСТВО ДЛЯ РУКОВОДИТЕЛЕЙ И ПРАКТИКОВ</div>
  <div style="font-family:'Playfair Display'; font-weight:800; font-size:46pt; line-height:1.03; color:#141413;">Не просто<br>накормить</div>
  <div style="width:70pt; height:3pt; background:#C15F3C; margin:16pt 0 18pt;"></div>
  <p style="font-family:'Playfair Display'; font-style:italic; font-size:15pt; line-height:1.45; color:#3D3929; margin:0 0 14pt;">Как организовать безопасное, достойное и вариативное питание людей с психическими нарушениями в домах социального обслуживания</p>
  <p style="font-family:'PT Serif'; font-size:11pt; line-height:1.6; color:#6E6A5E; margin:0;">Связное руководство, которое читается подряд и к которому возвращаются за ответом. Проверяемые источники, честные оговорки о границах данных, разбор ситуаций.</p>
  <p style="font-family:'PT Serif'; font-size:11.5pt; color:#C15F3C; margin-top:26pt;">Чистяков Е. В., директор СПб ГАСУСОН «ДСО „Серафимовский“»</p>
</div>
'''

html = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<title>Не просто накормить — руководство</title>' + css + '</head><body>'
        + COVER + frag + '</body></html>')

html_path = os.path.join(OUT, '_rukovodstvo.html')
open(html_path, 'w', encoding='utf-8').write(html)
print('HTML written:', len(html), 'chars')

pdf_path = os.path.join(OUT, 'Не_просто_накормить_РУКОВОДСТВО.pdf')
r = subprocess.run(['weasyprint', html_path, pdf_path], cwd=OUT, env=env,
                   capture_output=True, text=True)
if r.returncode != 0:
    sys.stderr.write((r.stderr or r.stdout or 'weasyprint failed')[-3000:])
    raise SystemExit('weasyprint failed')
try:
    from pypdf import PdfReader
    print(f'PDF: {pdf_path} — {len(PdfReader(pdf_path).pages)} стр.')
except Exception:
    print('PDF:', pdf_path)
