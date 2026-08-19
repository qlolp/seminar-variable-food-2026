# -*- coding: utf-8 -*-
"""v3: финальная колода дискуссии «Организация питания: опыт реализации проектов»
(26.08.2026, 14:00–15:30). 36 слайдов 960×540 в стилистике программы семинара:
белый фон, глубокий синий #005A9C, Oswald (заголовки/цифры) + PT Sans (текст).
Сборка: HTML → PDF (headless Edge) → склейка (pypdf). Шрифты woff2 (Google Fonts, SIL OFL)."""
import os, subprocess, glob, sys

HERE = os.path.dirname(os.path.abspath(__file__))

C = dict(primary='#005A9C', navy='#123A5F', ink='#1A2733', muted='#5A6B7B',
         gold='#E8A13D', goldsoft='#FBEFD9', risk='#B33A3A', risksoft='#F8E7E7',
         soft='#EDF3F8', line='#D5DEE6', white='#FFFFFF', green='#2E7D5B',
         greensoft='#E7F2ED')

CSS = """
@font-face { font-family:'Oswald'; src:url('fonts/oswald-500.woff2') format('woff2'); font-weight:500; }
@font-face { font-family:'Oswald'; src:url('fonts/oswald-600.woff2') format('woff2'); font-weight:600; }
@font-face { font-family:'Oswald'; src:url('fonts/oswald-700.woff2') format('woff2'); font-weight:700; }
@font-face { font-family:'PT Sans'; src:url('fonts/ptsans-400.woff2') format('woff2'); }
@font-face { font-family:'PT Sans'; src:url('fonts/ptsans-700.woff2') format('woff2'); font-weight:bold; }
@page { size:960px 540px; margin:0 }
html,body { margin:0; padding:0 }
.slide { position:relative; width:960px; height:540px; background:#fff; overflow:hidden;
         font-family:'PT Sans'; color:%(ink)s; }
.foot { position:absolute; left:48px; right:48px; bottom:16px; display:flex;
        justify-content:space-between; font-size:10.5px; color:%(muted)s; }
.foot b { color:%(primary)s }
.kicker { font-family:'Oswald'; font-weight:600; font-size:12.5px; letter-spacing:3px;
          color:%(primary)s; text-transform:uppercase; }
.kickrow { position:absolute; left:48px; top:34px; right:48px; display:flex; align-items:center; gap:14px; }
.kickrow .rule { flex:1; height:2px; background:%(line)s; }
h1 { font-family:'Oswald'; font-weight:600; margin:0; line-height:1.12; }
.big { font-family:'Oswald'; font-weight:600; }
.qmark { font-family:'Oswald'; font-weight:700; }
.card { background:%(soft)s; border-radius:10px; }
.tag { display:inline-block; font-family:'Oswald'; font-weight:500; font-size:11px;
       letter-spacing:1.5px; padding:3px 10px 2px; border-radius:3px; }
""" % C

def slide(num, body, kicker=None, foot=None, bg=None):
    k = ''
    if kicker:
        k = f'<div class="kickrow"><span class="kicker">{kicker}</span><span class="rule"></span></div>'
    f_src, f_num = (foot or ''), str(num)
    foot_html = (f'<div class="foot"><span>{f_src}</span><span><b>{f_num}</b> / 36</span></div>')
    style = f' style="background:{bg}"' if bg else ''
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head>' \
           f'<body><div class="slide"{style}>{k}{body}{foot_html}</div></body></html>'

def h(text, size=30, color=None, top=64, left=48, width=864, lh=1.12):
    col = f'color:{color}' if color else ''
    return (f'<h1 style="position:absolute;left:{left}px;top:{top}px;width:{width}px;'
            f'font-size:{size}px;{col};line-height:{lh}">{text}</h1>')

def p(text, top, left=48, width=864, size=15, lh=1.5, color=None, align='left', bold=False):
    col = f'color:{color};' if color else ''
    b = 'font-weight:bold;' if bold else ''
    return (f'<p style="position:absolute;left:{left}px;top:{top}px;width:{width}px;'
            f'font-size:{size}px;line-height:{lh};{col}{b}text-align:{align};margin:0">{text}</p>')

def box(x, y, w, h, fill, radius=10, border=None):
    b = f'border:1.5px solid {border};' if border else ''
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;'
            f'background:{fill};border-radius:{radius}px;{b}"></div>')

def txt(text, x, y, w, size=13.5, lh=1.45, color=None, bold=False, align='left', oswald=False, ls=None):
    col = f'color:{color};' if color else ''
    fam = "font-family:'Oswald';" if oswald else ''
    fw = 'font-weight:600;' if (bold or oswald) else ''
    l = f'letter-spacing:{ls}px;' if ls else ''
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;font-size:{size}px;'
            f'line-height:{lh};{col}{fam}{fw}{l}text-align:{align}">{text}</div>')

def hbar(labels, values, x, y, w, row_h=44, gap=14, maxv=None, unit='', colors=None):
    maxv = maxv or max(values)
    out = []
    for i, (lab, val) in enumerate(zip(labels, values)):
        yy = y + i * (row_h + gap)
        fill = (colors[i] if colors else C['primary'])
        bw = int((w - 300) * val / maxv)
        out.append(f'<div style="position:absolute;left:{x}px;top:{yy}px;width:230px;height:{row_h}px;'
                   f'display:flex;align-items:center;justify-content:flex-end;text-align:right;'
                   f'font-size:12.5px;color:{C["ink"]};line-height:1.2">{lab}</div>')
        out.append(f'<div style="position:absolute;left:{x+240}px;top:{yy}px;width:{w-240-70}px;height:{row_h}px;'
                   f'background:{C["soft"]};border-radius:5px">'
                   f'<div style="width:{bw}px;height:100%;background:{fill};border-radius:5px 0 0 5px"></div></div>')
        out.append(f'<div style="position:absolute;left:{x+w-62}px;top:{yy}px;height:{row_h}px;display:flex;'
                   f'align-items:center;font-family:Oswald;font-weight:600;font-size:17px;color:{fill}">'
                   f'{val}{unit}</div>')
    return ''.join(out)

