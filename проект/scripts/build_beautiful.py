# -*- coding: utf-8 -*-
"""Красивая версия: _report_full.md → HTML (Playfair Display + PT Serif, тёмно-синяя
обложка fullbleed, teal-акценты, полноформатные разделители частей) → PDF через headless Edge.
Шрифты лежат в output/fonts/ (Google Fonts, SIL OFL)."""
import os, re, sys, json, subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT  = os.path.join(BASE, 'output')
sys.path.insert(0, os.path.join(BASE, 'scripts'))
from figures_html import FIG
import figures_html2, figures_inf
FIG.update(figures_html2.FIG); INF = figures_inf.INF

md = open(f'{OUT}/_report_full.md', encoding='utf-8').read()

env = dict(os.environ); env['LANG'] = 'C.UTF-8'
frag = subprocess.run(
    ['pandoc', '-f', 'markdown+superscript+autolink_bare_uris', '-t', 'html', '--wrap=none'],
    input=md, capture_output=True, text=True, env=env).stdout

frag = re.sub(r'<p>\[\[FIG:([a-z0-9_]+)\]\]</p>', lambda m: FIG.get(m.group(1), ''), frag)
frag = re.sub(r'<p>\[\[INF:([a-z0-9_]+)\]\]</p>', lambda m: INF.get(m.group(1), ''), frag)

PART_RE = re.compile(r'^(Часть [IVX]+\.|Список источников)')
ROMAN = re.compile(r'Часть ([IVX]+)\.')

def add_anchor(m):
    t = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    aid = re.sub(r'[^0-9A-Za-zА-Яа-я]+', '_', t)[:60]
    cls = ' class="part"' if PART_RE.match(t) else ''
    return f'<h1 id="{aid}"{cls}>{m.group(1)}</h1>'
frag = re.sub(r'<h1[^>]*>(.*?)</h1>', add_anchor, frag)

heads = re.findall(r'<h1[^>]*>(.*?)</h1>', frag, re.S)
toc_entries = [re.sub(r'<[^>]+>', '', h).strip() for h in heads]
frag = re.sub(r'<h1[^>]*>НЕ ПРОСТО НАКОРМИТЬ</h1>', '', frag, count=1)

SPARK = ('<svg class="spark" viewBox="0 0 100 100"><path d="M50 0 L60 38 L85 15 L62 40 L100 50 '
         'L62 60 L85 85 L60 62 L50 100 L40 62 L15 85 L38 60 L0 50 L38 40 L15 15 L40 38 Z"/></svg>')
COVER = '''
<section class="cover">
  <div class="cov-top">''' + SPARK + '''<span class="cov-brand">ПРОСТРАНСТВО НОВЫХ ИДЕЙ 2.0</span></div>
  <div class="cov-kick">МЕТОДИЧЕСКОЕ РУКОВОДСТВО К СЕМИНАРУ</div>
  <h1 class="cov-title">Не просто<br>накормить</h1>
  <div class="cov-rule"></div>
  <p class="cov-sub">Как организовать безопасное, достойное и вариативное питание людей
  с психическими нарушениями в домах социального обслуживания</p>
  <p class="cov-sub2">От единого меню к поддерживаемому выбору: здоровье, безопасность, права жителей,
  организация пищеблока, деньги и ответственность руководителя</p>
  <div class="cov-meta">
    <p>Санкт-Петербург · 25–27 августа 2026 года</p>
    <p>Министерство труда и социальной защиты Российской Федерации<br>
    Комитет по социальной политике Санкт-Петербурга</p>
    <p class="cov-aud">Для руководителей стационарных организаций социального обслуживания из 51 субъекта Российской Федерации</p>
    <p class="cov-author">Чистяков Е. В., директор СПб ГАСУСОН «ДСО „Серафимовский“»</p>
  </div>
</section>
'''

toc_pages = json.load(open(f'{OUT}/toc_pages_color.json')) if os.path.exists(f'{OUT}/toc_pages_color.json') else {}
toc_rows = []
for t in toc_entries:
    if t == 'НЕ ПРОСТО НАКОРМИТЬ':
        continue
    aid = re.sub(r'[^0-9A-Za-zА-Яа-я]+', '_', t)[:60]
    pg = toc_pages.get(aid, '')
    cls = ' class="toc-part"' if PART_RE.match(t) else ''
    toc_rows.append('<li' + cls + '><a href="#' + aid + '"><span class="toc-t">' + t
                    + '</span><span class="toc-p">' + str(pg) + '</span></a></li>')
