# -*- coding: utf-8 -*-
"""Журнальная цветная сборка: _report_full.md → HTML (современный дизайн) → PDF.
Отличия от официальной версии: sans-serif, палитра, цветная обложка, разделители частей,
цветные таблицы и врезки, поля 18 мм (без переплёта — журнальная печать)."""
import os, re, sys, json, subprocess

BASE = '/mnt/agents/output/seminar_variable_food_2026'
OUT  = os.path.join(BASE, 'output')
sys.path.insert(0, os.path.join(BASE, 'scripts'))
from figures_html import FIG
from figures_color import CSS_COLOR
import figures_html2, figures_inf
FIG.update(figures_html2.FIG); INF = figures_inf.INF

md = open(f'{OUT}/_report_full.md', encoding='utf-8').read()

env = dict(os.environ); env['LANG'] = 'C.UTF-8'
frag = subprocess.run(
    ['pandoc', '-f', 'markdown+superscript+autolink_bare_uris', '-t', 'html', '--wrap=none'],
    input=md, capture_output=True, text=True, env=env).stdout

frag = re.sub(r'<p>\[\[FIG:([a-z0-9_]+)\]\]</p>', lambda m: FIG.get(m.group(1), ''), frag)
frag = re.sub(r'<p>\[\[INF:([a-z0-9_]+)\]\]</p>', lambda m: INF.get(m.group(1), ''), frag)

# якоря + разделители частей
heads = re.findall(r'<h1[^>]*>(.*?)</h1>', frag, re.S)
toc_entries = [re.sub(r'<[^>]+>', '', h).strip() for h in heads]

PART_RE = re.compile(r'^(Часть [IVX]+\..*|Список источников)')
def add_anchor(m):
    t = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    aid = re.sub(r'[^0-9A-Za-zА-Яа-я]+', '_', t)[:60]
    cls = ' class="part"' if PART_RE.match(t) else ''
    return f'<h1 id="{aid}"{cls}>{m.group(1)}</h1>'
frag = re.sub(r'<h1[^>]*>(.*?)</h1>', add_anchor, frag)

# первый h1 (титул) заменяем цветной обложкой
COVER = '''
<div class="cover">
  <div class="cover-kick">МЕЖРЕГИОНАЛЬНЫЙ МЕТОДИЧЕСКИЙ СЕМИНАР-СОВЕЩАНИЕ<br>«ПРОСТРАНСТВО НОВЫХ ИДЕЙ 2.0»</div>
  <div class="cover-rule"></div>
  <div class="cover-title">НЕ ПРОСТО<br>НАКОРМИТЬ</div>
  <div class="cover-sub">Как организовать безопасное, достойное и вариативное питание людей с психическими нарушениями в домах социального обслуживания</div>
  <div class="cover-meta">Санкт-Петербург · 25–27 августа 2026 года<br>Министерство труда и социальной защиты Российской Федерации · Комитет по социальной политике Санкт-Петербурга</div>
  <div class="cover-aud">Доклад для руководителей стационарных организаций социального обслуживания из 51 субъекта Российской Федерации</div>
</div>
'''
frag = re.sub(r'<h1[^>]*>НЕ ПРОСТО НАКОРМИТЬ</h1>', COVER, frag, count=1)

toc_pages = {}
if os.path.exists(f'{OUT}/toc_pages_color.json'):
    toc_pages = json.load(open(f'{OUT}/toc_pages_color.json'))

toc_rows = []
for i, t in enumerate(toc_entries):
    if t == 'НЕ ПРОСТО НАКОРМИТЬ': continue
    aid = re.sub(r'[^0-9A-Za-zА-Яа-я]+', '_', t)[:60]
    pg = toc_pages.get(aid, '')
    part = ' class="toc-part"' if PART_RE.match(t) else ''
    toc_rows.append(f'<tr{part}><td class="toc-t"><a href="#{aid}">{t}</a></td><td class="toc-p">{pg}</td></tr>')
TOC_HTML = ('<div class="toc"><p class="toc-title">Содержание</p><table>'
            + ''.join(toc_rows) + '</table></div>')

