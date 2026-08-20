# -*- coding: utf-8 -*-
"""v4: колода дискуссии «Организация питания: опыт реализации проектов» (26.08.2026,
14:00–15:30) в едином стиле с докладом «стиль claude»: тёплая слоновая кость,
чернильный текст, терракотовый акцент, Playfair Display + PT Sans.
Подача: одна мысль на слайд, минимум текста, крупные цифры, современные графики
(donut, slope, bars, timeline, лестницы). 38 слайдов 960×540.
Сборка: python build_v4.py [--pdf]  (PDF через headless Edge + pypdf)."""
import os, subprocess, glob, sys

HERE = os.path.dirname(os.path.abspath(__file__))

C = dict(ivory='#FAF9F5', panel='#F0EEE6', panelwarm='#F6F1E9', ink='#141413',
         body='#3D3929', muted='#87867F', soft='#6E6A5E', accent='#C15F3C',
         accentdeep='#B8552F', accentsoft='#F5E7DE', line='#E3DCCE',
         gray='#B7AFA0', dark='#141413', white='#FFFFFF')

CSS = """
@font-face { font-family:'Playfair Display'; src:url('fonts/playfair-700.woff2') format('woff2'); font-weight:700; }
@font-face { font-family:'Playfair Display'; src:url('fonts/playfair-800.woff2') format('woff2'); font-weight:800; }
@font-face { font-family:'Playfair Display'; src:url('fonts/playfair-900.woff2') format('woff2'); font-weight:900; }
@font-face { font-family:'Playfair Display'; src:url('fonts/playfair-600i.woff2') format('woff2'); font-style:italic; font-weight:600; }
@font-face { font-family:'PT Sans'; src:url('fonts/ptsans-400.woff2') format('woff2'); }
@font-face { font-family:'PT Sans'; src:url('fonts/ptsans-700.woff2') format('woff2'); font-weight:bold; }
@page { size:960px 540px; margin:0 }
html,body { margin:0; padding:0 }
.slide { position:relative; width:960px; height:540px; background:%(ivory)s; overflow:hidden;
         font-family:'PT Sans'; color:%(body)s; }
.foot { position:absolute; left:52px; right:52px; bottom:16px; display:flex;
        justify-content:space-between; font-size:10.5px; color:%(muted)s; }
.foot b { color:%(accent)s; font-weight:bold }
.kicker { font-weight:bold; font-size:11.5px; letter-spacing:3px; color:%(accent)s;
          text-transform:uppercase; }
.kickrow { position:absolute; left:52px; top:34px; right:52px; display:flex; align-items:center; gap:14px; }
.kickrow .rule { flex:1; height:1.5px; background:%(line)s; }
h1 { font-family:'Playfair Display'; font-weight:800; margin:0; line-height:1.12; color:%(ink)s; }
.serif { font-family:'Playfair Display'; }
.card { background:%(panel)s; border-radius:14px; }
.tag { display:inline-block; font-weight:bold; font-size:11px; letter-spacing:1.5px;
       padding:3px 10px 2px; border-radius:6px; }
""" % C

def slide(num, body, kicker=None, foot=None, bg=None):
    k = ''
    if kicker:
        k = f'<div class="kickrow"><span class="kicker">{kicker}</span><span class="rule"></span></div>'
    foot_html = (f'<div class="foot"><span>{foot or ""}</span><span><b>{num}</b> / 38</span></div>')
    style = f' style="background:{bg}"' if bg else ''
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body><div class="slide"{style}>{k}{body}{foot_html}</div></body></html>')

def h(text, size=31, color=None, top=66, left=52, width=856, italic=False, weight=800):
    col = f'color:{color};' if color else ''
    it = 'font-style:italic;font-weight:600;' if italic else ''
    w = f'font-weight:{weight};' if weight != 800 else ''
    return (f'<h1 style="position:absolute;left:{left}px;top:{top}px;width:{width}px;'
            f'font-size:{size}px;{col}{it}{w}line-height:1.12">{text}</h1>')

def p(text, top, left=52, width=856, size=15, lh=1.5, color=None, bold=False, align='left', italic=False):
    col = f'color:{color};' if color else ''
    b = 'font-weight:bold;' if bold else ''
    it = 'font-style:italic;' if italic else ''
    return (f'<p style="position:absolute;left:{left}px;top:{top}px;width:{width}px;'
            f'font-size:{size}px;line-height:{lh};{col}{b}{it}text-align:{align};margin:0">{text}</p>')

def box(x, y, w, h, fill=None, radius=14, border=None):
    f = f'background:{fill};' if fill else ''
    b = f'border:1.5px solid {border};' if border else ''
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'{f}{b}border-radius:{radius}px"></div>')

def txt(text, x, y, w, size=13.5, lh=1.45, color=None, bold=False, align='left', serif=False, ls=None, italic=False):
    col = f'color:{color};' if color else ''
    fam = "font-family:'Playfair Display';font-weight:700;" if serif else ''
    fw = 'font-weight:bold;' if (bold and not serif) else ''
    l = f'letter-spacing:{ls}px;' if ls else ''
    it = 'font-style:italic;' if italic else ''
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;font-size:{size}px;'
            f'line-height:{lh};{col}{fam}{fw}{l}{it}text-align:{align}">{text}</div>')

def hbar(labels, values, x, y, w, row_h=42, gap=14, maxv=None, unit='', colors=None):
    maxv = maxv or max(values)
    out = []
    for i, (lab, val) in enumerate(zip(labels, values)):
        yy = y + i * (row_h + gap)
        fill = (colors[i] if colors else C['accent'])
        bw = int((w - 300) * val / maxv)
        out.append(f'<div style="position:absolute;left:{x}px;top:{yy}px;width:230px;height:{row_h}px;'
                   f'display:flex;align-items:center;justify-content:flex-end;text-align:right;'
                   f'font-size:12.5px;color:{C["ink"]};line-height:1.2">{lab}</div>')
        out.append(f'<div style="position:absolute;left:{x+240}px;top:{yy}px;width:{w-240-70}px;height:{row_h}px;'
                   f'background:{C["panel"]};border-radius:7px">'
                   f'<div style="width:{bw}px;height:100%;background:{fill};border-radius:7px 0 0 7px"></div></div>')
        out.append(f'<div style="position:absolute;left:{x+w-64}px;top:{yy}px;height:{row_h}px;display:flex;'
                   f'align-items:center;font-family:\'Playfair Display\';font-weight:700;font-size:19px;color:{fill}">'
                   f'{val}{unit}</div>')
    return ''.join(out)

def donut(pct, cx, cy, r=86, label='', sub=''):
    import math
    circ = 2 * math.pi * r
    dash = circ * pct / 100
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{C["panel"]}" stroke-width="30"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{C["accent"]}" stroke-width="30" '
            f'stroke-dasharray="{dash:.1f} {circ:.1f}" stroke-dashoffset="0" transform="rotate(-90 {cx} {cy})" stroke-linecap="butt"/>'
            f'<text x="{cx}" y="{cy+6}" text-anchor="middle" font-family="Playfair Display" font-weight="800" '
            f'font-size="52" fill="{C["ink"]}">{label}</text>'
            f'<text x="{cx}" y="{cy+38}" text-anchor="middle" font-family="PT Sans" font-size="12" fill="{C["muted"]}">{sub}</text>')

def question_slide(num, kicker, qtext, sub=None, hint=None, foot=None):
    body = box(52, 90, 856, 330, C['panelwarm'], radius=18, border=C['line'])
    inner = (f'<div style="position:absolute;left:84px;top:122px;width:176px;height:176px;'
             f'border-radius:50%;background:{C["ivory"]};border:2px solid {C["line"]};'
             f'box-shadow:0 0 0 9px {C["panel"]};display:flex;align-items:center;justify-content:center">'
             f'<span class="serif" style="font-weight:800;font-size:98px;color:{C["accent"]};line-height:1">?</span></div>')
    inner += (f'<div style="position:absolute;left:298px;top:134px;width:4px;height:150px;'
              f'background:{C["accent"]};border-radius:2px"></div>')
    inner += txt(qtext, 322, 130, 540, size=24, lh=1.32, color=C['ink'], serif=True)
    if sub:
        inner += txt(sub, 322, 318, 540, size=14.5, lh=1.5, color=C['soft'])
    if hint:
        inner += txt(hint, 52, 445, 856, size=12.5, color=C['muted'])
    return slide(num, inner, kicker=kicker, foot=foot or 'Вопрос залу')