def question_slide(num, kicker, qtext, sub=None, hint=None, foot=None):
    body = box(48, 90, 864, 330, C['goldsoft'], radius=14, border=C['gold'])
    inner = (f'<div style="position:absolute;left:76px;top:120px;width:180px;height:180px;'
             f'border-radius:50%;background:{C["gold"]};display:flex;align-items:center;justify-content:center">'
             f'<span class="qmark" style="font-size:96px;color:#fff">?</span></div>')
    inner += txt(qtext, 300, 130, 570, size=25, lh=1.3, color=C['ink'], oswald=True)
    if sub:
        inner += txt(sub, 300, 320, 570, size=14.5, lh=1.5, color=C['muted'])
    if hint:
        inner += txt(hint, 48, 445, 864, size=12.5, color=C['muted'])
    return slide(num, inner, kicker=kicker, foot=foot or 'Вопрос залу')

S = []

# ═══ 01 Обложка ═══
body = f'''
<div style="position:absolute;left:0;top:0;width:100%;height:8px;background:{C['primary']}"></div>
<div style="position:absolute;left:48px;top:44px;display:flex;align-items:center;gap:12px">
  <svg width="26" height="26" viewBox="0 0 100 100"><path d="M50 0 L60 38 L85 15 L62 40 L100 50 L62 60 L85 85 L60 62 L50 100 L40 62 L15 85 L38 60 L0 50 L38 40 L15 15 L40 38 Z" fill="{C['gold']}"/></svg>
  <span class="kicker" style="color:{C['ink']}">ПРОСТРАНСТВО НОВЫХ ИДЕЙ 2.0 · ПРАВА И ОБЯЗАННОСТИ ПРОЖИВАЮЩИХ И РАБОТАЮЩИХ</span>
</div>
<div style="position:absolute;left:48px;top:96px;width:640px;height:8px;background:{C['primary']}"></div>
<div class="big" style="position:absolute;left:48px;top:130px;font-size:23px;color:{C['muted']};letter-spacing:1px">ДИСКУССИЯ · 26 АВГУСТА · 14.00–15.30</div>
<h1 style="position:absolute;left:48px;top:168px;width:760px;font-size:47px;color:{C['primary']};line-height:1.08">ОРГАНИЗАЦИЯ ПИТАНИЯ:<br>ОПЫТ РЕАЛИЗАЦИИ ПРОЕКТОВ</h1>
<div style="position:absolute;left:48px;top:296px;width:70px;height:5px;background:{C['gold']}"></div>
<div style="position:absolute;left:48px;top:318px;width:700px;font-size:16px;line-height:1.5;color:{C['ink']}">
Не просто накормить: безопасное, достойное и <b>вариативное</b> питание людей<br>с психическими нарушениями в домах социального обслуживания</div>
<div style="position:absolute;left:48px;top:412px;width:420px;font-size:13.5px;line-height:1.65;color:{C['ink']}">
<b>Евгений Чистяков</b> · директор ДСО «Серафимовский», Санкт-Петербург<br>
<b>Тимур Нурбаев</b> · директор ДСО «Тесовый берег», Санкт-Петербург</div>
<div style="position:absolute;right:48px;top:412px;text-align:right;font-size:11.5px;color:{C['muted']};line-height:1.6">
Санкт-Петербург · 25–27 августа 2026<br>Минтруд России · Комитет по социальной политике СПб</div>
'''
S.append(slide(1, body, foot='«Пространство новых идей 2.0» · семинар руководителей стационарных организаций'))

# ═══ 02 Формат ═══
body = h('Это не лекция. Это разговор на шести вопросах', 30)
items = [
    ('1', 'Кто выбирает форму питания — проживающий или руководитель учреждения?'),
    ('2', 'Как формировать меню в условиях нормативных и финансовых ограничений?'),
    ('3', 'Должно ли быть питание в социальных домах «лечебным»?'),
    ('4', 'Как совместить «лечебное питание» и «вариативное меню»?'),
    ('5', 'Баланс между правом выбора недееспособного и медицинскими показаниями'),
    ('6', 'Качество продуктов против нормирования цен: как совместить?'),
]
for i, (n, t) in enumerate(items):
    col, row = i % 2, i // 2
    x, y = 48 + col * 442, 150 + row * 96
    body += box(x, y, 422, 84, C['soft'])
    body += txt(n, x + 18, y + 14, 40, size=30, oswald=True, color=C['gold'])
    body += txt(t, x + 66, y + 12, 340, size=13, lh=1.35, color=C['ink'])
body += p('Программа семинара, сессия 26.08 · вопросы воспроизведены дословно', 452, size=12, color=C['muted'])
S.append(slide(2, body, kicker='Формат · 90 минут', foot='Формат сессии · вопросы — из программы семинара'))

# ═══ 03 Вопрос залу (открытие) ═══
S.append(question_slide(3, 'Разогрев · 1 минута',
    'Вспомните вчерашний ужин. Поднимите руку, если хоть один житель вашего дома мог выбрать второе блюдо.',
    sub='Рука, которая не поднимается, — это и есть повестка наших 90 минут.',
    hint='Честный ответ «никто не мог» — нормальный старт, а не провал.'))

# ═══ 04 Три числа ═══
body = h('Еда — самое массовое ежедневное событие дома', 30)
nums = [('1 095', 'приёмов пищи на жителя в год — больше, чем любых других услуг', C['primary']),
        ('74 %', 'жителей ПНИ недееспособны — и всё равно имеют предпочтения', C['gold']),
        ('15–20', 'лет разрыв смертности с общей популяцией; стол — часть этого разрыва', C['risk'])]
for i, (n, t, col) in enumerate(nums):
    x = 48 + i * 296
    body += box(x, 150, 276, 230, C['soft'])
    body += txt(n, x + 24, 176, 230, size=64, oswald=True, color=col)
    body += txt(t, x + 24, 264, 228, size=13.5, lh=1.5)
body += p('Вопросы выбора еды — это не «кухня». Это права, здоровье и безопасность — три раза в день, каждый день.', 415, size=14.5, bold=True)
S.append(slide(4, body, kicker='Почему это важно', foot='Данные: реестр источников доклада (125 позиций, проверены 07–19.08.2026)'))