CSS = """
<style>
@page { size: A4; margin: 20mm 18mm 18mm 18mm;
  @bottom-right { content: counter(page); font-family:'MiSans',sans-serif; font-size:10pt; color:#2F5D50; }
  @bottom-left { content: 'Не просто накормить · 2026'; font-family:'MiSans',sans-serif; font-size:8.5pt; color:#9AA7A1; } }
@page cover { margin:0; @bottom-right{content:none} @bottom-left{content:none} }
html { font-size: 11pt; }
body { font-family:'MiSans','PT Sans',sans-serif; font-size:11pt; line-height:1.55; text-align:left; color:#20242A; }
p, li { text-align:justify; }
p { margin:0 0 7pt; orphans:2; widows:2; }

.cover { page: cover; page-break-after:always; height:297mm; background:linear-gradient(160deg,#1F3D33 0%,#2F5D50 55%,#3A6E5D 100%); color:#fff; padding:34mm 24mm; box-sizing:border-box; }
.cover-kick { font-size:10.5pt; letter-spacing:2.5pt; color:#DCE6E0; line-height:1.7; }
.cover-rule { width:90pt; height:3.5pt; background:#B57517; margin:16pt 0 26pt; }
.cover-title { font-size:44pt; font-weight:bold; line-height:1.05; letter-spacing:1pt; }
.cover-sub { font-size:14.5pt; line-height:1.5; color:#DCE6E0; margin-top:22pt; max-width:150mm; }
.cover-meta { font-size:10.5pt; line-height:1.6; color:#B9C9C1; margin-top:34pt; }
.cover-aud { font-size:10pt; color:#9DB4AB; margin-top:14pt; border-top:1pt solid #4E7A6C; padding-top:10pt; }

h1 { font-size:17pt; color:#1F3D33; page-break-before:always; margin:0 0 4pt; text-align:left; line-height:1.25; padding-bottom:6pt; border-bottom:2.5pt solid #B57517; page-break-after:avoid; }
h1.part { background:linear-gradient(135deg,#1F3D33,#2F5D50); color:#fff; font-size:20pt; padding:26pt 20pt; border-bottom:none; margin-top:40pt; }
h1.part + p, h1.part + p + p { font-size:11.5pt; }
h2 { font-size:13pt; color:#2F5D50; margin:15pt 0 5pt; text-align:left; page-break-after:avoid; break-after:avoid; padding-left:9pt; border-left:3.5pt solid #B57517;}
h3 { font-size:11.5pt; color:#B57517; margin:11pt 0 4pt; font-style:normal; font-weight:bold; page-break-after:avoid; break-after:avoid;}

table { border-collapse:collapse; width:100%; font-size:9.5pt; margin:9pt 0; page-break-inside:auto; }
tr { page-break-inside:avoid; }
thead { display:table-header-group; }
td, th { border:0.7pt solid #C7BFAF; padding:4pt 6pt; vertical-align:top; text-align:left; line-height:1.3; overflow-wrap:anywhere; word-break:break-word; }
th { background:#2F5D50; color:#fff; font-size:9.5pt; }
tr:nth-child(even) td { background:#F4F1EA; }

sup { font-size:8pt; color:#B57517; font-weight:bold; }
a { color:#1F3D33; text-decoration:none; }
blockquote { margin:7pt 14pt; padding:8pt 12pt; background:#F2F5F3; border-left:3.5pt solid #2F5D50; font-style:italic; color:#37423C; }
ul, ol { margin:0 0 7pt 0; padding-left:20pt; }
li { margin-bottom:3pt; }
li::marker { color:#B57517; font-weight:bold; }
hr { border:none; border-top:1pt solid #C7BFAF; margin:12pt 0; }

.srclist p, .srclist li, .srclist a { font-size:9pt; line-height:1.35; overflow-wrap:anywhere; word-break:break-all; text-align:left; margin-bottom:3.5pt; }
.srclist b { color:#2F5D50; }

.toc { page-break-after:always; }
.toc-title { font-size:17pt; font-weight:bold; color:#1F3D33; margin-bottom:12pt; padding-bottom:6pt; border-bottom:2.5pt solid #B57517; }
.toc table { font-size:10pt; }
.toc td { border:none; border-bottom:0.5pt dotted #B9A77F; padding:3pt 4pt; text-align:left !important; }
.toc td a { display:inline; text-align:left; }
.toc-p { width:40pt; text-align:right; color:#2F5D50; font-weight:bold; }
.toc-part td { background:#EEF4F1; font-weight:bold; color:#1F3D33; padding-top:6pt; }

.page-inf h1, .page-inf h2 { page-break-before:avoid; }
</style>
"""

html = f'''<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">
<title>Не просто накормить — журнальная версия</title>{CSS}{CSS_COLOR}</head><body>
{TOC_HTML}
{frag}
</body></html>'''

open(f'{OUT}/_report_color.html', 'w', encoding='utf-8').write(html)
print('color HTML written:', len(html), 'chars; TOC entries:', len(toc_rows))
