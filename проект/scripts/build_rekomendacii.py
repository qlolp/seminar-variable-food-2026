# -*- coding: utf-8 -*-
"""«Организация вариативного питания…: опыт реализации проектов» — методические
рекомендации в повествовательном стиле. Источник: проект/rekomendacii.md.
Запуск из корня репозитория: python3 проект/scripts/build_rekomendacii.py
Итог: проект/output/Вариативное_питание_опыт_реализации.pdf"""
import os, re, subprocess, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'output')
SRC = os.path.join(BASE, 'rekomendacii.md')

md = open(SRC, encoding='utf-8').read()
md = re.sub(r'\A# .*\n', '', md, count=1)  # титул — своим блоком

env = dict(os.environ); env['LANG'] = 'C.UTF-8'
frag = subprocess.run(
    ['pandoc', '-f', 'markdown+superscript+autolink_bare_uris', '-t', 'html', '--wrap=none'],
    input=md, capture_output=True, text=True, env=env).stdout

claude_src = open(os.path.join(BASE, 'scripts', 'build_claude.py'), encoding='utf-8').read()
a = claude_src.index('CSS = """') + len('CSS = """')
b = claude_src.index('"""', a)
css = claude_src[a:b]
css = css.replace('</style>',
                  '\n@page { size: A4; margin: 22mm 24mm; }'
                  '\nhtml { font-size: 11.5pt; }'
                  '\nbody { line-height: 1.55; }'
                  '\np { margin: 0 0 9pt; text-align: justify; }'
                  '\nh2 { page-break-before: always; margin: 0 0 10pt; }'
                  '\nh2 + p::first-letter, .lead::first-letter { }'
                  '\nh3 { margin: 15pt 0 6pt; }\nh1 { margin: 0 0 6pt; }\n</style>')

COVER = '''
<div style="page-break-after:always; padding:38mm 0 0;">
  <div style="font-family:'PT Sans'; font-size:9pt; letter-spacing:3pt; color:#87867F; margin-bottom:26mm;">МЕТОДИЧЕСКИЕ РЕКОМЕНДАЦИИ · ОПЫТ РЕАЛИЗАЦИИ ПРОЕКТОВ</div>
  <div style="font-family:'Playfair Display'; font-weight:800; font-size:40pt; line-height:1.06; color:#141413;">Организация<br>вариативного питания<br>в домах социального<br>обслуживания</div>
  <div style="width:70pt; height:3pt; background:#C15F3C; margin:18pt 0 20pt;"></div>
  <p style="font-family:'PT Serif'; font-size:12pt; line-height:1.6; color:#6E6A5E; margin:0; max-width:150mm;">Рассказ о том, как вернуть человеку право самому решить, что окажется у него на тарелке, — с сомнениями, ошибками и честностью о том, чего мы пока не знаем.</p>
  <p style="font-family:'PT Serif'; font-size:11.5pt; color:#C15F3C; margin-top:28pt;">Чистяков Е. В., директор СПб ГАСУСОН «ДСО „Серафимовский“»</p>
</div>
'''

html = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<title>Организация вариативного питания — опыт реализации проектов</title>' + css
        + '</head><body>' + COVER + frag + '</body></html>')

html_path = os.path.join(OUT, '_rekomendacii.html')
open(html_path, 'w', encoding='utf-8').write(html)
print('HTML written:', len(html), 'chars')

pdf_path = os.path.join(OUT, 'Вариативное_питание_опыт_реализации.pdf')
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