# ═══ 05 Кто решает (схема) ═══
body = h('Кто сегодня решает, что окажется на тарелке?', 30)
chain = ['Регион:<br>нормы и<br>финансы', 'Раскладка:<br>меню-цикл', 'Кухня:<br>закладка', 'Смена:<br>раздача']
for i, node in enumerate(chain):
    x = 48 + i * 196
    body += box(x, 160, 150, 96, C['soft'])
    body += txt(node, x + 12, 180, 126, size=13, align='center', lh=1.4)
    if i < 3:
        body += f'<div style="position:absolute;left:{x+158}px;top:196px;width:30px;height:3px;background:{C["primary"]}"></div>'
body += box(48, 300, 864, 90, C['risksoft'])
body += txt('ЖИТЕЛЬ', 76, 322, 140, size=24, oswald=True, color=C['risk'])
body += txt('— единственный, кто ест — в этой цепочке не участвует. Его preference — не вход, а помеха: «не ест это», «опять перловка».', 220, 318, 670, size=14.5, lh=1.5)
body += p('Дискуссия 26.08 начинается ровно здесь: вопрос № 1 программы — «кто выбирает?»', 415, size=14.5, bold=True)
S.append(slide(5, body, kicker='Стартовая точка', foot='Типовая цепочка решения о рационе в стационарной организации'))

# ═══ 06 Право ═══
body = h('Право уже разрешает выбор. Запрета нет ни в одном акте', 30)
cards = [('442-ФЗ', '«учёт индивидуальной потребности» получателя — выбор блюда укладывается в неё напрямую'),
         ('Закон 3185-1, ст. 37 и 43', 'достоинство и гуманное отношение — права, распространённые на проживающих ДСО и ПНИ'),
         ('СанПиН (обе редакции)', 'не менее 3 приёмов пищи, диетическое по показаниям — число вариантов не ограничено')]
for i, (t, d) in enumerate(cards):
    x = 48 + i * 296
    body += box(x, 150, 276, 210, C['soft'])
    body += txt(t, x + 22, 172, 232, size=17, oswald=True, color=C['primary'])
    body += txt(d, x + 22, 224, 232, size=13, lh=1.5)
body += p('С 1 сентября 2026 действует новый СанПиН 2.3/2.4.4282-26 — модель выбора не меняется ни на йоту.', 400, size=14, bold=True)
body += p('подробнее — слайды 29–30', 440, size=12, color=C['muted'])
S.append(slide(6, body, kicker='Правовая рамка · коротко', foot='ФЗ-442 ст. 9, 16 · Закон РФ 3185-1 ст. 37, 43 · СанПиН 2.3/2.4.3590-20 → 2.3/2.4.4282-26'))

# ═══ 07 Ночной интервал (переделка старого «слайда 7») ═══
body = h('Сколько часов ваш дом не кормит жителей ночью?', 30)
body += hbar(['Швеция — ориентир', 'США — норма CMS', 'Типовой дом, РФ'],
             [11, 14, 15], 48, 160, 700, unit=' ч',
             colors=[C['green'], C['primary'], C['risk']])
body += p('Ужин в 17:30 → завтрак в 8:30. Пятнадцать часов без еды — не экзотика, а типовой распорядок.', 330, size=14.5)
body += p('Для жителей на антипсихотиках голодная ночь — это ещё и вес, и поведение, и ночные «набеги» на кухню.', 360, size=14.5)
body += box(48, 396, 864, 52, C['goldsoft'], border=C['gold'])
body += txt('Вопрос залу: какая цифра в вашем доме? Замер — три дня, одна строка в журнале, ноль рублей.', 68, 410, 830, size=13.5, bold=True)
S.append(slide(7, body, kicker='Одна цифра, которая меняет всё', foot='Швеция: Livsmedelsverket · США: 42 CFR 483.60 · РФ: оценка по типовым графикам'))

# ═══ 08 Опыт: карточки практик ═══
body = h('Это уже делают. Шесть публичных историй, 2024–2026', 30)
pts = [('Болотнинский ПНИ', 'Новосибирская обл.', '2024 · два вторых блюда на старте'),
       ('Успенский ПНИ', 'Новосибирская обл.', '2024 · выбор во всех отделениях'),
       ('Усть-Илимский ДСО', 'Иркутская обл.', '2024 · опрос предпочтений → выбор'),
       ('Иркутская область', 'масштаб региона', '2025 · решение для всех учреждений'),
       ('Серафимовский ДСО', 'Санкт-Петербург', '2025–2026 · зал заказного питания'),
       ('Тесовый берег ДСО', 'Санкт-Петербург', 'фарфор, линия раздачи — со-эксперт')]
for i, (name, reg, what) in enumerate(pts):
    col, row = i % 2, i // 2
    x, y = 48 + col * 442, 140 + row * 90
    body += box(x, y, 422, 80, C['soft'])
    body += f'<div style="position:absolute;left:{x+18}px;top:{y+22}px;width:12px;height:12px;border-radius:50%;background:{C["gold"]};border:3px solid {C["primary"]}"></div>'
    body += txt(f'<b>{name}</b> <span style="color:{C["muted"]};font-size:11.5px">· {reg}</span><br>{what}', x + 44, y + 15, 360, size=12.5, lh=1.4)
body += p('Все — публичные сообщения учреждений и учредителей. Ни один кейс не начинался с «сначала дайте деньги и разрешение».', 435, size=13.5, bold=True)
S.append(slide(8, body, kicker='Опыт · 2024–2026', foot='Источники: официальные сайты учреждений и учредителей, СМИ (2024–2026); полный реестр — в докладе'))

# ═══ 09 Кейс Серафимовского ═══
body = h('Я запустил это у себя. Вот цена и вот где сломалось', 28)
body += box(48, 140, 424, 240, C['soft'])
body += txt('ЧТО СДЕЛАЛИ', 70, 158, 300, size=15, oswald=True, color=C['primary'])
body += txt('Несколько месяцев часть жителей выбирала рацион на следующий день. Выбор приняли с энтузиазмом.<br><br>Итог: <b>приказ № 124 от 10.03.2026</b> — зал заказного питания, вариативное меню.', 70, 194, 380, size=13, lh=1.5)
body += box(490, 140, 424, 240, C['goldsoft'], border=C['gold'])
body += txt('ЧТО ЭТО СТОИЛО', 512, 158, 300, size=15, oswald=True, color=C['gold'])
body += txt('Дополнительное оборудование и ставки пищеблока.<br><br>Старт <b>не был бесплатным</b> — и я говорю это прямо.', 512, 194, 380, size=13.5, lh=1.55)
body += box(48, 396, 864, 50, C['risksoft'])
body += txt('ГДЕ СЛОМАЛОСЬ: полный переход труден — нормы сбалансированности, здоровье, тяга к популярному, но неполезному. Ответ — пары эквивалентов, а не запрет.', 68, 410, 830, size=13, bold=True)
S.append(slide(9, body, kicker='Кейс докладчика · ДСО «Серафимовский»', foot='Комитет по социальной политике СПб, 22.07.2025 · Приказ № 124 от 10.03.2026 — www.pni9.ru'))

