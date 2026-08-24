# -*- coding: utf-8 -*-
"""Комплект спикера к 25–26.08 — PDF в двух папках.

выступление_26.08/  — плоский комплект (v6, речь, Q&A, карточка панели).
пакет_26.08/        — каталог: участникам / себе / экран + ПРОЧТИ_ПЕРВЫМ.md.

Колода зала — v6 (копируется, не пересобирается). v5 не класть.
Запуск из корня репозитория:
    python3 проект/scripts/build_speaker_kit.py
"""
import os, re, shutil, subprocess, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))       # проект/
ROOT = os.path.dirname(BASE)                                             # репозиторий
OUT = os.path.join(BASE, 'output')
KIT = os.path.join(ROOT, 'выступление_26.08')
PKG = os.path.join(ROOT, 'пакет_26.08')
SEM = os.path.join(ROOT, '03_семинарский_пакет')
V6 = os.path.join(ROOT, '02_презентация', 'презентация_v6')
os.makedirs(KIT, exist_ok=True)
os.makedirs(OUT, exist_ok=True)
env = dict(os.environ); env['LANG'] = 'C.UTF-8'

claude_src = open(os.path.join(BASE, 'scripts', 'build_claude.py'), encoding='utf-8').read()
_a = claude_src.index('CSS = """') + len('CSS = """')
_b = claude_src.index('"""', _a)
CLAUDE_CSS = claude_src[_a:_b]


def md_to_pdf(src_md, out_pdf, kicker, title, subtitle, font_pt=10.6):
    md = open(src_md, encoding='utf-8').read()
    md = re.sub(r'^# .*\n', '', md, count=1)
    frag = subprocess.run(
        ['pandoc', '-f', 'markdown+superscript+autolink_bare_uris', '-t', 'html', '--wrap=none'],
        input=md, capture_output=True, text=True, env=env).stdout
    css = CLAUDE_CSS.replace('</style>',
        f'\n@page {{ size: A4; margin: 16mm 18mm; }}'
        f'\nhtml {{ font-size: {font_pt}pt; }}'
        f'\nbody {{ line-height: 1.42; }}'
        f'\nh2 {{ page-break-before: auto; margin: 11pt 0 4pt; }}'
        f'\nh3 {{ margin: 8pt 0 3pt; }}\nh1 {{ margin: 0 0 5pt; }}'
        f'\nblockquote {{ border-left: 3pt solid #C15F3C; margin: 6pt 0; padding: 2pt 0 2pt 10pt; color:#3D3929; }}\n</style>')
    cover = (
        f'<div style="border-bottom:2.5pt solid #C15F3C; padding-bottom:6pt; margin-bottom:9pt;">'
        f'<div style="font-family:\'PT Sans\'; font-size:8pt; letter-spacing:2.5pt; color:#87867F;">{kicker}</div>'
        f'<div style="font-family:\'Playfair Display\'; font-weight:800; font-size:22pt; line-height:1.05; color:#141413; margin-top:3pt;">{title}</div>'
        f'<div style="font-family:\'PT Serif\'; font-style:italic; font-size:10.5pt; color:#3D3929; margin-top:4pt;">{subtitle}</div>'
        f'</div>')
    html = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
            f'<title>{title}</title>' + css + '</head><body>' + cover + frag + '</body></html>')
    tmp_html = os.path.join(OUT, '_kit_tmp.html')
    open(tmp_html, 'w', encoding='utf-8').write(html)
    r = subprocess.run(['weasyprint', tmp_html, out_pdf], cwd=OUT, env=env,
                       capture_output=True, text=True)
    os.remove(tmp_html)
    if r.returncode != 0:
        sys.stderr.write((r.stderr or r.stdout or 'weasyprint failed')[-2500:])
        raise SystemExit(f'weasyprint failed: {out_pdf}')


