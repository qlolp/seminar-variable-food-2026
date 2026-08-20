# -*- coding: utf-8 -*-
"""Сборка доклада: MD (с {{Sxxx}}/{{M-key}}/{{I-key}} + [[FIG:key]]) → HTML (TNR 14/1.5) → PDF + DOCX."""
import os, re, glob, json, subprocess, sys, openpyxl

BASE = 'C:/Users/Evgenii/AppData/Local/Temp/seminar-food/проект'
OUT  = os.path.join(BASE, 'output')
os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.join(BASE, 'scripts'))
from figures_html import CSS as FIGCSS, FIG
import figures_html2, figures_inf
FIG.update(figures_html2.FIG)
INF = figures_inf.INF

# ---------- 1. Реестры → база цитирования ----------
def load_reg(path, sheet=0):
    wb = openpyxl.load_workbook(path)
    ws = wb[wb.sheetnames[sheet]]
    hdr = [c.value for c in ws[1]]
    d = {}
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r[0]:
            continue
        row = dict(zip(hdr, r))
        d[row['ID']] = row
    return d

REGS = load_reg(f'{BASE}/SOURCE_REGISTRY.xlsx')
REGM = load_reg(f'{BASE}/MEDICAL_EVIDENCE.xlsx')
REGI = load_reg(f'{BASE}/INTERNATIONAL_PRACTICES.xlsx')

def cite_text(cid):
    if cid in REGS:
        r = REGS[cid]
        url = r.get('URL') or ''
        return f"[{cid}] {r.get('Источник (наименование)','')}. {url} (проверено: {r.get('Дата проверки','')})"
    if cid in REGM:
        r = REGM[cid]
        url = r.get('URL') or ''
        return f"[{cid}] {r.get('Источник','')} ({r.get('Орган/автор, год','')}). {url}"
    if cid in REGI:
        r = REGI[cid]
        url = r.get('URL') or ''
        return f"[{cid}] {r.get('Источник','')} — {r.get('Юрисдикция/орган','')}. {url}"
    return None

# ---------- 2. Сборка маркдауна ----------
FIG_AFTER = {  # файл главы → список фигур после неё
 '05_odin_obed':['f1_obed'],'08_lestnica':['f4_lestnica'],'10_disfagiya':['f9_disf','d10_disf_prev'],
 '11_lekarstva':['f10_ogran','d7_kloz'],'12_otkaz':['f8_otkaz'],'13_giperfagiya':['d4_ves'],
 '14_pika':['f21_heat'],'15_neverbalny':['f6_put'],'16_deesposobnost':['f7_tri','f5_matrica'],
 '19_dva_varianta':['f18_derevo1'],'21_vybor_izmenilsya':['f15_fiktiv'],'22_audit':['f20_dash'],
 '23_geografiya':['f2_karta','f3_tipy'],'26_mejdunarodny':['d6_noch'],
 '27_issledovaniya':['d8_nijs','d9_triggery'],'28_personal':['f11_roli'],
 '29_finansy':['f12_stoimost','f13_modeli','d5_syrie'],'31_dokumenty':['f19_derevo2'],
 '33_otvetstvennost':['f14_riski'],'35_pilot90':['f16_pilot'],'36_dorozhnaya_karta':['f17_karta12'],
}

parts = []
for f in sorted(glob.glob(f'{BASE}/chapters/*.md')):
    name = os.path.basename(f)[:-3]
    txt = open(f, encoding='utf-8').read()
    parts.append(txt)
    for fig in FIG_AFTER.get(name, []):
        parts.append(f'\n[[FIG:{fig}]]\n')

# кейсы
parts.append('''\n# Часть II. Учебные кейсы (22 разбора)

Двадцать два ситуационных разбора переводят материал разделов в плоскость ежедневных решений: что нельзя делать, что сделать немедленно, кто принимает решение, какие документы нужны, каково долгосрочное решение и где граница вывода. Все кейсы — учебные, составленные для анализа; они не описывают конкретные организации и людей. Формат разбора на семинаре: 15 минут на кейс по восьми пунктам структуры.''')
for f in sorted(glob.glob(f'{BASE}/cases/*.md')):
    parts.append(open(f, encoding='utf-8').read())