# ═══ 10 Мост к коллеге ═══
body = h('Слово со-эксперту', 30)
body += box(48, 150, 864, 200, C['soft'])
body += txt('ТИМУР НУРБАЕВ', 80, 178, 400, size=26, oswald=True, color=C['primary'])
body += txt('директор ДСО «Тесовый берег»,<br>Санкт-Петербург', 80, 222, 400, size=14.5, lh=1.5)
body += txt('ЧТО УЖЕ ВИДНО В «ТЕСОВОМ БЕРЕГЕ»', 520, 170, 380, size=13, oswald=True, color=C['gold'])
for i, f in enumerate(['фарфор вместо железных мисок', 'вилки и ножи на столе', 'самообслуживание: поднос и линия раздачи', 'тренировочная кухня — доступ круглосуточно']):
    body += txt('—  ' + f, 520, 200 + i * 33, 380, size=13.5)
body += p('Мы договорились: два эксперта — один разговор. Мой блок — вариативность и право выбора; дальше — общая дискуссия по шести вопросам.', 400, size=14)
S.append(slide(10, body, kicker='Со-эксперт сессии', foot='Практика ДСО «Тесовый берег» — портал ОЮП СПб (upchspb.ru), 2026'))

# ═══ 11 Лестница 0-5 ═══
body = h('Лестница вариативности: пять ступеней вверх', 30)
steps = [('0', 'Мономеню с учётом отказов'), ('1', 'Выбор из двух в одной позиции'), ('2', 'Выбор по всем позициям ежедневно'),
         ('3', 'Шведская линия'), ('4', 'Семейная подача'), ('5', 'Своя кухня')]
for i, (n, t) in enumerate(steps):
    x = 48 + i * 145
    y = 330 - i * 38
    body += box(x, y, 130, 60 + i * 38, C['soft'] if i < 2 else C['primary'] if i < 4 else C['navy'], radius=6)
    col = C['ink'] if i < 2 else '#fff'
    body += txt(f'<span style="font-family:Oswald;font-weight:700;font-size:22px">{n}</span><br>{t}', x + 10, y + 10, 110, size=11, lh=1.3, color=col)
body += p('Ступень 1–2 подтверждены практикой 2024–2025 (Новосибирская и Иркутская области). Ступени 3–5 — горизонт, а не требование.', 445, size=13.5, bold=True)
S.append(slide(11, body, kicker='Как растет вариативность', foot='Доклад «Не просто накормить», раздел 8'))

# ═══ 12 Лестница участия ═══
body = h('Вторая ось: сколько контроля вернулось жителю', 29)
rows = [('0', 'Выбора нет — еда определена чужими решениями'),
        ('1', 'Спросили — но тарелка та же'),
        ('2', 'Его выбор дошёл до тарелки сегодня'),
        ('3', 'Выбрал ещё время и место еды'),
        ('4', 'Влияет на меню через совет жителей'),
        ('5', 'Еда снова часть жизни: кухня, гости, биография')]
for i, (n, t) in enumerate(rows):
    y = 138 + i * 47
    body += box(48, y, 60, 38, C['primary'] if i >= 2 else C['soft'], radius=6)
    body += txt(n, 48, y + 6, 60, size=20, oswald=True, align='center', color='#fff' if i >= 2 else C['ink'])
    body += txt(t, 124, y + 8, 780, size=14, bold=(i >= 2))
body += p('Две лестницы не совпадают по номерам: можно стоять на «шведской линии» и не спрашивать никого.', 438, size=13, color=C['muted'])
S.append(slide(12, body, kicker='Лестница участия жителя', foot='Доклад, раздел 8.6'))

# ═══ 13 В1: суть ═══
body = h('Вопрос 1. Кто выбирает: проживающий или руководитель?', 27)
body += box(48, 140, 280, 250, C['soft'])
body += txt('СУБЪЕКТ ВОЛИ', 70, 158, 200, size=14, oswald=True, color=C['primary'])
body += txt('Права принадлежат жителю (ст. 37, 43 закона 3185-1). Недееспособность отменяет сделки, не предпочтения.', 70, 190, 236, size=13, lh=1.5)
body += box(340, 140, 280, 250, C['soft'])
body += txt('ПРОЦЕДУРА', 362, 158, 200, size=14, oswald=True, color=C['primary'])
body += txt('Руководитель — организатор условий выбора: меню с парами, журнал, гарантия стандартного варианта.', 362, 190, 236, size=13, lh=1.5)
body += box(632, 140, 280, 250, C['soft'])
body += txt('ДЕНЬГИ', 654, 158, 200, size=14, oswald=True, color=C['primary'])
body += txt('Финансирование ограничивает набор позиций — но не право выбрать внутри предложенного.', 654, 190, 236, size=13, lh=1.5)
body += p('«Хозяина» в этой схеме нет. Есть должность, которая обязана спросить.', 415, size=15, bold=True, color=C['primary'])
S.append(slide(13, body, kicker='Вопрос 1 · три слоя ответа', foot='442-ФЗ · 3185-1 ст. 37, 43 · ГК ст. 29, 30 · доклад, разделы 15–16'))

# ═══ 14 В1: голосование ═══
S.append(question_slide(14, 'Вопрос 1 · голосование',
    'Кто в вашем доме сегодня отвечает на вопрос «что сегодня на обед»?',
    sub='Поднимите руку: кухня? диетсестра? директор? совет жителей? сам житель?',
    hint='В большинстве домов ответ — «раскладка три года назад». Это и есть первый кандидат на изменение.'))

