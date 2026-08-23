# -*- coding: utf-8 -*-
"""v5: 21 слайд дискуссии 26.08.2026. Стиль claude, факты по канону доклада.
Сборка: PATH=/opt/homebrew/bin:$PATH python3 build_v5.py --pdf
HTML всегда; PDF — WeasyPrint CLI + pdfunite. PYTHONPATH не задавать.
Google Fonts — только в браузерных HTML; WeasyPrint видит local @font-face."""
import glob, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))

IVORY, CARD = '#FAF9F5', '#F5EFE6'
INK, MID, MUTED = '#2B1D14', '#5C3D2E', '#87867F'
ACCENT, LINE = '#B96420', '#E3DCCE'
DARK = '#2B1D14'

# Local first (Lat before Cyr — U+0020 lives in Lat subset). Google names last.
SERIF = "'Playfair Lat','Playfair Cyr','Playfair Display',serif"
SANS = "'Inter Lat','Inter Ext','Inter Cyr','Inter',system-ui,sans-serif"

GGL = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600'
    '&family=Playfair+Display:ital,wght@0,700;0,800;0,900;1,600&display=swap" '
    'rel="stylesheet">'
)

FACE = """
@font-face { font-family:'Playfair Lat'; src:url('fonts/playfair-700-lat.woff2') format('woff2'); font-weight:700; }
@font-face { font-family:'Playfair Cyr'; src:url('fonts/playfair-700-cyr.woff2') format('woff2'); font-weight:700; }
@font-face { font-family:'Playfair Lat'; src:url('fonts/playfair-800-lat.woff2') format('woff2'); font-weight:800; }
@font-face { font-family:'Playfair Cyr'; src:url('fonts/playfair-800-cyr.woff2') format('woff2'); font-weight:800; }
@font-face { font-family:'Playfair Lat'; src:url('fonts/playfair-900-lat.woff2') format('woff2'); font-weight:900; }
@font-face { font-family:'Playfair Cyr'; src:url('fonts/playfair-900-cyr.woff2') format('woff2'); font-weight:900; }
@font-face { font-family:'Playfair Lat'; src:url('fonts/playfair-600i-lat.woff2') format('woff2'); font-style:italic; font-weight:600; }
@font-face { font-family:'Playfair Cyr'; src:url('fonts/playfair-600i-cyr.woff2') format('woff2'); font-style:italic; font-weight:600; }
@font-face { font-family:'Inter Lat'; src:url('fonts/inter-400-lat.woff2') format('woff2'); font-weight:400; }
@font-face { font-family:'Inter Ext'; src:url('fonts/inter-400-ext.woff2') format('woff2'); font-weight:400; }
@font-face { font-family:'Inter Cyr'; src:url('fonts/inter-400-cyr.woff2') format('woff2'); font-weight:400; }
@font-face { font-family:'Inter Lat'; src:url('fonts/inter-600-lat.woff2') format('woff2'); font-weight:600; }
@font-face { font-family:'Inter Ext'; src:url('fonts/inter-600-ext.woff2') format('woff2'); font-weight:600; }
@font-face { font-family:'Inter Cyr'; src:url('fonts/inter-600-cyr.woff2') format('woff2'); font-weight:600; }
"""

CSS = f"""
{FACE}
@page {{ size:960px 540px; margin:0 }}
html,body {{ margin:0; padding:0 }}
.slide {{ position:relative; width:960px; height:540px; background:{IVORY};
         overflow:hidden; font-family:{SANS}; color:{INK}; }}
.foot {{ position:absolute; right:52px; bottom:14px; font-size:32px;
        color:{MUTED}; line-height:1; font-weight:400; }}
.kicker {{ font-weight:600; font-size:11px; letter-spacing:2px; color:{MID};
           text-transform:uppercase; }}
h1 {{ font-family:{SERIF}; font-weight:800; margin:0; line-height:1.12; color:{INK}; }}
.serif {{ font-family:{SERIF}; }}
"""


def slide(num, body, bg=None, foot_color=None):
    fc = foot_color or MUTED
    foot = f'<div class="foot" style="color:{fc}">{num}</div>'
    style = f' style="background:{bg}"' if bg else ''
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8">'
            f'{GGL}<style>{CSS}</style></head>'
            f'<body><div class="slide"{style}>{body}{foot}</div></body></html>')