# приложения
parts.append('''\n# Часть III. Приложения: проекты локальных форм (45 шаблонов)

Сорок пять шаблонов — рабочий инструментарий доклада: чек-листы, формы, журналы, алгоритмы, проекты приказов и положений. Каждый шаблон снабжён дисклеймером: это проект локальной формы, не нормативно установленный документ; он требует адаптации под региональное законодательство, учётную политику, структуру учреждения, медицинскую лицензию и требования учредителя. Порядок внедрения комплекта — раздел 36 и конец части III.''')
for f in sorted(glob.glob(f'{BASE}/appendices/*.md')):
    parts.append(open(f, encoding='utf-8').read())

# инфографики
parts.append('''\n# Часть IV. Одностраничные инфографики (для печати и раздатки)

Десять одностраничных материалов для печати: плакаты для поста и столовой, памятки для инструктажей, раздатка для совета жителей и семинара. Каждая страница самодостаточна и может копироваться отдельно от доклада; источники данных указаны на самих страницах либо в разделах, на которые инфографика ссылается.''')
for k in sorted(INF):
    parts.append(f'\n[[INF:{k}]]\n')

# библиография вставлена в раздел 44 по маркеру [[SOURCES]]

full_md = '\n\n'.join(parts)

# ---------- 3. Нумерация цитирований ----------
order, cmap = [], {}
def repl(m):
    cid = m.group(1)
    if cid not in cmap:
        cmap[cid] = len(cmap) + 1
        order.append(cid)
    return f'<sup>{cmap[cid]}</sup>'

full_md = re.sub(r'\{\{([SM]-?[A-Za-z0-9_]+|I-[A-Za-z0-9_]+)\}\}', repl, full_md)

# источники: нумерованный список
src_items, missing = [], []
for i, cid in enumerate(order, 1):
    t = cite_text(cid)
    if t:
        src_items.append(f'{i}. {t}')
    else:
        missing.append(cid)
src_html = '\n'.join(f'<p class="srcitem">{s}</p>' for s in src_items)
if missing:
    print('!!! НЕ НАЙДЕНЫ В РЕЕСТРАХ:', missing)

def _esc(x):
    m2 = re.match(r'(\d+)\. (.*)', x, re.S)
    return (f'<p><b>{m2.group(1)}.</b> {m2.group(2)}</p>' if m2 else f'<p>{x}</p>')

src_block = ('\n<div class="srclist"><p class="srchead">Источники приведены в порядке первого упоминания в тексте. '
             'Полные машиночитаемые реестры — контрольные файлы SOURCE_REGISTRY.xlsx, MEDICAL_EVIDENCE.xlsx, '
             'INTERNATIONAL_PRACTICES.xlsx (канон: папка проект/).</p>'
             + ''.join(_esc(x) for x in src_items) + '</div>\n')
if '[[SOURCES]]' not in full_md:
    raise SystemExit('маркер [[SOURCES]] не найден в тексте доклада')
full_md = full_md.replace('[[SOURCES]]', src_block)

# сохранить маркдаун для DOCX-конвертера и матрицу цитирований
open(f'{OUT}/_report_full.md', 'w', encoding='utf-8').write(full_md)
jsonl = []
for i, cid in enumerate(order, 1):
    if cid in REGS:
        r = REGS[cid]; page = {'site_name': r.get('Источник (наименование)', '')}
        url = r.get('URL', '')
    elif cid in REGM:
        r = REGM[cid]; page = {'site_name': f"{r.get('Источник','')} ({r.get('Орган/автор, год','')})"}
        url = r.get('URL', '')
    else:
        r = REGI[cid]; page = {'site_name': f"{r.get('Источник','')} — {r.get('Юрисдикция/орган','')}"}
        url = r.get('URL', '')
    jsonl.append({'citation_number': i, 'url': url, 'page': page})
with open(f'{OUT}/_citations.jsonl', 'w', encoding='utf-8') as fh:
    for j in jsonl:
        fh.write(json.dumps(j, ensure_ascii=False) + '\n')
print(f'Цитирований: {len(order)}; недостающих: {len(missing)}')
print('build_md done')