# ── библиотека линейных пиктограмм (24×24, stroke) ──
ICONS = {
 'person': '<circle cx="12" cy="7" r="3.2"/><path d="M5.5 20c0-3.6 2.9-6.3 6.5-6.3s6.5 2.7 6.5 6.3"/>',
 'people': '<circle cx="9" cy="8" r="2.8"/><path d="M3.5 19c0-3 2.5-5.4 5.5-5.4s5.5 2.4 5.5 5.4"/><circle cx="16.5" cy="9" r="2.3"/><path d="M15.8 13.9c2.4.4 4.3 2.5 4.3 5.1"/>',
 'plate': '<circle cx="12" cy="12" r="8.6"/><circle cx="12" cy="12" r="4.6"/>',
 'fork': '<path d="M7 3v4.5M9.5 3v4.5M12 3v4.5M9.5 7.5V21M7 7.5h5"/>',
 'knife': '<path d="M16.5 3v18"/><path d="M16.5 3c2.5 3.5 2.5 8.5.5 11h-.5"/>',
 'bowl': '<path d="M4 11.5h16c0 4.4-3.6 8-8 8s-8-3.6-8-8Z"/><path d="M8.5 8c0-1.5 1-2 1-3.5M12.5 8c0-1.5 1-2 1-3.5"/>',
 'cup': '<path d="M5 9h11v4.5a5.5 5.5 0 0 1-11 0Z"/><path d="M16 10.5h1.5a2.5 2.5 0 0 1 0 5H16"/>',
 'grain': '<ellipse cx="8" cy="14" rx="2" ry="3"/><ellipse cx="14.5" cy="12" rx="2" ry="3"/><ellipse cx="11" cy="18.5" rx="2" ry="3"/>',
 'chicken': '<circle cx="9" cy="10" r="4.5"/><path d="M12.2 13.2 17 18M17 18l2.6.6M17 18l.6 2.6"/>',
 'fish': '<path d="M6.5 12c2.5-3.5 6-5 8.7-5 2.1 1.5 3.3 3.2 3.3 5s-1.2 3.5-3.3 5c-2.7 0-6.2-1.5-8.7-5Z"/><path d="M6.5 12 3.5 8.8v6.4Z"/>',
 'moon': '<path d="M19 14.5A8 8 0 0 1 9.5 5 8 8 0 1 0 19 14.5Z"/>',
 'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6 7 7M17 17l1.4 1.4M18.4 5.6 17 7M7 17l-1.4 1.4"/>',
 'doc': '<path d="M6 3h9l4 4v14H6Z"/><path d="M15 3v4h4"/><path d="M9 12h7M9 15.5h7M9 8.5h3"/>',
 'scales': '<path d="M12 4v16M8 20h8M12 6 5 8.5M12 6l7 2.5"/><path d="M2.5 13.5a2.5 2.5 0 0 0 5 0M16.5 13.5a2.5 2.5 0 0 0 5 0"/>',
 'shield': '<path d="M12 3 5 6v6c0 4.5 3 7.5 7 9 4-1.5 7-4.5 7-9V6Z"/>',
 'medcross': '<circle cx="12" cy="12" r="8.5"/><path d="M12 8v8M8 12h8"/>',
 'pill': '<rect x="4" y="9" width="16" height="6.5" rx="3.25" transform="rotate(-35 12 12)"/><path d="M9.6 7.9l4.8 8.2"/>',
 'coin': '<circle cx="12" cy="12" r="8.5"/><path d="M14.5 9.3c-.6-1-1.7-1.5-3-1.5-1.8 0-3 .9-3 2.2 0 3 6 1.6 6 4.4 0 1.4-1.3 2.4-3.2 2.4-1.5 0-2.7-.6-3.3-1.7M12 6.2v1.6M12 16.2v1.6"/>',
 'cart': '<path d="M4 5h2l2.2 10.5h9.3L20 8H7"/><circle cx="9.5" cy="19" r="1.6"/><circle cx="16.5" cy="19" r="1.6"/>',
 'calc': '<rect x="6" y="3" width="12" height="18" rx="2"/><path d="M9 7h6M9 11h.01M12 11h.01M15 11h.01M9 14.5h.01M12 14.5h.01M15 14.5h.01M9 18h4"/>',
 'book': '<path d="M12 6c-2-1.6-4.5-2-8-2v14c3.5 0 6 .4 8 2 2-1.6 4.5-2 8-2V4c-3.5 0-6 .4-8 2Z"/><path d="M12 6v14"/>',
 'checklist': '<path d="M9 4h6v3H9Z"/><path d="M15 5h2a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h2"/><path d="M9 12l1.8 1.8L15 10M9 16.5l1.8 1.8L15 14.5"/>',
 'db': '<ellipse cx="12" cy="6" rx="7" ry="2.8"/><path d="M5 6v12c0 1.6 3.1 2.8 7 2.8s7-1.2 7-2.8V6"/><path d="M5 12c0 1.6 3.1 2.8 7 2.8s7-1.2 7-2.8"/>',
 'warn': '<path d="M12 4 21 19H3Z"/><path d="M12 10v4M12 16.8v.01"/>',
 'pin': '<path d="M12 21s-7-5.7-7-11a7 7 0 0 1 14 0c0 5.3-7 11-7 11Z"/><circle cx="12" cy="10" r="2.6"/>',
 'eye': '<path d="M3 12s3.5-6 9-6 9 6 9 6-3.5 6-9 6-9-6-9-6Z"/><circle cx="12" cy="12" r="2.6"/>',
 'house': '<path d="M4.5 11 12 4l7.5 7"/><path d="M6.5 10v10h11V10"/>',
 'pot': '<rect x="5" y="10" width="14" height="8" rx="2"/><path d="M3.5 12v4M20.5 12v4M9 10V8M15 10V8M9 8h6"/>',
 'tray': '<path d="M4 15h16v3H4Z"/><path d="M6 15a6 6 0 0 1 12 0"/>',
 'arrowrl': '<path d="M7 9h9l-2.5-2.5M17 15H8l2.5 2.5"/>',
 'refresh': '<path d="M19 12a7 7 0 1 1-2-4.9"/><path d="M17.5 3v4.5H13"/>',
 'gear': '<circle cx="12" cy="12" r="3.2"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6 7.7 7.7M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/>',
 'heart': '<path d="M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7a4.3 4.3 0 0 1 7.5 3c0 5.4-7.5 10-7.5 10Z"/>',
 'stamp': '<path d="M9 10h6l1 5H8Z"/><path d="M6 19h12v2H6Z"/><path d="M10 10V7a2 2 0 0 1 4 0v3"/>',
}

def ic(name, x, y, s=28, col=None, sw=1.8, op=1.0):
    col = col or C['accent']
    inner = ICONS[name]
    o = f';opacity:{op}' if op != 1.0 else ''
    return (f'<svg style="position:absolute;left:{x}px;top:{y}px{o}" width="{s}" height="{s}" '
            f'viewBox="0 0 24 24" fill="none" stroke="{col}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{inner}</svg>')

S = []

SPARK = ('<svg width="24" height="24" viewBox="0 0 100 100"><path d="M50 0 L60 38 L85 15 L62 40 L100 50 '
         'L62 60 L85 85 L60 62 L50 100 L40 62 L15 85 L38 60 L0 50 L38 40 L15 15 L40 38 Z" fill="' + C['accent'] + '"/></svg>')