def kick(text, y=52, color=None):
    col = color or MID
    return (f'<div class="kicker" style="position:absolute;left:52px;top:{y}px;'
            f'width:856px;color:{col}">{text}</div>')


def h(text, size=42, top=88, left=52, width=856, color=None, weight=800):
    col = color or INK
    return (f'<h1 style="position:absolute;left:{left}px;top:{top}px;width:{width}px;'
            f'font-size:{size}px;font-weight:{weight};color:{col}">{text}</h1>')


def t(text, x, y, w, size=16, color=None, bold=False, serif=False,
      italic=False, align='left', lh=1.3, weight=None):
    col = color or INK
    fam = f'font-family:{SERIF};' if serif else ''
    if weight is None:
        weight = 600 if bold else 400
    it = 'font-style:italic;' if italic else ''
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;'
            f'font-size:{size}px;line-height:{lh};color:{col};{fam}'
            f'font-weight:{weight};{it}text-align:{align}">{text}</div>')


def bar(x=52, y=200, w=48, h=3):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;'
            f'height:{h}px;background:{ACCENT}"></div>')


def panel(x, y, w, h, inner='', leftbar=True):
    lb = (f'<div style="position:absolute;left:0;top:0;width:4px;height:{h}px;'
          f'background:{ACCENT}"></div>' if leftbar else '')
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;'
            f'height:{h}px;background:{CARD};border-radius:8px;overflow:hidden">'
            f'{lb}{inner}</div>')


def donut_svg(x, y, size=200, pct=74, stroke=22):
    r = (size / 2) - stroke
    cx = cy = size / 2
    circ = 2 * 3.14159265 * r
    dash = circ * pct / 100.0
    gap = circ - dash
    return (
        f'<svg style="position:absolute;left:{x}px;top:{y}px" width="{size}" '
        f'height="{size}" viewBox="0 0 {size} {size}">'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{CARD}" '
        f'stroke-width="{stroke}"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ACCENT}" '
        f'stroke-width="{stroke}" stroke-linecap="butt" '
        f'stroke-dasharray="{dash:.2f} {gap:.2f}" '
        f'transform="rotate(-90 {cx} {cy})"/>'
        f'</svg>'
    )


OUT = []


def add(html):
    OUT.append(html)


# ── 01 Титул ──
add(slide(1,
    kick('Санкт-Петербург · 26 августа 2026 · 14:00–15:30') +
    h('Не просто накормить', 64, top=118, weight=900) +
    bar(52, 214, 48, 3) +
    t('Как право выбора доходит до тарелки', 52, 236, 856, size=20,
      italic=True, serif=True, weight=600, color=MID) +
    t('<b style="font-weight:600">Чистяков Евгений Владимирович</b><br>'
      'директор СПб ГАСУСОН «ДСО „Серафимовский“»<br>223-ФЗ',
      52, 360, 420, size=15, color=INK, lh=1.4) +
    t('<b style="font-weight:600">Нурбаев Тимур Аликович</b><br>'
      'директор СПб ГБСУСОН «ДСО „Тесовый берег“»<br>44-ФЗ',
      500, 360, 408, size=15, color=INK, lh=1.4)
))

# ── 02 Три конфликта ──
conf = [
    ('1', 'Выбор или безопасность?', 'Врач задаёт рамку. Внутри рамки — пары.'),
    ('2', 'Вариативность или норматив и бюджет?', 'Норма ограничивает набор продуктов. Не выбор.'),
    ('3', 'Единое меню или индивидуальная поддержка?', 'Стандарт всегда на линии. Предпочтение — в карте.'),
]
body = kick('Формат · 90 минут') + h('Разговор о трёх конфликтах', 38, top=84)
for i, (n, title, desc) in enumerate(conf):
    y = 148 + i * 108
    inner = (
        t(n, 20, 16, 56, size=40, serif=True, weight=900, color=ACCENT) +
        t(title, 84, 18, 740, size=18, bold=True) +
        t(desc, 84, 48, 740, size=15, color=MID)
    )
    # t() uses absolute page coords; nest with inline instead
    inner = (
        f'<div class="serif" style="position:absolute;left:20px;top:18px;'
        f'font-weight:900;font-size:40px;color:{ACCENT};line-height:1">{n}</div>'
        f'<div style="position:absolute;left:84px;top:20px;width:740px;'
        f'font-size:18px;font-weight:600;color:{INK}">{title}</div>'
        f'<div style="position:absolute;left:84px;top:50px;width:740px;'
        f'font-size:15px;font-weight:400;color:{MID}">{desc}</div>'
    )
    body += panel(52, y, 856, 96, inner)
