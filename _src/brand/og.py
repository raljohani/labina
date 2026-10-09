import asyncio,sys,base64,os
# Renders the 1200x630 share cards into _src/brand/out. Needs: pip install playwright && playwright install chromium,
# and the Arabic fonts as woff2 (npm pack @fontsource/noto-kufi-arabic @fontsource/noto-naskh-arabic, unpacked into FONTS_DIR).
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0,HERE)
from playwright.async_api import async_playwright
F=os.environ.get('FONTS_DIR', os.path.join(HERE,'fonts'))
css=''
for fam,d,ws in [('Noto Kufi Arabic','fontsource-noto-kufi-arabic-5.3.0',(500,700)),('Noto Naskh Arabic','fontsource-noto-naskh-arabic-5.3.0',(400,))]:
    slug=d.split('-5.')[0].replace('fontsource-','')
    for w in ws: css+=f"@font-face{{font-family:'{fam}';font-weight:{w};src:url('file://{F}/{d}/files/{slug}-arabic-{w}-normal.woff2')}}"
wl=open(os.path.join(HERE,'svg','wordmark-light.svg')).read()
def b64(p): return 'data:image/webp;base64,'+base64.b64encode(open(p,'rb').read()).decode()
A={'mizan':('ميزان','الصق رسالة البنك، واعرف كم تقدر تصرف اليوم.','#3FAF86','العمل ١'),
   'sana':('سنا','أسماء الله الحسنى: معناها وشواهدها ونصيبك منها.','#E2C27A','العمل ٢'),
   'midmak':('مدماك','دفتر بناء بيتك، من الحفر إلى المفتاح.','#E8865F','العمل ٣')}
base=f"<style>{css}*{{margin:0;box-sizing:border-box}}body{{width:1200px;height:630px;background:#0E1110;color:#ECEDEA;font-family:'Noto Naskh Arabic';position:relative;overflow:hidden}}</style>"
def app_html(k):
    n,t,c,no=A[k]
    return base+f'''<div style="position:absolute;inset:0;background:radial-gradient(ellipse 38% 70% at 22% 0,{c}44,transparent 70%)"></div>
<div style="position:absolute;left:110px;top:150px;width:290px;height:290px;border-radius:22.4%;overflow:hidden;box-shadow:0 40px 80px -30px #000,0 0 0 1px #ffffff1f"><img src="{b64(os.path.join(ROOT,'_src','assets',f'{k}-icon.webp'))}" style="width:100%;height:100%"></div>
<div dir="rtl" style="position:absolute;right:90px;top:150px;width:620px">
<div style="font-family:'Noto Kufi Arabic';font-size:26px;color:#A3ABA8">{no}، ٢٠٢٦</div>
<div style="font-family:'Noto Kufi Arabic';font-weight:700;font-size:120px;line-height:1.25;color:{c}">{n}</div>
<div style="font-size:36px;line-height:1.6;color:#ECEDEA">{t}</div></div>
<div style="position:absolute;right:90px;bottom:56px;display:flex;align-items:center;gap:22px;direction:ltr"><span style="font-family:-apple-system,Helvetica,Arial;font-size:24px;color:#A3ABA8">labina.app</span><div style="width:104px">{wl}</div></div>'''
home=base+f'''<div style="position:absolute;inset:0;background:radial-gradient(ellipse 40% 70% at 80% 0,#EDB23026,transparent 70%)"></div>
<div style="position:absolute;right:110px;top:64px;width:440px">{wl}</div>
<div dir="rtl" style="position:absolute;right:110px;bottom:90px;width:900px">
<div style="font-family:'Noto Kufi Arabic';font-weight:700;font-size:58px;line-height:1.35">كل تطبيق قطعة، وهذا معرضها.</div>
<div style="font-size:30px;color:#A3ABA8;margin-top:6px">معرض تطبيقات لبنة: ميزان، سنا، مدماك</div></div>
<div style="position:absolute;left:110px;bottom:96px;font-family:-apple-system,Helvetica,Arial;font-size:26px;color:#A3ABA8">labina.app</div>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1200,'height':630})
        for k,h in [('labina',home)]+[(k,app_html(k)) for k in A]:
            await pg.set_content('<!doctype html><html><head><meta charset="utf-8"></head><body>'+h+'</body></html>')
            await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            await pg.screenshot(path=os.path.join(HERE,'out',f'og-{k}.png'))
        await b.close()
asyncio.run(main())
