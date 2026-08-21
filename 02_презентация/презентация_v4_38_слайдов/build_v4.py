# -*- coding: utf-8 -*-
"""v4: колода дискуссии «Организация питания: опыт реализации проектов» (26.08.2026).
Стиль «2 190»: одна мысль, крупная цифра или 3–6 слов, Playfair, без пиктограмм.
20 слайдов основного показа + разделитель + резерв.
Сборка: PATH=/opt/homebrew/bin:$PATH python3 build_v4.py --pdf
(HTML всегда; PDF — WeasyPrint CLI + pdfunite. PYTHONPATH не задавать.)"""
import glob, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))

C = dict(ivory='#FAF9F5', panel='#F0EEE6', panelwarm='#F6F1E9', ink='#141413',
         body='#3D3929', muted='#87867F', soft='#6E6A5E', accent='#C15F3C',
         accentdeep='#B8552F', accentsoft='#F5E7DE', line='#E3DCCE',
         gray='#B7AFA0', dark='#141413', white='#FFFFFF')
TAG = dict(law='#2B5A8A', money='#C45C26', kitchen='#2F6B4F', clinic='#1F6F78')
TAG_LABEL = dict(law='ПРАВО', money='ДЕНЬГИ', kitchen='КУХНЯ', clinic='КЛИНИКА')

CSS = """
@font-face { font-family:'Playfair Lat'; src:url('../fonts/playfair-700-lat.woff2') format('woff2'); font-weight:700; }
@font-face { font-family:'Playfair Cyr'; src:url('../fonts/playfair-700-cyr.woff2') format('woff2'); font-weight:700; }
@font-face { font-family:'Playfair Lat'; src:url('../fonts/playfair-800-lat.woff2') format('woff2'); font-weight:800; }
@font-face { font-family:'Playfair Cyr'; src:url('../fonts/playfair-800-cyr.woff2') format('woff2'); font-weight:800; }
@font-face { font-family:'Playfair Lat'; src:url('../fonts/playfair-900-lat.woff2') format('woff2'); font-weight:900; }
@font-face { font-family:'Playfair Cyr'; src:url('../fonts/playfair-900-cyr.woff2') format('woff2'); font-weight:900; }
@font-face { font-family:'Playfair Lat'; src:url('../fonts/playfair-600i-lat.woff2') format('woff2'); font-style:italic; font-weight:600; }
@font-face { font-family:'Playfair Cyr'; src:url('../fonts/playfair-600i-cyr.woff2') format('woff2'); font-style:italic; font-weight:600; }
@font-face { font-family:'PT Sans'; src:url('../fonts/ptsans-400.woff2') format('woff2'); }
@font-face { font-family:'PT Sans'; src:url('../fonts/ptsans-700.woff2') format('woff2'); font-weight:bold; }
@page { size:960px 540px; margin:0 }
html,body { margin:0; padding:0 }
.slide { position:relative; width:960px; height:540px; background:%(ivory)s; overflow:hidden;
         font-family:'PT Sans'; color:%(body)s; }
.foot { position:absolute; right:48px; bottom:18px; font-size:15px; color:%(muted)s; }
.foot b { color:%(accent)s; font-weight:bold }
.kicker { font-weight:bold; font-size:12px; letter-spacing:3px; color:%(accent)s;
          text-transform:uppercase; }
.kickrow { position:absolute; left:52px; top:34px; right:52px; display:flex; align-items:center; gap:14px; }
.kickrow .rule { flex:1; height:1.5px; background:%(line)s; }
h1 { font-family:'Playfair Lat', 'Playfair Cyr', 'PT Sans', serif; font-weight:800; margin:0; line-height:1.12; color:%(ink)s; }
.serif { font-family:'Playfair Lat', 'Playfair Cyr', 'PT Sans', serif; }
""" % C