# ═══ 01 Обложка ═══
body = f'''
<div style="position:absolute;left:0;top:0;width:100%;height:100%;background:{C['ivory']}"></div>
<div style="position:absolute;left:0;bottom:0;width:100%;height:14px;background:{C['panel']}"></div>
<div style="position:absolute;left:52px;top:44px;display:flex;align-items:center;gap:12px">
  {SPARK}
  <span class="kicker" style="color:{C['soft']}">ПРОСТРАНСТВО НОВЫХ ИДЕЙ 2.0 · САНКТ-ПЕТЕРБУРГ · 25–27 АВГУСТА 2026</span>
</div>
<div style="position:absolute;left:52px;top:104px;font-size:15px;letter-spacing:2px;color:{C['accent']};font-weight:bold">ДИСКУССИЯ · 26 АВГУСТА · 14.00–15.30 · ПЛОЩАДКА № 2</div>
<h1 style="position:absolute;left:52px;top:146px;width:820px;font-size:46px;line-height:1.08">Организация питания:<br>опыт реализации проектов</h1>
<div style="position:absolute;left:52px;top:280px;width:70px;height:4px;background:{C['accent']}"></div>
<div class="serif" style="position:absolute;left:52px;top:302px;width:740px;font-style:italic;font-weight:600;font-size:17px;line-height:1.5;color:{C['body']}">
Не просто накормить: безопасное, достойное и вариативное питание людей<br>с психическими нарушениями в домах социального обслуживания</div>
<div style="position:absolute;left:52px;top:400px;width:860px;height:1.5px;background:{C['line']}"></div>
<div style="position:absolute;left:52px;top:420px;width:420px;font-size:13.5px;line-height:1.65">
<b>Евгений Чистяков</b> · директор ДСО «Серафимовский», Санкт-Петербург</div>
<div style="position:absolute;left:500px;top:420px;width:412px;font-size:13.5px;line-height:1.65;color:{C['body']}">
<b>Тимур Нурбаев</b> · директор ДСО «Тесовый берег», Санкт-Петербург</div>
<div style="position:absolute;left:446px;top:484px;display:flex;gap:26px;align-items:center">''' + ic('fork', 0, 0, 24, C['soft'], 1.6) + ic('plate', 0, 0, 24, C['accent'], 1.6) + ic('knife', 0, 0, 24, C['soft'], 1.6) + ic('bowl', 0, 0, 24, C['soft'], 1.6) + ic('cup', 0, 0, 24, C['soft'], 1.6) + '''</div>
'''
S.append(slide(1, body, foot='Министерство труда и социальной защиты РФ · Комитет по социальной политике Санкт-Петербурга'))

# ═══ 02 Формат: шесть вопросов ═══
body = h('Разговор на шести вопросах программы', 31)
items = [
    ('1', 'Кто выбирает форму питания — проживающий или руководитель учреждения?', 'person'),
    ('2', 'Как формировать меню в условиях нормативных и финансовых ограничений?', 'doc'),
    ('3', 'Должно ли быть питание в социальных домах «лечебным»?', 'medcross'),
    ('4', 'Как совместить «лечебное питание» и «вариативное меню»?', 'arrowrl'),
    ('5', 'Баланс между правом выбора недееспособного и медицинскими показаниями', 'scales'),
    ('6', 'Качество продуктов против нормирования цен: как совместить?', 'coin'),
]
for i, (n, t, ico) in enumerate(items):
    col, row = i % 2, i // 2
    x, y = 52 + col * 440, 148 + row * 92
    body += box(x, y, 420, 82, C['panel'])
    body += txt(n, x + 20, y + 16, 40, size=30, serif=True, color=C['accent'])
    body += txt(t, x + 64, y + 13, 300, size=13, lh=1.35, color=C['ink'])
    body += ic(ico, x + 376, y + 24, 30, C['accent'], 1.6, 0.9)
S.append(slide(2, body, kicker='Формат · 90 минут', foot='Вопросы воспроизведены дословно по программе семинара'))

# ═══ 03 Разогрев ═══
S.append(question_slide(3, 'Разогрев · 1 минута',
    'Вспомните вчерашний ужин. Поднимите руку, если хоть один житель вашего дома мог выбрать второе блюдо.',
    sub='Рука, которая не поднимается, — это и есть повестка наших 90 минут.',
    hint='Честное «никто не мог» — нормальный старт, а не провал.'))

# ═══ 04 1 095 ═══
body = f'''
<div class="serif" style="position:absolute;left:52px;top:132px;font-weight:900;font-size:185px;line-height:1;color:{C['ink']}">1 095</div>
<div style="position:absolute;left:52px;top:348px;width:60px;height:5px;background:{C['accent']}"></div>
'''
meals = [('cup', 'завтрак'), ('plate', 'обед'), ('bowl', 'ужин')]
for i, (ico, lab) in enumerate(meals):
    x = 52 + i * 190
    body += ic(ico, x, 378, 30, C['accent'], 1.8)
    body += txt(f'<b>{lab}</b> <span style="color:{C["muted"]}">× 365</span>', x + 42, 383, 140, size=14, color=C['ink'])
body += p('приёмов пищи на жителя в год. Каждый из них — решение, которое кто-то принял за человека.', 430, size=16, lh=1.5, bold=True)
S.append(slide(4, body, kicker='Контекст · одно число', foot='Доклад «Не просто накормить», раздел 5'))

# ═══ 05 74 % (donut) ═══
body = h('Недееспособность не отменяет предпочтений', 30)
body += f'<svg style="position:absolute;left:96px;top:150px" width="220" height="220" viewBox="0 0 220 220">{donut(74, 110, 110, 86, "74 %", "недееспособны")}</svg>'
body += txt('Четыре из пяти жителей ПНИ не могут юридически заявить выбор — но выбирают взглядом, ложкой, отказом.', 380, 172, 500, size=16.5, lh=1.55, color=C['ink'])
body += txt('Задача системы — услышать этот выбор другими каналами: наблюдение, биография, «те, кто знает».', 380, 262, 500, size=14.5, lh=1.55, color=C['soft'])
for i in range(10):
    body += ic('person', 382 + i * 40, 348, 32, C['accent'] if i < 7 else C['gray'], 2.0 if i < 7 else 1.6)
body += txt('<b>7 из 10</b> — недееспособны', 382, 390, 400, size=13, color=C['muted'])
S.append(slide(5, body, kicker='Контекст · недееспособность', foot='Доклад, раздел 16 · КПИ, Замечание № 1 к ст. 12'))

# ═══ 06 Ночной интервал ═══
body = h('Ночь без еды: 15 часов — это не экзотика', 30)
# лента суток 0–24: приёмы пищи точками, ночное окно терракотой
SX, SW = 52, 856
body += f'''<div style="position:absolute;left:{SX}px;top:132px;width:{SW}px;height:34px;background:{C['panel']};border-radius:8px;overflow:hidden">
<div style="position:absolute;left:0;top:0;width:{SW*8.5/24:.0f}px;height:100%;background:{C['accent']}"></div>
<div style="position:absolute;left:{SW*17.5/24:.0f}px;top:0;right:0;height:100%;background:{C['accent']}"></div></div>'''
for hr in (0, 6, 12, 18, 24):
    body += txt(f'{hr:02d}', SX - 14 + hr / 24 * SW, 170, 28, size=10.5, align='center', color=C['muted'])
INK, IVORY = C['ink'], C['ivory']
for hr, lab in ((8.5, 'завтрак'), (13, 'обед'), (17.5, 'ужин')):
    body += f'<div style="position:absolute;left:{SX - 5 + hr/24*SW:.0f}px;top:141px;width:10px;height:10px;border-radius:50%;background:{INK};border:2px solid {IVORY}"></div>'
    body += txt(lab, SX - 45 + hr / 24 * SW, 116, 90, size=11.5, align='center', color=C['ink'])
body += ic('moon', SX + SW - 118, 176, 22, C['accentdeep'], 1.8)
body += txt('<b style="color:' + C['accentdeep'] + '">15 ч без еды</b>', SX + SW - 88, 180, 100, size=12.5, color=C['ink'])
body += hbar(['Швеция — ориентир', 'США — норма CMS', 'Типовой дом, РФ'],
             [11, 14, 15], 52, 212, 696, row_h=38, gap=12, unit=' ч',
             colors=[C['gray'], C['soft'], C['accent']])
body += p('Ужин в 17:30 → завтрак в 8:30. Для жителей на антипсихотиках это вес, поведение и ночные «набеги» на кухню.', 376, size=13.5, lh=1.5)
body += box(52, 420, 856, 48, C['accentsoft'])
body += txt('Вопрос залу: какая цифра в вашем доме? Замер — три дня, одна строка в журнале, ноль рублей.', 74, 433, 820, size=13, bold=True, color=C['ink'])
S.append(slide(6, body, kicker='Проблема · ночной интервал', foot='Швеция: Livsmedelsverket · США: 42 CFR 483.60 · РФ: типовые графики'))

