#!/usr/bin/env python3
"""Сборка второй редакции в HTML и PDF.

  python3 doklad-v2/build/build.py full    -> ne-prosto-nakormit-v2.md + Не_просто_накормить_v2.pdf
  python3 doklad-v2/build/build.py short   -> Не_просто_накормить_краткая_версия.pdf

Маркеры {{KEY}} превращаются в затекстовые ссылки [n] (нумерация по первому
упоминанию), раздел 44 — в нумерованный список литературы по ГОСТ Р 7.0.100-2018
(doklad-v2/bibliografiya_gost.tsv; при отсутствии записи берётся строка из таблиц раздела 44).
Нужны pandoc и Playwright Chromium (/opt/node-tools/node_modules/playwright).
"""
import glob, html, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DOC = os.path.dirname(HERE)
MARK = re.compile(r'((?:\{\{[^}]+\}\})+)')
KEY = re.compile(r'\{\{([^}]+)\}\}')
PARTS = {
    '05': 'Сцена, терминология, лестница моделей', '09': 'Клиника за столом',
    '15': 'Право и санитария', '19': 'Меню, раздача, замер', '23': 'Контекст',
    '28': 'Люди и деньги', '31': 'Документы, риски, стратегия',
}


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def part(num, title, rng):
    return (f'\n<section class="part"><div class="part-num">Часть {num}</div>'
            f'<div class="part-title">{title}</div><div class="part-range">{rng}</div></section>\n\n')


def bib_sources():
    """KEY -> запись: сначала таблицы раздела 44, поверх — ГОСТ-файл."""
    bib = {}
    for line in read(os.path.join(DOC, '44_bibliografiya.md')).splitlines():
        m = re.match(r'\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*([^|]*?)\s*\|', line)
        if m and m.group(1) not in bib:
            what, url = m.group(2), m.group(3)
            bib[m.group(1)] = what.rstrip('.') + '.' + (f' – URL: {url}' if url.startswith('http') else '')
    gost = os.path.join(DOC, 'bibliografiya_gost.tsv')
    if os.path.exists(gost):
        for line in read(gost).splitlines():
            if '\t' in line:
                k, v = line.split('\t', 1)
                if v.strip():
                    bib[k.strip()] = v.strip()
    return bib


def corrections():
    t = read(os.path.join(DOC, '44_bibliografiya.md'))
    m = re.search(r'## Исправления к записям первой редакции\n(.*?)\n## ', t, re.S)
    return m.group(1).strip() if m else ''


def number_refs(md, order):
    def repl(m):
        nums = []
        for k in KEY.findall(m.group(1)):
            k = k.strip()
            if k not in order:
                order[k] = len(order) + 1
            nums.append(order[k])
        links = ', '.join(f'<a href="#ref-{n}">{n}</a>' for n in sorted(set(nums)))
        return f'<span class="ref">[{links}]</span>'
    return MARK.sub(repl, md)


def bibliography(order, bib, title, intro, with_corr):
    out = [f'# {title}\n', intro, '\n<ol class="biblio">']
    for k, n in sorted(order.items(), key=lambda x: x[1]):
        text = bib.get(k, f'Источник {k} (запись не найдена).')
        text = html.escape(text, quote=False)
        text = re.sub(r'(https?://[^\s<]+?)([.,;)]?)(?=\s|$)', r'<a href="\1">\1</a>\2', text)
        out.append(f'<li id="ref-{n}">{text}</li>')
    out.append('</ol>\n')
    if with_corr:
        corr = corrections()
        corr = re.sub(r'`([^`]+)`', lambda m: f'[{order[m.group(1)]}]' if m.group(1) in order else m.group(1), corr)
        out += ['## Исправления к записям первой редакции\n',
                'Номер в квадратных скобках — номер источника в списке выше.\n', corr, '']
    return '\n'.join(out)


def full_md():
    chapters = sorted(glob.glob(os.path.join(DOC, '[0-4][0-9]_*.md')))
    parts_n = 1
    body = []
    for f in chapters:
        name = os.path.basename(f)
        nn = name[:2]
        if nn in ('01', '44'):
            continue
        t = read(f).strip()
        t = re.sub(r'^### Блок I\.\d+\..*\n+', '', t, flags=re.M)
        if nn in PARTS:
            parts_n += 1
            rng = re.search(r'\(([\d–]+)\)', [l for l in read(f).splitlines() if l.startswith('### Блок')][0]).group(1)
            body.append(part(parts_n, PARTS[nn], 'разделы ' + rng))
        if nn == '02':
            body.append(part(1, 'Вступление и резюме', 'разделы 1–4'))
        body.append(t + '\n')
    body.append(part(parts_n + 1, 'Учебные кейсы', 'двадцать два кейса для разбора'))
    body += [read(f).strip() + '\n' for f in sorted(glob.glob(os.path.join(DOC, 'кейсы', '*.md')))]
    body.append(part(parts_n + 2, 'Приложения-шаблоны', 'приложения 1–45'))
    body += [read(f).strip() + '\n' for f in sorted(glob.glob(os.path.join(DOC, 'приложения', '*.md')))]
    return '\n'.join(body)


