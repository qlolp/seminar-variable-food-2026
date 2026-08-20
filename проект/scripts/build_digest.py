# -*- coding: utf-8 -*-
"""Краткая версия (15–18 стр.): chapters/_digest.md → HTML в стиле claude → PDF (Edge).
CSS переиспользуется из build_claude.py; обложка — компактный титульный блок."""
import os, re, subprocess, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'output')
SRC = os.path.join(BASE, 'chapters', '_digest.md')

md = open(SRC, encoding='utf-8').read()
md = re.sub(r'^# .*\n', '', md, count=1)  # титул даём своим блоком

env = dict(os.environ); env['LANG'] = 'C.UTF-8'
frag = subprocess.run(
    ['pandoc', '-f', 'markdown+superscript+autolink_bare_uris', '-t', 'html', '--wrap=none'],
    input=md, capture_output=True, text=True, env=env).stdout

# CSS из build_claude.py (между 'CSS = """' и закрывающим '"""')
claude_src = open(os.path.join(BASE, 'scripts', 'build_claude.py'), encoding='utf-8').read()
a = claude_src.index("CSS = \"\"\"") + len("CSS = \"\"\"")
b = claude_src.index("\"\"\"", a)
css = claude_src[a:b]
# краткая версия: компактные поля, корпус крупнее, книжная вёрстка (раздел = страница)
css = css.replace('</style>',
                  "\nhtml { font-size: 11.5pt; }\nh2 { page-break-before: always; margin-top: 0; }\n</style>")

COVER = '''
<div style="page-break-after:always; padding:30mm 0 14mm;">
  <div style="display:flex; align-items:center; gap:9pt; margin-bottom:26mm;">
    <svg width="20pt" height="20pt" viewBox="0 0 100 100" fill="#C15F3C"><path d="M50 0 L60 38 L85 15 L62 40 L100 50 L62 60 L85 85 L60 62 L50 100 L40 62 L15 85 L38 60 L0 50 L38 40 L15 15 L40 38 Z"/></svg>
    <span style="font-family:'PT Sans'; font-size:11.5pt; letter-spacing:3pt; color:#87867F;">ПРОСТРАНСТВО НОВЫХ ИДЕЙ 2.0</span>
  </div>
  <div style="font-family:'PT Sans'; font-size:10.5pt; letter-spacing:3.5pt; color:#C15F3C; margin-bottom:14pt;">КРАТКАЯ ВЕРСИЯ · ВЕЧЕР ЧТЕНИЯ</div>
  <div style="font-family:'Playfair Display'; font-weight:800; font-size:44pt; line-height:1.05; color:#141413;">Не просто<br>накормить</div>
  <div style="width:70pt; height:3pt; background:#C15F3C; margin:14pt 0 16pt;"></div>
  <p style="font-family:'Playfair Display'; font-style:italic; font-size:15pt; line-height:1.45; color:#3D3929; margin:0 0 10pt;">Как организовать безопасное, достойное и вариативное питание людей с психическими нарушениями в домах социального обслуживания</p>
  <p style="font-family:'PT Serif'; font-size:11pt; line-height:1.5; color:#6E6A5E; margin:0;">Суть · лестница вариативности · красные линии · пилот на 90 дней · панель пяти чисел</p>
  <div style="font-family:'PT Sans'; font-size:10.5pt; line-height:1.7; color:#3D3929; margin-top:22pt;">
    <p style="margin:0 0 6pt;">Дискуссия «Организация питания: опыт реализации проектов» · 26.08.2026, 14:00–15:30<br>
    Площадка № 2 — ДСО «Тесовый берег» · модераторы: Чистяков Е. В., Нурбаев Т. А.</p>
    <p style="margin:0; color:#C15F3C; font-family:'PT Serif'; font-size:11.5pt;">Чистяков Е. В., директор СПб ГАСУСОН «ДСО „Серафимовский“» · версия 1.0</p>
  </div>
</div>
'''

html = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<title>Не просто накормить — краткая версия</title>' + css + '</head><body>'
        + COVER + frag + '</body></html>')

open(f'{OUT}/_digest.html', 'w', encoding='utf-8').write(html)
print('digest HTML written:', len(html), 'chars')
