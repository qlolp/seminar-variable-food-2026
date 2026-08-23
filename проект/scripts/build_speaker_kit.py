# -*- coding: utf-8 -*-
"""Комплект спикера к сессии 26.08 — всё в PDF, одной папкой.
Собирает: презентацию v5, «Доклад» (7 стр.), «Материал на стол» (2 стр.),
сценарий выступления 20 мин, карточку Q&A. Кладёт в выступление_26.08/.
Запуск из корня репозитория:
    python3 проект/scripts/build_speaker_kit.py"""
import os, re, shutil, subprocess, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))       # проект/
ROOT = os.path.dirname(BASE)                                             # репозиторий
OUT = os.path.join(BASE, 'output')
KIT = os.path.join(ROOT, 'выступление_26.08')
os.makedirs(KIT, exist_ok=True)
env = dict(os.environ); env['LANG'] = 'C.UTF-8'

# --- общий рендер markdown → PDF в стиле claude ---
claude_src = open(os.path.join(BASE, 'scripts', 'build_claude.py'), encoding='utf-8').read()
_a = claude_src.index('CSS = """') + len('CSS = """')
_b = claude_src.index('"""', _a)
CLAUDE_CSS = claude_src[_a:_b]


def md_to_pdf(src_md, out_pdf, kicker, title, subtitle, font_pt=10.6):
    md = open(src_md, encoding='utf-8').read()
    md = re.sub(r'^# .*\n', '', md, count=1)  # первый заголовок даём своим блоком
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


def pages(pdf):
    try:
        from pypdf import PdfReader
        return len(PdfReader(pdf).pages)
    except Exception:
        return '?'


def run(script):
    subprocess.run([sys.executable, os.path.join(BASE, 'scripts', script)],
                   cwd=ROOT, check=True)


# 1. Презентация v5 (21 + резерв) — пересобрать и забрать
print('1/5 презентация v5 …')
subprocess.run([sys.executable,
                os.path.join(ROOT, '02_презентация', 'презентация_v5_21_слайд', 'build_v5.py'),
                '--pdf'], cwd=ROOT, check=True)
shutil.copy(os.path.join(ROOT, '02_презентация', 'Презентация_дискуссия_26_08_v5_стиль_claude.pdf'),
            os.path.join(KIT, '1_Презентация_v5.pdf'))

# 2. Доклад (7 стр.)
print('2/5 доклад …')
run('build_doklad.py')
shutil.copy(os.path.join(OUT, 'Не_просто_накормить_ДОКЛАД_10-12.pdf'),
            os.path.join(KIT, '2_Доклад.pdf'))

# 3. Материал на стол (2 стр.)
print('3/5 материал …')
run('build_material.py')
shutil.copy(os.path.join(OUT, 'Материал_к_сессии_26_08.pdf'),
            os.path.join(KIT, '3_Материал_на_стол.pdf'))

# 4. Сценарий выступления 20 мин
print('4/5 сценарий 20 мин …')
md_to_pdf(os.path.join(ROOT, '07_редакция_доклада_v2', '08_версии', '04_выступление_20_минут.md'),
          os.path.join(KIT, '4_Сценарий_выступления_20мин.pdf'),
          'КОМПЛЕКТ СПИКЕРА · 26.08.2026', 'Сценарий выступления · 18–20 минут',
          'С таймингом по слайдам · площадка № 2, ДСО «Тесовый берег»', font_pt=10.8)

# 5. Карточка Q&A
print('5/5 карточка Q&A …')
md_to_pdf(os.path.join(ROOT, '07_редакция_доклада_v2', '08_версии', '07_QA.md'),
          os.path.join(KIT, '5_Карточка_QA.pdf'),
          'КОМПЛЕКТ СПИКЕРА · 26.08.2026', 'Карточка Q&A · 22 вопроса',
          'Короткий ответ · развёрнутый · источник · граница уверенности', font_pt=10.2)

print('\nГотово. Файлы в', KIT)
for f in sorted(os.listdir(KIT)):
    if f.endswith('.pdf'):
        print(f'  {f} — {pages(os.path.join(KIT, f))} стр.')