# ═══ 07 Цепочка решений ═══
body = h('Единственный, кто ест, — вне цепочки решений', 29)
chain = [('house', 'Регион:<br>нормы и<br>финансы'), ('doc', 'Раскладка:<br>меню-цикл'), ('pot', 'Кухня:<br>закладка'), ('tray', 'Смена:<br>раздача')]
for i, (ico, node) in enumerate(chain):
    x = 52 + i * 196
    body += box(x, 160, 150, 96, C['panel'])
    body += ic(ico, x + 61, 170, 26, C['accent'], 1.7)
    body += txt(node, x + 12, 202, 126, size=12, align='center', lh=1.32, color=C['ink'])
    if i < 3:
        body += f'<div style="position:absolute;left:{x+160}px;top:202px;width:28px;height:2.5px;background:{C["gray"]}"></div>'
body += box(52, 300, 856, 92, C['accentsoft'])
body += txt('ЖИТЕЛЬ', 84, 326, 150, size=24, serif=True, color=C['accentdeep'])
body += txt('— единственный, кто ест, — в этой цепочке не участвует. Его предпочтение — не вход, а помеха: «не ест это», «опять перловка».', 240, 320, 640, size=14.5, lh=1.5, color=C['ink'])
body += p('Дискуссия начинается ровно здесь: вопрос № 1 программы — «кто выбирает?»', 415, size=14.5, bold=True)
S.append(slide(7, body, kicker='Проблема · кто решает', foot='Типовая цепочка решения о рационе в стационаре'))

# ═══ 08 Право ═══
body = h('Право уже разрешает выбор. Запрета нет', 30)
cards = [('442-ФЗ', '«учёт индивидуальной потребности» — выбор блюда укладывается в неё напрямую', 'doc'),
         ('3185-1, ст. 37 и 43', 'достоинство и гуманное отношение — распространены на проживающих ДСО и ПНИ', 'scales'),
         ('СанПиН · обе редакции', 'не менее 3 приёмов, диетическое по показаниям — число вариантов не ограничено', 'shield')]
for i, (t, d, ico) in enumerate(cards):
    x = 52 + i * 294
    body += box(x, 150, 274, 212, C['panel'])
    body += ic(ico, x + 222, 170, 30, C['accent'], 1.7)
    body += txt(t, x + 24, 180, 190, size=17, serif=True, color=C['accentdeep'])
    body += txt(d, x + 24, 226, 228, size=13, lh=1.55, color=C['ink'])
body += p('С 1 сентября 2026 действует новый СанПиН 2.3/2.4.4282-26 — модель выбора не меняется ни на йоту.', 400, size=14.5, bold=True)
S.append(slide(8, body, kicker='Право', foot='ФЗ-442 ст. 9, 16 · Закон 3185-1 ст. 37, 43 · СанПиН 3590-20 → 4282-26'))

# ═══ 09 Практики ═══
body = h('Это уже делают. Шесть публичных историй, 2024–2026', 29)
pts = [('Болотнинский ПНИ', 'Новосибирская обл.', '2024 · два вторых блюда на старте'),
       ('Успенский ПНИ', 'Новосибирская обл.', '2024 · выбор во всех отделениях'),
       ('Усть-Илимский ДСО', 'Иркутская обл.', '2024 · опрос предпочтений → выбор'),
       ('Иркутская область', 'масштаб региона', '2025 · решение для всех учреждений'),
       ('Серафимовский ДСО', 'Санкт-Петербург', '2025–2026 · зал заказного питания'),
       ('Тесовый берег ДСО', 'Санкт-Петербург', 'фарфор, линия раздачи — со-эксперт')]
for i, (name, reg, what) in enumerate(pts):
    col, row = i % 2, i // 2
    x, y = 52 + col * 440, 140 + row * 90
    body += box(x, y, 420, 80, C['panel'])
    body += ic('pin', x + 16, y + 16, 26, C['accent'], 1.7)
    body += txt(f'<b>{name}</b> <span style="color:{C["muted"]};font-size:11.5px">· {reg}</span><br>{what}', x + 54, y + 15, 350, size=12.5, lh=1.4, color=C['ink'])
body += p('Ни один кейс не начинался с «сначала дайте деньги и разрешение».', 435, size=14, bold=True)
S.append(slide(9, body, kicker='Опыт · 2024–2026', foot='Официальные сайты учреждений и учредителей, СМИ · полный реестр — в докладе'))

# ═══ 10 Кейс: что сделали ═══
body = h('Наш кейс: житель заказывает ужин накануне', 30)
body += box(52, 150, 856, 170, C['panel'])
body += ic('checklist', 852, 170, 34, C['accent'], 1.6, 0.9)
body += txt('ЧТО СДЕЛАЛИ', 84, 176, 300, size=13, bold=True, ls=2, color=C['accentdeep'])
body += txt('Несколько месяцев часть жителей выбирала рацион следующего дня по меню. Заказ — накануне, к вечеру известно, что готовить.', 84, 212, 792, size=16, lh=1.6, color=C['ink'])
body += p('Жители приняли выбор с энтузиазмом. Директор — я: рассказываю и про цену, и про пределы.', 350, size=15, italic=False, bold=False)
S.append(slide(10, body, kicker='Кейс · ДСО «Серафимовский»', foot='Комитет по социальной политике СПб, 22.07.2025'))

# ═══ 11 Кейс: цена и предел ═══
body = h('Честно о цене и о пределе', 31)
body += box(52, 146, 424, 220, C['panel'])
body += ic('coin', 424, 166, 32, C['accent'], 1.6, 0.9)
body += txt('ЧТО ЭТО СТОИЛО', 76, 170, 300, size=13, bold=True, ls=2, color=C['accentdeep'])
body += txt('Дополнительное оборудование и ставки пищеблока.<br><br>Старт <b>не был бесплатным</b> — говорю это прямо.', 76, 206, 372, size=14, lh=1.55, color=C['ink'])
body += box(490, 146, 424, 220, C['panelwarm'], border=C['line'])
body += ic('warn', 862, 166, 32, C['accentdeep'], 1.6, 0.9)
body += txt('ГДЕ СЛОМАЛОСЬ', 514, 170, 300, size=13, bold=True, ls=2, color=C['soft'])
body += txt('Полный переход труден: нормы сбалансированности, здоровье, тяга к популярному, но неполезному.<br><br>Ответ — пары эквивалентов, а не запрет.', 514, 206, 372, size=14, lh=1.55, color=C['ink'])
body += p('Универсального «бесплатного старта» нет — это калибрует ожидания зала.', 400, size=14, bold=True)
S.append(slide(11, body, kicker='Кейс · цена и предел', foot='Доклад, раздел 25.5 · публикация учредителя, 22.07.2025'))

# ═══ 12 Кейс: приказ ═══
body = f'''
<div style="position:absolute;left:52px;top:120px;width:70px;height:4px;background:{C['accent']}"></div>
<div class="serif" style="position:absolute;left:52px;top:150px;width:860px;font-weight:800;font-size:34px;line-height:1.3;color:{C['ink']}">Вариативность закреплена<br>локальным актом</div>
'''
body += txt('Приказ № 124 от 10.03.2026', 52, 288, 500, size=26, serif=True, color=C['accentdeep'])
body += ic('stamp', 470, 286, 40, C['accent'], 1.6, 0.9)
body += txt('зал заказного питания · вариативное меню', 52, 334, 500, size=16, color=C['soft'])
body += box(600, 150, 308, 210, C['panel'])
body += txt('ЧТО ЭТО МЕНЯЕТ', 624, 172, 260, size=12, bold=True, ls=2, color=C['accentdeep'])
body += txt('Не «эксперимент по новости», а локальный акт: пережил смену настроения и стал опорой перед проверяющими.', 624, 204, 262, size=13, lh=1.55, color=C['ink'])
body += p('Первый известный нам случай фиксации вариативности приказом в российском ПНИ/ДСО.', 400, size=14.5, bold=True)
S.append(slide(12, body, kicker='Кейс · развитие', foot='Источник S035: www.pni9.ru — официальный сайт учреждения'))

