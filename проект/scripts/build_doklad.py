# -*- coding: utf-8 -*-
"""«Доклад» (10–12 стр. A4): chapters/../doklad.md → HTML (стиль claude) → PDF (WeasyPrint).
CSS переиспользуется из build_claude.py. Запуск из корня репозитория:
    python3 проект/scripts/build_doklad.py
Итог: проект/output/Не_просто_накормить_ДОКЛАД_10-12.pdf"""
import os, re, subprocess, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'output')
SRC = os.path.join(BASE, 'doklad.md')

md = open(SRC, encoding='utf-8').read()
md = re.sub(r'^# .*\n', '', md, count=1)  # титул даём своим блоком

env = dict(os.environ); env['LANG'] = 'C.UTF-8'
frag = subprocess.run(
    ['pandoc', '-f', 'markdown+superscript+autolink_bare_uris', '-t', 'html', '--wrap=none'],
    input=md, capture_output=True, text=True, env=env).stdout

claude_src = open(os.path.join(BASE, 'scripts', 'build_claude.py'), encoding='utf-8').read()
a = claude_src.index('CSS = """') + len('CSS = """')
b = claude_src.index('"""', a)
css = claude_src[a:b]
# доклад: A4, книжные поля, корпус читаемый, каждый раздел (h2) — с новой страницы не заставляем
css = css.replace('</style>',
                  '\n@page { size: A4; margin: 18mm 20mm; }'
                  '\nhtml { font-size: 11.5pt; }'
                  '\nbody { line-height: 1.5; }'
                  '\np { margin: 0 0 7pt; }'
                  '\nh2 { page-break-before: auto; margin: 13pt 0 5pt; }'
                  '\nh1 { margin: 0 0 6pt; }\n</style>')

COVER = '''
<div style="page-break-after:always; padding:26mm 0 0;">
  <div style="font-family:'PT Sans'; font-size:9pt; letter-spacing:3pt; color:#87867F; margin-bottom:20mm;">ПРОСТРАНСТВО НОВЫХ ИДЕЙ 2.0 · СЕМИНАР 25–27.08.2026</div>
  <div style="font-family:'PT Sans'; font-size:9.5pt; letter-spacing:3pt; color:#C15F3C; margin-bottom:10pt;">ДОКЛАД · 20 МИНУТ ЧТЕНИЯ · ОДИН ТЕЗИС НА РАЗДЕЛ</div>
  <div style="font-family:'Playfair Display'; font-weight:800; font-size:40pt; line-height:1.05; color:#141413;">Не просто<br>накормить</div>
  <div style="width:64pt; height:3pt; background:#C15F3C; margin:13pt 0 15pt;"></div>
  <p style="font-family:'Playfair Display'; font-style:italic; font-size:14pt; line-height:1.45; color:#3D3929; margin:0 0 10pt;">Как право выбора доходит до тарелки: безопасность, документы и пилот в домах социального обслуживания</p>
  <div style="font-family:'PT Sans'; font-size:10pt; line-height:1.7; color:#3D3929; margin-top:16pt;">
    <p style="margin:0 0 6pt;">Дискуссия «Организация питания: опыт реализации проектов» · 26.08.2026, 14:00–15:30<br>Площадка № 2 — ДСО «Тесовый берег» · модераторы: Чистяков Е. В., Нурбаев Т. А.</p>
    <p style="margin:0; color:#C15F3C; font-family:'PT Serif'; font-size:11pt;">Чистяков Е. В., директор СПб ГАСУСОН «ДСО „Серафимовский“» · версия 1.0 · сверка 22.08.2026</p>
  </div>
</div>
'''

html = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<title>Не просто накормить — доклад</title>' + css + '</head><body>'
        + COVER + frag + '</body></html>')

html_path = os.path.join(OUT, '_doklad.html')
open(html_path, 'w', encoding='utf-8').write(html)
print('doklad HTML written:', len(html), 'chars')

pdf_path = os.path.join(OUT, 'Не_просто_накормить_ДОКЛАД_10-12.pdf')
r = subprocess.run(['weasyprint', html_path, pdf_path], cwd=OUT, env=env,
                   capture_output=True, text=True)
if r.returncode != 0:
    sys.stderr.write((r.stderr or r.stdout or 'weasyprint failed')[-3000:])
    raise SystemExit('weasyprint failed on doklad')
try:
    from pypdf import PdfReader
    n = len(PdfReader(pdf_path).pages)
    print(f'PDF: {pdf_path} — {n} стр.')
except Exception:
    print(f'PDF: {pdf_path}')