# ═══ 15 В2: суть ═══
body = h('Вопрос 2. Меню в условиях ограничений', 30)
body += p('Нормы и деньги ограничивают набор продуктов. Но внутри набора почти всегда есть законное пространство выбора.', 130, size=15)
body += box(48, 180, 424, 200, C['soft'])
body += txt('ПАРЫ ЭКВИВАЛЕНТОВ', 70, 198, 300, size=15, oswald=True, color=C['primary'])
body += txt('Гречка ↔ рис ↔ пшено. Курица ↔ индейка. Треска ↔ хек.<br><br>Таблицы замены в раскладках — <b>существующий законный механизм</b>: равноценная замена внутри группы.', 70, 232, 380, size=13.5, lh=1.5)
body += box(490, 180, 424, 200, C['soft'])
body += txt('ЧТО ЭТО СТОИТ', 512, 198, 300, size=15, oswald=True, color=C['primary'])
body += txt('Сырьё пары сопоставимо: разница — копейки на порцию.<br><br>Реальная цена — труд и порядок: журнал заказа, вторая гастроёмкость, обучение смены.', 512, 232, 380, size=13.5, lh=1.5)
body += p('Норма — рамка содержимого тарелки, а не число тарелок.', 415, size=15, bold=True, color=C['primary'])
S.append(slide(15, body, kicker='Вопрос 2 · суть', foot='Приказ Минтруда 520н (рекомендательные нормы) · таблицы замены · доклад, раздел 19'))

# ═══ 16 В2: график стоимости ═══
body = h('Что действительно стоит второй вариант', 30)
body += hbar(['Сырьё: пара «гречка/рис»', 'Сырьё: пара «курица/индейка»', 'Труд смены (мин/день)', 'Отходы несъеденного (замер)'],
             [1, 4, 3, 30], 48, 150, 700, unit='', maxv=30,
             colors=[C['green'], C['green'], C['primary'], C['risk']])
body += p('Иллюстративные доли; сырьё пары — копейки. Настоящая статья потерь — то, что лежит в тарелках несъеденным.', 330, size=14.5)
body += box(48, 380, 864, 66, C['goldsoft'], border=C['gold'])
body += txt('Калькулятор стоимости (приложение 42) считает вашу пару за вечер — входные данные: цена кг и масса порции.', 68, 394, 830, size=13.5, bold=True)
body += txt('Никаких «общих цифр» — только ваш замер.', 68, 418, 830, size=12.5, color=C['muted'])
S.append(slide(16, body, kicker='Вопрос 2 · экономика', foot='Иллюстративный расчёт; методика — доклад, раздел 29 и приложение 42'))

# ═══ 17 В2: вопрос залу ═══
S.append(question_slide(17, 'Вопрос 2 · к залу',
    'Что дороже: второй вариант на линии — или тарелки, которые уносят несъеденными?',
    sub='Замер отходов за 7 дней отвечает на этот вопрос в рублях. У кого есть такой замер?',
    hint='Формула доклада: «замер до и после» — единственная честная экономика вариативности.'))

# ═══ 18 В3: суть ═══
body = h('Вопрос 3. Должно ли питание быть «лечебным»?', 29)
body += box(48, 140, 424, 220, C['soft'])
body += txt('ЧТО ГОВОРЯТ НОРМЫ', 70, 158, 340, size=14, oswald=True, color=C['primary'])
body += txt('Приказы о лечебном питании (330н, 395н) адресованы <b>медицинским</b> организациям.<br><br>Для ДСО СанПиН требует: 3 приёма + <b>диетическое по медицинским показаниям</b>.', 70, 192, 380, size=13, lh=1.5)
body += box(490, 140, 424, 220, C['soft'])
body += txt('ЧЕМ ЭТО ГРОЗИТ', 512, 158, 340, size=14, oswald=True, color=C['risk'])
body += txt('«Лечебность» руками кухни без врача — это диагноз повара. Диагнозы (и отмену диет) ставит врач.<br><br>Самовольная «диетизация» всего дома — риск и для здоровья, и для проверки.', 512, 192, 380, size=13, lh=1.5)
body += p('Позиция доклада: обычное питание + диетическое по показаниям. «Лечебное всем» — не стандарт, а его имитация.', 400, size=14, bold=True)
S.append(slide(18, body, kicker='Вопрос 3 · суть', foot='Приказы Минздрава 330н, 395н · СанПиН п. 56 · доклад, раздел 17.5'))

# ═══ 19 В3: голосование А/Б ═══
body = h('Голосование: должно ли питание быть «лечебным»?', 27)
body += box(48, 130, 424, 260, C['greensoft'], border=C['green'])
body += txt('А', 80, 150, 60, size=44, oswald=True, color=C['green'])
body += txt('Нет. Обычное питание, диетическое — поимённо по показаниям, назначает врач.', 80, 210, 360, size=15, lh=1.5)
body += box(490, 130, 424, 260, C['risksoft'], border=C['risk'])
body += txt('Б', 522, 150, 60, size=44, oswald=True, color=C['risk'])
body += txt('Да. Стол дома должен быть лечебным по умолчанию — так безопаснее.', 522, 210, 360, size=15, lh=1.5)
body += p('Руки за А. Руки за Б. Возражения — микрофон: самое интересное начнётся здесь.', 420, size=14.5, bold=True)
S.append(slide(19, body, kicker='Вопрос 3 · голосование', foot='Дискуссия: аргументы обеих позиций — доклад, раздел 17.12, вопрос 3'))

