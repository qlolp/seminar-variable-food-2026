# -*- coding: utf-8 -*-
import subprocess, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

r = r'C:\Users\Evgenii\OneDrive\Документы\DSeek\repo-svf'
# (repo-relative path, origin path) — брать версию origin/main
take_origin = [
    'README.md',
    'ПРОЧТИ_МЕНЯ.md',
    '02_презентация/презентация_34_слайда/pages/01_cover.page',
    'проект/seminar_package/03_презентация/pages/01_cover.page',
    'проект/seminar_package/03_презентация/pages/37_final.page',
    '01_доклад/Не_просто_накормить_доклад.html',
    '01_доклад/Не_просто_накормить_доклад.md',
    '01_доклад/Не_просто_накормить_доклад_официальный.pdf',
    '01_доклад/Не_просто_накормить_доклад_журнальный.pdf',
    '01_доклад/Не_просто_накормить_доклад_красивая_версия.pdf',
    'проект/output/toc_pages.json',
    'проект/output/toc_pages_color.json',
    'проект/output/Не_просто_накормить_доклад.pdf',
    'проект/output/Не_просто_накормить_доклад_журнальный.pdf',
    'проект/output/Не_просто_накормить_доклад_красивая_версия.pdf',
    'проект/output/_report.pdf',
    'проект/output/_report_color.pdf',
    'проект/output/_report_beautiful.pdf',
]
for p in take_origin:
    out = subprocess.run(['git', '-C', r, 'show', 'origin/main:' + p],
                         capture_output=True)
    if out.returncode != 0:
        print('FAIL', p, out.stderr.decode('utf-8', 'replace')[:120])
        continue
    with open(r + '\\' + p.replace('/', '\\'), 'wb') as f:
        f.write(out.stdout)
    print('ok', p)