add(slide(2, body))

# ── 03 2 190 ──
meals = ['завтрак', '2-й завтрак', 'обед', 'полдник', 'ужин', '2-й ужин']
body = t('2 190', 52, 48, 856, size=200, serif=True, weight=900, color=ACCENT, lh=0.9)
body += t('приёмов пищи на жителя в год', 52, 248, 856, size=18, color=MID)
for i, lab in enumerate(meals):
    col, row = i % 3, i // 3
    x, y = 52 + col * 292, 292 + row * 72
    inner = (f'<div class="serif" style="position:absolute;left:0;top:18px;width:276px;'
             f'text-align:center;font-weight:700;font-size:18px;color:{INK}">{lab}</div>')
    body += panel(x, y, 276, 60, inner, leftbar=False)
body += t('Каждый из них — решение, принятое за человека', 52, 448, 800, size=16, bold=True)
add(slide(3, body))

# ── 04 74 % — недееспособность, не блюда ──
body = t('74 %', 52, 72, 520, size=180, serif=True, weight=900, color=ACCENT, lh=0.9)
body += donut_svg(680, 64, size=200, pct=74, stroke=24)
body += t('порядка трёх из четырёх жителей — недееспособны', 52, 280, 856, size=22,
          serif=True, weight=700)
body += t('Агрегированно по ПНИ РФ, 2024. Выбор блюда — не сделка (ст. 29 ГК).', 52, 322, 856, size=16, color=MID)
body += t('«Если быть точным», 2024. Не ТАСС. Не Минтруд.', 52, 390, 856, size=15, color=MUTED)
body += t('В вашем доме цифра будет другой.', 52, 424, 856, size=16, bold=True)
add(slide(4, body))

# ── 05 15 часов — пример, не норма ──
body = h('15 часов без еды', 52, top=64, weight=900)
body += t('пример расписания, не норма; цель дома — не длиннее 13 часов',
          52, 140, 856, size=14, color=MID)
# time bar 19:00 → 10:00
body += t('19:00', 52, 210, 120, size=18, bold=True, color=ACCENT)
body += t('ужин', 52, 234, 120, size=14, color=MUTED)
body += t('10:00', 788, 210, 120, size=18, bold=True, align='right', color=ACCENT)
body += t('завтрак', 788, 234, 120, size=14, color=MUTED, align='right')
body += f'<div style="position:absolute;left:52px;top:280px;width:856px;height:16px;background:{CARD};border-radius:8px;overflow:hidden"><div style="width:100%;height:16px;background:{ACCENT}"></div></div>'
body += t('15 часов', 52, 308, 856, size=18, serif=True, weight=700, align='center', color=ACCENT)
body += t('14 часов — потолок CMS (США), не чек-лист дома.', 52, 400, 856, size=15, color=MUTED)
body += t('Какая цифра у вас?', 52, 436, 856, size=18, bold=True)
add(slide(5, body))

# ── 06 Право ──
body = h('Закон не требует выбора.<br>И не запрещает замену.', 36, top=52)
left = (
    f'<div style="position:absolute;left:24px;top:28px;width:360px;'
    f'font-family:{SERIF};font-weight:700;font-size:18px;color:{INK};line-height:1.3">'
    f'442-ФЗ не даёт права<br>на ежедневный выбор блюда</div>'
)
right = (
    f'<div style="position:absolute;left:24px;top:28px;width:360px;'
    f'font-family:{SERIF};font-weight:700;font-size:18px;color:{INK};line-height:1.3">'
    f'И не запрещает замену<br>внутри раскладки</div>'
)
body += panel(52, 168, 412, 140, left)
body += panel(496, 168, 412, 140, right)
body += t('С 01.09.2026 — СанПиН 2.3/2.4.4282-26. Число вариантов не ограничено.',
          52, 332, 856, size=16, color=MID)
body += t('На проверку — папка, не формула.', 52, 400, 856, size=22, serif=True, weight=700, color=ACCENT)
add(slide(6, body))