def slide(num, body, kicker=None, bg=None):
    k = ''
    if kicker:
        k = (f'<div class="kickrow"><span class="kicker">{kicker}</span>'
             f'<span class="rule"></span></div>')
    foot = f'<div class="foot"><span><b>{num}</b></span></div>'
    style = f' style="background:{bg}"' if bg else ''
    return (f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body><div class="slide"{style}>{k}{body}{foot}</div></body></html>')


def num(text, top=118, size=185, left=52, color=None):
    col = color or C['ink']
    return (f'<div class="serif" style="position:absolute;left:{left}px;top:{top}px;'
            f'font-weight:900;font-size:{size}px;line-height:0.95;color:{col}">{text}</div>')


def bar(top=348, left=52, w=60):
    return (f'<div style="position:absolute;left:{left}px;top:{top}px;width:{w}px;'
            f'height:5px;background:{C["accent"]}"></div>')


def h(text, size=40, color=None, top=108, left=52, width=856, italic=False):
    col = f'color:{color};' if color else ''
    it = 'font-style:italic;font-weight:600;' if italic else ''
    return (f'<h1 style="position:absolute;left:{left}px;top:{top}px;width:{width}px;'
            f'font-size:{size}px;{col}{it}line-height:1.12">{text}</h1>')


def txt(text, x, y, w, size=22, lh=1.35, color=None, bold=False, align='left',
        serif=False, italic=False):
    col = f'color:{color};' if color else ''
    fam = ("font-family:'Playfair Lat','Playfair Cyr','PT Sans',serif;font-weight:700;"
           if serif else '')
    fw = 'font-weight:bold;' if (bold and not serif) else ''
    it = 'font-style:italic;' if italic else ''
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;font-size:{size}px;'
            f'line-height:{lh};{col}{fam}{fw}{it}text-align:{align}">{text}</div>')


def cap(text, top=372, size=22, color=None, width=856):
    return txt(text, 52, top, width, size=size, lh=1.4, color=color or C['ink'])


def region_body(place, fact, year):
    """Одна история: крупное имя + одна строка факта. Без сетки, без иконок."""
    return (
        num(place, top=120, size=52) +
        bar(198, 52, 72) +
        txt(fact, 52, 230, 856, size=40, serif=True, color=C['accentdeep']) +
        txt(year, 52, 400, 856, size=22, color=C['soft'])
    )


MAIN, RESERVE = [], []  # RESERVE: (html, kind|None)


def add_main(html):
    MAIN.append(html)


def add_res(html, kind=None):
    RESERVE.append((html, kind))


# ═══ ОСНОВНОЙ ПОКАЗ · 20 ═══

# 01 Титул
body = f'''
<div style="position:absolute;left:0;bottom:0;width:100%;height:14px;background:{C['panel']}"></div>
<div class="kicker" style="position:absolute;left:52px;top:48px;color:{C['soft']}">Пространство новых идей 2.0 · 26 августа 2026 · площадка № 2</div>
<h1 style="position:absolute;left:52px;top:130px;width:860px;font-size:48px;line-height:1.08">Организация питания:<br>опыт реализации проектов</h1>
{bar(268, 52, 72)}
<div class="serif" style="position:absolute;left:52px;top:292px;width:820px;font-style:italic;font-weight:600;font-size:24px;line-height:1.35;color:{C['body']}">Не просто накормить</div>
<div style="position:absolute;left:52px;top:400px;width:430px;font-size:20px;line-height:1.45">
<b>Чистяков Е. В.</b><br>ДСО «Серафимовский» · 223-ФЗ</div>
<div style="position:absolute;left:500px;top:400px;width:412px;font-size:20px;line-height:1.45">
<b>Нурбаев Т. А.</b><br>ДСО «Тесовый берег» · 44-ФЗ</div>
'''
add_main(slide(1, body))

# 02 Боль
chips = ['очередь', 'отказ', 'кофе', 'добавка', 'журналы']
body = h('Один обед — пять конфликтов', 40, top=100)
for i, lab in enumerate(chips):
    x = 52 + i * 176
    body += txt(lab, x, 196, 168, size=32, serif=True, color=C['ink'])
body += bar(268, 52, 72)
body += cap('Голодный житель и сырьё в баке — одна система.', 300, 24)
body += txt('Национальной цифры отходов нет. Не «40 %». Не «котлеты».', 52, 400, 856, size=22, color=C['soft'])
add_main(slide(2, body, kicker='Боль · не витрина'))

