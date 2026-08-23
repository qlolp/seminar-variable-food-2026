# -*- coding: utf-8 -*-
"""WeasyPrint-PDF колоды v6. LibreOffice на машине сборки может отсутствовать.
Шрифты — локальные split-woff2 из v5 (url('../fonts/...') относительно HTML).
PYTHONPATH не задавать. PATH=/opt/homebrew/bin:$PATH python3 build_v6_pdf.py
"""
import glob, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
V5_FONTS = os.path.join(os.path.dirname(os.path.dirname(HERE)),
                        "презентация_v5_21_слайд", "fonts")
HTML_DIR = os.path.join(ROOT, "_html")
PDF_DIR = os.path.join(ROOT, "_pdf")

IVORY, CARD, WARM = "#FAF9F5", "#F0EEE6", "#F5E7DE"
INK, SOFT, MUTED = "#141413", "#6E6A5E", "#87867F"
ACCENT, DARK = "#C15F3C", "#141413"
SERIF = "'Playfair Lat','Playfair Cyr','Playfair Display',serif"
SANS = "'Inter Lat','Inter Ext','Inter Cyr','Inter',system-ui,sans-serif"

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
CSS = f"""{FACE}
@page {{ size:960px 540px; margin:0 }}
html,body {{ margin:0; padding:0 }}
.slide {{ position:relative; width:960px; height:540px; background:{IVORY};
         overflow:hidden; font-family:{SANS}; color:{INK}; }}
.foot {{ position:absolute; right:40px; bottom:14px; font-size:15px;
        color:{ACCENT}; font-weight:600; }}
.kicker {{ font-weight:600; font-size:11px; letter-spacing:1.6px; color:{SOFT};
           text-transform:uppercase; }}
h1 {{ font-family:{SERIF}; font-weight:800; margin:0; line-height:1.12; color:{INK}; }}
.card {{ background:{CARD}; border-radius:10px; }}
.warm {{ background:{WARM}; border-radius:10px; }}
.note {{ font-style:italic; color:{SOFT}; }}
"""


def page(num, body, bg=None, foot=None):
    style = f' style="background:{bg}"' if bg else ""
    lab = foot if foot is not None else str(num)
    fc = "#C15F3C" if not bg else ACCENT
    return (f'<!DOCTYPE html><html lang="ru"><head><meta charset="utf-8">'
            f"<style>{CSS}</style></head><body>"
            f'<div class="slide"{style}>{body}'
            f'<div class="foot" style="color:{fc}">{lab}</div>'
            f"</div></body></html>")


def k(text, y=36):
    return (f'<div class="kicker" style="position:absolute;left:48px;top:{y}px;'
            f'width:864px">{text}</div>')


def h(text, size=34, top=68, color=None, w=864):
    col = color or INK
    return (f'<h1 style="position:absolute;left:48px;top:{top}px;width:{w}px;'
            f'font-size:{size}px;color:{col}">{text}</h1>')


def t(text, x, y, w, size=15, color=None, bold=False, serif=False,
      italic=False, align="left", lh=1.35):
    col = color or INK
    fam = f"font-family:{SERIF};" if serif else ""
    wt = 600 if bold else 400
    it = "font-style:italic;" if italic else ""
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;'
            f"font-size:{size}px;line-height:{lh};color:{col};{fam}"
            f'font-weight:{wt};{it}text-align:{align}">{text}</div>')


def box(x, y, w, hh, cls="card"):
    return (f'<div class="{cls}" style="position:absolute;left:{x}px;top:{y}px;'
            f'width:{w}px;height:{hh}px"></div>')


OUT = []


def add(html):
    OUT.append(html)