# ── 07 Регионы 2×2 ──
regs = [
    ('Болотнинский ПНИ', 'Новосибирская обл.', 'Два вторых на старте'),
    ('Успенский ПНИ', 'Новосибирская обл.', 'М2 · все отделения · по два: второе, салат, напиток'),
    ('Усть-Илимский ДСО', 'Иркутская обл.', 'Опрос предпочтений → выбор'),
    ('Серафимовский ДСО', 'Санкт-Петербург', 'Заказное питание'),
]
body = kick('Опыт · 2024–2026') + h('Это уже делают', 40, top=80)
for i, (name, place, fact) in enumerate(regs):
    col, row = i % 2, i // 2
    x, y = 52 + col * 436, 148 + row * 132
    inner = (
        f'<div style="position:absolute;left:20px;top:14px;width:392px;font-size:11px;'
        f'font-weight:600;letter-spacing:2px;text-transform:uppercase;color:{MID}">{place}</div>'
        f'<div class="serif" style="position:absolute;left:20px;top:36px;width:392px;'
        f'font-weight:800;font-size:20px;color:{INK}">{name}</div>'
        f'<div style="position:absolute;left:20px;top:72px;width:392px;font-size:15px;'
        f'font-weight:400;color:{MID};line-height:1.3">{fact}</div>'
    )
    body += panel(x, y, 420, 120, inner)
body += t('Ни один кейс не начинался со «сначала дайте деньги».', 52, 424, 856, size=16, bold=True)
add(slide(7, body))

# ── 08 Заказное · приказ 124 от 10.03.2026 ──
steps8 = [
    ('1', 'Житель выбирает рацион накануне из предложенного меню'),
    ('2', 'Предпочтение фиксируется в журнале отделения'),
    ('3', 'Кухня готовит по заявкам отделений'),
]
body = h('Модель «заказное питание»', 38, top=52)
for i, (n, line) in enumerate(steps8):
    y = 128 + i * 80
    inner = (
        f'<div class="serif" style="position:absolute;left:20px;top:16px;'
        f'font-weight:900;font-size:32px;color:{ACCENT}">{n}</div>'
        f'<div style="position:absolute;left:72px;top:22px;width:740px;font-size:18px;'
        f'font-weight:600;color:{INK}">{line}</div>'
    )
    body += panel(52, y, 856, 68, inner)
body += t('Приказ № 124 от 10.03.2026 — заказное в правилах дома.', 52, 388, 856, size=16, color=MID)
body += t('СПб ГАСУСОН · 223-ФЗ. Полный переход дома — не закрыт.', 52, 420, 856, size=15, color=MUTED)
add(slide(8, body))

# ── 09 Тимур / Тесовый ──
tes = [
    'Фарфор вместо железных мисок',
    'Вилки и ножи на столе',
    'Поднос и линия раздачи',
    'Тренировочная кухня — круглосуточно',
]
body = kick('Со-модератор сессии') + h('Слово Тимуру Нурбаеву', 40, top=80)
body += t('Нурбаев Тимур Аликович', 52, 150, 400, size=18, bold=True)
body += t('директор СПб ГБСУСОН<br>«ДСО „Тесовый берег“»<br>бюджетное · 44-ФЗ',
          52, 184, 400, size=15, color=MID, lh=1.45)
body += t('Что уже видно в «Тесовом береге»', 496, 150, 412, size=14, color=MUTED, bold=True)
for i, line in enumerate(tes):
    y = 180 + i * 52
    inner = (
        f'<div style="position:absolute;left:20px;top:14px;width:372px;font-size:16px;'
        f'font-weight:600;color:{INK}">{line}</div>'
    )
    body += panel(496, y, 412, 44, inner)
add(slide(9, body))

# ── 10 Кто решает ──
who = ['Он сам', 'Сотрудник отделения', 'Врач', 'Кухня', 'Региональная норма']
body = h('Кто решает, что на тарелке?', 38, top=52)
for i, lab in enumerate(who):
    y = 118 + i * 58
    body += t(str(i + 1), 52, y, 48, size=28, serif=True, weight=900, color=ACCENT)
    body += t(lab, 110, y + 4, 740, size=22, serif=True, weight=700)
body += t('Чаще всего отвечают «кухня» и «норма».', 52, 424, 856, size=16, bold=True, color=MID)
add(slide(10, body))