# ═══ 20 В4: мост ═══
body = h('Вопрос 4. «Лечебное» × «вариативное» — не враги', 29)
svg = f'''<svg style="position:absolute;left:150px;top:140px" width="660" height="230" viewBox="0 0 660 230">
<circle cx="240" cy="115" r="105" fill="{C['soft']}" opacity="0.95"/>
<circle cx="420" cy="115" r="105" fill="{C['goldsoft']}" opacity="0.95"/>
<text x="185" y="110" font-family="PT Sans" font-size="15" font-weight="bold" fill="{C['primary']}">ЛЕЧЕБНАЯ РАМКА</text>
<text x="160" y="135" font-family="PT Sans" font-size="12.5" fill="{C['ink']}">назначил врач:</text>
<text x="160" y="153" font-family="PT Sans" font-size="12.5" fill="{C['ink']}">стол, текстура, соль</text>
<text x="395" y="110" font-family="PT Sans" font-size="15" font-weight="bold" fill="{C['gold']}">ВАРИАТИВНОСТЬ</text>
<text x="365" y="135" font-family="PT Sans" font-size="12.5" fill="{C['ink']}">выбор внутри рамки:</text>
<text x="365" y="153" font-family="PT Sans" font-size="12.5" fill="{C['ink']}">пары, вкус, привычное</text>
<text x="268" y="105" font-family="Oswald" font-size="14" font-weight="600" fill="{C['ink']}">ЗОНА</text>
<text x="245" y="127" font-family="Oswald" font-size="14" font-weight="600" fill="{C['ink']}">ПРАКТИКИ</text>
</svg>'''
body += svg
body += p('Пример-образец: дом в Московской области работает по распоряжению 19РВ-32 — медицинская рамка питания + совет по питанию + замены по желанию жителей. Рецепт: врач задаёт стол — внутри него всегда есть пары.', 390, size=14, lh=1.5)
S.append(slide(20, body, kicker='Вопрос 4 · конструкция', foot='Распоряжение Минсоцразвития МО 19РВ-32 · доклад, разделы 17.5, 19'))

# ═══ 21 В4: алгоритм ═══
body = h('Четыре шага, чтобы совместить', 30)
steps = [('1', 'Врач назначает рамку', 'стол/текстура/ограничения — поимённо, с пересмотром'),
         ('2', 'Внутри рамки — пары', 'диетический стол тоже имеет эквиваленты: рис ↔ гречка в пределах стола'),
         ('3', 'Журнал замен', 'выбор и замена фиксируются — это защита и жителя, и врача'),
         ('4', 'Пересмотр', 'статистика выбора → корректировка меню-цикла раз в квартал')]
for i, (n, t, d) in enumerate(steps):
    x = 48 + i * 222
    body += box(x, 150, 202, 220, C['soft'])
    body += txt(n, x + 20, 170, 40, size=34, oswald=True, color=C['gold'])
    body += txt(f'<b>{t}</b><br><br>{d}', x + 20, 220, 165, size=12.5, lh=1.5)
body += p('Диета — ограничение множества, а не его сжатие до одного блюда.', 415, size=15, bold=True, color=C['primary'])
S.append(slide(21, body, kicker='Вопрос 4 · алгоритм', foot='Доклад, разделы 19, 21 — пары эквивалентов и пересчёт цикла'))

# ═══ 22 В5: суть ═══
body = h('Вопрос 5. Недееспособный выбирает. Как?', 30)
body += p('74 % жителей ПНИ недееспособны. Это не отменяет предпочтений — отменяет предположение «за него решат».', 130, size=15)
body += box(48, 175, 424, 195, C['soft'])
body += txt('ЧЕТЫРЕ КАНАЛА ВОЛИ', 70, 193, 300, size=14, oswald=True, color=C['primary'])
body += txt('Показ двух порций · наблюдение за съеденным · пищевая биография · те, кто знает человека.<br><br>Замещающее решение («мы знаем лучше») — запрещено подходом КПИ.', 70, 226, 380, size=13, lh=1.5)
body += box(490, 175, 424, 195, C['soft'])
body += txt('ГРАНИЦА — МЕДИЦИНА', 512, 193, 300, size=14, oswald=True, color=C['risk'])
body += txt('Когда выбор небезопасен (дисфагия, текстуры, запреты врача) — выбор сужается до безопасного, но не исчезает:<br><br>«два безопасных» вместо «одно назначенное».', 512, 226, 380, size=13, lh=1.5)
body += p('Баланс — не «выбор или здоровье», а «выбор внутри того, что безопасно».', 412, size=14.5, bold=True)
S.append(slide(22, body, kicker='Вопрос 5 · суть', foot='КПИ, Замечание № 1 к ст. 12 · доклад, разделы 15–16, 10'))

# ═══ 23 В5: график IDDSI ═══
body = h('Текстуры: обучение работает лучше оборудования', 29)
body += hbar(['Соответствие текстур — до', 'После внедрения IDDSI', 'Загущённые напитки — до', 'После'],
             [44, 90, 31, 100], 48, 150, 700, unit=' %',
             colors=[C['risk'], C['green'], C['risk'], C['green']])
body += p('Пять учреждений, единая шкала текстур IDDSI. Главный барьер — не техника, а осведомлённость смены.', 330, size=14.5)
body += box(48, 375, 864, 70, C['soft'])
body += txt('Практика для зала: шесть признаков дисфагии на посту + скрининг-шкала (GUSS) силами медсестры. Дисфагия — главный съедобный риск психиатрии, и она измерима.', 68, 390, 830, size=13.5, lh=1.5, bold=True)
S.append(slide(23, body, kicker='Вопрос 5 · безопасность', foot='Исследование внедрения IDDSI (5 учреждений) · GUSS, Trapl 2007 · доклад, разделы 10.9–10.10'))

# ═══ 24 В5: вопрос залу ═══
S.append(question_slide(24, 'Вопрос 5 · к залу',
    'Вспомните жителя, который не говорит. Как он вчера дал понять, что не хочет это блюдо?',
    sub='Отвернулся? ест только хлеб? доел компот и оставил котлету? — это и была его «заявка».',
    hint='Кто может назвать один такой сигнал из своего дома? Микрофон.'))

# ═══ 25 В6: суть ═══
body = h('Вопрос 6. Качество против нормирования цен', 29)
body += p('Полная стоимость обеда в 3–6 раз выше сырьевой строки. Нормируя цену порции, мы нормируем самое дешёвое — и не управляем главным.', 130, size=15, lh=1.5)
body += hbar(['Сырьё (то, что нормируем)', 'Труд кухни и раздачи', 'Энергия, логистика, оборудование'],
             [1, 3, 5], 48, 195, 700, unit='×', maxv=5,
             colors=[C['gold'], C['primary'], C['navy']])
body += p('Иллюстративные доли (канадский аудит стационаров: полная стоимость 3–6× сырьевой).', 330, size=12.5, color=C['muted'])
body += p('Вывод: экономить надо на потерях (отходы, срывы поставок, картельные наценки), а не на белке в тарелке.', 370, size=15, bold=True, color=C['primary'])
S.append(slide(25, body, kicker='Вопрос 6 · экономика качества', foot='Аудит стоимости стационарного питания (Канада) · доклад, разделы 29, 42'))