# 03 Дисфагия
body = num('21,9–69,5 %', top=128, size=92)
body += bar(248, 52, 72)
body += cap('дисфагия — в изученных клинических группах', 280, 26)
body += txt('На все российские ДСО это не переносится.', 52, 400, 856, size=22, color=C['soft'])
add_main(slide(3, body, kicker='Боль · клиника'))

# 04 2 190
body = num('2 190', top=118, size=185)
body += bar(348, 52, 60)
body += cap('шесть приёмов × 365. Решение за человека.', 372, 24)
body += txt('завтрак · 2-й завтрак · обед · полдник · ужин · 2-й ужин', 52, 430, 856, size=22, color=C['soft'])
add_main(slide(4, body, kicker='Контекст · наш дом'))

# 05 74 %
body = num('74 %', top=118, size=185)
body += bar(348, 52, 60)
body += cap('порядка трёх из четырёх. Типичный контингент.', 372, 24)
body += txt('Не Минтруд. Не ТАСС. 2024, «Если быть точным». Ваш дом — свой процент.', 52, 430, 856, size=22, color=C['soft'])
add_main(slide(5, body, kicker='Контекст · недееспособность'))

# 06 Ночь
body = num('15 ч', top=100, size=140)
body += txt('пример расписания. Не «типовой дом РФ».', 52, 268, 856, size=22, color=C['soft'])
body += num('≤13 ч', top=330, size=72, color=C['accentdeep'])
body += txt('цель нашего дома. Какая цифра у вас?', 52, 430, 856, size=22, color=C['ink'])
add_main(slide(6, body, kicker='Проблема · ночной интервал'))

# 07 Папка
docs = ['положение', 'журнал заказа', 'журнал замен', 'пищевые карты', 'учредитель']
body = h('Ответ проверке — папка', 42, top=96)
body += bar(168, 52, 72)
for i, lab in enumerate(docs):
    body += txt(lab, 52, 188 + i * 42, 856, size=32, serif=True, color=C['ink'])
body += txt('Не формула «запрета нет». Гуманное отношение — ст. 5 ч. 2 3185-1.', 52, 430, 856, size=22, color=C['soft'])
add_main(slide(7, body, kicker='Право · броня'))

# 08 Герой: Иркутск (одна из шести историй на основном пути)
body = region_body('Иркутская область', 'масштаб региона', '2025 · два первых · два вторых · гарниры')
add_main(slide(8, body, kicker='Опыт · одна история'))

# 09 Приказ 124
body = num('№ 124', top=110, size=140)
body += bar(278, 52, 72)
body += cap('заказное питание — правила дома', 310, 32, color=C['accentdeep'])
body += txt('10 марта 2026. Включая маломобильных.', 52, 420, 856, size=22, color=C['soft'])
add_main(slide(9, body, kicker='Наш дом · приказ'))

# 10 Два закона
body = num('223', top=110, size=120, left=52)
body += num('44', top=110, size=120, left=520)
body += txt('Серафимовский', 52, 268, 400, size=24, serif=True, color=C['ink'])
body += txt('Тесовый берег', 520, 268, 400, size=24, serif=True, color=C['ink'])
body += bar(330, 52, 72)
body += cap('Один учредитель. Разные контуры закупок.', 360, 26)
body += txt('Не путать кухни и законы.', 52, 430, 856, size=22, color=C['soft'])
add_main(slide(10, body, kicker='Со-модератор · два дома'))

# 11 Сначала врач
body = h('Сначала врач', 64, top=130)
body += bar(230, 52, 72)
body += cap('текстура · стол · отказ · инсулин — не смена', 270, 28)
body += txt('Три отказа подряд — врач сегодня. Поперхнулся — немедленно.', 52, 420, 856, size=22, color=C['soft'])
add_main(slide(11, body, kicker='Граница врача'))