# ── 11 Организация, не бюджет ──
body = h('Вариативность — вопрос организации, не бюджета', 32, top=52)
ex = [
    ('Пары эквивалентов', 'Гречка или рис. Курица или индейка. Сырьё то же.'),
    ('Два котла, не вторая кухня', 'Один поток, две закладки. Журнал — тетрадь.'),
]
for i, (title, desc) in enumerate(ex):
    x = 52 + i * 436
    inner = (
        f'<div class="serif" style="position:absolute;left:24px;top:28px;width:368px;'
        f'font-weight:800;font-size:22px;color:{INK};line-height:1.25">{title}</div>'
        f'<div style="position:absolute;left:24px;top:100px;width:368px;font-size:16px;'
        f'color:{MID};line-height:1.4">{desc}</div>'
    )
    body += panel(x, 140, 420, 200, inner)
body += t('Норматив на продукты не меняется.', 52, 368, 856, size=18, bold=True)
body += t('М1–М2: сырьё перераспределяется внутри строки. Не добавляется.', 52, 404, 856, size=15, color=MUTED)
add(slide(11, body))

# ── 12 Кто не говорит ──
ways = [
    ('1', 'Показ двух порций', 'выбор глазами'),
    ('2', 'Наблюдение за тарелкой', 'что съедено, что осталось'),
    ('3', 'Пищевая биография', 'привычки из прошлого'),
    ('4', 'Те, кто знает', 'персонал, родные, опекун'),
]
body = h('Индивидуальная поддержка не требует речи', 32, top=52)
for i, (n, title, desc) in enumerate(ways):
    col, row = i % 2, i // 2
    x, y = 52 + col * 436, 128 + row * 140
    inner = (
        f'<div class="serif" style="position:absolute;left:20px;top:20px;'
        f'font-weight:900;font-size:36px;color:{ACCENT}">{n}</div>'
        f'<div class="serif" style="position:absolute;left:72px;top:24px;width:320px;'
        f'font-weight:800;font-size:20px;color:{INK}">{title}</div>'
        f'<div style="position:absolute;left:72px;top:60px;width:320px;font-size:15px;'
        f'color:{MID}">{desc}</div>'
    )
    body += panel(x, y, 420, 124, inner)
add(slide(12, body))

# ── 13 Безопасность · IDDSI · КПИ без усиления ──
body = h('Безопасность и выбор — не противоречат', 32, top=52)
body += t('Замещающее решение («мы знаем лучше») — не стандарт ст. 12 КПИ.', 52, 128, 856, size=18, color=INK)
body += t('Замечание общего порядка № 1: поддержать волю, не заменить её «лучшими интересами».',
          52, 160, 856, size=15, color=MID)
inner = (
    f'<div class="serif" style="position:absolute;left:24px;top:24px;width:808px;'
    f'font-weight:800;font-size:22px;color:{INK}">Текстуру назначает врач</div>'
    f'<div style="position:absolute;left:24px;top:64px;width:808px;font-size:16px;'
    f'color:{MID}">IDDSI — язык описания консистенции, не само назначение.</div>'
)
body += panel(52, 220, 856, 120, inner)
body += t('Рамка врача сжимает множество. Не тарелку до одного блюда.', 52, 368, 856, size=16, bold=True)
add(slide(13, body))

# ── 14 Измеряйте ──
mets = [
    ('1', 'Доля жителей, выбравших блюдо сегодня'),
    ('2', 'Сколько порций ушло целиком'),
    ('3', 'Активные предпочтения в реестре'),
]
body = h('Измеряйте, не декларируйте', 40, top=52)
for i, (n, line) in enumerate(mets):
    y = 128 + i * 72
    inner = (
        f'<div class="serif" style="position:absolute;left:20px;top:16px;'
        f'font-weight:900;font-size:28px;color:{ACCENT}">{n}</div>'
        f'<div style="position:absolute;left:68px;top:20px;width:740px;font-size:18px;'
        f'font-weight:600;color:{INK}">{line}</div>'
    )
    body += panel(52, y, 856, 60, inner)
body += t('(измеренное / возможное) × 100%', 52, 368, 856, size=22, serif=True, weight=700, color=ACCENT)
body += t('Процент выбравших — не KPI. Человек вправе не выбирать.', 52, 408, 856, size=15, color=MUTED)
add(slide(14, body))