# ═══ 26 В6: закупки ═══
body = h('Где действительно теряются деньги', 30)
body += box(48, 140, 424, 230, C['risksoft'])
body += txt('543 ТОРГА · 4,7 МЛРД ₽', 70, 160, 380, size=22, oswald=True, color=C['risk'])
body += txt('Картель на поставках социально значимых продуктов (ФАС, 2024): Москва, Подмосковье, Владимирская область, Дагестан.', 70, 205, 380, size=13, lh=1.5)
body += txt('Сигналы для директора: два-три «своих» поставщика, минус доли процента от начальной цены, «проигравший» побеждает в соседнем лоте.', 70, 285, 380, size=12.5, lh=1.5, color=C['muted'])
body += box(490, 140, 424, 230, C['soft'])
body += txt('АУТСОРСИНГ: 8 СТРОК', 512, 160, 380, size=22, oswald=True, color=C['primary'])
body += txt('Если кормит подрядчик — вариативность живёт в контракте: группы позиций, пропорции, гарантия двух вариантов, замены, текстуры, пробы, раскладка, отчётность.', 512, 205, 380, size=13, lh=1.5)
body += p('И пробы, и бракераж, и ответственность — остаются у учреждения. Даже когда плита — у подрядчика.', 400, size=13.5, bold=True)
S.append(slide(26, body, kicker='Вопрос 6 · закупки и подряд', foot='ФАС России, 2024 · СанПиН п. 56 (подп. 4, 12, 14) · доклад, раздел 42'))

# ═══ 27 В6: вопрос залу ═══
S.append(question_slide(27, 'Вопрос 6 · к залу',
    'Сколько стоит один обед в вашем доме — в рублях? Кто знает точную цифру?',
    sub='Не «на тысячу проживающих в год». Один обед. Один житель. Сегодня.',
    hint='Знание цены — начало управления ею. Цифра есть у каждого на калькуляторе приложения 42.'))

# ═══ 28 Ошибки ═══
body = h('Три ошибки, которые дороже бездействия', 30)
errs = [('Имитация выбора', '«Выбирайте!» — при одном блюде на линии. Хуже, чем честное мономеню: обманывает журнал и проверяющего.'),
        ('Выбор без гарантии', 'Житель выбрал Б — Б закончилось. Нет стандартного варианта — нет системы, есть лотерея.'),
        ('«Лечебность» без врача', 'Кухня назначает столы сама. Диагноз от повара — риск здоровью и готовое дело по ст. 6.6 КоАП.')]
for i, (t, d) in enumerate(errs):
    x = 48 + i * 296
    body += box(x, 150, 276, 230, C['risksoft'])
    body += txt(str(i + 1), x + 22, 168, 40, size=30, oswald=True, color=C['risk'])
    body += txt(f'<b>{t}</b><br><br>{d}', x + 22, 220, 232, size=12.5, lh=1.5)
S.append(slide(28, body, kicker='Красные линии', foot='Доклад, разделы 21, 12, 17 · практика проверок 2021–2025'))

# ═══ 29 Сентябрь ═══
body = h('1 сентября 2026: новый СанПиН — без паники', 30)
body += box(48, 140, 424, 240, C['soft'])
body += txt('ЧТО МЕНЯЕТСЯ', 70, 158, 340, size=15, oswald=True, color=C['primary'])
body += txt('СанПиН 2.3/2.4.3590-20 → 2.3/2.4.4282-26.<br><br>Перепривязать: положение о питании, формы журналов (приложения 4–5), ППК и ХАССП.<br><br>Переходного периода нет.', 70, 192, 380, size=13, lh=1.5)
body += box(490, 140, 424, 240, C['greensoft'])
body += txt('ЧТО НЕ МЕНЯЕТСЯ', 512, 158, 340, size=15, oswald=True, color=C['green'])
body += txt('Питание — не менее 3 раз в день, диетическое по показаниям.<br><br>Число вариантов блюда не ограничено.<br><br>Вариативность не конфликтует ни с одной редакцией правил.', 512, 192, 380, size=13, lh=1.5)
body += p('Журналы до 31.08 законны как заполнены — задним числом не переписывать.', 410, size=14, bold=True)
S.append(slide(29, body, kicker='СанПиН 2.3/2.4.4282-26', foot='Постановление от 02.06.2026 № 18 · чек-лист перехода — приложение 39 доклада'))

# ═══ 30 С понедельника ═══
body = h('Три шага с понедельника. Без денег и без разрешений', 28)
steps = [('Замер', '7 дней: ночной интервал, отходы, кто выбирал. Одна страница, ноль рублей.'),
         ('Один вариант выбора', 'Одна позиция, одно отделение, два блюда. Журнал заказа — тетрадь.'),
         ('Правило трёх отказов', 'Три отказа подряд — врач сегодня. Поперхнулся — врач немедленно.')]
for i, (t, d) in enumerate(steps):
    x = 48 + i * 296
    body += box(x, 150, 276, 210, C['soft'])
    body += txt(t, x + 22, 172, 232, size=19, oswald=True, color=C['primary'])
    body += txt(d, x + 22, 218, 232, size=13, lh=1.5)
body += p('Через 90 дней у вас будет то, чего нет почти ни у кого: числа. С ними идут и к учредителю, и к проверяющему.', 400, size=14.5, bold=True)
S.append(slide(30, body, kicker='Что сделать в понедельник', foot='Доклад, раздел 35 «Пилот 90 дней» · чек-лист — приложение 5 семинарского пакета'))

# ═══ 31 Смежные площадки ═══
body = h('Смежные площадки семинара: наши пересечения', 28)
cross = [('«Право на выбор: есть или нет?»', 'наш вопрос 1 и 2: выбор реализуется людьми, а не приказом'),
         ('«Право быть недееспособным»', 'наш вопрос 5: интересы выявляются, а не назначаются'),
         ('«Нужны ли врачи в доме?»', 'наш вопрос 3: «лечебность» без врача — не забота, а риск'),
         ('«Со-настройка с опекой»', 'наш вопрос 1: опекун — не цензор меню, а участник выявления воли'),
         ('«Чьи голоса громче?»', 'совет жителей обсуждает еду первой: жалобы на стол — самые частые'),
         ('«Право на достойный уход»', 'комфортное кормление в конце жизни — тоже право выбора')]
