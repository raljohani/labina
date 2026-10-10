import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kufic import word, HARAKAT, HK_W, HK_H, HK_A, HK_O
U=10; G=1.5; R=0.6          # cell, mortar gap, corner radius
NIGHT='#0E1110'; GYP='#ECEDEA'; LAMP='#EDB230'
def cellsvg(cells,gold,ink,lamp,ox=0,oy=0):
    out=[]
    for (x,y) in sorted(cells|gold):
        f=lamp if (x,y) in gold else ink
        out.append(f'<rect x="{ox+x*U+G/2:.1f}" y="{oy+y*U+G/2:.1f}" width="{U-G:.1f}" height="{U-G:.1f}" rx="{R}" fill="{f}"/>')
    return ''.join(out)
MARK_C={(2,0),(2,1),(2,2),(0,2),(1,2)}; MARK_G={(0,0)}
def mark(ink=NIGHT,lamp=LAMP,bg=None,pad=0):
    s=3*U+2*pad
    b=f'<rect width="{s}" height="{s}" rx="{s*0.22:.1f}" fill="{bg}"/>' if bg else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s} {s}">{b}{cellsvg(MARK_C,MARK_G,ink,lamp,pad,pad)}</svg>'
VB=f'0 -{2*U} {13*U} {11*U}'   # the word's 13x7 cells plus room for the harakat above and below
def harakat(fill=None,cls=None):
    f=f'class="{cls}"' if cls else f'fill="{fill}" opacity="{HK_O}"'
    out=[]
    for cx,cy in HARAKAT:
        x,y=cx*U,(cy-1)*U; w,h=HK_W*U,HK_H*U
        out.append(f'<rect {f} x="{x-w/2:.1f}" y="{y-h/2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="1" transform="rotate({HK_A} {x:.1f} {y:.1f})"/>')
    return ''.join(out)
def wordmark(ink=NIGHT,lamp=LAMP):
    c,d=word()
    c={(x,y-1) for x,y in c}; d={(x,y-1) for x,y in d}   # rows 0..6
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}" role="img" aria-label="لَبِنَة">{cellsvg(c,d,ink,lamp)}{harakat(ink)}</svg>'
if __name__=='__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__))); os.makedirs('svg',exist_ok=True)
    files={'mark.svg':mark(),'mark-light.svg':mark(GYP),'mark-icon.svg':mark(GYP,LAMP,NIGHT,pad=7),
           'mark-icon-light.svg':mark(NIGHT,LAMP,GYP,pad=7),
           'wordmark.svg':wordmark(),'wordmark-light.svg':wordmark(GYP),
           'mark-mono.svg':mark(NIGHT,NIGHT),'wordmark-mono.svg':wordmark(NIGHT,NIGHT)}
    for n,s in files.items(): open('svg/'+n,'w').write(s)
    print(sorted(files))