# 1
add(page(1,
    k("Пространство Новых Идей 2.0 · Санкт-Петербург · 25–27 августа 2026") +
    t("Дискуссия · 26 августа · 14:00–15:30 · площадка № 2 — ДСО «Тесовый берег»",
      48, 64, 864, 14, color=SOFT) +
    h("Не просто накормить", 52, 120) +
    t("Как организовать безопасное, достойное и вариативное питание<br>"
      "людей с психическими нарушениями в домах социального обслуживания",
      48, 200, 864, 18, serif=True, italic=True, color=SOFT) +
    box(48, 300, 420, 160) + box(492, 300, 420, 160, "warm") +
    t("Евгений Чистяков", 68, 320, 380, 20, serif=True, bold=True) +
    t("директор СПб ГАСУСОН «ДСО „Серафимовский“» · 223-ФЗ", 68, 356, 380, 14, color=SOFT) +
    t("Тимур Нурбаев", 512, 320, 380, 20, serif=True, bold=True) +
    t("директор СПб ГБСУСОН «ДСО „Тесовый берег“» · 44-ФЗ", 512, 356, 380, 14, color=SOFT)))

# 2
dims = [("01", "Безопасность", "текстуры, лекарства, риск аспирации"),
        ("02", "Достоинство", "уважение к жителю, имя на тарелке"),
        ("03", "Предпочтение", "свой голос — словом, жестом, биографией"),
        ("04", "Возможности кухни", "что реально приготовить сегодня"),
        ("05", "Документ проверки", "журнал, карта, согласование")]
body = k("Конфликт за одним столом") + h("За одним обедом — пять вещей одновременно", 28, 68)
for i, (n, title, desc) in enumerate(dims):
    x = 48 + (i % 5) * 180
    body += box(x, 200, 168, 220)
    body += t(n, x + 12, 216, 140, 22, serif=True, bold=True, color=ACCENT)
    body += t(title, x + 12, 260, 144, 15, bold=True)
    body += t(desc, x + 12, 300, 144, 13, color=SOFT)
add(page(2, body))

# 3
add(page(3,
    k("Почему кухня не выбирает") +
    h("Дисфагия встречается часто.", 30, 68) +
    t("Именно поэтому текстуру назначает врач, а не повар.", 48, 118, 864, 18, serif=True, italic=True, color=SOFT) +
    t("21,9–69,5 %", 48, 180, 500, 56, serif=True, bold=True, color=ACCENT) +
    t("в отдельных изученных клинических группах", 48, 260, 500, 16, color=SOFT) +
    box(560, 180, 352, 220, "warm") +
    t("ОГОВОРКА", 580, 200, 312, 12, bold=True, color=ACCENT) +
    t("Переносить этот диапазон на все российские ДСО нельзя. Это не аудит Минтруда.",
      580, 230, 312, 16)))

# 4
add(page(4,
    k("Масштаб повседневности") +
    h("Самые частые решения, которые дом принимает за жителя", 26, 68) +
    t("2 190", 48, 160, 500, 88, serif=True, bold=True, color=ACCENT) +
    t("приёмов пищи в год за одного человека · 6 × 365 · Серафимовский",
      48, 280, 700, 16, color=SOFT) +
    t("завтрак · 2-й завтрак · обед · полдник · ужин · вечерний",
      48, 340, 800, 16)))

# 5
add(page(5,
    k("Контекст · недееспособность") +
    h("Порядка трёх из четырёх — недееспособны.", 28, 68) +
    t("74 %", 48, 150, 280, 80, serif=True, bold=True, color=ACCENT) +
    box(360, 160, 552, 200) +
    t("Сделки совершает опекун (ст. 29 ГК). Повседневное предпочтение — мнение, его обязаны выяснять. Кто не говорит — показ, наблюдение, биография.",
      380, 180, 512, 16) +
    t("Расчёт проекта «Если быть точным», данные за 2024 г. · не статотчётность Минтруда · в вашем доме цифра будет другой.",
      48, 420, 864, 14, italic=True, color=SOFT)))

# 6
add(page(6,
    k("Физиология · ужин → завтрак") +
    h("Ужин 17:30 → завтрак 8:30 = 15 часов без еды", 26, 68) +
    t("Цель нашего дома — не больше 13 часов.", 48, 118, 864, 18, serif=True, italic=True, color=SOFT) +
    box(48, 200, 420, 200) + box(492, 200, 420, 200, "warm") +
    t("ОРИЕНТИРЫ", 68, 220, 380, 12, bold=True, color=ACCENT) +
    t("≤ 11 ч — Швеция<br>≤ 13 ч — цель нашего дома<br>≤ 14 ч — потолок CMS (США), не среднее РФ",
      68, 250, 380, 15) +
    t("ОГОВОРКА", 512, 220, 380, 12, bold=True, color=ACCENT) +
    t("15 ч — арифметика одного расписания, не статистика по российским ДСО. Швеция/США — другие системы.",
      512, 250, 380, 15)))