# 12 Campforts
body = num('76,3 %', top=110, size=140)
body += bar(278, 52, 72)
body += cap('клозапин. Прибавка веса. Campforts, 2023.', 310, 26)
body += txt('Оланзапин 36,9 % · рисперидон 23 %. Не «уберите котлету».', 52, 420, 856, size=22, color=C['soft'])
add_main(slide(12, body, kicker='Граница врача · вес'))

# 13 Пары
body = h('Гречка или рис', 56, top=120)
body += txt('Курица или индейка', 52, 210, 856, size=40, serif=True, color=C['accentdeep'])
body += bar(280, 52, 72)
body += cap('Норма ограничивает набор. Не выбор.', 320, 26)
body += txt('Два варианта на завтрак и обед. Стандарт всегда на линии.', 52, 420, 856, size=22, color=C['soft'])
add_main(slide(13, body, kicker='Кухня · пары'))

# 14 Рамка × выбор
body = h('Врач задаёт рамку', 48, top=130)
body += txt('внутри — пары', 52, 210, 856, size=48, serif=True, color=C['accentdeep'])
body += bar(290, 52, 72)
body += cap('Диета сжимает множество. Не тарелку до одного блюда.', 330, 24)
add_main(slide(14, body, kicker='Лечебное × вариативное'))

# 15 Каналы воли — четыре слова, без абзацев
words4 = ['показ', 'наблюдение', 'биография', 'те, кто знает']
body = h('Кто не говорит', 40, top=96)
body += bar(164, 52, 72)
for i, w in enumerate(words4):
    col, row = i % 2, i // 2
    x, y = 52 + col * 430, 200 + row * 110
    body += txt(f'{i + 1}', x, y, 50, size=36, serif=True, color=C['accent'])
    body += txt(w, x + 56, y + 6, 360, size=36, serif=True, color=C['ink'])
add_main(slide(15, body, kicker='Каналы воли'))

# 16 Путь директора
steps = [('1', 'Замер'), ('2', 'Приказ'), ('3', 'Смена'), ('4', '90 дней'), ('5', 'Масштаб')]
body = h('Пять шагов. Не весь дом', 36, top=96)
for i, (n, t) in enumerate(steps):
    x = 52 + i * 176
    fill = C['accent'] if i == 3 else C['panel']
    ncol = '#FFF9F2' if i == 3 else C['accent']
    tcol = '#FFF9F2' if i == 3 else C['ink']
    body += (f'<div style="position:absolute;left:{x}px;top:180px;width:164px;height:168px;'
             f'background:{fill};border-radius:14px"></div>')
    body += txt(n, x, 198, 164, size=36, serif=True, align='center', color=ncol)
    body += txt(t, x, 260, 164, size=24, serif=True, align='center', color=tcol)
body += txt('Не сдвинулось — возврат к цикличке. Успенский = М2, не буфет.', 52, 430, 856, size=22, color=C['soft'])
add_main(slide(16, body, kicker='Путь директора'))

# 17 Три ошибки
errs = ['Имитация выбора', 'Выбор без гарантии', 'Повар назначил стол']
body = h('Три ошибки дороже бездействия', 32, top=96)
body += bar(160, 52, 72)
for i, t in enumerate(errs):
    body += txt(f'{i + 1}', 52, 196 + i * 70, 50, size=36, serif=True, color=C['accent'])
    body += txt(t, 110, 204 + i * 70, 740, size=32, serif=True, color=C['ink'])
add_main(slide(17, body, kicker='Красные линии'))

# 18 СанПиН
body = num('01.09', top=110, size=140)
body += bar(278, 52, 72)
body += cap('новый СанПиН. Журналы августа не переписывать.', 310, 24)
body += txt('Число вариантов блюда не ограничено ни в одной редакции.', 52, 420, 856, size=22, color=C['soft'])
add_main(slide(18, body, kicker='Переход · через шесть дней'))

# 19 Пилот
body = num('90 дней', top=110, size=110)
body += bar(250, 52, 72)
body += cap('Одно отделение. Не весь дом.', 290, 32, color=C['accentdeep'])
body += txt('Не сдвинулись отходы и жалобы — возврат к цикличке. Это управление.', 52, 400, 856, size=22, color=C['ink'])
add_main(slide(19, body, kicker='Пилот · риск локализован'))