# ── 15 Качество × цена — без выдуманного майонеза ──
body = h('Качество не требует повышения норматива', 32, top=52)
q = [
    ('Нормативная цена', 'Верхняя граница расходов. Ниже неё — уложиться.'),
    ('Качество', 'Нижняя граница товара. Планка — в ТЗ до торгов.'),
]
for i, (title, desc) in enumerate(q):
    x = 52 + i * 436
    inner = (
        f'<div class="serif" style="position:absolute;left:24px;top:28px;width:368px;'
        f'font-weight:800;font-size:22px;color:{INK}">{title}</div>'
        f'<div style="position:absolute;left:24px;top:72px;width:368px;font-size:16px;'
        f'color:{MID};line-height:1.4">{desc}</div>'
    )
    body += panel(x, 128, 420, 160, inner)
body += t('Серафимовский — 223-ФЗ. Тесовый берег — 44-ФЗ. Один учредитель, разные контуры.',
          52, 320, 856, size=16, color=INK)
body += t('Экономить на потерях, не на белке. Сырьевая строка — замер, не лозунг.',
          52, 400, 856, size=16, bold=True, color=MID)
add(slide(15, body))

# ── 16 Три ошибки ──
errs = [
    ('1', 'Ждать разрешения сверху', 'Папка делается дома. Не в министерстве.'),
    ('2', 'Внедрять сразу для всех', 'Одно отделение. Один приём пищи.'),
    ('3', 'Не измерять результат', 'Без замера — убеждение, не знание.'),
]
body = kick('Действия · чего не делать') + h('Три главные ошибки', 40, top=80)
for i, (n, title, desc) in enumerate(errs):
    x = 52 + i * 292
    inner = (
        f'<div class="serif" style="position:absolute;left:20px;top:20px;'
        f'font-weight:900;font-size:40px;color:{ACCENT}">{n}</div>'
        f'<div class="serif" style="position:absolute;left:20px;top:76px;width:236px;'
        f'font-weight:800;font-size:18px;color:{INK};line-height:1.25">{title}</div>'
        f'<div style="position:absolute;left:20px;top:140px;width:236px;font-size:14px;'
        f'color:{MID};line-height:1.35">{desc}</div>'
    )
    body += panel(x, 148, 276, 220, inner)
body += t('Начните с одного отделения и одного приёма пищи.', 52, 392, 856, size=16, bold=True)
add(slide(16, body))

# ── 17 СанПиН — возможность, не обязанность, не запрет ──
body = t('01.09', 52, 48, 856, size=160, serif=True, weight=900, color=ACCENT, lh=0.9)
body += t('2026', 52, 200, 400, size=28, serif=True, weight=700, color=MID)
body += t('В контуре стационара вариативное меню не запрещено новым СанПиН 4282-26.',
          52, 252, 856, size=20, serif=True, weight=700)
body += t('Это возможность, не обязанность. И не запрет.', 52, 330, 856, size=18, color=INK)
body += t('Журналы августа не переписывать. Число вариантов блюда не ограничено ни в одной редакции.',
          52, 400, 856, size=15, color=MUTED)
add(slide(17, body))

# ── 18 Три шага с понедельника ──
mon = [
    ('1', 'Спросите жителей', 'Кто ест котлету, кто — рыбу. Один обед.'),
    ('2', 'Запишите', 'Простая таблица. Журнал, не система.'),
    ('3', 'Передайте на кухню', 'Заявка на вторник. Житель выбрал — житель получил.'),
]
body = kick('Действия · что делать') + h('Три шага с понедельника', 38, top=80)
for i, (n, title, desc) in enumerate(mon):
    x = 52 + i * 292
    inner = (
        f'<div class="serif" style="position:absolute;left:20px;top:20px;'
        f'font-weight:900;font-size:40px;color:{ACCENT}">{n}</div>'
        f'<div class="serif" style="position:absolute;left:20px;top:76px;width:236px;'
        f'font-weight:800;font-size:18px;color:{INK}">{title}</div>'
        f'<div style="position:absolute;left:20px;top:120px;width:236px;font-size:15px;'
        f'color:{MID};line-height:1.35">{desc}</div>'
    )
    body += panel(x, 148, 276, 220, inner)
