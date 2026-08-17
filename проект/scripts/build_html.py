# -*- coding: utf-8 -*-
"""Стадия 2: _report_full.md → HTML (TNR 14pt, 1.5 интервал, статичный TOC) → готов к html_to_pdf.js."""
import os, re, sys, json, subprocess

BASE = 'C:/Users/Evgenii/AppData/Local/Temp/seminar-food/проект'
OUT  = os.path.join(BASE, 'output')
sys.path.insert(0, os.path.join(BASE, 'scripts'))
from figures_html import CSS as FIGCSS, FIG
import figures_html2, figures_inf
FIG.update(figures_html2.FIG); INF = figures_inf.INF

md = open(f'{OUT}/_report_full.md', encoding='utf-8').read()

# pandoc → фрагмент HTML
env = dict(os.environ); env['LANG'] = 'C.UTF-8'
frag = subprocess.run(
    ['pandoc', '-f', 'markdown+superscript+autolink_bare_uris', '-t', 'html', '--wrap=none'],
    input=md, capture_output=True, text=True, env=env).stdout

# вставка фигур
def fig_repl(m):
    key = m.group(1)
    return FIG.get(key, f'<!-- missing fig {key} -->')
frag = re.sub(r'<p>\[\[FIG:([a-z0-9_]+)\]\]</p>', fig_repl, frag)
def inf_repl(m):
    key = m.group(1)
    return INF.get(key, f'<!-- missing inf {key} -->')
frag = re.sub(r'<p>\[\[INF:([a-z0-9_]+)\]\]</p>', inf_repl, frag)

# TOC: h1-заголовки
heads = re.findall(r'<h1[^>]*>(.*?)</h1>', frag, re.S)
toc_entries = [re.sub(r'<[^>]+>', '', h).strip() for h in heads]
# якоря
def add_anchor(m):
    t = re.sub(r'<[^>]+>', '', m.group(1)).strip()
    aid = re.sub(r'[^0-9A-Za-zА-Яа-я]+', '_', t)[:60]
    return f'<h1 id="{aid}">{m.group(1)}</h1>'
frag = re.sub(r'<h1[^>]*>(.*?)</h1>', add_anchor, frag)

toc_pages = {}
if os.path.exists(f'{OUT}/toc_pages.json'):
    toc_pages = json.load(open(f'{OUT}/toc_pages.json'))

toc_rows = []
for t in toc_entries:
    aid = re.sub(r'[^0-9A-Za-zА-Яа-я]+', '_', t)[:60]
    pg = toc_pages.get(aid, '')
    toc_rows.append(f'<tr><td class="toc-t"><a href="#{aid}">{t}</a></td><td class="toc-p">{pg}</td></tr>')
TOC_HTML = ('<div class="toc"><p class="toc-title">Содержание</p><table>'
            + ''.join(toc_rows) + '</table></div>')

CSS_DOC = """
<style>
@page { size: A4; margin: 20mm 15mm 20mm 30mm;
  @bottom-center { content: counter(page); font-family:'Times New Roman'; font-size:12pt; } }
@page :first { @bottom-center { content: none; } }
html { font-size: 14pt; }
body { font-family:'Times New Roman','Liberation Serif',serif; font-size:14pt; line-height:1.5; text-align:left; }
p, li, blockquote { text-align:justify; }
h1 { font-size:16pt; page-break-before:always; margin:0 0 12pt; text-align:left; }
h1:first-of-type { page-break-before:avoid; }
h2 { font-size:14pt; margin:14pt 0 6pt; text-align:left; page-break-after:avoid; break-after:avoid;}
h3 { font-size:14pt; margin:12pt 0 4pt; font-style:italic; page-break-after:avoid; break-after:avoid;}
p { margin:0 0 8pt; orphans:2; widows:2; }
table { page-break-inside:auto; }
tr { page-break-inside:avoid; }
thead { display:table-header-group; }
table { border-collapse:collapse; width:100%; font-size:12pt; margin:8pt 0; }
td, th { border:0.8pt solid #333; padding:4pt 6pt; vertical-align:top; text-align:left; line-height:1.3; overflow-wrap:anywhere; word-break:break-word; }
th { background:#ececec; }
sup { font-size:9pt; }
a { color:#000; text-decoration:none; }
.srclist p, .srclist li, .srclist a { font-size:11pt; line-height:1.35; overflow-wrap:anywhere; word-break:break-all; text-align:left; margin-bottom:4pt;}
.toc { page-break-after:always; }
.toc-title { font-size:16pt; font-weight:bold; margin-bottom:10pt; }
.toc table { font-size:12pt; }
.toc td { border:none; border-bottom:0.5pt dotted #888; padding:2.5pt 4pt; text-align:left !important; }
.toc td a { display:inline; text-align:left; }
.toc-p { width:40pt; text-align:right; }
blockquote { margin:6pt 18pt; font-style:italic; }
ul, ol { margin:0 0 8pt 0; padding-left:22pt; }
li { margin-bottom:3pt; }
</style>
"""

# титул — первый h1 без разрыва перед ним (ch01 titul)
html = f'''<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">
<title>Не просто накормить</title>{CSS_DOC}{FIGCSS}</head><body>
{TOC_HTML}
{frag}
</body></html>'''

open(f'{OUT}/_report.html', 'w', encoding='utf-8').write(html)
print('HTML written:', len(html), 'chars; TOC entries:', len(toc_entries))
