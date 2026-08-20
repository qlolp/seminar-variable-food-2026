# -*- coding: utf-8 -*-
"""Рендер слайдов презентации: pages/*.page + <deck>/<pptd>.pptd → <deck>/_render/*.html (960×540).

Запуск: python render_slides.py [папка_дека] [файл_pptd]
По умолчанию: презентация_34_слайда 03_презентация.pptd

Дополнения к базовой версии:
- стили-референсы вида style: "$kicker" резолвятся из textStyles темы .pptd;
- shape поддерживает скругление fill.radius / cornerRadius и opacity (только для превью/PDF);
- @font-face для PT Serif из ../проект/output/fonts (шрифт не установлен в системе).
"""
import yaml, glob, os, re, sys

DECK = sys.argv[1] if len(sys.argv) > 1 else 'презентация_34_слайда'
PPTD = sys.argv[2] if len(sys.argv) > 2 else '03_презентация.pptd'
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), DECK))

CFG = yaml.safe_load(open(PPTD, encoding='utf-8'))
theme = CFG['theme']
COLORS = theme['colors']
TEXT_STYLES = theme.get('textStyles', {})

FONT_FACES = """
@font-face { font-family:'PT Serif'; src:url('../../проект/output/fonts/PTSerif-Regular.ttf'); font-weight:400; }
@font-face { font-family:'PT Serif'; src:url('../../проект/output/fonts/PTSerif-Bold.ttf'); font-weight:700; }
@font-face { font-family:'PT Serif'; src:url('../../проект/output/fonts/PTSerif-Italic.ttf'); font-style:italic; }
"""


def col(c):
    if isinstance(c, str) and c.startswith('$'):
        return COLORS.get(c[1:], '#000')
    return c or '#000'


def px(v):
    return str(v) + 'px'


def render_text(el):
    c = el.get('content', {})
    x, y, w, h = el['bounds']
    # стиль-референс из темы (style: "$name")
    ref = {}
    if isinstance(c.get('style'), str) and c['style'].startswith('$'):
        ref = TEXT_STYLES.get(c['style'][1:], {})
    fs = c.get('fontSize', ref.get('fontSize', 14))
    lh = c.get('lineHeight', ref.get('lineHeight', 1.35))
    color = col(c.get('color', ref.get('color', '#141413')))
    family = c.get('fontFamily', ref.get('fontFamily', 'Noto Sans'))
    style = ('position:absolute;left:%s;top:%s;width:%s;height:%s;'
             'font-size:%s;line-height:%s;color:%s;font-family:\'%s\';'
             % (px(x), px(y), px(w), px(h), px(fs), lh, color, family))
    if c.get('bold', ref.get('bold')):
        style += 'font-weight:bold;'
    if c.get('letterSpacing', ref.get('letterSpacing')):
        style += 'letter-spacing:%spx;' % c.get('letterSpacing', ref.get('letterSpacing'))
    al = c.get('align')
    if al:
        if isinstance(al, list):
            ta = next((a for a in ('left', 'right', 'center', 'justify') if a in al), None)
            if ta:
                style += 'text-align:%s;' % ta
        else:
            style += 'text-align:%s;' % al
    extra = c.get('style')
    if isinstance(extra, str) and not extra.startswith('$'):
        style += extra
    return '<div style="%s">%s</div>' % (style, c.get('text', ''))


def render_shape(el):
    x, y, w, h = el['bounds']
    name = el.get('shapeName', 'rect')
    f = el.get('fill', {})
    bg = col(f.get('color')) if f.get('type') == 'solid' else 'transparent'
    rad = {'ellipse': 'border-radius:50%;',
           'homePlate': 'clip-path:polygon(0 0,72% 0,100% 50%,72% 100%,0 100%);'}.get(name, '')
    if f.get('radius'):
        rad += 'border-radius:%spx;' % f['radius']
    if el.get('cornerRadius'):
        rad += 'border-radius:%spx;' % el['cornerRadius']
    op = el.get('opacity', f.get('opacity'))
    opac = ('opacity:%s;' % op) if op not in (None, 1, 1.0) else ''
    return ('<div style="position:absolute;left:%s;top:%s;width:%s;height:%s;'
            'background:%s;%s%s"></div>' % (px(x), px(y), px(w), px(h), bg, rad, opac))


def render_line(el):
    x, y, w, h = el['bounds']
    vb = el.get('viewBox', [w, h])
    pts = el.get('points', '')
    b = el.get('border', {})
    arrows = el.get('arrow') or [None, None]
    mk = (('marker-start="url(#arr)" ' if arrows[0] == 'arrow' else '') +
          ('marker-end="url(#arr)" ' if arrows[1] == 'arrow' else ''))
    return ('<svg style="position:absolute;left:%s;top:%s" width="%s" height="%s" viewBox="0 0 %s %s">'
            '<defs><marker id="arr" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
            '<path d="M0,0 L6,3 L0,6" fill="none" stroke="%s" stroke-width="1.5"/></marker></defs>'
            '<polyline points="%s" fill="none" stroke="%s" stroke-width="%s" %s/></svg>'
            % (px(x), px(y), w, h, vb[0], vb[1], col(b.get('color')), pts,
               col(b.get('color')), b.get('width', 2), mk))