# 20 Измеряйте
body = f'''
<div style="position:absolute;left:0;top:0;width:100%;height:100%;background:{C['dark']}"></div>
<div style="position:absolute;left:52px;top:74px;width:120px;height:5px;background:{C['accent']}"></div>
<div style="position:absolute;left:52px;top:130px;width:850px;font-family:'Playfair Lat','Playfair Cyr','PT Sans',serif;font-weight:800;font-size:42px;line-height:1.2;color:#FAF9F5">
Тарелка — самое частое решение,<br>которое дом принимает за жителя.</div>
<div style="position:absolute;left:52px;top:330px;width:820px;font-family:'Playfair Lat','Playfair Cyr','PT Sans',serif;font-style:italic;font-weight:600;font-size:36px;line-height:1.3;color:{C['accent']}">Измеряйте.</div>
'''
add_main(slide(20, body))


# ═══ РЕЗЕРВ ═══
# Сначала — пять остальных публичных историй, одна на слайд (после легенды).

add_res(slide(0, region_body('Успенский ПНИ', 'М2 · не шведская линия',
                             'Новосибирская обл. · два вторых ежедневно · буфет — ДДСОЛ')),
        'kitchen')
add_res(slide(0, region_body('Болотнинский ПНИ', 'несколько раз в неделю',
                             'Новосибирская обл. · 2024 · завтрак и обед')),
        'kitchen')
add_res(slide(0, region_body('Усть-Илимский ДСО', 'опрос → выбор',
                             'Иркутская обл. · 2024 · старт со столовой')),
        'kitchen')
add_res(slide(0, region_body('Серафимовский ДСО', 'заказ накануне',
                             'Санкт-Петербург · часть жителей · новость Комитета')),
        'kitchen')
add_res(slide(0, region_body('Тесовый берег ДСО', 'фарфор · линия раздачи',
                             'Санкт-Петербург · 44-ФЗ · дом со-модератора')),
        'kitchen')

# Три конфликта
conf = ['Выбор или безопасность', 'Вариативность или норматив', 'Единое меню или поддержка']
body = h('Три конфликта зала', 40, top=100)
body += bar(168, 52, 72)
for i, t in enumerate(conf):
    body += txt(f'{i + 1}', 52, 200 + i * 70, 50, size=36, serif=True, color=C['accent'])
    body += txt(t, 110, 208 + i * 70, 740, size=28, serif=True, color=C['ink'])
add_res(slide(0, body, kicker='Формат'), 'law')

# Цена старта
body = h('Старт не был бесплатным', 40, top=120)
body += bar(190, 52, 72)
body += cap('Оборудование и ставки. Говорю прямо.', 230, 28)
body += txt('Универсального «бесплатного старта» нет.', 52, 400, 856, size=22, color=C['soft'])
add_res(slide(0, body, kicker='Кейс · цена'), 'money')

# М0–М5
mods = [('0', 'мономеню'), ('1', 'выбор из двух'), ('2', 'выбор везде'),
        ('3', 'шведская линия'), ('4', 'семейная подача'), ('5', 'своя кухня')]
