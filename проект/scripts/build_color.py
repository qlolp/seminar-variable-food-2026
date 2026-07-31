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

# первый h1 (титул) убираем из тела — светлая обложка выводится первой страницей, до оглавления
SPARK = ('<svg class="spark" viewBox="0 0 100 100"><path d="M50 0 L60 38 L85 15 L62 40 L100 50 '
         'L62 60 L85 85 L60 62 L50 100 L40 62 L15 85 L38 60 L0 50 L38 40 L15 15 L40 38 Z"/></svg>')
COVER = f'''
<div class="cover">
  <div class="cover-top">{SPARK}<span class="cover-brand">Пространство новых идей 2.0</span></div>
  <div class="cover-kick">МЕЖРЕГИОНАЛЬНЫЙ МЕТОДИЧЕСКИЙ СЕМИНАР-СОВЕЩАНИЕ</div>
  <div class="cover-title">Не просто накормить</div>
  <div class="cover-rule"></div>
  <div class="cover-sub">Как организовать безопасное, достойное и вариативное питание людей с психическими нарушениями в домах социального обслуживания</div>
  <div class="cover-meta">Санкт-Петербург · 25–27 августа 2026 года<br>Министерство труда и социальной защиты Российской Федерации · Комитет по социальной политике Санкт-Петербурга</div>
  <div class="cover-aud">Доклад для руководителей стационарных организаций социального обслуживания из 51 субъекта Российской Федерации</div>
</div>
'''
frag = re.sub(r'<h1[^>]*>НЕ ПРОСТО НАКОРМИТЬ</h1>', '', frag, count=1)

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
@page { size: A4; margin: 20mm 18mm 18mm 18mm; background:#F9F9F7;
  @bottom-right { content: counter(page); font-family:'Noto Sans',sans-serif; font-size:10pt; color:#D97757; }
  @bottom-left { content: 'Не просто накормить · 2026'; font-family:'Noto Sans',sans-serif; font-size:8.5pt; color:#A8A294; } }
@page cover { margin:0; background:#F9F9F7; @bottom-right{content:none} @bottom-left{content:none} }
html { font-size: 11pt; }
body { font-family:'Noto Sans',sans-serif; font-size:11pt; line-height:1.62; text-align:left; color:#141413; background:#F9F9F7; }
p, li { text-align:justify; }
p { margin:0 0 7pt; orphans:2; widows:2; }

.spark { width:11pt; height:11pt; fill:#D97757; }
.cover { page: cover; page-break-after:always; height:297mm; background:#F9F9F7; color:#141413; padding:26mm 26mm; box-sizing:border-box; }
.cover-top { display:flex; align-items:center; gap:8pt; margin-bottom:50mm; }
.cover-top .spark { width:22pt; height:22pt; }
.cover-brand { font-family:'PT Serif',serif; font-size:16pt; color:#141413; }
.cover-kick { font-size:10.5pt; letter-spacing:2.5pt; color:#B85C3D; font-weight:bold; line-height:1.7; margin-bottom:14pt; }
.cover-title { font-family:'PT Serif',serif; font-size:42pt; font-weight:bold; line-height:1.12; color:#141413; max-width:165mm; }
.cover-rule { width:64pt; height:3.5pt; background:#D97757; margin:24pt 0 20pt; }
.cover-sub { font-size:14pt; line-height:1.5; color:#4A463C; max-width:150mm; }
.cover-meta { font-size:10.5pt; line-height:1.6; color:#6E6A5E; margin-top:32pt; }
.cover-aud { font-size:10pt; color:#8A8578; margin-top:16pt; border-top:1pt solid #E5E2D8; padding-top:10pt; }

h1 { font-family:'PT Serif',serif; font-weight:bold; font-size:20pt; color:#141413; page-break-before:always; margin:0 0 4pt; text-align:left; line-height:1.25; padding-bottom:6pt; border-bottom:2.5pt solid #D97757; page-break-after:avoid; }
h1.part { background:#F1EDE3; color:#141413; font-size:22pt; padding:24pt 20pt; border-bottom:none; border-top:4pt solid #D97757; margin-top:40pt; }
h1.part + p, h1.part + p + p { font-size:11.5pt; }
h2 { font-family:'PT Serif',serif; font-weight:bold; font-size:14pt; color:#141413; margin:15pt 0 5pt; text-align:left; page-break-after:avoid; break-after:avoid; padding-left:9pt; border-left:3.5pt solid #D97757;}
h3 { font-size:11.5pt; color:#B85C3D; margin:11pt 0 4pt; font-style:normal; font-weight:bold; page-break-after:avoid; break-after:avoid;}

table { border-collapse:collapse; width:100%; font-size:9.5pt; margin:9pt 0; page-break-inside:auto; background:#FFFFFF; }
tr { page-break-inside:avoid; }
thead { display:table-header-group; }
td, th { border:0.7pt solid #E5E2D8; padding:4pt 6pt; vertical-align:top; text-align:left; line-height:1.3; overflow-wrap:anywhere; word-break:break-word; }
th { background:#F2EFE6; color:#141413; font-size:9.5pt; border-bottom:1.2pt solid #D97757; }
tr:nth-child(even) td { background:#FAF8F3; }

sup { font-size:8pt; color:#B85C3D; font-weight:bold; }
a { color:#B85C3D; text-decoration:none; }
blockquote { margin:7pt 14pt; padding:8pt 12pt; background:#F2EFE6; border-left:3.5pt solid #D97757; font-style:italic; color:#4A463C; }
ul, ol { margin:0 0 7pt 0; padding-left:20pt; }
li { margin-bottom:3pt; }
li::marker { color:#D97757; font-weight:bold; }
hr { border:none; border-top:1pt solid #E5E2D8; margin:12pt 0; }

.srclist p, .srclist li, .srclist a { font-size:9pt; line-height:1.35; overflow-wrap:anywhere; word-break:break-all; text-align:left; margin-bottom:3.5pt; }
.srclist b { color:#B85C3D; }

.toc { page-break-after:always; }
.toc-title { font-family:'PT Serif',serif; font-size:20pt; font-weight:bold; color:#141413; margin-bottom:12pt; padding-bottom:6pt; border-bottom:2.5pt solid #D97757; }
.toc table { font-size:10pt; }
.toc td { border:none; border-bottom:0.5pt dotted #D8D2C4; padding:3pt 4pt; text-align:left !important; }
.toc td a { display:inline; text-align:left; }
.toc-p { width:40pt; text-align:right; color:#B85C3D; font-weight:bold; }
.toc-part td { background:#F2EFE6; font-weight:bold; color:#141413; padding-top:6pt; }

.page-inf h1, .page-inf h2 { page-break-before:avoid; }
</style>
"""

html = f'''<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">
<title>Не просто накормить — журнальная версия</title>{CSS}{CSS_COLOR}</head><body>
{COVER}
{TOC_HTML}
{frag}
</body></html>'''

open(f'{OUT}/_report_color.html', 'w', encoding='utf-8').write(html)
print('color HTML written:', len(html), 'chars; TOC entries:', len(toc_rows))