body += t('Первый цикл занимает один день.', 52, 392, 856, size=16, bold=True)
add(slide(18, body))

# ── 19 Четыре показателя ──
inds = [
    ('1', 'Сколько жителей выбирают', 'человек'),
    ('2', 'Сколько отделений участвуют', 'шт.'),
    ('3', 'Доля съеденного', '%'),
    ('4', 'Вариантов в меню', 'шт.'),
]
body = h('Четыре показателя для старта', 36, top=52)
for i, (n, title, unit) in enumerate(inds):
    col, row = i % 2, i // 2
    x, y = 52 + col * 436, 120 + row * 130
    inner = (
        f'<div class="serif" style="position:absolute;left:20px;top:20px;'
        f'font-weight:900;font-size:36px;color:{ACCENT}">{n}</div>'
        f'<div style="position:absolute;left:72px;top:24px;width:320px;font-size:18px;'
        f'font-weight:600;color:{INK};line-height:1.3">{title}</div>'
        f'<div style="position:absolute;left:72px;top:72px;width:320px;font-size:14px;'
        f'color:{MUTED}">{unit}</div>'
    )
    body += panel(x, y, 420, 114, inner)
body += t('Через месяц сравните с началом.', 52, 392, 856, size=16, bold=True)
add(slide(19, body))

# ── 20 Формула ──
body = t('(измеренное / возможное) × 100%', 52, 140, 856, size=36, serif=True,
         weight=900, align='center', color=INK)
body += bar(356, 220, 248, 3)
body += t('Последнее слово руководства — не «внедряйте», а «измеряйте».',
          52, 268, 856, size=22, serif=True, weight=700, align='center', color=ACCENT)
body += t('Семь дней замера отделяют убеждение от знания.', 52, 360, 856, size=16, align='center', color=MID)
add(slide(20, body))

# ── 21 Финал ──
body = (
    f'<div style="position:absolute;left:52px;top:72px;font-family:{SERIF};'
    f'font-weight:900;font-size:120px;line-height:0.8;color:{ACCENT}">«</div>'
    f'<div style="position:absolute;left:52px;top:140px;width:856px;font-family:{SERIF};'
    f'font-weight:800;font-size:42px;line-height:1.22;color:{CARD}">'
    f'Последнее слово руководства —<br>не «внедряйте», а «измеряйте».</div>'
    f'<div class="kicker" style="position:absolute;left:52px;top:300px;width:856px;color:{ACCENT}">'
    f'Из доклада «Не просто накормить»</div>'
    + t('Полный текст — в памятке и полном руководстве (PDF)', 52, 400, 800, size=16, color='#C4B8A8')
)
add(slide(21, body, bg=DARK, foot_color=MUTED))

# ── Р · РЕЗЕРВ: шесть вопросов дискуссии (разд. 17.12 доклада) ──
# Не входит в основной показ (стр. 1–21). Модератор открывает по запросу зала.
# Формулировки — по файлу 01_доклад/дополнения_18.08.2026/модератор_26.08_правовые_ответы.md
qs = [
    'Кто выбирает форму питания — проживающий социального дома или его руководитель?',
    'Как формировать меню при жёстких нормативно-правовых и финансовых ограничениях?',
    'Должно ли быть питание в социальных домах «лечебным»?',
    'Как совместить «лечебное питание» и «вариативное меню», не ограничивая право выбора?',
    'Как соблюсти баланс между выбором недееспособного «что ему есть» и его медицинскими рекомендациями?',
    'Как совместить качество продуктов и нормирование цен при планировании бюджета?',
]
body = kick('РЕЗЕРВ · НЕ ДЛЯ ОСНОВНОГО ПОКАЗА · РАЗДЕЛ 17.12') + h('Шесть вопросов дискуссии 26.08', 30, top=70)
for i, q in enumerate(qs):
    y = 126 + i * 64
    body += t(str(i + 1), 52, y, 40, size=24, serif=True, weight=900, color=ACCENT)
    body += t(q, 100, y + 2, 808, size=15, color=INK, lh=1.28)
add(slide('Р', body))