body = h('М0–М5. Не путать с путём директора', 32, top=96)
for i, (n, t) in enumerate(mods):
    x = 52 + (i % 3) * 292
    y = 180 + (i // 3) * 130
    body += txt(f'M{n}', x, y, 260, size=36, serif=True, color=C['accent'] if i >= 2 else C['ink'])
    body += txt(t, x, y + 50, 260, size=22, color=C['body'])
body += txt('Подтверждены М1–М2. М3–М5 — горизонт.', 52, 440, 856, size=22, color=C['soft'])
add_res(slide(0, body, kicker='Модели раздачи'), 'kitchen')

# Вопрос залу
body = h('Кто сегодня решает, что на обед?', 36, top=150)
body += bar(260, 52, 72)
body += cap('Кухня · диетсестра · директор · совет · житель', 300, 24)
add_res(slide(0, body, kicker='Вопрос залу'), 'law')

# Второй вариант
body = num('не сырьё', top=120, size=72)
body += bar(230, 52, 72)
body += cap('Цена второго варианта — труд и порядок.', 270, 26)
body += txt('Журнал. Вторая гастроёмкость. Обучение смены. Отходы — замер.', 52, 400, 856, size=22, color=C['soft'])
add_res(slide(0, body, kicker='Экономика пары'), 'money')

# Лечебное голосование
body = txt('А', 52, 120, 80, size=72, serif=True, color=C['ink'])
body += txt('Обычное. Диета — поимённо.', 160, 148, 700, size=28, serif=True, color=C['ink'])
body += txt('Б', 52, 260, 80, size=72, serif=True, color=C['accentdeep'])
body += txt('Лечебное всем — так безопаснее?', 160, 288, 700, size=28, serif=True, color=C['accentdeep'])
body += txt('Руки за А. Руки за Б.', 52, 430, 856, size=22, color=C['soft'])
add_res(slide(0, body, kicker='Вопрос 3'), 'clinic')

# IDDSI
body = num('90 %', top=110, size=160)
body += bar(300, 52, 72)
body += cap('соответствие текстур после обучения. Не после закупки.', 340, 24)
body += txt('Текстуру назначает врач. IDDSI — язык описания.', 52, 430, 856, size=22, color=C['soft'])
add_res(slide(0, body, kicker='Безопасность · IDDSI'), 'clinic')

# 3–6×
body = num('3–6×', top=118, size=160)
body += bar(310, 52, 72)
body += cap('полная цена обеда выше сырьевой строки.', 350, 24)
body += txt('Экономить на потерях, не на белке.', 52, 430, 856, size=22, color=C['soft'])
add_res(slide(0, body, kicker='Экономика качества'), 'money')

# ФАС
body = num('543', top=110, size=160)
body += bar(300, 52, 72)
body += cap('торга · 4,7 млрд ₽ · картель ФАС, 2024.', 340, 26)
add_res(slide(0, body, kicker='Закупки'), 'money')

# Шесть вопросов — короткие заголовки, не простыня
qs = ['Кто выбирает — житель или руководитель?',
      'Меню при норме и бюджете',
      'Должно ли питание быть «лечебным»?',
      'Лечебное × вариативное',
      'Выбор и медицинские рамки',
      'Качество и цена порции']
body = h('Шесть вопросов программы', 32, top=88)
for i, q in enumerate(qs):
    body += txt(f'{i + 1}', 52, 150 + i * 52, 40, size=24, serif=True, color=C['accent'])
    body += txt(q, 100, 154 + i * 52, 800, size=22, color=C['ink'])
add_res(slide(0, body, kicker='Резерв · программа'), 'law')

# Материалы
body = h('Доклад · калькулятор · чек-листы', 36, top=120)
body += bar(190, 52, 72)
body += cap('github.com/qlolp/seminar-variable-food-2026', 230, 24)
body += '<img src="qr.png" style="position:absolute;left:52px;top:320px;width:120px;height:120px;border-radius:10px">'
body += txt('Открыто. Без выдуманной «восемнадцати».', 200, 360, 600, size=22, color=C['soft'])
add_res(slide(0, body, kicker='Материалы'))

# Спасибо
body = h('Спасибо', 72, top=140)
body += bar(250, 52, 72)
body += cap('Чистяков · Серафимовский · 223-ФЗ', 290, 24)
body += txt('Нурбаев · Тесовый берег · 44-ФЗ', 52, 400, 856, size=24, serif=True, color=C['ink'])
add_res(slide(0, body, kicker='Контакты'))

# Формула
body = h('Способ выразить · вариант · отказ услышан', 32, top=140)
body += bar(230, 52, 72)
body += cap('Профиль → заказ → тарелка → съедено → замена.', 280, 26)
body += txt('Процент выбравших — не KPI.', 52, 420, 856, size=22, color=C['soft'])
add_res(slide(0, body, kicker='Формула результата'), 'law')

# Открытый микрофон
body = h('Что ломается первым?', 48, top=150)
body += bar(240, 52, 72)
body += cap('Деньги · руки · страх проверки · «особые жители»', 290, 24)
add_res(slide(0, body, kicker='Открытый микрофон'))


# ── сборка: 20 + легенда + резерв ──
def apply_edge_tag(html, kind):
    color, label = TAG[kind], TAG_LABEL[kind]
    bar_html = (
        f'<div style="position:absolute;left:0;top:0;width:12px;height:540px;background:{color};z-index:6"></div>'
        f'<div style="position:absolute;right:22px;top:12px;z-index:6;font-size:12px;font-weight:bold;'
        f'letter-spacing:2.2px;color:{color};border:2px solid {color};padding:4px 11px;border-radius:4px;'
        f'background:{C["ivory"]}">{label}</div>'
    )
    return re.sub(r'(<div class="slide"[^>]*>)', lambda m: m.group(1) + bar_html, html, count=1)


div = h('Резерв для ответов', 40, top=100)
div += cap('Основной показ закончен. Дальше — прыжок по вопросу зала.', 170, 22)
legend = ['law', 'money', 'kitchen', 'clinic']
for i, k in enumerate(legend):
    x = 52 + i * 220
    div += (f'<div style="position:absolute;left:{x}px;top:300px;width:14px;height:56px;'
            f'background:{TAG[k]};border-radius:3px"></div>')
    div += txt(TAG_LABEL[k], x + 28, 310, 180, size=28, serif=True, color=TAG[k])
divider = slide(0, div, kicker='Резерв · легенда')


def _restamp(html, label):
    return re.sub(r'<div class="foot"><span>.*?</span></div>',
                  f'<div class="foot"><span>{label}</span></div>', html, count=1)


out = []
for i, html in enumerate(MAIN, 1):
    out.append(_restamp(html, f'<b>{i}</b>'))
out.append(_restamp(divider, ''))
for j, (html, kind) in enumerate(RESERVE, 1):
    if kind:
        html = apply_edge_tag(html, kind)
    out.append(_restamp(html, f'<b>R{j}</b>'))

# ── запись ──
os.makedirs(f'{HERE}/slides', exist_ok=True)
for old in glob.glob(f'{HERE}/slides/slide-*.html'):
    os.remove(old)
for i, html_doc in enumerate(out, 1):
    open(f'{HERE}/slides/slide-{i:02d}.html', 'w', encoding='utf-8').write(html_doc)
print(len(MAIN), 'main +', 1, 'legend +', len(RESERVE), 'reserve =', len(out), 'written')

# ── PDF ──
if '--pdf' in sys.argv:
    PDF_DIR = f'{HERE}/_pdf'
    os.makedirs(PDF_DIR, exist_ok=True)
    for old in glob.glob(f'{PDF_DIR}/p*.pdf'):
        os.remove(old)
    env = os.environ.copy()
    env.pop('PYTHONPATH', None)
    for i in range(1, len(out) + 1):
        html = f'{HERE}/slides/slide-{i:02d}.html'
        p_pdf = f'{PDF_DIR}/p{i:02d}.pdf'
        r = subprocess.run(['weasyprint', html, p_pdf], env=env, capture_output=True, text=True)
        if r.returncode != 0:
            sys.stderr.write(r.stderr or r.stdout or 'weasyprint failed\n')
            raise SystemExit(f'weasyprint failed on slide {i}')
    dest_here = f'{HERE}/Презентация_v4_дискуссия_26_08_стиль_claude.pdf'
    dest_root = os.path.join(os.path.dirname(HERE), 'Презентация_дискуссия_26_08_v4_стиль_claude.pdf')
    pages = sorted(glob.glob(f'{PDF_DIR}/p*.pdf'))
    subprocess.run(['pdfunite', *pages, dest_here], check=True, env=env)
    subprocess.run(['cp', dest_here, dest_root], check=True)
    print(f'PDF: {len(pages)} slides -> {dest_here}')
    print(f'copy -> {dest_root}')