for i, (t, d) in enumerate(cross):
    col, row = i % 2, i // 2
    x, y = 48 + col * 442, 145 + row * 88
    body += box(x, y, 422, 78, C['soft'])
    body += txt(f'<b>{t}</b><br><span style="color:{C["muted"]}">{d}</span>', x + 18, y + 13, 390, size=12, lh=1.4)
S.append(slide(31, body, kicker='Программа 25–27.08 · связи', foot='Формулировки площадок — по программе семинара; связи — раздел 17.12 доклада'))

# ═══ 32 Материалы ═══
body = h('Что вы уносите с собой', 30)
items = [('Доклад «Не просто накормить»', '315 страниц: право, клиника, экономика, 45 приложений-шаблонов'),
         ('Калькулятор стоимости', 'Excel: ваша пара блюд и ваши отходы — за один вечер'),
         ('Чек-листы и журналы', 'экспресс-аудит, журнал замен, пищевой паспорт, План Б'),
         ('Реестр источников', '125 проверенных позиций с датами проверки — каждое число проверяемо')]
for i, (t, d) in enumerate(items):
    x = 48 + i * 222
    body += box(x, 150, 202, 220, C['soft'])
    body += txt(f'<b>{t}</b><br><br>{d}', x + 18, 172, 168, size=12.5, lh=1.5)
body += p('Всё открыто: репозиторий материалов — по QR после сессии.', 410, size=14.5, bold=True)
S.append(slide(32, body, kicker='Материалы', foot='github.com/qlolp/seminar-variable-food-2026'))

# ═══ 33 Открытый микрофон ═══
S.append(question_slide(33, 'Открытый микрофон · 20 минут',
    'Что в ваших домах ломается первым — когда речь заходит о выборе блюд?',
    sub='Деньги? руки? страх проверки? «у нас особые жители»? начать не с чего?',
    hint='Каждое «ломается» из зала — это готовый пункт повестки для ваших учредителей.'))

# ═══ 34 Финальная мысль ═══
body = f'''
<div style="position:absolute;left:0;top:0;width:100%;height:100%;background:{C['primary']}"></div>
<div style="position:absolute;left:48px;top:70px;width:120px;height:6px;background:{C['gold']}"></div>
<div style="position:absolute;left:48px;top:110px;width:820px;font-family:Oswald;font-weight:600;font-size:38px;line-height:1.25;color:#fff">
Тарелка — самое частое решение,<br>которое дом принимает за жителя.<br><span style="color:{C['gold']}">Вернуть его жителю — самое простое<br>из всех прав, что у нас есть.</span></div>
<div style="position:absolute;left:48px;bottom:52px;font-size:13px;color:#cfe0ef">Дискуссия «Организация питания: опыт реализации проектов» · 26.08.2026 · Чистяков · Нурбаев</div>
'''
S.append(slide(34, body, foot=''))

# ═══ 35 Спасибо ═══
body = h('Спасибо. Продолжаем разговор', 34)
body += p('Евгений Чистяков · ДСО «Серафимовский», Санкт-Петербург<br>Тимур Нурбаев · ДСО «Тесовый берег», Санкт-Петербург', 150, size=15, lh=1.7)
body += box(48, 240, 864, 120, C['soft'])
body += txt('Материалы сессии — доклад, калькулятор, чек-листы, реестр источников:<br><b>github.com/qlolp/seminar-variable-food-2026</b>', 76, 272, 810, size=15, lh=1.7)
body += p('Вопросы после сессии — лично и по каналам связи в раздатке.', 400, size=13, color=C['muted'])
S.append(slide(35, body, kicker='Контакты', foot='«Пространство новых идей 2.0» · 25–27.08.2026 · Санкт-Петербург'))

# ═══ 36 Резерв: реквизиты ═══
body = h('Резервный слайд: реквизиты для точных вопросов', 26)
refs = [('442-ФЗ', 'ст. 9 (права), ст. 16 (ИППСУ)'),
        ('Закон 3185-1', 'ст. 37, 43 — права проживающих'),
        ('СанПиН', '3590-20 → 4282-26 (с 01.09.2026), п. 56'),
        ('Приказ 520н', '13.09.2022, нормы питания — рекомендательные'),
        ('Приказы 330н, 395н', 'лечебное питание — для медорганизаций'),
        ('Ст. 6.6 КоАП', 'санитарные требования к питанию')]
for i, (t, d) in enumerate(refs):
    col, row = i % 2, i // 2
    x, y = 48 + col * 442, 140 + row * 78
    body += box(x, y, 422, 68, C['soft'])
    body += txt(f'<b>{t}</b> — {d}', x + 18, y + 20, 390, size=13.5)
body += p('Полные реквизиты и ссылки — реестр источников доклада (125 позиций).', 400, size=13, color=C['muted'])
S.append(slide(36, body, kicker='Резерв', foot='Для точных вопросов из зала'))

# ---------- запись и сборка ----------
os.makedirs(os.path.join(HERE, 'slides'), exist_ok=True)
for i, html in enumerate(S, 1):
    open(os.path.join(HERE, 'slides', f'slide-{i:02d}.html'), 'w', encoding='utf-8').write(html)
print(f'{len(S)} slides written')

if '--pdf' in sys.argv:
    import shutil
    tmp = os.path.join(HERE, '_pdf'); os.makedirs(tmp, exist_ok=True)
    edge = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
    n = 0
    for f in sorted(glob.glob(os.path.join(HERE, 'slides', 'slide-*.html'))):
        n += 1
        out = os.path.join(tmp, f'p{n:02d}.pdf')
        if os.path.exists(out):
            continue
        subprocess.run([edge, '--headless', '--disable-gpu', '--no-pdf-header-footer',
                        f'--print-to-pdf={out}', 'file:///' + f.replace('\\', '/')],
                       capture_output=True)
    from pypdf import PdfWriter, PdfReader
    w = PdfWriter()
    for f in sorted(glob.glob(os.path.join(tmp, 'p*.pdf'))):
        for pg in PdfReader(f).pages:
            w.add_page(pg)
    out_pdf = os.path.join(HERE, 'Презентация_v3_дискуссия_26_08.pdf')
    with open(out_pdf, 'wb') as fh:
        w.write(fh)
    print('PDF:', len(w.pages), 'slides ->', out_pdf)