# ═══ 13 Мост к коллеге ═══
body = h('Слово со-эксперту', 32)
body += box(52, 150, 856, 200, C['panel'])
body += txt('ТИМУР НУРБАЕВ', 84, 178, 400, size=26, serif=True, color=C['ink'])
body += txt('директор ДСО «Тесовый берег»,<br>Санкт-Петербург', 84, 222, 400, size=14.5, lh=1.5, color=C['soft'])
body += txt('ЧТО УЖЕ ВИДНО В «ТЕСОВОМ БЕРЕГЕ»', 524, 172, 380, size=12, bold=True, ls=2, color=C['accentdeep'])
for i, (f, ico) in enumerate([('фарфор вместо железных мисок', 'plate'), ('вилки и ножи на столе', 'fork'), ('самообслуживание: поднос и линия раздачи', 'tray'), ('тренировочная кухня — доступ круглосуточно', 'house')]):
    body += ic(ico, 524, 200 + i * 33, 22, C['accent'], 1.7)
    body += txt(f, 556, 203 + i * 33, 340, size=13.5, color=C['ink'])
body += p('Два эксперта — один разговор: мой блок — вариативность и право выбора, дальше — общая дискуссия.', 400, size=14.5, bold=True)
S.append(slide(13, body, kicker='Со-эксперт сессии', foot='Практика ДСО «Тесовый берег» — портал ОЮП СПб (upchspb.ru), 2026'))

# ═══ 14 Лестница вариативности ═══
body = h('Лестница вариативности: пять ступеней вверх', 30)
steps = [('0', 'Мономеню с учётом отказов'), ('1', 'Выбор из двух в одной позиции'), ('2', 'Выбор по всем позициям'),
         ('3', 'Шведская линия'), ('4', 'Семейная подача'), ('5', 'Своя кухня')]
for i, (n, t) in enumerate(steps):
    x = 52 + i * 144
    y = 330 - i * 38
    fill = C['panel'] if i < 2 else C['accent'] if i < 4 else C['ink']
    body += box(x, y, 130, 60 + i * 38, fill, radius=8)
    col = C['ink'] if i < 2 else '#FFF9F2'
    body += txt(f'<span class="serif" style="font-weight:800;font-size:22px">{n}</span><br>{t}', x + 10, y + 10, 110, size=11, lh=1.3, color=col)
body += p('Ступени 1–2 подтверждены практикой 2024–2025 годов. Ступени 3–5 — горизонт, а не требование.', 445, size=14, bold=True)
S.append(slide(14, body, kicker='Как растёт вариативность', foot='Доклад, раздел 8'))

# ═══ 15 Лестница участия ═══
body = h('Вторая ось: сколько контроля вернулось жителю', 29)
rows = [('0', 'Выбора нет — еда определена чужими решениями'),
        ('1', 'Спросили — но тарелка та же'),
        ('2', 'Его выбор дошёл до тарелки сегодня'),
        ('3', 'Выбрал ещё время и место еды'),
        ('4', 'Влияет на меню через совет жителей'),
        ('5', 'Еда снова часть жизни: кухня, гости, биография')]
for i, (n, t) in enumerate(rows):
    y = 138 + i * 47
    body += box(52, y, 60, 38, C['accent'] if i >= 2 else C['panel'], radius=8)
    body += txt(n, 52, y + 6, 60, size=20, serif=True, align='center', color='#FFF9F2' if i >= 2 else C['ink'])
    body += txt(t, 130, y + 9, 770, size=14.5, color=C['ink'])
body += p('Проект поднимает сразу по двум осям — ступень следует выбирать по жителю, а не по бюджету.', 432, size=13.5, bold=True)
S.append(slide(15, body, kicker='Как растёт участие', foot='Доклад, раздел 8.4'))

# ═══ 16 В1 суть ═══
body = h('Вопрос 1. Три слоя ответа', 31)
layers = [('person', 'Право', '442-ФЗ, 3185-1, ГК 29/30: выбор — реализация прав, а не милость'),
          ('gear', 'Процедура', 'кто и как фиксирует выбор: журнал, совет, опекун — роль каждого'),
          ('heart', 'Культура', '«за него решили» → «у него спросили» — самый медленный и главный слой')]
for i, (ico, t, d) in enumerate(layers):
    y = 148 + i * 88
    body += box(52, y, 856, 78, C['panel'])
    body += ic(ico, 258, y + 24, 30, C['accent'], 1.7)
    body += txt(t, 84, y + 24, 200, size=19, serif=True, color=C['accentdeep'])
    body += txt(d, 310, y + 16, 570, size=14.5, lh=1.5, color=C['ink'])
body += p('«Хозяин» из формулировки программы читаем как «руководитель учреждения» (правка № 15).', 424, size=12.5, color=C['muted'])
S.append(slide(16, body, kicker='Вопрос 1 · суть', foot='442-ФЗ · 3185-1 ст. 37, 43 · ГК ст. 29, 30 · доклад, разделы 15–16'))

# ═══ 17 В1 голосование ═══
S.append(question_slide(17, 'Вопрос 1 · голосование',
    'Кто в вашем доме сегодня отвечает на вопрос «что сегодня на обед»?',
    sub='Поднимите руку: кухня? диетсестра? директор? совет жителей? сам житель?',
    hint='В большинстве домов ответ — «раскладка три года назад». Это и есть первый кандидат на изменение.'))

# ═══ 18 В2 пары ═══
body = h('Норма ограничивает набор. Не выбор', 31)
pairs = [('grain', 'Гречка ↔ рис ↔ пшено', C['ink']), ('chicken', 'Курица ↔ индейка', C['accentdeep']), ('fish', 'Треска ↔ хек', C['ink'])]
for i, (ico, lab, col) in enumerate(pairs):
    body += ic(ico, 52, 162 + i * 62, 34, C['accent'], 1.8)
    body += txt(lab, 102, 168 + i * 62, 430, size=28, serif=True, color=col)
body += txt('Таблицы замены в раскладках — существующий законный механизм: равноценная замена внутри группы продуктов.', 52, 356, 470, size=14, lh=1.55, color=C['soft'])
body += box(560, 150, 348, 240, C['panel'])
body += txt('ЧТО ЭТО СТОИТ', 584, 174, 300, size=12, bold=True, ls=2, color=C['accentdeep'])
body += txt('Сырьё пары сопоставимо — копейки на порцию.<br><br>Реальная цена — труд и порядок: журнал заказа, вторая гастроёмкость, обучение смены.', 584, 206, 302, size=13.5, lh=1.55, color=C['ink'])
body += p('Норма — рамка содержимого тарелки, а не число тарелок.', 420, size=15, bold=True)
S.append(slide(18, body, kicker='Вопрос 2 · суть', foot='Приказ Минтруда 520н (рекомендательные нормы) · доклад, раздел 19'))

# ═══ 19 В2 стоимость ═══
body = h('Что действительно стоит второй вариант', 30)
body += hbar(['Сырьё: пара «гречка/рис»', 'Сырьё: пара «курица/индейка»', 'Труд смены (мин/день)', 'Отходы несъеденного (замер)'],
             [1, 4, 3, 30], 52, 150, 696, unit='', maxv=30,
             colors=[C['gray'], C['gray'], C['soft'], C['accent']])
body += p('Настоящая статья потерь — то, что лежит в тарелках несъеденным.', 340, size=15, lh=1.5)
body += box(52, 400, 856, 52, C['accentsoft'])
body += txt('Калькулятор (приложение 42) считает вашу пару за вечер: цена кг и масса порции. Никаких «общих цифр» — только ваш замер.', 74, 415, 820, size=13, bold=True, color=C['ink'])
S.append(slide(19, body, kicker='Вопрос 2 · экономика', foot='Иллюстративные доли; методика — доклад, раздел 29 и приложение 42'))

# ═══ 20 В2 вопрос ═══
S.append(question_slide(20, 'Вопрос 2 · к залу',
    'Что дороже: второй вариант на линии — или тарелки, которые уносят несъеденными?',
    sub='Замер отходов за 7 дней отвечает на этот вопрос в рублях. У кого есть такой замер?',
    hint='«Замер до и после» — единственная честная экономика вариативности.'))