def html_to_pdf(src_html, out_pdf):
    r = subprocess.run(['weasyprint', src_html, out_pdf], cwd=ROOT, env=env,
                       capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write((r.stderr or r.stdout or 'weasyprint failed')[-2500:])
        raise SystemExit(f'weasyprint failed: {out_pdf}')


def pages(pdf):
    try:
        from pypdf import PdfReader
        return len(PdfReader(pdf).pages)
    except Exception:
        return '?'


def run(script):
    subprocess.run([sys.executable, os.path.join(BASE, 'scripts', script)],
                   cwd=ROOT, check=True)


def copyf(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)


# --- сборка исходников ---
print('1/8 колода v6 (копия, без пересборки) …')
v6_pdf = os.path.join(V6, 'Презентация_v6_Не_просто_накормить.pdf')
if not os.path.isfile(v6_pdf):
    raise SystemExit('нет колоды v6: ' + v6_pdf)
old_v5 = os.path.join(KIT, '1_Презентация_v5.pdf')
if os.path.isfile(old_v5):
    os.remove(old_v5)

print('2/8 доклад 10–12 …')
run('build_doklad.py')

print('3/8 материал на стол …')
run('build_material.py')

print('4/8 сценарий 20 мин (актуальный текст под v6) …')
speech_pdf = os.path.join(KIT, '4_Сценарий_выступления_20мин.pdf')
md_to_pdf(os.path.join(SEM, '02_выступление_20мин.md'),
          speech_pdf,
          'КОМПЛЕКТ СПИКЕРА · 26.08.2026', 'Сценарий выступления · 18–20 минут',
          'Под колоду v6 · площадка № 2, ДСО «Тесовый берег» · со-модератор Нурбаев Т. А.',
          font_pt=10.8)
copyf(speech_pdf, os.path.join(SEM, '02_выступление_20мин.pdf'))

print('5/8 карточка Q&A …')
md_to_pdf(os.path.join(ROOT, '07_редакция_доклада_v2', '08_версии', '07_QA.md'),
          os.path.join(KIT, '5_Карточка_QA.pdf'),
          'КОМПЛЕКТ СПИКЕРА · 26.08.2026', 'Карточка Q&A · 22 вопроса',
          'Короткий ответ · развёрнутый · источник · граница уверенности', font_pt=10.2)

print('6/8 HTML-карточки …')
html_to_pdf(os.path.join(SEM, 'памятка_на_стол.html'),
            os.path.join(SEM, 'Памятка_что_унести_в_регион.pdf'))
html_to_pdf(os.path.join(SEM, 'карточка_спикера_26_08.html'),
            os.path.join(SEM, 'карточка_спикера_26_08.pdf'))
html_to_pdf(os.path.join(SEM, '21_если_инспектор_не_принял.html'),
            os.path.join(SEM, '21_если_инспектор_не_принял.pdf'))
html_to_pdf(os.path.join(SEM, 'панель_25_08_карточка.html'),
            os.path.join(SEM, 'панель_25_08_карточка.pdf'))

print('7/8 плоский комплект выступление_26.08 …')
copyf(v6_pdf, os.path.join(KIT, '1_Презентация_v6.pdf'))
copyf(os.path.join(OUT, 'Не_просто_накормить_ДОКЛАД_10-12.pdf'),
      os.path.join(KIT, '2_Доклад.pdf'))
copyf(os.path.join(OUT, 'Материал_к_сессии_26_08.pdf'),
      os.path.join(KIT, '3_Материал_на_стол.pdf'))
copyf(os.path.join(SEM, 'панель_25_08_карточка.pdf'),
      os.path.join(KIT, '6_Карточка_панели_25_08.pdf'))
copyf(os.path.join(SEM, 'карточка_спикера_26_08.pdf'),
      os.path.join(KIT, '7_Карточка_спикера_26_08.pdf'))

print('8/8 каталог пакет_26.08 …')
for sub in ('1_участникам', '2_себе', '3_экран'):
    os.makedirs(os.path.join(PKG, sub), exist_ok=True)

copyf(os.path.join(SEM, 'Памятка_что_унести_в_регион.pdf'),
      os.path.join(PKG, '1_участникам', 'Памятка_что_унести_в_регион.pdf'))
brochure = os.path.join(OUT, 'Вариативное_питание_опыт_реализации.pdf')
if os.path.isfile(brochure):
    copyf(brochure, os.path.join(PKG, '1_участникам', 'Вариативное_питание_опыт_реализации.pdf'))

copyf(os.path.join(SEM, 'панель_25_08_карточка.pdf'),
      os.path.join(PKG, '2_себе', '25_карточка_панели_Право_на_выбор.pdf'))
copyf(os.path.join(SEM, 'карточка_спикера_26_08.pdf'),
      os.path.join(PKG, '2_себе', '26_карточка_спикера_питание_v6.pdf'))
copyf(os.path.join(SEM, '21_если_инспектор_не_принял.pdf'),
      os.path.join(PKG, '2_себе', '26_если_инспектор_не_принял.pdf'))
copyf(speech_pdf, os.path.join(PKG, '2_себе', '26_сценарий_20мин.pdf'))
copyf(os.path.join(OUT, 'Материал_к_сессии_26_08.pdf'),
      os.path.join(PKG, '2_себе', '26_материал_на_стол.pdf'))

copyf(v6_pdf, os.path.join(PKG, '3_экран', 'Презентация_v6_Не_просто_накормить.pdf'))
v6_pptx = os.path.join(V6, 'Презентация_v6_Не_просто_накормить.pptx')
if os.path.isfile(v6_pptx):
    copyf(v6_pptx, os.path.join(PKG, '3_экран', 'Презентация_v6_Не_просто_накормить.pptx'))
v6_nr = os.path.join(V6, 'Презентация_v6_Не_просто_накормить_без_резерва.pdf')
if os.path.isfile(v6_nr):
    copyf(v6_nr, os.path.join(PKG, '3_экран', 'Презентация_v6_без_резерва.pdf'))
notes = os.path.join(V6, 'speaker_notes_v6.pdf')
if os.path.isfile(notes):
    copyf(notes, os.path.join(PKG, '3_экран', 'speaker_notes_v6.pdf'))
guide = os.path.join(ROOT, '01_доклад', 'Не_просто_накормить_доклад_стиль_claude.pdf')
if os.path.isfile(guide):
    copyf(guide, os.path.join(PKG, '3_экран', 'Не_просто_накормить_доклад_стиль_claude.pdf'))
prog = os.path.join(SEM, 'ПРОГРАММА_семинара_обновлённая.pdf')
if os.path.isfile(prog):
    copyf(prog, os.path.join(PKG, '3_экран', 'ПРОГРАММА_семинара_обновлённая.pdf'))
copyf(os.path.join(KIT, '5_Карточка_QA.pdf'),
      os.path.join(PKG, '3_экран', '5_Карточка_QA.pdf'))

print('\nГотово.')
print('выступление_26.08/')
for f in sorted(os.listdir(KIT)):
    if f.endswith('.pdf'):
        print(f'  {f} — {pages(os.path.join(KIT, f))} стр.')
print('пакет_26.08/')
for root, _dirs, files in os.walk(PKG):
    for f in sorted(files):
        if f.endswith(('.pdf', '.pptx', '.md')):
            p = os.path.join(root, f)
            rel = os.path.relpath(p, PKG)
            extra = f' — {pages(p)} стр.' if f.endswith('.pdf') else ''
            print(f'  {rel}{extra}')