def render_table(el):
    x, y, w, h = el['bounds']
    rows = el.get('rows', [])
    cw = el.get('columnWidths')
    rh = el.get('rowHeights')
    st = el.get('style', {})
    cs = st.get('cellStyle', {})
    fr = st.get('firstRowStyle', {})
    out = ['<table style="position:absolute;left:%s;top:%s;width:%s;border-collapse:collapse;table-layout:fixed">'
           % (px(x), px(y), px(w))]
    if cw:
        out.append('<colgroup>' + ''.join('<col style="width:%s%%">' % (c * 100) for c in cw) + '</colgroup>')
    for ri, row in enumerate(rows):
        out.append('<tr>')
        hgt = ('height:%spx;' % (rh[ri] * h)) if rh else ''
        for cell in row:
            txt = cell.get('text', '') if isinstance(cell, dict) else str(cell)
            bold = 'font-weight:bold;' if ri == 0 else ''
            color = col(fr.get('color')) if ri == 0 else col(cs.get('color'))
            fs = fr.get('fontSize', 13) if ri == 0 else cs.get('fontSize', 13)
            out.append('<td style="%sborder:0.5px solid %s;padding:4px 6px;font-size:%spx;line-height:1.3;%scolor:%s;font-family:Noto Sans;vertical-align:middle">%s</td>'
                       % (hgt, col(COLORS.get('line')), fs, bold, color, txt))
        out.append('</tr>')
    out.append('</table>')
    return ''.join(out)


def render_chart(el):
    x, y, w, h = el['bounds']
    d = el.get('data', {})
    series = el.get('series', [])
    rows = d.get('rows', [])
    cols = d.get('cols', [])
    num_cols = [i for i, c in enumerate(cols) if rows and all(isinstance(r[i], (int, float)) for r in rows)]
    lab_col = 0 if 0 not in num_cols else 1
    mx = el.get('xAxis', {}).get('max') or max((r[i] for r in rows for i in num_cols), default=100) or 100
    head = "<div style='font:11px Noto Sans;color:#8A8578;margin:0 0 6px'>%s</div>" % (el.get('xAxis', {}).get('title', ''))
    bars = []
    for r in rows:
        lab = r[lab_col]
        inner = ''
        for si, i in enumerate(num_cols):
            val = float(r[i])
            pct = min(100, val / mx * 100)
            fill = col(series[si].get('fill')) if si < len(series) else COLORS.get('primary', '#1A7A70')
            inner += "<div style='width:%s%%;height:%s%%;background:%s'></div>" % (pct, 100.0 / len(num_cols), fill)
        total = sum(float(r[i]) for i in num_cols)
        pctall = min(100, total / mx * 100)
        lab_txt = ' / '.join(str(r[i]) for i in num_cols)
        bars.append(
            "<div style='display:flex;align-items:center;gap:8px;margin:7px 0'>"
            "<div style='flex:0 0 46%%;font:12.5px Noto Sans;color:#4A463C;text-align:right'>%s</div>"
            "<div style='flex:1;background:#EFECE3;height:%spx;position:relative'>"
            "<div style='display:flex;flex-direction:column;justify-content:center;width:%s%%;height:100%%'>%s</div>"
            "<span style='position:absolute;left:%s%%;top:50%%;transform:translateY(-50%%);margin-left:8px;font:bold 12px Noto Sans;color:#1F6E5C'>%s</span>"
            "</div></div>" % (lab, max(18, 24 * len(num_cols)), pctall, inner, pctall, lab_txt))
    return "<div style='position:absolute;left:%s;top:%s;width:%s'>%s%s</div>" % (px(x), px(y), px(w), head, ''.join(bars))


RENDER = {'text': render_text, 'shape': render_shape, 'line': render_line,
          'table': render_table, 'chart': render_chart}

os.makedirs('_render', exist_ok=True)
pages = []
for fn in sorted(glob.glob('pages/*.page')):
    d = yaml.safe_load(open(fn, encoding='utf-8'))
    bg = d.get('background', {})
    bgcolor = col(bg.get('color')) if bg.get('type') == 'solid' else '#F9F9F7'
    body = ''.join(RENDER[el['elementType']](el) for el in d.get('elements', []) if el['elementType'] in RENDER)
    htmlsrc = ('<!DOCTYPE html><html><head><meta charset="utf-8"><style>@page{size:960px 540px;margin:0}'
               'body{margin:0}.slide{position:relative;width:960px;height:540px;background:%s;overflow:hidden}'
               '%s</style></head><body><div class="slide">%s</div></body></html>') % (bgcolor, FONT_FACES, body)
    out = os.path.join('_render', os.path.basename(fn).replace('.page', '.html'))
    open(out, 'w', encoding='utf-8').write(htmlsrc)
    pages.append(out)
print(len(pages), 'pages rendered')
