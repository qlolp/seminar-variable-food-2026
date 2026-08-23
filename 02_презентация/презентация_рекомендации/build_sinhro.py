# -*- coding: utf-8 -*-
"""Синхронная презентация к брошюре «Организация вариативного питания:
опыт реализации проектов». Стиль claude, повторяет арку брошюры + шесть вопросов.
Сборка: python3 build_sinhro.py --pdf  (HTML + WeasyPrint + pdfunite)."""
import glob, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IVORY, CARD = '#FAF9F5', '#F5EFE6'
INK, MID, MUTED = '#2B1D14', '#5C3D2E', '#87867F'
ACCENT, LINE, DARK = '#B96420', '#E3DCCE', '#2B1D14'
SERIF = "'Playfair Cyr','Playfair Lat','Playfair Display',serif"
SANS = "'Inter Cyr','Inter Lat','Inter',system-ui,sans-serif"

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
@font-face { font-family:'Inter Cyr'; src:url('fonts/inter-400-cyr.woff2') format('woff2'); font-weight:400; }
@font-face { font-family:'Inter Lat'; src:url('fonts/inter-600-lat.woff2') format('woff2'); font-weight:600; }
@font-face { font-family:'Inter Cyr'; src:url('fonts/inter-600-cyr.woff2') format('woff2'); font-weight:600; }
"""
CSS = f"""{FACE}
@page {{ size:960px 540px; margin:0 }}
html,body {{ margin:0; padding:0 }}
.slide {{ position:relative; width:960px; height:540px; background:{IVORY};
         overflow:hidden; font-family:{SANS}; color:{INK}; }}
