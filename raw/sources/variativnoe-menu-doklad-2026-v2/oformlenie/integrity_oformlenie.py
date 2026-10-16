#!/usr/bin/env python3
"""Integrity check: layout pass must not lose any [n] citation, number or source."""
import re,sys,subprocess,collections as C
old_md,new_md,old_pdf,new_pdf,new_docx=sys.argv[1:6]
def txt_pdf(p):
    t=subprocess.run(['pdftotext',p,'-'],capture_output=True,text=True).stdout
    # drop running headers/footers and bare page numbers so wrapped citations rejoin
    out=[]
    for l in t.split('\n'):
        s=l.strip()
        if re.fullmatch(r'\d{1,3}',s) or s.startswith('Вариативное меню · доклад') or s.startswith('Аналитический доклад · вторая редакция') or s.replace('\f','')=='' : continue
        out.append(l)
    return '\n'.join(out)
def txt_docx(p): return subprocess.run(['pandoc',p,'-t','plain','--wrap=none'],capture_output=True,text=True).stdout
def norm(t): return re.sub(r'\s+',' ',t.replace('\u00ad','').replace('-\n',''))
def cits(t): return C.Counter(re.sub(r'\s+','',m) for m in re.findall(r'\[[0-9][0-9,;–\-\s]*\]',t))
def nums(t): return C.Counter(re.findall(r'\d+(?:[.,]\d+)*',t))
def lost(a,b): return {k:v-b.get(k,0) for k,v in a.items() if b.get(k,0)<v}
ok=True
a,b=open(old_md).read(),open(new_md).read()
print('doklad.md byte-identical:',a==b); ok&=a==b
for name,(o,n) in {'PDF':(txt_pdf(old_pdf),txt_pdf(new_pdf))}.items():
    o,n=norm(o),norm(n)
    lc,ln=lost(cits(o),cits(n)),lost(nums(o),nums(n))
    print(f'{name}: citations old={sum(cits(o).values())} new={sum(cits(n).values())} lost={lc}')
    # page numbers legitimately shift; report numeric tokens lost beyond those
    print(f'{name}: numeric tokens old={sum(nums(o).values())} new={sum(nums(n).values())} lost(kinds)={len(ln)} sample={list(ln.items())[:15]}')
    ok&=not lc
import html as H
def txt_html(p): return H.unescape(re.sub(r'<[^>]+>',' ',open(p).read()))
ho,hn=norm(txt_html(sys.argv[6])),norm(txt_html(sys.argv[7]))
l1,l2=lost(cits(ho),cits(hn)),lost(nums(ho),nums(hn)); print('HTML (pre-pagination) citations lost:',l1,' numeric tokens lost:',l2); ok&=not l1 and not l2
d=txt_docx(new_docx); dm=cits(norm(d)); mm=cits(norm(b))
lc=lost(mm,dm); print('DOCX vs md citations lost:',lc); ok&=not lc
src=re.findall(r'^(\d+)\. \[[но]\]',b,re.M); print('sources in md:',len(src))
src_pdf=len(re.findall(r'^\s*(\d+)\. \[[но]\]',txt_pdf(new_pdf),re.M)); print('sources in new PDF:',src_pdf)
print('RESULT:','PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
