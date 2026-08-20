# -*- coding: utf-8 -*-
"""Собрать все слайды <deck>/_render/*.html в один combined.html (960x540 на страницу)
и отдать путь для weasyprint. Запуск: python combine_slides.py [папка_дека]
"""
import glob, re, io, sys, os
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DECK = sys.argv[1] if len(sys.argv) > 1 else 'презентация_34_слайда'
BASE = Path(__file__).resolve().parent / DECK
RENDER = BASE / '_render'
FONTS = BASE.parent.parent / 'проект' / 'output' / 'fonts'

files = sorted(p for p in RENDER.glob('*.html') if p.name != 'combined.html')
parts = []
for f in files:
    html = f.read_text(encoding='utf-8')
    body = re.search(r'<body>(.*)</body>', html, re.S).group(1)
    parts.append('<div style="page-break-after:always">' + body + '</div>')

def face(name, fname, weight='400', style_='normal'):
    url = (FONTS / fname).as_uri()
    s = "font-weight:%s;" % weight if weight else ''
    if style_ != 'normal':
        s += "font-style:%s;" % style_
    return "@font-face { font-family:'%s'; src:url('%s'); %s }" % (name, url, s)

FONT_FACES = (face('PT Serif', 'PTSerif-Regular.ttf') +
              face('PT Serif', 'PTSerif-Bold.ttf', weight='700') +
              face('PT Serif', 'PTSerif-Italic.ttf', style_='italic'))

head = ('<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
        '<style>@page{size:960px 540px;margin:0}body{margin:0}'
        + FONT_FACES + '</style></head><body>')
(RENDER / 'combined.html').write_text(head + ''.join(parts) + '</body></html>', encoding='utf-8')
print('combined:', len(files), 'slides ->', RENDER / 'combined.html')