# ═══ 21 В3 суть ═══
body = h('Вопрос 3. «Лечебное» — не кухня, а врач', 30)
body += box(52, 146, 424, 220, C['panel'])
body += ic('doc', 424, 166, 32, C['accent'], 1.6, 0.9)
body += txt('ЧТО ГОВОРЯТ НОРМЫ', 76, 170, 340, size=12, bold=True, ls=2, color=C['accentdeep'])
body += txt('Приказы о лечебном питании (330н, 395н) адресованы медицинским организациям.<br><br>Для ДСО: 3 приёма + диетическое по показаниям.', 76, 202, 372, size=13.5, lh=1.55, color=C['ink'])
body += box(490, 146, 424, 220, C['accentsoft'])
body += ic('warn', 862, 166, 32, C['accentdeep'], 1.6, 0.9)
body += txt('ЧЕМ ЭТО ГРОЗИТ', 514, 170, 340, size=12, bold=True, ls=2, color=C['accentdeep'])
body += txt('«Лечебность» руками кухни — диагноз повара. Диагнозы ставит врач.<br><br>Самовольная «диетизация» — риск и для здоровья, и для проверки.', 514, 202, 372, size=13.5, lh=1.55, color=C['ink'])
body += p('Позиция доклада: обычное питание + диетическое по показаниям. «Лечебное всем» — имитация стандарта.', 400, size=14.5, bold=True)
S.append(slide(21, body, kicker='Вопрос 3 · суть', foot='Приказы Минздрава 330н, 395н · СанПиН п. 56 · доклад, раздел 17.5'))

# ═══ 22 В3 голосование ═══
body = h('Голосование: должно ли питание быть «лечебным»?', 28)
body += box(52, 130, 424, 260, C['panel'])
body += f'<div style="position:absolute;left:52px;top:130px;width:424px;height:5px;background:{C["soft"]};border-radius:4px 4px 0 0"></div>'
body += txt('А', 84, 160, 60, size=46, serif=True, color=C['ink'])
body += ic('doc', 140, 168, 30, C['soft'], 1.7)
body += txt('Нет. Обычное питание, диетическое — поимённо по показаниям, назначает врач.', 84, 224, 360, size=15, lh=1.55, color=C['ink'])
body += box(490, 130, 424, 260, C['accentsoft'])
body += f'<div style="position:absolute;left:490px;top:130px;width:424px;height:5px;background:{C["accent"]};border-radius:4px 4px 0 0"></div>'
body += txt('Б', 522, 160, 60, size=46, serif=True, color=C['accentdeep'])
body += ic('pill', 578, 168, 30, C['accentdeep'], 1.7)
body += txt('Да. Стол дома должен быть лечебным по умолчанию — так безопаснее.', 522, 224, 360, size=15, lh=1.55, color=C['ink'])
body += p('Руки за А. Руки за Б. Возражения — микрофон: самое интересное начнётся здесь.', 422, size=14.5, bold=True)
S.append(slide(22, body, kicker='Вопрос 3 · голосование', foot='Аргументы обеих позиций — доклад, раздел 17.12, вопрос 3'))

# ═══ 23 В4 venn ═══
body = h('«Лечебное» × «вариативное» — не враги', 30)
svg = f'''<svg style="position:absolute;left:150px;top:140px" width="660" height="230" viewBox="0 0 660 230">
<circle cx="240" cy="115" r="105" fill="{C['panel']}" opacity="0.95"/>
<circle cx="420" cy="115" r="105" fill="{C['accentsoft']}" opacity="0.95"/>
<text x="185" y="110" font-family="PT Sans" font-size="15" font-weight="bold" fill="{C['ink']}">ЛЕЧЕБНАЯ РАМКА</text>
<text x="160" y="135" font-family="PT Sans" font-size="12.5" fill="{C['body']}">назначил врач:</text>
<text x="160" y="153" font-family="PT Sans" font-size="12.5" fill="{C['body']}">стол, текстура, соль</text>
<text x="395" y="110" font-family="PT Sans" font-size="15" font-weight="bold" fill="{C['accentdeep']}">ВАРИАТИВНОСТЬ</text>
<text x="365" y="135" font-family="PT Sans" font-size="12.5" fill="{C['body']}">выбор внутри рамки:</text>
<text x="365" y="153" font-family="PT Sans" font-size="12.5" fill="{C['body']}">пары, вкус, привычное</text>
<text x="268" y="105" font-family="Playfair Display" font-size="14" font-weight="700" fill="{C['ink']}">ЗОНА</text>
<text x="245" y="127" font-family="Playfair Display" font-size="14" font-weight="700" fill="{C['ink']}">ПРАКТИКИ</text>
</svg>'''
body += svg
body += p('Рецепт: врач задаёт стол — внутри него всегда есть пары. Так работает дом в Московской области (распоряжение 19РВ-32).', 392, size=14.5, lh=1.55)
S.append(slide(23, body, kicker='Вопрос 4 · конструкция', foot='Распоряжение Минсоцразвития МО 19РВ-32 · доклад, разделы 17.5, 19'))

# ═══ 24 В4 алгоритм ═══
body = h('Четыре шага, чтобы совместить', 31)
steps = [('doc', '1', 'Врач назначает рамку', 'стол/текстура/ограничения — поимённо, с пересмотром'),
         ('arrowrl', '2', 'Внутри рамки — пары', 'диетический стол тоже имеет эквиваленты'),
         ('checklist', '3', 'Журнал замен', 'выбор фиксируется — защита жителя и врача'),
         ('refresh', '4', 'Пересмотр', 'статистика выбора → корректировка цикла раз в квартал')]
for i, (ico, n, t, d) in enumerate(steps):
    x = 52 + i * 220
    body += box(x, 150, 200, 222, C['panel'])
    body += ic(ico, x + 156, 168, 28, C['accent'], 1.6, 0.9)
    body += txt(n, x + 20, 172, 40, size=34, serif=True, color=C['accent'])
    body += txt(f'<b>{t}</b><br><br>{d}', x + 20, 224, 164, size=12.5, lh=1.5, color=C['ink'])
body += p('Диета — ограничение множества, а не сжатие до одного блюда.', 415, size=15, bold=True)
S.append(slide(24, body, kicker='Вопрос 4 · алгоритм', foot='Доклад, разделы 19, 21'))

# ═══ 25 В5 каналы воли ═══
body = h('Недееспособный выбирает. Каналы воли', 30)
body += box(52, 150, 856, 180, C['panel'])
ch = [('eye', 'Показ двух порций', 'выбор глазами и рукой'), ('plate', 'Наблюдение за съеденным', 'что осталось — то и сигнал'),
      ('book', 'Пищевая биография', 'привычки всей жизни'), ('people', '«Те, кто знает»', 'персонал, родные, опекун')]
for i, (ico, t, d) in enumerate(ch):
    x = 84 + i * 208
    body += txt(f'<span class="serif" style="font-weight:800;font-size:24px;color:{C["accent"]}">{i+1}</span>', x, 172, 40)
    body += ic(ico, x + 152, 172, 26, C['accent'], 1.6, 0.9)
    body += txt(f'<b>{t}</b>', x, 212, 186, size=12.5, lh=1.4, color=C['ink'])
    body += txt(f'<span style="color:{C["soft"]}">{d}</span>', x, 254, 186, size=11.5, lh=1.4)
body += p('Замещающее решение («мы знаем лучше») — запрещено подходом КПИ. Граница — медицина: «два безопасных» вместо «одно назначенное».', 366, size=14.5, lh=1.55, bold=False)
S.append(slide(25, body, kicker='Вопрос 5 · суть', foot='КПИ, Замечание № 1 к ст. 12 · доклад, разделы 15–16'))