TITLES = [
    'Не просто накормить',
    'Разговор о трёх конфликтах',
    '2 190 приёмов',
    '74 % — недееспособность',
    '15 часов без еды',
    'На проверку — папка',
    'Это уже делают',
    'Модель «заказное питание»',
    'Слово Тимуру Нурбаеву',
    'Кто решает, что на тарелке?',
    'Организация, не бюджет',
    'Поддержка не требует речи',
    'Безопасность и выбор',
    'Измеряйте, не декларируйте',
    'Качество и норматив',
    'Три главные ошибки',
    '01.09.2026 — СанПиН 4282-26',
    'Три шага с понедельника',
    'Четыре показателя',
    '(измеренное / возможное) × 100%',
    'Измеряйте',
]


def write_index():
    items = '\n'.join(
        f'<li><a href="slide-{i:02d}.html">{i:02d}. {title}</a></li>'
        for i, title in enumerate(TITLES, 1)
    )
    items += ('\n<li style="margin-top:14px;list-style:none;color:#87867F">'
              '<a href="slide-22.html">Р. Шесть вопросов дискуссии 26.08 '
              '(резерв, не для основного показа)</a></li>')
    html = f'''<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8">
<title>v5 · Не просто накормить · 21 слайд</title>
{GGL}
<style>
{FACE}
body {{ font-family:{SANS}; background:{IVORY}; color:{INK}; max-width:720px;
       margin:48px auto; padding:0 24px; }}
h1 {{ font-family:{SERIF}; font-weight:800; font-size:32px; }}
a {{ color:{ACCENT}; }}
li {{ margin:8px 0; font-size:16px; }}
.note {{ color:{MUTED}; font-size:14px; margin-top:32px; line-height:1.45; }}
</style></head>
<body>
<h1>Не просто накормить</h1>
<p>21 слайд основного показа + резервный · 26.08.2026 · площадка № 2 · ДСО «Тесовый берег»</p>
<ol>{items}</ol>
<p class="note">Офлайн: шрифты лежат в <code>fonts/</code>. Откройте этот файл
в браузере с диска (<code>file://</code>) — Google Fonts не нужны.
Для показа в зале удобнее PDF.</p>
</body></html>'''
    open(f'{HERE}/index.html', 'w', encoding='utf-8').write(html)


# ── запись (слайды в корне папки: url('fonts/...')) ──
for old in glob.glob(f'{HERE}/slide-*.html'):
    os.remove(old)
for old in glob.glob(f'{HERE}/slides/slide-*.html'):
    os.remove(old)
for i, html_doc in enumerate(OUT, 1):
    open(f'{HERE}/slide-{i:02d}.html', 'w', encoding='utf-8').write(html_doc)
write_index()
print(len(OUT), 'slides written')

if '--pdf' in sys.argv:
    PDF_DIR = f'{HERE}/_pdf'
    os.makedirs(PDF_DIR, exist_ok=True)
    for old in glob.glob(f'{PDF_DIR}/p*.pdf'):
        os.remove(old)
    env = os.environ.copy()
    env.pop('PYTHONPATH', None)
    # PDF: strip Google Fonts so WeasyPrint stays on local files
    for i in range(1, len(OUT) + 1):
        src = f'{HERE}/slide-{i:02d}.html'
        tmp = f'{HERE}/_t{i:02d}.html'
        raw = open(src, encoding='utf-8').read()
        raw = re.sub(r'<link[^>]*fonts\.(googleapis|gstatic)\.com[^>]*>', '', raw)
        open(tmp, 'w', encoding='utf-8').write(raw)
        p_pdf = f'{PDF_DIR}/p{i:02d}.pdf'
        r = subprocess.run(['weasyprint', tmp, p_pdf], env=env, capture_output=True, text=True)
        os.remove(tmp)
        if r.returncode != 0:
            sys.stderr.write(r.stderr or r.stdout or 'weasyprint failed\n')
            raise SystemExit(f'weasyprint failed on slide {i}')
    dest_here = f'{HERE}/Презентация_v5_дискуссия_26_08_стиль_claude.pdf'
    dest_root = os.path.join(os.path.dirname(HERE), 'Презентация_дискуссия_26_08_v5_стиль_claude.pdf')
    pages = sorted(glob.glob(f'{PDF_DIR}/p*.pdf'))
    subprocess.run(['pdfunite', *pages, dest_here], check=True, env=env)
    subprocess.run(['cp', dest_here, dest_root], check=True)
    print(f'PDF: {len(pages)} slides -> {dest_here}')
    print(f'copy -> {dest_root}')