# 7
items7 = [("①", "Положение", "о питании, с учётом вариативности"),
          ("②", "Меню", "с вариантами и парами эквивалентов"),
          ("③", "Журнал заказа", "что заказал, кто принял"),
          ("④", "Журнал замен", "когда варианта не оказалось"),
          ("⑤", "Пищевые карты", "профиль, текстура, исключения"),
          ("⑥", "Согласование", "с учредителем")]
body = k("Право · не лозунг, а папка") + h("Проверяющему нужна не фраза «запрета нет».", 26, 64)
body += t("А положение, журнал, карты, согласование с учредителем.", 48, 110, 864, 16, serif=True, italic=True, color=SOFT)
body += box(48, 160, 864, 250)
for i, (n, title, desc) in enumerate(items7):
    x = 64 + (i % 3) * 280
    y = 180 + (i // 3) * 110
    body += t(n, x, y, 40, 22, serif=True, bold=True, color=ACCENT)
    body += t(title, x + 40, y, 220, 16, bold=True)
    body += t(desc, x + 40, y + 28, 220, 13, color=SOFT)
body += t("Федеральное право не запрещает и не обязывает — закрепить локально. 442-ФЗ ст. 9, 16, 32 ч. 4 · 3185-1 ст. 5 ч. 2; ст. 37, 43 · ГК ст. 29",
          48, 430, 864, 13, color=SOFT)
add(page(7, body))

# 8
add(page(8,
    k("Российская практика") +
    h("Иркутская область масштабирует выбор на регион.", 26, 68) +
    t("Не один эксперимент — контур для учредителя.", 48, 118, 864, 16, serif=True, italic=True, color=SOFT) +
    box(48, 180, 420, 240) + box(492, 180, 420, 240, "warm") +
    t("ЧТО СДЕЛАНО", 68, 200, 380, 12, bold=True, color=ACCENT) +
    t("Два первых · два вторых · два гарнира. Публикация 14.02.2025.", 68, 236, 380, 16) +
    t("ДЛЯ ДИРЕКТОРА", 512, 200, 380, 12, bold=True, color=ACCENT) +
    t("Масштаб области как аудит не подтверждён. Показано как контур, не как результат. Внедрено публично ≠ доказанный эффект.",
      512, 236, 380, 15)))

# 9
add(page(9,
    k("Кейс · наш дом") +
    h("Житель заказывает ужин накануне.", 30, 68) +
    t("К вечеру известно, что готовить. Старт не был бесплатным — оборудование и ставки пищеблока.",
      48, 130, 864, 16, serif=True, italic=True, color=SOFT) +
    t("Источник S030 · gov.spb.ru, 22.07.2025 · СПб ГАСУСОН «ДСО „Серафимовский“». Кейс — практика, не доказательство эффекта.",
      48, 400, 864, 14, italic=True, color=SOFT)))

# 10 — P0: no live pni9.ru
add(page(10,
    k("Локальный норматив") +
    h("Приказ № 124 от 10.03.2026", 36, 64) +
    t("Заказное питание вошло в правила внутреннего распорядка жителей ДСО «Серафимовский».",
      48, 120, 864, 16, serif=True, italic=True, color=SOFT) +
    box(48, 180, 420, 220) + box(492, 180, 420, 220, "warm") +
    t("ЧТО ЗАКРЕПЛЕНО", 68, 200, 380, 12, bold=True, color=ACCENT) +
    t("Вариативное меню как часть правил дома, включая маломобильных: приём в жилых комнатах, помощь в кормлении.",
      68, 236, 380, 15) +
    t("ПОЧЕМУ ОПОРА", 512, 200, 380, 12, bold=True, color=ACCENT) +
    t("Локальный акт одного учреждения, не федеральная норма. Проверяющему — документ, не слова.",
      512, 236, 380, 15) +
    t("S035 · архив правил web.archive.org/web/20260415001233 · pni9.ru с 21.08.2026 не работает",
      48, 430, 864, 13, color=SOFT)))

# 11
add(page(11,
    k("Закупки") +
    h("Один учредитель — две разные закупки.", 28, 68) +
    t("Вариативность не от номера закона.", 48, 118, 864, 16, serif=True, italic=True, color=SOFT) +
    box(48, 180, 420, 240) + box(492, 180, 420, 240, "warm") +
    t("СЕРАФИМОВСКИЙ · 223-ФЗ", 68, 200, 380, 14, bold=True, color=ACCENT) +
    t("ГАСУСОН · автономное · конкурсная основа", 68, 236, 380, 16) +
    t("ТЕСОВЫЙ БЕРЕГ · 44-ФЗ", 512, 200, 380, 14, bold=True, color=ACCENT) +
    t("ГБСУСОН · бюджетное · ИНН 7827661874 (ЕГРЮЛ)", 512, 236, 380, 16)))

# 12 — SanPiN not yet in force
add(page(12,
    k("Сначала рамка") +
    h("Сначала медицинская рамка. Потом выбор.", 28, 68) +
    t("Кухня исполняет назначение, а не ставит его.", 48, 118, 864, 16, serif=True, italic=True, color=SOFT) +
    box(48, 180, 864, 100) +
    t("РЕШАЕТ ВРАЧ · текстура, стол, противопоказания, лекарственно-пищевые исключения. Приказы 330н, 395н; СанПиН 4282-26 п. 56(11) — с 01.09.2026, на 26.08 ещё не в силе.",
      68, 196, 824, 15) +
    box(48, 300, 864, 100, "warm") +
    t("РЕШАЕТ УЧРЕЖДЕНИЕ · сколько вариантов, где фиксируется, что делает смена, когда вариант кончился.",
      68, 316, 824, 15)))

# 13
add(page(13,
    k("Модель решения") +
    h("Врач задаёт рамку. Внутри — пары эквивалентов.", 26, 68) +
    "".join(
        box(48 + i * 225, 180, 210, 200) +
        t(["① Мед. рамка", "② Пары", "③ Выбор", "④ Фиксация"][i], 64 + i * 225, 200, 180, 16, bold=True) +
        t(["текстура, стол", "гречка/рис", "показ, слово", "журнал смены"][i], 64 + i * 225, 250, 180, 14, color=SOFT)
        for i in range(4)
    ) +
    t("Стандартный вариант гарантирован всегда. Человек вправе не выбирать.",
      48, 420, 864, 15, italic=True, color=SOFT)))

# 14
add(page(14,
    k("Выбор не требует дееспособности") +
    h("Четыре канала выражения воли.", 28, 68) +
    "".join(
        box(48 + i * 225, 160, 210, 200) +
        t(["Показ", "Наблюдение", "Биография", "Сведения"][i], 64 + i * 225, 180, 180, 16, bold=True) +
        t(["две порции", "тарелка как сигнал", "что ел всю жизнь", "кто знает человека"][i],
          64 + i * 225, 220, 180, 14, color=SOFT)
        for i in range(4)
    ) +
    t("Наблюдение — сигнал, не автоматическое согласие. Решение документируется. IDDSI — терминология; текстуру назначает врач.",
      48, 400, 864, 14, italic=True, color=SOFT)))

# 15
add(page(15,
    k("Что сделать в понедельник") +
    h("Пилот на 90 дней. Одно отделение.", 28, 68) +
    "".join(
        box(48 + i * 180, 160, 168, 180) +
        t(["Замер", "Приказ", "Обучение", "Пилот", "Масштаб"][i], 60 + i * 180, 180, 144, 15, bold=True) +
        t(["7 дней", "одна строка", "15 минут", "90 дней", "письмо учредителю"][i],
          60 + i * 180, 220, 144, 13, color=SOFT)
        for i in range(5)
    ) +
    t("Процент выбравших — не KPI. Пять чисел: карта, реальный выбор, исполненные заказы, отказы/замены/отходы, события риска.",
      48, 380, 864, 14, color=SOFT)))

# 16
add(page(16,
    k("Красные линии") +
    h("Три ошибки дороже бездействия.", 28, 68) +
    "".join(
        box(48 + i * 300, 160, 284, 260, "warm" if i == 2 else "card") +
        t(["Имитация выбора", "Выбор без гарантии", "«Лечебность» руками кухни"][i],
          64 + i * 300, 180, 252, 16, bold=True) +
        t(["Одно блюдо на линии.", "Выбрал Б — Б кончилось.", "Повар назначает диету."][i],
          64 + i * 300, 240, 252, 14, color=SOFT)
        for i in range(3)
    )))

# 17
add(page(17,
    k("Новый санитарный контекст") +
    h("Через шесть дней после нашей встречи", 26, 64) +
    t("01.09.2026", 48, 130, 500, 56, serif=True, bold=True, color=ACCENT) +
    t("вступает СанПиН 2.3/2.4.4282-26. На 26.08 он ещё не в силе — действует 3590-20.",
      48, 210, 864, 16) +
    t("п. 56(11) — не менее трёх приёмов, в т. ч. диетическое по показаниям. Число вариантов блюда не ограничено. Журналы августа задним числом не переписывать.",
      48, 270, 864, 16, color=SOFT)))

# 18
add(page(18,
    k("Пилот", ) +
    h("90 дней", 64, 80, color=ACCENT) +
    t("одно отделение · одна неделя замера", 48, 180, 864, 20, serif=True, italic=True, color=SOFT) +
    t("Измерить → проверить → скорректировать → решить о масштабе", 48, 280, 864, 20, serif=True, bold=True) +
    t("Не внедряйте вслепую. Измеряйте.", 48, 360, 864, 22, serif=True, italic=True, color=ACCENT),
    bg=DARK, foot="18"))
# fix foot color on dark - page() already handles bg

# 19 separator
add(page("—",
    k("Резерв · не показывать в основном ходе") +
    h("Основной показ закончен.", 32, 80) +
    t("R1 разогрев · R2 три конфликта · R3 Успенский М2 · R4 Болотнинский М1 · R5 Усть-Илимск · R6 Серафимовский · R7 IDDSI · R8 право · R9 карта · R10 журнал · R11 закупки · R12 показатели",
      48, 180, 864, 16) +
    t("На 90 минут достаточно слайдов 1–18.", 48, 320, 864, 16, italic=True, color=SOFT),
    foot="—"))

# R1–R12
add(page("R1", k("Разогрев") + h("Вспомните вчерашний ужин.", 28, 80) +
         t("Поднимите руку, если хоть один житель мог выбрать второе блюдо. Рука, которая не поднимается, — повестка 90 минут.",
           48, 180, 864, 18), foot="R1"))
add(page("R2", k("Три конфликта программы") +
         t("Выбор ↔ безопасность · вариативность ↔ норматив · единое меню ↔ индивидуальная поддержка. Шесть вопросов программы внутри этих трёх.",
           48, 100, 864, 18), foot="R2"))
add(page("R3", k("Модель М2 · Успенский ПНИ") +
         h("Два первых, два вторых, два салата, два напитка — ежедневно.", 24, 80) +
         t("Не шведская линия. Буфет — ДДСОЛ, S019. Источник S016.", 48, 200, 864, 16, color=SOFT),
         foot="R3"))
add(page("R4", k("Модель М1 · Болотнинский ПНИ") +
         h("Выбор на завтрак и обед, несколько раз в неделю.", 24, 80) +
         t("Перечень определяет диетсестра. Источник S015. Не путать с Успенским.", 48, 200, 864, 16, color=SOFT),
         foot="R4"))
add(page("R5", k("Усть-Илимский ДСО") +
         t("Публикация 27.09.2024. Не аудит эффекта. Источник S017.", 48, 100, 864, 18), foot="R5"))
add(page("R6", k("Подробно · Серафимовский") +
         t("S030 — gov.spb.ru, 22.07.2025. Старт не бесплатный. 223-ФЗ. Кейс, не доказанный эффект.",
           48, 100, 864, 18), foot="R6"))
add(page("R7", k("IDDSI") +
         h("Язык описания текстур, не диагноз.", 28, 80) +
         t("Восемь уровней 0–7. Текстуру назначает врач. Кухня исполняет. Русского официального перевода на 22.08.2026 нет.",
           48, 180, 864, 16, color=SOFT), foot="R7"))
add(page("R8", k("Правовая цепочка") +
         t("3185-1 ст. 5 ч. 2 — гуманное отношение (не ст. 37 ч. 2). Ст. 37 и 43 — права и статус проживающих.<br>"
           "442-ФЗ ст. 9, 16, 32 ч. 4 — 75 % потолок платы, не право на ежедневный выбор блюда.<br>"
           "ГК ст. 29 — опекун и мнение.<br>"
           "СанПиН 4282-26 п. 56(11) — с 01.09.2026; на 26.08 ещё 3590-20.",
           48, 100, 864, 17), foot="R8"))
add(page("R9", k("Пищевая карта") +
         t("Профиль · текстура (врач) · исключения · предпочтения · способ фиксации. Подпись врача обязательна. Шаблон — проект, не норматив.",
           48, 100, 864, 18), foot="R9"))
add(page("R10", k("Журнал выбора") +
         t("Дата · отделение · житель · заказал · получил · подпись смены. Не выбрал — стандартный вариант. Без давления.",
           48, 100, 864, 18), foot="R10"))
add(page("R11", k("Закупочная модель") +
         t("Серафимовский — 223-ФЗ. Тесовый берег — 44-ФЗ, ИНН 7827661874. В обоих случаях: положение, журнал, согласование с учредителем.",
           48, 100, 864, 18), foot="R11"))
add(page("R12", k("Пять показателей") +
         t("Карта · доля приёмов с реальным выбором · исполненные заказы · отказы/замены/отходы · события риска. Процент выбравших — не KPI.",
           48, 100, 864, 18), foot="R12"))


def main():
    if not os.path.isdir(V5_FONTS):
        raise SystemExit(f"Нет шрифтов v5: {V5_FONTS}")
    os.makedirs(HTML_DIR, exist_ok=True)
    fonts_dst = os.path.join(HTML_DIR, "fonts")
    if os.path.isdir(fonts_dst):
        shutil.rmtree(fonts_dst)
    shutil.copytree(V5_FONTS, fonts_dst)
    for old in glob.glob(os.path.join(HTML_DIR, "slide-*.html")):
        os.remove(old)
    for i, html in enumerate(OUT, 1):
        open(os.path.join(HTML_DIR, f"slide-{i:02d}.html"), "w", encoding="utf-8").write(html)
    print(len(OUT), "html slides")

    os.makedirs(PDF_DIR, exist_ok=True)
    for old in glob.glob(os.path.join(PDF_DIR, "p*.pdf")):
        os.remove(old)
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env["PATH"] = "/opt/homebrew/bin:" + env.get("PATH", "")
    for i in range(1, len(OUT) + 1):
        src = os.path.join(HTML_DIR, f"slide-{i:02d}.html")
        dst = os.path.join(PDF_DIR, f"p{i:02d}.pdf")
        r = subprocess.run(["weasyprint", src, dst], env=env, capture_output=True, text=True)
        if r.returncode != 0:
            sys.stderr.write(r.stderr or r.stdout or "weasyprint failed\n")
            raise SystemExit(f"weasyprint failed on slide {i}")
    pages = sorted(glob.glob(os.path.join(PDF_DIR, "p*.pdf")))
    dest = os.path.join(ROOT, "Презентация_v6_Не_просто_накормить.pdf")
    dest18 = os.path.join(ROOT, "Презентация_v6_Не_просто_накормить_без_резерва.pdf")
    subprocess.run(["pdfunite", *pages, dest], check=True, env=env)
    subprocess.run(["pdfunite", *pages[:18], dest18], check=True, env=env)
    print(f"PDF {len(pages)} стр. → {dest}")
    print(f"PDF 18 стр. → {dest18}")


if __name__ == "__main__":
    main()