# ═══ 26 В5 slope IDDSI ═══
body = h('Обучение работает лучше оборудования', 29)
svg = f'''<svg style="position:absolute;left:120px;top:140px" width="700" height="260" viewBox="0 0 700 260">
<line x1="200" y1="30" x2="200" y2="220" stroke="{C['line']}" stroke-width="2"/>
<line x1="520" y1="30" x2="520" y2="220" stroke="{C['line']}" stroke-width="2"/>
<text x="200" y="248" text-anchor="middle" font-family="PT Sans" font-size="12.5" fill="{C['muted']}">ДО внедрения</text>
<text x="520" y="248" text-anchor="middle" font-family="PT Sans" font-size="12.5" fill="{C['muted']}">ПОСЛЕ</text>
<line x1="200" y1="{220-44*1.9:.0f}" x2="520" y2="{220-90*1.9:.0f}" stroke="{C['accent']}" stroke-width="3.5"/>
<circle cx="200" cy="{220-44*1.9:.0f}" r="7" fill="{C['gray']}"/>
<circle cx="520" cy="{220-90*1.9:.0f}" r="7" fill="{C['accent']}"/>
<text x="185" y="{220-44*1.9-12:.0f}" text-anchor="end" font-family="Playfair Display" font-weight="700" font-size="17" fill="{C['soft']}">44 %</text>
<text x="535" y="{220-90*1.9-12:.0f}" font-family="Playfair Display" font-weight="700" font-size="17" fill="{C['accentdeep']}">90 %</text>
<text x="185" y="{220-44*1.9+16:.0f}" text-anchor="end" font-family="PT Sans" font-size="11.5" fill="{C['muted']}">соответствие</text>
<text x="535" y="{220-90*1.9+16:.0f}" font-family="PT Sans" font-size="11.5" fill="{C['muted']}">соответствие</text>
<line x1="200" y1="{220-31*1.9:.0f}" x2="520" y2="{220-100*1.9:.0f}" stroke="{C['soft']}" stroke-width="2.5" stroke-dasharray="1 0"/>
<circle cx="200" cy="{220-31*1.9:.0f}" r="6" fill="{C['gray']}"/>
<circle cx="520" cy="{220-100*1.9:.0f}" r="6" fill="{C['ink']}"/>
<text x="185" y="{220-31*1.9-10:.0f}" text-anchor="end" font-family="Playfair Display" font-weight="700" font-size="15" fill="{C['soft']}">31 %</text>
<text x="535" y="{220-100*1.9-10:.0f}" font-family="Playfair Display" font-weight="700" font-size="15" fill="{C['ink']}">100 %</text>
<text x="185" y="{220-31*1.9+14:.0f}" text-anchor="end" font-family="PT Sans" font-size="11" fill="{C['muted']}">загущённые</text>
<text x="535" y="{220-100*1.9+14:.0f}" font-family="PT Sans" font-size="11" fill="{C['muted']}">загущённые</text>
</svg>'''
body += svg
body += p('Пять учреждений, единая шкала текстур IDDSI. Главный барьер — не техника, а осведомлённость смены.', 400, size=14.5, bold=True)
S.append(slide(26, body, kicker='Вопрос 5 · безопасность', foot='Исследование внедрения IDDSI (5 учреждений) · GUSS, Trapl 2007 · доклад, разделы 10.9–10.10'))

# ═══ 27 В5 вопрос ═══
S.append(question_slide(27, 'Вопрос 5 · к залу',
    'Вспомните жителя, который не говорит. Как он вчера дал понять, что не хочет это блюдо?',
    sub='Отвернулся? ест только хлеб? доел компот и оставил котлету? — это и была его «заявка».',
    hint='Кто назовёт один такой сигнал из своего дома? Микрофон.'))

# ═══ 28 В6 3-6× ═══
body = h('Нормируя цену порции, управляем меньшей частью денег', 27)
body += hbar(['Сырьё — то, что нормируем', 'Труд кухни и раздачи', 'Энергия, логистика, оборудование'],
             [1, 3, 5], 52, 170, 696, unit='×', maxv=5,
             colors=[C['accent'], C['soft'], C['ink']])
body += p('Полная стоимость обеда в 3–6 раз выше сырьевой строки (канадский аудит стационаров).', 340, size=14.5, color=C['soft'])
body += p('Экономить надо на потерях — отходы, срывы поставок, картельные наценки, — а не на белке в тарелке.', 380, size=15.5, bold=True)
S.append(slide(28, body, kicker='Вопрос 6 · экономика качества', foot='Аудит стоимости стационарного питания (Канада) · доклад, разделы 29, 42'))

# ═══ 29 В6 закупки ═══
body = h('Где действительно теряются деньги', 30)
body += box(52, 146, 424, 230, C['accentsoft'])
body += ic('cart', 424, 166, 32, C['accentdeep'], 1.6, 0.9)
body += txt('543 ТОРГА · 4,7 МЛРД ₽', 76, 168, 380, size=22, serif=True, color=C['accentdeep'])
body += txt('Картель на поставках социально значимых продуктов (ФАС, 2024).', 76, 214, 372, size=13.5, lh=1.5, color=C['ink'])
body += txt('Сигналы: два-три «своих» поставщика, минус доли процента от начальной цены, «проигравший» побеждает в соседнем лоте.', 76, 288, 372, size=12.5, lh=1.5, color=C['soft'])
body += box(490, 146, 424, 230, C['panel'])
body += ic('doc', 862, 166, 32, C['accent'], 1.6, 0.9)
body += txt('АУТСОРСИНГ: 8 СТРОК', 514, 168, 380, size=22, serif=True, color=C['ink'])
body += txt('Если кормит подрядчик — вариативность живёт в контракте: группы позиций, гарантия двух вариантов, замены, текстуры, пробы, отчётность.', 514, 214, 372, size=13.5, lh=1.55, color=C['ink'])
body += p('Пробы, бракераж и ответственность остаются у учреждения — даже когда плита у подрядчика.', 402, size=13.5, bold=True)
S.append(slide(29, body, kicker='Вопрос 6 · закупки и подряд', foot='ФАС России, 2024 · СанПиН п. 56 (подп. 4, 12, 14) · доклад, раздел 42'))

# ═══ 30 В6 вопрос ═══
S.append(question_slide(30, 'Вопрос 6 · к залу',
    'Сколько стоит один обед в вашем доме — в рублях? Кто знает точную цифру?',
    sub='Не «на тысячу проживающих в год». Один обед. Один житель. Сегодня.',
    hint='Знание цены — начало управления ею. Цифра есть у каждого на калькуляторе приложения 42.'))

# ═══ 31 Три ошибки ═══
body = h('Три ошибки дороже бездействия', 31)
errs = [('Имитация выбора', '«Выбирайте!» — при одном блюде на линии. Хуже честного мономеню: обманывает журнал и проверяющего.'),
        ('Выбор без гарантии', 'Житель выбрал Б — Б закончилось. Нет стандартного варианта — нет системы, есть лотерея.'),
        ('«Лечебность» без врача', 'Кухня назначает столы сама. Диагноз от повара — риск здоровью и дело по ст. 6.6 КоАП.')]
for i, (t, d) in enumerate(errs):
    x = 52 + i * 294
    body += box(x, 148, 274, 232, C['panelwarm'], border=C['line'])
    body += ic('warn', x + 226, 166, 30, C['accentdeep'], 1.6, 0.9)
    body += txt(str(i + 1), x + 24, 168, 40, size=30, serif=True, color=C['accentdeep'])
    body += txt(f'<b>{t}</b><br><br>{d}', x + 24, 216, 228, size=12.5, lh=1.55, color=C['ink'])
S.append(slide(31, body, kicker='Красные линии', foot='Доклад, разделы 21, 12, 17 · практика проверок 2021–2025'))

# ═══ 32 Сентябрь: таймлайн ═══
body = h('1 сентября 2026: новый СанПиН — без паники', 30)
body += f'''<div style="position:absolute;left:52px;top:210px;width:856px;height:3px;background:{C['line']};border-radius:2px"></div>'''
miles = [('до 31.08', 'журналы законны<br>как заполнены', C['soft']), ('01.09', 'вступает<br>СанПиН 4282-26', C['accent']), ('сентябрь', 'перепривязать<br>документы', C['ink'])]
for i, (d, t, col) in enumerate(miles):
    x = 132 + i * 300
    body += f'<div style="position:absolute;left:{x-9}px;top:202px;width:18px;height:18px;border-radius:50%;background:{col}"></div>'
    body += txt(d, x - 125, 152, 250, size=19, serif=True, align='center', color=C['ink'])
    body += txt(t, x - 125, 246, 250, size=13.5, align='center', lh=1.5, color=C['body'])