def verso():
    t = read(os.path.join(DOC, '01_titul.md'))
    t = t.split('## Как организовать', 1)[1].split('\n', 1)[1]
    return t.strip()


def cover(kind):
    sub = ('Как организовать безопасное, достойное и вариативное питание людей с психическими нарушениями '
           'в домах социального обслуживания')
    kicker = 'Методическое руководство · вторая редакция' if kind == 'full' else 'Краткая версия для руководителя'
    return f'''<section class="cover">
<div class="cover-band"><div class="cover-kicker">{kicker}</div>
<div class="cover-title">Не просто<br>накормить</div><p class="cover-sub">{sub}</p></div>
<div class="cover-plate"><span style="background:#1f6f6a"></span><span style="background:#d6ebe8"></span><span style="background:#c08a2d"></span><span style="background:#f5e9d2"></span><span style="background:#a63d32"></span></div>
<div class="cover-meta"><b>Евгений Владимирович Чистяков</b><br>директор СПб ГАСУСО «Дом социального обслуживания „Серафимовский“»<br><br>
По материалам межрегионального семинара-совещания «Пространство Новых Идей 2.0»,<br>Санкт-Петербург, 25–27 августа 2026 года</div>
<div class="cover-foot"><span>Санкт-Петербург · 2026</span><span>{"Вторая редакция, дополненная и переработанная" if kind == "full" else "Полный том — «Не просто накормить», вторая редакция"}</span></div>
</section>
'''


def post_html(h):
    h = re.sub(r'<h1 id="([^"]*)">(\d+)\.\s*', r'<h1 id="\1"><span class="chap-num">\2</span>', h)
    h = re.sub(r'<blockquote>\s*<p><strong>(Назначение|Правовая рамка|Методическая рамка|Как формулировать|Дата актуальности)',
               r'<blockquote class="accent"><p><strong>\1', h)
    h = re.sub(r'<blockquote>\s*<p><strong>(Клинический)', r'<blockquote class="clinic"><p><strong>\1', h)
    return h


def render(md, out_pdf, kind, title):
    tmp = tempfile.mkdtemp()
    src = os.path.join(tmp, 'build.md')
    with open(src, 'w', encoding='utf-8') as f:
        f.write(md)
    before = os.path.join(tmp, 'before.html')
    with open(before, 'w', encoding='utf-8') as f:
        f.write(cover(kind))
        if kind == 'full':
            v = subprocess.run(['pandoc', '-f', 'gfm', '-t', 'html5'], input=verso(), capture_output=True, text=True, check=True).stdout
            f.write(f'<section class="verso">{v}</section>\n')
    out_html = os.path.join(tmp, 'build.html')
    subprocess.run(['pandoc', src, '-f', 'gfm', '-t', 'html5', '-s', '--toc', '--toc-depth=1',
                    '--metadata', f'pagetitle={title}', '--metadata', 'lang=ru',
                    '-B', before, '-c', os.path.join(HERE, 'style.css'),
                    '--resource-path', f'{DOC}:{HERE}', '--embed-resources', '-o', out_html], check=True, cwd=DOC)
    h = post_html(read(out_html))
    with open(out_html, 'w', encoding='utf-8') as f:
        f.write(h)
    subprocess.run(['node', os.path.join(HERE, 'pdf.js'), out_html, out_pdf, title], check=True)
    return out_html


def main():
    kind = sys.argv[1] if len(sys.argv) > 1 else 'full'
    bib = bib_sources()
    order = {}
    if kind == 'full':
        md = full_md()
        with open(os.path.join(DOC, 'ne-prosto-nakormit-v2.md'), 'w', encoding='utf-8') as f:
            f.write('<!-- Сборка (doklad-v2/build/build.py): главы 02–43, кейсы, приложения. Не править вручную. -->\n\n'
                    + md + '\n\n' + read(os.path.join(DOC, '44_bibliografiya.md')))
        md = number_refs(md, order)
        md += '\n' + bibliography(
            order, bib, '44. Список литературы',
            'Источники пронумерованы в порядке первого упоминания; номер в квадратных скобках в тексте — номер позиции в этом списке. '
            'Записи оформлены по ГОСТ Р 7.0.100-2018; для иностранных источников после заглавия дан перевод на русский язык. '
            'Выписки с переводом ключевых фрагментов и отметки о том, что именно было прочитано, хранятся в реестрах `raw/sources/` репозитория доклада.',
            True)
        render(md, os.path.join(DOC, 'Не_просто_накормить_v2.pdf'), 'full', 'Не просто накормить. Вторая редакция')
    else:
        md = read(os.path.join(DOC, 'kratkaya-versiya.md'))
        md = re.sub(r'\A\s*# [^\n]*Краткая версия[^\n]*\n', '', md)
        md = number_refs(md, order)
        md += '\n' + bibliography(order, bib, 'Источники',
                                  'Нумерация — по первому упоминанию в этой версии. Полный список литературы — раздел 44 полного тома.', False)
        render(md, os.path.join(DOC, 'Не_просто_накормить_краткая_версия.pdf'), 'short',
               'Не просто накормить. Краткая версия для руководителя')
    missing = [k for k in order if k not in bib]
    print(f'{kind}: {len(order)} источников' + (f'; без записи: {missing}' if missing else ''))


if __name__ == '__main__':
    main()