.foot {{ position:absolute; right:52px; bottom:16px; font-size:30px; color:{MUTED}; }}
.kicker {{ font-weight:600; font-size:12px; letter-spacing:2px; color:{MID}; text-transform:uppercase; }}
h1 {{ font-family:{SERIF}; font-weight:800; margin:0; line-height:1.12; color:{INK}; }}
"""


def slide(num, body, bg=None, fc=None):
    style = f' style="background:{bg}"' if bg else ''
    foot = f'<div class="foot" style="color:{fc or MUTED}">{num}</div>'
    return (f'<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body><div class="slide"{style}>{body}{foot}</div></body></html>')


def kick(t, y=52, color=None):
    return (f'<div class="kicker" style="position:absolute;left:52px;top:{y}px;width:856px;'
            f'color:{color or MID}">{t}</div>')


def h(t, size=44, top=92, left=52, width=856, color=None, weight=800):
    return (f'<h1 style="position:absolute;left:{left}px;top:{top}px;width:{width}px;'
            f'font-size:{size}px;font-weight:{weight};color:{color or INK}">{t}</h1>')


def tx(t, x, y, w, size=17, color=None, bold=False, serif=False, italic=False, align='left', lh=1.35, weight=None):
    fam = f'font-family:{SERIF};' if serif else ''
    weight = weight if weight is not None else (600 if bold else 400)
    it = 'font-style:italic;' if italic else ''
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;font-size:{size}px;'
            f'line-height:{lh};color:{color or INK};{fam}font-weight:{weight};{it}text-align:{align}">{t}</div>')


def bar(x=52, y=210, w=52, h=3):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{ACCENT}"></div>'


def panel(x, y, w, hh, inner, leftbar=True):
    lb = (f'<div style="position:absolute;left:0;top:0;width:4px;height:{hh}px;background:{ACCENT}"></div>'
          if leftbar else '')
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{hh}px;'
            f'background:{CARD};border-radius:8px;overflow:hidden">{lb}{inner}</div>')


OUT = []


def add(html):
    OUT.append(html)


# 01 Титул
add(slide(1,
    kick('Методическое руководство · опыт реализации проектов') +
    h('Организация<br>вариативного питания', 52, top=96, weight=900) +
    bar(52, 236, 52, 3) +
    tx('в домах социального обслуживания', 52, 256, 856, size=20, italic=True, serif=True, weight=600, color=MID) +
    tx('<b style="font-weight:600">Чистяков Евгений Владимирович</b><br>'
       'директор ДСО «Серафимовский»', 52, 400, 420, size=15, color=INK, lh=1.4) +
    tx('<b style="font-weight:600">Нурбаев Тимур Аликович</b><br>'
       'директор ДСО «Тесовый берег»', 500, 400, 408, size=15, color=INK, lh=1.4)))

# 02 Тихий обед
add(slide(2,
    kick('Часть первая') + h('Обед, которого мы не замечаем', 42, top=86) +
    tx('Сто двадцать человек едят одно и то же, из одинаковых тарелок,<br>в одном и том же порядке — как вчера и как завтра.', 52, 190, 856, size=22, serif=True, weight=700, lh=1.4) +
    tx('Никто не спросил их, чего им хочется. Никто и не думал, что об этом стоит спрашивать.', 52, 320, 856, size=18, color=MID)))

# 03 Она показала пальцем
add(slide(3,
    tx('«Какое?»', 52, 96, 856, size=64, serif=True, weight=900, color=ACCENT) +
    tx('Женщина, годами молчавшая, посмотрела на две тарелки долго,<br>внимательно — и показала пальцем.', 52, 220, 856, size=24, serif=True, weight=700, lh=1.4) +
    tx('Человек, за которого годами всё решали, вдруг решил сам. Это и есть возвращённое право.', 52, 350, 856, size=18, color=MID)))

# 04 Кто решает
who = ['Он сам', 'Помощник по уходу', 'Врач', 'Кухня', 'Поставщик по контракту', 'Региональная норма']
body = h('Кто решает, что на тарелке?', 40, top=64)
for i, w in enumerate(who):
    col, row = i % 2, i // 2
    x, y = 52 + col * 452, 150 + row * 84
    body += tx(str(i + 1), x, y, 40, size=26, serif=True, weight=900, color=ACCENT)
    body += tx(w, x + 48, y + 4, 380, size=21, serif=True, weight=700)
body += tx('Чаще всего честный ответ — «кухня» и «норма». Реже всего — «он сам».', 52, 424, 856, size=18, bold=True, color=MID)
add(slide(4, body))

# 05 Два соблазна
body = h('Два соблазна, которые лучше отбросить', 34, top=64)
duo = [('«Баловство»', 'Будто выбор — украшение, до которого дойдут руки потом. Но однообразная еда — это несъеденные калории и жалобы.'),
       ('«Ресторан»', 'Будто нужна вторая кухня и новая смета. Это удобный повод не начинать. Первый шаг стоит решимости спросить.')]
for i, (t_, d) in enumerate(duo):
    x = 52 + i * 436
    inner = (f'<div style="position:absolute;left:24px;top:26px;width:368px;font-family:{SERIF};'
             f'font-weight:800;font-size:26px;color:{INK}">{t_}</div>'
             f'<div style="position:absolute;left:24px;top:78px;width:368px;font-size:16px;'
             f'color:{MID};line-height:1.45">{d}</div>')
    body += panel(x, 150, 420, 210, inner)
body += tx('Вариативность — не подарок и не роскошь, а выполнимая работа со своими правилами безопасности.', 52, 396, 856, size=17, bold=True)
add(slide(5, body))

# 06 Сначала граница
body = h('Сначала — граница, потом меню', 38, top=60)
rows = [('Ограничения, лечебная диета, текстуры, лекарства и еда', 'Врач'),
        ('Какое из двух равноценных блюд сегодня', 'Житель'),
        ('Технология раздачи, подбор пар блюд', 'Заведующий производством'),
        ('Финансирование, ставки, статус', 'Учредитель')]
for i, (l, r) in enumerate(rows):
    y = 148 + i * 72
    inner = (f'<div style="position:absolute;left:20px;top:14px;width:560px;font-size:17px;color:{INK}">{l}</div>'
             f'<div style="position:absolute;left:600px;top:12px;width:230px;font-family:{SERIF};'
             f'font-weight:800;font-size:19px;color:{ACCENT}">{r}</div>')
    body += panel(52, y, 856, 60, inner)
body += tx('Кухня исполняет назначение, но не ставит диагноз. Без записанной границы выбор опасен.', 52, 452, 856, size=16, color=MID)
add(slide(6, body))

# 07 Начинать с малого
body = h('Начинать с малого', 42, top=64)
for i, (a, b) in enumerate([('Одно отделение', 'лучше — потруднее'), ('Один приём пищи', 'например, обед'), ('Заказ накануне', 'два равноценных варианта')]):
    x = 52 + i * 292
    inner = (f'<div style="position:absolute;left:20px;top:22px;width:236px;font-family:{SERIF};'
             f'font-weight:800;font-size:22px;color:{INK}">{a}</div>'
             f'<div style="position:absolute;left:20px;top:70px;width:236px;font-size:15px;color:{MID}">{b}</div>')
    body += panel(x, 160, 276, 130, inner)
body += tx('Гречка или рис. Курица или рыба. То же сырьё, та же норма — но человек сказал, чего он хочет.', 52, 330, 856, size=19, serif=True, weight=700) + \
        tx('Выбор записываем — сначала в обычную тетрадь. Она превращает добрую волю в проверяемый факт.', 52, 404, 856, size=16, color=MID)
add(slide(7, body))

# 08 Выбор стал правилом дома (кульминация)
body = kick('Часть третья · перелом') + h('Выбор стал правилом дома', 44, top=84)
body += tx('Мы закрепили заказное питание в правилах внутреннего распорядка — приказом.', 52, 200, 856, size=22, serif=True, weight=700, lh=1.4)
body += tx('С этого дня возможность выбрать перестала быть экспериментом «по новости» и стала нормой учреждения, на которую можно сослаться. Для маломобильных жителей — помощь и выбор прямо в комнатах.', 52, 300, 856, size=18, color=MID, lh=1.45)
add(slide(8, body))

# 09 Честно о цене
body = h('Честно о цене', 42, top=64)
body += tx('Наш переход дался не даром: дом закупил оборудование и добавил сотрудников.', 52, 168, 856, size=20, serif=True, weight=700)
body += tx('«Без новой сметы» — правда только для первого, пробного шага на одном отделении. Полный перевод большого дома требует ресурсов, и мы говорим об этом прямо.', 52, 250, 856, size=18, color=MID, lh=1.45)
body += tx('Но ни один наш шаг не начинался со слов «сначала дайте денег». Он начинался с решения спросить человека.', 52, 396, 856, size=18, bold=True)
add(slide(9, body))

# 10 Пилот 90 дней
body = h('Пилот на 90 дней: три шага', 40, top=64)
steps = [('1', 'Месяц замера', 'отходы, время раздачи, ночной перерыв — цифры «до»'),
         ('2', 'Месяц подготовки', 'граница врача, положение и журналы, обучение смены'),
         ('3', 'Месяц выбора', 'два варианта на приёме, запись, сравнение с «до»')]
for i, (n, hh, d) in enumerate(steps):
    x = 52 + i * 292
    inner = (f'<div style="position:absolute;left:20px;top:18px;font-family:{SERIF};font-weight:900;'
             f'font-size:38px;color:{ACCENT}">{n}</div>'
             f'<div style="position:absolute;left:20px;top:76px;width:236px;font-family:{SERIF};'
             f'font-weight:800;font-size:19px;color:{INK}">{hh}</div>'
             f'<div style="position:absolute;left:20px;top:118px;width:236px;font-size:14px;color:{MID};line-height:1.35">{d}</div>')
    body += panel(x, 152, 276, 210, inner)
body += tx('Без замера «до» через три месяца сравнивать будет не с чем.', 52, 392, 856, size=16, bold=True)
add(slide(10, body))

# 11 Измеряйте
body = tx('Не «внедряйте» —<br>а «измеряйте».', 52, 120, 856, size=52, serif=True, weight=900, color=INK, lh=1.15)
body += bar(52, 320, 64, 4)
body += tx('Доказать, что выбор продлевает жизнь, я не могу — таких исследований пока нет. Но организовать выбор безопасно и проследить, дошёл ли он до тарелки, — можно. Семь дней замера отделяют убеждение от знания.', 52, 356, 856, size=18, color=MID, lh=1.45)
add(slide(11, body))

# 12 Шесть вопросов
qs = ['Кто выбирает форму питания — проживающий или руководитель?',
      'Как формировать меню при жёстких нормах и ограничениях бюджета?',
      'Должно ли питание в социальных домах быть «лечебным»?',
      'Как совместить лечебное питание и выбор, не отнимая право выбирать?',
      'Как соблюсти баланс между выбором недееспособного и назначениями врача?',
      'Как совместить качество продуктов и нормирование цен?']
body = kick('Часть пятая · к разговору с коллегой') + h('Шесть вопросов дискуссии', 38, top=78)
for i, q in enumerate(qs):
    y = 150 + i * 60
    body += tx(str(i + 1), 52, y, 36, size=22, serif=True, weight=900, color=ACCENT)
    body += tx(q, 96, y + 2, 812, size=17, color=INK, lh=1.25)
add(slide(12, body))

# 13 Финал (тёмный)
body = (f'<div style="position:absolute;left:52px;top:96px;font-family:{SERIF};font-weight:900;'
        f'font-size:110px;line-height:0.8;color:{ACCENT}">«</div>'
        f'<div style="position:absolute;left:52px;top:160px;width:856px;font-family:{SERIF};'
        f'font-weight:800;font-size:38px;line-height:1.25;color:{CARD}">'
        f'Право выбора становится настоящим,<br>когда его можно проследить<br>до конкретной тарелки.</div>'
        f'<div class="kicker" style="position:absolute;left:52px;top:392px;width:856px;color:{ACCENT}">'
        f'Приглашаю коллег пройти этот путь вместе</div>')
add(slide(13, body, bg=DARK, fc=MUTED))


# ── запись + PDF ──
for old in glob.glob(f'{HERE}/slide-*.html'):
    os.remove(old)
for i, doc in enumerate(OUT, 1):
    open(f'{HERE}/slide-{i:02d}.html', 'w', encoding='utf-8').write(doc)
print(len(OUT), 'slides written')

if '--pdf' in sys.argv:
    PDF_DIR = f'{HERE}/_pdf'
    os.makedirs(PDF_DIR, exist_ok=True)
    for old in glob.glob(f'{PDF_DIR}/p*.pdf'):
        os.remove(old)
    env = os.environ.copy(); env.pop('PYTHONPATH', None)
    for i in range(1, len(OUT) + 1):
        src = f'{HERE}/slide-{i:02d}.html'
        p_pdf = f'{PDF_DIR}/p{i:02d}.pdf'
        r = subprocess.run(['weasyprint', src, p_pdf], env=env, capture_output=True, text=True, cwd=HERE)
        if r.returncode != 0:
            sys.stderr.write(r.stderr or r.stdout or 'weasyprint failed\n')
            raise SystemExit(f'weasyprint failed on slide {i}')
    dest = os.path.join(os.path.dirname(HERE), 'Презентация_рекомендации_синхронная.pdf')
    pages = sorted(glob.glob(f'{PDF_DIR}/p*.pdf'))
    subprocess.run(['pdfunite', *pages, dest], check=True, env=env)
    print(f'PDF: {len(pages)} слайдов -> {dest}')