body += box(52, 330, 856, 64, C['panel'])
body += txt('Перепривязать: положение о питании, формы журналов (приложения 4–5 нового СанПиН), ППК и ХАССП. Переходного периода нет.', 76, 348, 810, size=13.5, bold=True, color=C['ink'])
body += p('Число вариантов блюда не ограничено ни в одной редакции правил.', 424, size=14, bold=True)
S.append(slide(32, body, kicker='Переход', foot='Постановление от 02.06.2026 № 18 · чек-лист перехода — приложение 39 доклада'))

# ═══ 33 Три шага ═══
body = h('Три шага с понедельника. Без денег и разрешений', 28)
steps = [('checklist', 'Замер', '7 дней: ночной интервал, отходы, кто выбирал. Одна страница, ноль рублей.'),
         ('plate', 'Один вариант выбора', 'Одна позиция, одно отделение, два блюда. Журнал заказа — тетрадь.'),
         ('medcross', 'Правило трёх отказов', 'Три отказа подряд — врач сегодня. Поперхнулся — врач немедленно.')]
for i, (ico, t, d) in enumerate(steps):
    x = 52 + i * 294
    body += box(x, 148, 274, 212, C['panel'])
    body += ic(ico, x + 224, 166, 30, C['accent'], 1.6, 0.9)
    body += txt(t, x + 24, 176, 190, size=19, serif=True, color=C['accentdeep'])
    body += txt(d, x + 24, 222, 228, size=13, lh=1.55, color=C['ink'])
body += p('Через 90 дней у вас будут числа. С ними идут и к учредителю, и к проверяющему.', 400, size=14.5, bold=True)
S.append(slide(33, body, kicker='Что сделать в понедельник', foot='Доклад, раздел 35 «Пилот 90 дней» · чек-лист — приложение 5 семинарского пакета'))

# ═══ 34 Смежные площадки ═══
body = h('Смежные площадки: наши пересечения', 30)
cross = [('«Право на выбор: есть или нет?»', 'вопросы 1–2: выбор реализуется людьми, а не приказом'),
         ('«Право быть недееспособным»', 'вопрос 5: интересы выявляются, а не назначаются'),
         ('«Нужны ли врачи в доме?»', 'вопрос 3: «лечебность» без врача — не забота, а риск'),
         ('«Со-настройка с опекой»', 'вопрос 1: опекун — участник выявления воли, не цензор меню'),
         ('«Чьи голоса громче?»', 'совет жителей обсуждает еду первой: жалобы на стол — самые частые'),
         ('«Право на достойный уход»', 'комфортное кормление в конце жизни — тоже право выбора')]
for i, (t, d) in enumerate(cross):
    col, row = i % 2, i // 2
    x, y = 52 + col * 440, 145 + row * 88
    body += box(x, y, 420, 78, C['panel'])
    body += txt(f'<b>{t}</b><br><span style="color:{C["soft"]}">{d}</span>', x + 20, y + 13, 386, size=12, lh=1.4, color=C['ink'])
S.append(slide(34, body, kicker='Программа 25–27.08 · связи', foot='Формулировки площадок — по программе семинара · связи — раздел 17.12 доклада'))

# ═══ 35 Материалы ═══
body = h('Что вы уносите с собой', 31)
items = [('book', 'Доклад «Не просто накормить»', '250 страниц: право, клиника, экономика, 45 приложений-шаблонов'),
         ('calc', 'Калькулятор стоимости', 'Excel: ваша пара блюд и ваши отходы — за один вечер'),
         ('checklist', 'Чек-листы и журналы', 'экспресс-аудит, журнал замен, пищевой паспорт, План Б'),
         ('db', 'Реестр источников', '125 проверенных позиций — каждое число проверяемо')]
for i, (ico, t, d) in enumerate(items):
    x = 52 + i * 220
    body += box(x, 150, 200, 222, C['panel'])
    body += ic(ico, x + 160, 168, 28, C['accent'], 1.6, 0.9)
    body += txt(f'<b>{t}</b><br><br>{d}', x + 18, 176, 160, size=12.5, lh=1.55, color=C['ink'])
body += txt('Всё открыто — сканируйте QR:', 52, 408, 300, size=14, bold=True, color=C['ink'])
body += f'<img src="qr.png" style="position:absolute;left:388px;top:390px;width:92px;height:92px;border-radius:10px">'
body += txt('github.com/qlolp/<br>seminar-variable-food-2026', 502, 412, 400, size=14.5, color=C['body'])
S.append(slide(35, body, kicker='Материалы', foot='github.com/qlolp/seminar-variable-food-2026'))

# ═══ 36 Открытый микрофон ═══
S.append(question_slide(36, 'Открытый микрофон · 20 минут',
    'Что в ваших домах ломается первым — когда речь заходит о выборе блюд?',
    sub='Деньги? руки? страх проверки? «у нас особые жители»? начать не с чего?',
    hint='Каждое «ломается» из зала — готовый пункт повестки для ваших учредителей.'))

# ═══ 37 Финал ═══
body = f'''
<div style="position:absolute;left:0;top:0;width:100%;height:100%;background:{C['dark']}"></div>
<div style="position:absolute;left:52px;top:74px;width:120px;height:5px;background:{C['accent']}"></div>
<div style="position:absolute;left:52px;top:116px;width:830px;font-family:'Playfair Display';font-weight:800;font-size:39px;line-height:1.28;color:#FAF9F5">
Тарелка — самое частое решение,<br>которое дом принимает за жителя.<br><span style="color:{C['accent']}">Вернуть его жителю — самое простое<br>из всех прав, что у нас есть.</span></div>
<div style="position:absolute;left:52px;bottom:52px;font-size:13px;color:#87867F">Дискуссия «Организация питания: опыт реализации проектов» · 26.08.2026 · Чистяков · Нурбаев</div>
''' + ic('fork', 828, 60, 44, '#87867F', 1.4, 0.9) + ic('plate', 778, 56, 52, '#FAF9F5', 1.4, 0.85) + ic('knife', 736, 60, 44, '#87867F', 1.4, 0.9)
S.append(slide(37, body, foot=''))

# ═══ 38 Спасибо ═══
body = h('Спасибо. Продолжаем разговор', 34)
body += p('Евгений Чистяков · ДСО «Серафимовский», Санкт-Петербург<br>Тимур Нурбаев · ДСО «Тесовый берег», Санкт-Петербург', 150, size=15, lh=1.7)
body += box(52, 240, 856, 120, C['panel'])
body += txt('Материалы сессии — доклад, калькулятор, чек-листы, реестр источников:<br><b>github.com/qlolp/seminar-variable-food-2026</b>', 80, 268, 620, size=15, lh=1.7, color=C['ink'])
body += f'<img src="qr.png" style="position:absolute;left:782px;top:262px;width:76px;height:76px;border-radius:8px">'
body += p('Вопросы после сессии — лично и по каналам связи в раздатке.', 400, size=13, color=C['muted'])
S.append(slide(38, body, kicker='Контакты', foot='«Пространство новых идей 2.0» · 25–27.08.2026 · Санкт-Петербург'))

# ── запись ──
os.makedirs(f'{HERE}/slides', exist_ok=True)
for i, html_doc in enumerate(S, 1):
    open(f'{HERE}/slides/slide-{i:02d}.html', 'w', encoding='utf-8').write(html_doc)
print(len(S), 'slides written')

# ── PDF ──
if '--pdf' in sys.argv:
    from pypdf import PdfReader, PdfWriter
    EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    PDF_DIR = f'{HERE}/_pdf'
    os.makedirs(PDF_DIR, exist_ok=True)
    for i in range(1, len(S) + 1):
        p_pdf = f'{PDF_DIR}/p{i:02d}.pdf'
        if os.path.exists(p_pdf):
            continue
        url = 'file:///' + f'{HERE}/slides/slide-{i:02d}.html'.replace('\\', '/').lstrip('/')
        subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
                        '--no-sandbox', f'--print-to-pdf={p_pdf}', url],
                       capture_output=True, timeout=120)
    w = PdfWriter()
    ok = sorted(glob.glob(f'{PDF_DIR}/p*.pdf'))
    for f in ok:
        w.append(f)
    out = f'{HERE}/Презентация_v4_дискуссия_26_08_стиль_claude.pdf'
    with open(out, 'wb') as fh:
        w.write(fh)
    print(f'PDF: {len(ok)} slides -> {out}')