TOC_HTML = ('<section class="toc"><p class="toc-title">Содержание</p><ul>'
            + ''.join(toc_rows) + '</ul></section>')

CSS = """
<style>
@font-face { font-family:'Playfair Display'; src:url('fonts/playfair-400.woff2') format('woff2'); font-weight:400; }
@font-face { font-family:'Playfair Display'; src:url('fonts/playfair-700.woff2') format('woff2'); font-weight:700; }
@font-face { font-family:'Playfair Display'; src:url('fonts/playfair-800.woff2') format('woff2'); font-weight:800; }
@font-face { font-family:'Playfair Display'; src:url('fonts/playfair-900.woff2') format('woff2'); font-weight:900; }
@font-face { font-family:'Playfair Display'; src:url('fonts/playfair-600i.woff2') format('woff2'); font-style:italic; font-weight:600; }
@font-face { font-family:'PT Serif'; src:url('fonts/PTSerif-Regular.ttf'); }
@font-face { font-family:'PT Serif'; src:url('fonts/PTSerif-Bold.ttf'); font-weight:bold; }
@font-face { font-family:'PT Serif'; src:url('fonts/PTSerif-Italic.ttf'); font-style:italic; }
@font-face { font-family:'PT Sans'; src:url('fonts/PTSans-Regular.ttf'); }
@font-face { font-family:'PT Sans'; src:url('fonts/PTSans-Bold.ttf'); font-weight:bold; }

@page { size: A4; margin: 22mm 19mm 20mm 19mm;
  @bottom-center { content: counter(page); font-family:'PT Sans'; font-size:9.5pt; color:#2A7F76; }
  @top-center { content: 'НЕ ПРОСТО НАКОРМИТЬ · 2026'; font-family:'PT Sans'; font-size:7.5pt; letter-spacing:2pt; color:#9AA7B5; } }
@page cover { margin:0; background:#152238; @bottom-center{content:none} @top-center{content:none} }
@page part   { margin:0; background:#152238; @bottom-center{content:none} @top-center{content:none} }

html { font-size: 10.5pt; }
body { font-family:'PT Serif'; line-height:1.58; color:#232B36; background:#FFFFFF; text-align:justify; }
p { margin:0 0 6.5pt; orphans:2; widows:2; }

.spark { width:12pt; height:12pt; fill:#2A9D8F; }
.cover { page: cover; page-break-after:always; height:297mm; background:#152238; color:#F2F5F9;
         padding:24mm 22mm; box-sizing:border-box; text-align:left; }
.cov-top { display:flex; align-items:center; gap:9pt; margin-bottom:44mm; }
.cov-top .spark { width:20pt; height:20pt; }
.cov-brand { font-family:'PT Sans'; font-size:12pt; letter-spacing:3pt; color:#8FB3AE; }
.cov-kick { font-family:'PT Sans'; font-size:10.5pt; letter-spacing:3.5pt; color:#2A9D8F; margin-bottom:16pt; }
.cov-title { font-family:'Playfair Display'; font-weight:800; font-size:56pt; line-height:1.04; margin:0 0 10pt; color:#F2F5F9; text-align:left; }
.cov-rule { width:70pt; height:3pt; background:#2A9D8F; margin:14pt 0 18pt; }
.cov-sub { font-family:'Playfair Display'; font-style:italic; font-size:16pt; line-height:1.45; color:#D8E2EC; margin:0 0 10pt; }
.cov-sub2 { font-family:'PT Serif'; font-size:11pt; line-height:1.5; color:#A9B7C6; margin:0 0 auto; }
.cov-meta { font-family:'PT Sans'; font-size:10.5pt; line-height:1.7; color:#C7D2DD; margin-top:26pt; }
.cov-aud { font-size:9.5pt; color:#8FA0B3; border-top:0.7pt solid #2E4159; padding-top:10pt; margin-top:14pt; }
.cov-author { font-family:'PT Serif'; font-size:11.5pt; color:#8FB3AE; }

h1 { font-family:'Playfair Display'; font-weight:800; font-size:21pt; color:#152238;
     page-break-before:always; margin:0 0 8pt; text-align:left; line-height:1.2;
     padding-bottom:7pt; border-bottom:2.5pt solid #2A9D8F; page-break-after:avoid; }
h1.part { page: part; page-break-before:always; page-break-after:always;
  background:#152238; color:#152238; font-size:0; border:none; padding:0; margin:0;
  height:297mm; box-sizing:border-box; position:relative; }
h1.part span.pnum { position:absolute; top:100mm; left:0; right:0; text-align:center;
  font-family:'Playfair Display'; font-weight:800; font-size:64pt; color:#2A9D8F; }
h1.part span.ptit { position:absolute; top:150mm; left:30mm; right:30mm; text-align:center;
  font-family:'Playfair Display'; font-style:italic; font-size:17pt; color:#D8E2EC; }

h2 { font-family:'Playfair Display'; font-weight:700; font-size:13.5pt; color:#152238;
     margin:14pt 0 5pt; text-align:left; page-break-after:avoid; break-after:avoid; }
h3 { font-family:'PT Sans'; font-weight:bold; font-size:10pt; letter-spacing:1pt;
     text-transform:uppercase; color:#2A7F76; margin:10pt 0 4pt; page-break-after:avoid; break-after:avoid; }

table { border-collapse:collapse; width:100%; font-family:'PT Sans'; font-size:8.8pt; margin:9pt 0; background:#FFFFFF; }
tr { page-break-inside:avoid; }
thead { display:table-header-group; }
td, th { border:0.5pt solid #D9DFE6; padding:4pt 6pt; vertical-align:top; text-align:left; line-height:1.35; overflow-wrap:anywhere; }
th { font-weight:bold; color:#152238; background:#EEF3F6; border-bottom:1.2pt solid #2A9D8F; }
tr:nth-child(even) td { background:#F7FAFB; }

sup { font-family:'PT Sans'; font-size:7.5pt; color:#2A7F76; font-weight:bold; }
a { color:#2A7F76; text-decoration:none; }
blockquote { margin:8pt 14pt; padding:8pt 12pt; background:#F0F6F5; border-left:3pt solid #2A9D8F;
             font-style:italic; color:#3C4855; }
ul, ol { margin:0 0 7pt 0; padding-left:19pt; }
li { margin-bottom:2.5pt; }
li::marker { color:#2A9D8F; }
hr { border:none; border-top:0.6pt solid #D9DFE6; margin:12pt 0; }
em { color:#2F3A46; }

.toc { page-break-after:always; }
.toc-title { font-family:'Playfair Display'; font-weight:800; font-size:22pt; color:#152238; margin:0 0 14pt;
  padding-bottom:7pt; border-bottom:2.5pt solid #2A9D8F; text-align:left; }
.toc ul { list-style:none; padding:0; margin:0; }
.toc li { margin:0; }
.toc a { display:flex; justify-content:space-between; gap:6pt; align-items:baseline;
         font-family:'PT Sans'; font-size:9.5pt; color:#2F3A46; padding:2.4pt 0;
         border-bottom:0.5pt dotted #C9D2DA; }
.toc .toc-t { text-align:left; }
.toc .toc-p { color:#2A7F76; font-weight:bold; }
.toc li.toc-part a { font-family:'Playfair Display'; font-weight:700; font-size:11pt; color:#152238;
  border-bottom:0.9pt solid #2A9D8F; margin-top:7pt; }

.srclist p, .srclist li, .srclist a { font-family:'PT Sans'; font-size:8.6pt; line-height:1.4;
  overflow-wrap:anywhere; text-align:left; margin-bottom:3.2pt; }
.srclist b { color:#2A7F76; }
</style>
"""

def part_divider(m):
    inner = m.group(1)
    t = re.sub(r'<[^>]+>', '', inner).strip()
    rom = ROMAN.match(t)
    num = '<span class="pnum">' + (rom.group(1) if rom else '§') + '</span>'
    title = re.sub(r'^Часть [IVX]+\.\s*', '', t)
    return '<h1 class="part"><span class="ptit">' + (title or t) + '</span>' + num + '</h1>'

frag = re.sub(r'<h1 class="part">(.*?)</h1>',
              lambda m: part_divider(m) if PART_RE.match(re.sub(r'<[^>]+>', '', m.group(1)).strip()) else m.group(0),
              frag, flags=re.S)

html = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<title>Не просто накормить — красивая версия</title>' + CSS + '</head><body>'
        + COVER + TOC_HTML + frag + '</body></html>')

open(f'{OUT}/_report_beautiful.html', 'w', encoding='utf-8').write(html)
print('beautiful HTML written:', len(html), 'chars; TOC entries:', len(toc_rows))
