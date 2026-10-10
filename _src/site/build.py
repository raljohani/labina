#!/usr/bin/env python3
"""Builds the Labina gallery site.
usage (from the repo root):  python3 _src/site/build.py        → writes the site into the repo root
                              python3 _src/site/build.py OUT    → writes it elsewhere (preview)"""
import os, re, shutil, sys, json
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))            # the repo root
SRC = os.path.join(ROOT, '_src', 'content')              # the apps' original pages (privacy/support text source)
ASSETS = os.path.join(ROOT, '_src', 'assets')            # resized icons + screenshots (webp)
BRAND = os.path.join(ROOT, '_src', 'brand')              # logo generator, svg, share images
OUT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else ROOT
PRESS = os.path.join(OUT, 'press', 'files')              # full-res press files live in the site itself
DOMAIN = 'https://labina.app'
EMAIL = 'support@labina.app'
YEAR = '٢٠٢٦'
import hashlib
sys.path.insert(0, HERE)
from extra import *
VER = hashlib.md5(open(os.path.join(HERE,'style.css'),'rb').read()).hexdigest()[:8]
COUNTER = 'https://count.labina.app'
EULA = 'https://www.apple.com/legal/internet-services/itunes/dev/stdeula/'

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@500;600;700'
         '&family=Noto+Naskh+Arabic:wght@400;600;700&display=swap" rel="stylesheet">')

# the Labina identity: square-kufic wordmark + mark (see _src/brand)
sys.path.insert(0, BRAND)
import logo as _logo
from kufic import word as _word
def _cells(cells, gold, cls_ink='ink', cls_lamp='lamp'):
    U, G, R = _logo.U, _logo.G, _logo.R
    return ''.join(f'<rect class="{cls_lamp if p in gold else cls_ink}" x="{p[0]*U+G/2:.1f}" y="{p[1]*U+G/2:.1f}" width="{U-G:.1f}" height="{U-G:.1f}" rx="{R}"/>' for p in sorted(cells | gold))
MARK = (f'<svg class="mk" viewBox="0 0 30 30" aria-hidden="true">{_cells(_logo.MARK_C, _logo.MARK_G)}</svg>')
_wc, _wd = _word(); _wc = {(x, y-1) for x, y in _wc}; _wd = {(x, y-1) for x, y in _wd}
WORDMARK = f'<svg class="wm" viewBox="{_logo.VB}" role="img" aria-label="لَبِنَة">{_cells(_wc, _wd)}{_logo.harakat(cls="hk")}</svg>'
FAVICON = _logo.mark('#ECEDEA', '#EDB230', '#0E1110', pad=7)

APPS = {
 'mizan': dict(
   no='١', name='ميزان', latin='Mizan', year='٢٠٢٦',
   tag='الصق رسالة البنك، واعرف كم تقدر تصرف اليوم.',
   meta='تطبيق لآيفون وآيباد، وقريبًا على Google Play', play=None,
   store='https://apps.apple.com/app/id6808957329',
   about=['تطبيق ميزانية عربي. تلصق رسالة البنك فيسجّل المصروف بنفسه، ويقول لك كم تقدر تصرف اليوم.',],
   features=['يقرأ رسائل البنك وكشوف الحساب (PDF وCSV) وصور الفواتير على جهازك.',
             'تصحيحك لتصنيف تاجر يصير قاعدة، تراها وتعدّلها متى شئت.',
             'يتابع ميزانياتك وأهدافك والتزاماتك من أقساط وقروض وجمعيات، وزكاتك.',
             'اسأل دفترك كما تفكّر: «مطاعم هذا الشهر»، وصدّر ما تراه ملف إكسل.',
             'بياناتك المالية لا تغادر جهازك، ومزامنة iCloud اختيارية تذهب إلى حسابك أنت.'],
   shots=[('mizan-02-today','كم تقدر تصرف اليوم'),('mizan-01-sms','من رسالة البنك إلى مصروف'),
          ('mizan-04-budgets','سقوف الميزانية'),('mizan-07-zakat','الزكاة بالنصاب والحول'),('mizan-09-widgets','الودجتات')],
   phone=False, docs=['support','privacy','terms'], subs=True),
 'sana': dict(
   no='٢', name='سنا', latin='Sana', year='٢٠٢٦',
   tag='أسماء الله الحسنى: معناها وشواهدها ونصيبك منها.',
   meta='تطبيق لآيفون وآيباد وساعة Apple، وقريبًا على Google Play', play=None,
   store='https://apps.apple.com/app/id6812705355',
   about=['تطبيق لأسماء الله الحسنى يعرّفك بربك من خلال أسمائه: معنى كل اسم، وشواهده، ونصيبك منه عملًا في يومك.'],
   features=['سماء من الأسماء تتنقل فيها، وتتحول إلى قائمة مرتبة متى احتجت.',
             'سبحة تظهر في الجزيرة الديناميكية وشاشة القفل ومركز التحكّم، وتطبيق للساعة.',
             'تسع وتسعون لوحة بخط الثلث، وكل سطر منقول تحته عزوه، والآيات برسم مصحف المدينة.',
             'تذكير باسم اليوم، وأدوات للشاشة الرئيسية وشاشة القفل.',
             'يعمل كاملًا دون إنترنت، ولا يجمع عنك أي بيانات.'],
   shots=[('sana-01-sky','سماء الأسماء'),('sana-03-name','الاسم يُكتب أمامك'),('sana-05-amal','نصيبك من الاسم عملًا'),
          ('sana-06-mihrab','بطاقة المحراب'),('sana-08-island','السبحة في الجزيرة الديناميكية')],
   phone=False, docs=['support','privacy','terms','accessibility'], subs=False),
 'midmak': dict(
   no='٣', name='مدماك', latin='Midmak', year='٢٠٢٦',
   tag='دفتر بناء بيتك، من الحفر إلى المفتاح.',
   meta='تطبيق لآيفون وآيباد، في التجربة على TestFlight، وقريبًا على App Store', play=False, beta=True,
   store=None,
   about=['تطبيق آيفون وآيباد للمالك الذي يبني بيته بنفسه: كل ريال مسجّل، وكل اتفاق محفوظ، وحقك واضح، من الحفر إلى المفتاح.'],
   features=['المصروفات والمقاولون والعمالة اليومية في دفتر واحد.',
             'صور الموقع والفواتير والمستندات في مكان واحد.',
             'تسجيل المصروف بصوتك، وتذكير بالمواعيد والدفعات.',
             'بياناتك على جهازك وفي حسابك الخاص على iCloud.'],
   shots=[('midmak-01-home','كل ريال مسجّل'),('midmak-02-pay','قبل ما تدفع'),('midmak-03-contractor','حساب المقاول'),
          ('midmak-04-wall','جدار البيت'),('midmak-05-scan','قراءة الفاتورة')],
   phone=False, docs=['support','privacy','terms'], subs=True),
}
DOCNAMES = {'support': ('الدعم', 'تواصل معنا وأسئلة شائعة'),
            'privacy': ('سياسة الخصوصية', 'ما يجمعه التطبيق، ولا يجمعه'),
            'terms': ('شروط الاستخدام', 'اتفاقية الاستخدام والاشتراكات'),
            'accessibility': ('إمكانية الوصول', 'ما يدعمه التطبيق اليوم')}

def notice(a, en=False):
    """the pill on a work: TestFlight before launch, Android soon while Google Play is pending"""
    if a.get('beta'): t = 'TestFlight'
    elif not a['store']: t = 'Soon' if en else 'قريبًا'
    elif a.get('play') is None: t = 'Android soon' if en else 'قريبًا على أندرويد'
    else: return ''
    return f' <em class="pill">{t}</em>'

def read(p): return open(os.path.join(SRC, p), encoding='utf-8').read()
def mailto(subject): return f'mailto:{EMAIL}?subject={quote(subject)}'
def write(path, html):
    full = os.path.join(OUT, path); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(html)

T = {
 'ar': dict(nav=('المعرض','الوثائق','تواصل'), skip='انتقل إلى المحتوى', brand='لبنة', navlabel='الموقع',
            foot='© ٢٠٢٦ لبنة. صُنعت هذه الأعمال بعناية، لبنةً لبنة.', quick='روابط سريعة', press='الملف الصحفي', switch='English', switch_lang='en'),
 'en': dict(nav=('Gallery','Documents','Contact'), skip='Skip to content', brand='Labina', navlabel='Site',
            foot='© 2026 Labina. Made with care, brick by brick.', quick='Quick links', press='Press kit', switch='العربية', switch_lang='ar'),
}
STORE_ID = {'mizan': '6808957329', 'sana': '6812705355'}

def shell(rel, title, desc, body, here=None, app=None, dark_top=False, path='', lang='ar'):
    """rel: prefix back to the site root. path: this page's path from the root (en pages start with en/)."""
    t = T[lang]
    style = f' style="--app:var(--{app});--app-lit:var(--{app}-lit)"' if app else ''
    base = rel + ('en/' if lang == 'en' else '')
    hrefs = [base or './', base + 'docs/', None]
    navh = ''
    for (h, lbl, key) in zip(hrefs, t['nav'], ('', 'docs/', '#contact')):
        if key == '#contact': navh += f'<a href="#contact">{lbl}</a>'
        else: navh += f'<a href="{h}"' + (' aria-current="page"' if key == here else '') + f'>{lbl}</a>'
    ar_path = path[3:] if lang == 'en' else path
    en_path = 'en/' + ar_path
    other = en_path if lang == 'ar' else ar_path
    navh += f'<a class="lang" href="{rel}{other}" hreflang="{t["switch_lang"]}" lang="{t["switch_lang"]}">{t["switch"]}</a>'
    og = f'{DOMAIN}/assets/og-{app or "labina"}.png'
    banner = f'<meta name="apple-itunes-app" content="app-id={STORE_ID[app]}">\n' if app in STORE_ID else ''
    mail_subject = 'لبنة' if lang == 'ar' else 'Labina'
    return f"""<!doctype html>
<html lang="{lang}" dir="{'rtl' if lang == 'ar' else 'ltr'}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{DOMAIN}/{path}">
<link rel="alternate" hreflang="ar" href="{DOMAIN}/{ar_path}">
<link rel="alternate" hreflang="en" href="{DOMAIN}/{en_path}">
{banner}<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{DOMAIN}/{path}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="{'#0E1110' if dark_top else '#E8EAE8'}" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="{'#0E1110' if dark_top else '#121514'}" media="(prefers-color-scheme: dark)">
<link rel="icon" href="{rel}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{rel}assets/labina-180.png">
{FONTS}
<link rel="stylesheet" href="{rel}style.css?v={VER}">
<script>document.documentElement.classList.remove('no-js')</script>
</head>
<body{style}>
<a class="skip" href="#main">{t['skip']}</a>
<header class="bar{' dark' if dark_top else ''}"><div class="wrap">
  <a class="brand" href="{base or './'}">{MARK}{t['brand']}</a>
  <nav aria-label="{t['navlabel']}">{navh}</nav>
</div></header>
{body}
<footer class="site" id="contact"><div class="wrap">
  <div class="sig">{WORDMARK}</div>
  <span>{t['foot']}</span>
  <nav aria-label="{t['quick']}"><a href="{base}docs/">{t['nav'][1]}</a><a href="{base}press/">{t['press']}</a><a href="{mailto(mail_subject)}" class="latin">{EMAIL}</a></nav>
</div></footer>
</body>
</html>
"""

def soon_block(lang, k, wall_cls='wall'):
    s = SOON[lang]
    subj = 'أخبرني عند إطلاق مدماك' if lang == 'ar' else 'Tell me when Midmak launches'
    return (f'<div class="soon"><div class="soon-wall">{wall_svg(wall_cls)}</div>'
            f'<div class="soon-text"><span class="soon-badge">{s["badge"]}</span><p class="soon-kicker">{s["kicker"]}</p>'
            f'<p class="soon-title">{s["title"]}</p><p class="soon-body">{s["body"]}</p>'
            f'<a class="btn line" href="{mailto(subj)}">{s["notify"]}</a></div></div>')

def frame(k, rel, alt=True):
    a = APPS[k]
    return f'<div class="frame"><img src="{rel}assets/{k}-icon.webp" width="512" height="512" alt="{"أيقونة " + a["name"] if alt else ""}"></div>'


# ================= visitors' wall =================
VW = {
 'ar': dict(kicker='جدار الزوار', you='أنت اللبنة رقم', back='زار المعرض', back2='زائرًا، ولبنتك في الجدار من قبل.',
            body='كل زائر يضع لبنة في جدار المعرض. لا نعرف من أنت ولا من أين جئت؛ نحسب اللبنات فقط.', locale='ar-SA', label='عدد زوار المعرض'),
 'en': dict(kicker="Visitors' wall", you='You are brick number', back='The gallery has had', back2='visitors, and your brick is already in the wall.',
            body='Every visitor lays a brick in the gallery wall. We do not know who you are or where you came from; we only count the bricks.', locale='en-US', label='Gallery visitors'),
}
def visitors_wall(lang):
    v = VW[lang]
    return f"""
<section class="section vwall" id="visitors" hidden aria-labelledby="vw-h" data-locale="{v['locale']}"><div class="wrap">
  <div class="vw-grid">
    <div class="vw-bricks" role="img" aria-label="{v['label']}"></div>
    <div class="vw-text">
      <p class="vw-kicker">{v['kicker']}</p>
      <h2 id="vw-h" class="vw-title"><span class="vw-lead"></span> <span class="vw-num"></span></h2>
      <p class="vw-tail"></p>
      <p class="vw-body">{v['body']}</p>
    </div>
  </div>
</div></section>
<script>
(function(){{
var sec=document.getElementById('visitors');if(!sec||!window.fetch)return;
var L={{you:{json.dumps(v['you'])},back:{json.dumps(v['back'])},back2:{json.dumps(v['back2'])}}};
var key='labina-brick',today=new Date().toISOString().slice(0,10),mine=null;
try{{mine=JSON.parse(localStorage.getItem(key)||'null')}}catch(e){{}}
var fresh=!(mine&&mine.d===today);
fetch('{COUNTER}/'+(fresh?'hit':''),{{method:fresh?'POST':'GET',cache:'no-store'}}).then(function(r){{if(!r.ok)throw 0;return r.json()}}).then(function(j){{
  var n=j&&j.visits;if(typeof n!=='number'||n<1)return;
  if(fresh){{mine={{d:today,n:n}};try{{localStorage.setItem(key,JSON.stringify(mine))}}catch(e){{}}}}
  var fmt=new Intl.NumberFormat(sec.getAttribute('data-locale'),{{useGrouping:false}});
  var digits=fmt.format(n).split('');
  var box=sec.querySelector('.vw-bricks');box.innerHTML='';
  digits.forEach(function(d,i){{var b=document.createElement('span');b.className='vw-b'+(i===digits.length-1?' lit':'');b.textContent=d;b.style.setProperty('--i',i);box.appendChild(b)}});
  var g=new Intl.NumberFormat(sec.getAttribute('data-locale')).format(n);
  if(fresh){{sec.querySelector('.vw-lead').textContent=L.you;sec.querySelector('.vw-num').textContent=g;sec.querySelector('.vw-tail').textContent=''}}
  else{{sec.querySelector('.vw-lead').textContent=L.back;sec.querySelector('.vw-num').textContent=g;sec.querySelector('.vw-tail').textContent=L.back2}}
  sec.hidden=false;
  if(fresh&&!matchMedia('(prefers-reduced-motion: reduce)').matches)sec.classList.add('laying');
}}).catch(function(){{}});
}})();
</script>"""

# ---------------- home ----------------
def home():
    works = ''.join(f'''
    <a class="work" href="{k}/" style="--app-lit:var(--{k}-lit)">
      <i class="cone" aria-hidden="true"><i class="beam"></i></i><i class="lamp" aria-hidden="true"></i>
      {frame(k, '', alt=False)}
      <span class="plaque"><span class="no">العمل {a["no"]}، {a["year"]}{notice(a)}</span><b>{a["name"]}</b><span>{a["tag"]}</span></span>
    </a>''' for k, a in APPS.items())
    entries = ''
    for k, a in APPS.items():
        imgs = ''.join(f'<img src="assets/{s}.webp" alt="" loading="lazy" width="660" height="1434">' for s, _ in a['shots'][:3])
        fan = f'<div class="fan" aria-hidden="true">{imgs}</div>' if a['store'] else f'<div class="fan wallfan">{wall_svg("wall mini")}</div>' 
        store = (f'<a class="btn line" href="{a["store"]}">App Store</a>' if a['store']
                 else '<span class="btn" aria-disabled="true">قريبًا على App Store</span>')
        entries += f'''
      <article class="entry" style="--app:var(--{k});--app-lit:var(--{k}-lit)">
        {fan}
        <div>
          <div class="label"><div class="no">العمل {a["no"]}، {a["year"]}{notice(a)}</div><h3>{a["name"]}</h3><p class="meta">{a["meta"]}</p></div>
          <p>{a["about"][0]}</p>
          <div class="actions"><a class="btn" href="{k}/">ادخل قاعة {a["name"]}</a>{store}</div>
        </div>
      </article>'''
    body = f'''<main id="main">
<section class="gallery dark" aria-labelledby="hall-h">
  <div class="wrap">
    <h1 id="hall-h">كل تطبيق قطعة، وهذا معرضها.</h1>
    <p class="lede">لبنة استوديو صغير يصنع تطبيقات عربية لآيفون وأندرويد. ثلاثة أعمال معروضة اليوم، والجدار يتّسع لما بعدها.</p>
    <div class="hall">{works}
    </div>
    <div class="bricks" aria-label="التنقل بين الأعمال">{''.join(f'<button type="button" data-i="{i}" aria-label="العمل {a["no"]}: {a["name"]}"></button>' for i, a in enumerate(APPS.values()))}<span class="ghost-brick" aria-hidden="true"></span></div>
  </div>
</section>

<section class="section" aria-labelledby="cat-h"><div class="wrap">
  <h2 id="cat-h">دليل المعرض</h2>
  <p class="sub">لكل عمل قاعته: لقطاته، وقصته، ووثائقه.</p>
  <div class="catalogue">{entries}
  </div>
</div></section>

<section class="section" aria-labelledby="ways-h"><div class="wrap">
  <h2 id="ways-h">ما يجمع هذه الأعمال</h2>
  <p class="sub">ثلاثة تطبيقات مختلفة، وطريقة صنع واحدة.</p>
  <ul class="principles">
    <li><b>بياناتك على جهازك</b><span>ما تسجّله يُحفظ ويُعالج على جهازك، وما نملك خادمًا يستقبله.</span></li>
    <li><b>بلا حسابات ولا إعلانات</b><span>تفتح التطبيق وتبدأ، ولا نبيع انتباهك لأحد.</span></li>
    <li><b>عربية من أول سطر</b><span>الكلمات والأرقام والاتجاه مصممة للعربية، لا مترجمة إليها.</span></li>
  </ul>
</div></section>

<section class="section"><div class="wrap">
  <div class="teaser">
    <div><h2>الوثائق</h2><p>روابط الدعم وسياسات الخصوصية وشروط الاستخدام لكل الأعمال، في صفحة واحدة.</p></div>
    <a class="btn line" href="docs/">افتح الوثائق</a>
  </div>
</div></section>

{visitors_wall('ar')}
<section class="section" aria-labelledby="contact-h"><div class="wrap">
  <h2 id="contact-h">تواصل</h2>
  <p class="sub">سؤال، أو خطأ وجدته، أو فكرة لعمل قادم؟ نرد عادة خلال يومي عمل.</p>
  <a class="mail" href="{mailto('لبنة')}">{EMAIL}</a>
</div></section>
</main>
<script>
(function(){{var h=document.querySelector('.gallery');if(!h)return;
var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
if(rm){{h.classList.add('lit')}}else{{var o=new IntersectionObserver(function(e){{if(e[0].isIntersecting){{h.classList.add('lit');o.disconnect()}}}},{{threshold:.3}});o.observe(h)}}
/* corridor (phones): light follows the work in front of you */
var hall=h.querySelector('.hall'),works=[].slice.call(hall.querySelectorAll('.work')),dots=[].slice.call(h.querySelectorAll('.bricks button'));
function set(i){{works.forEach(function(w,j){{w.classList.toggle('on',j===i)}});dots.forEach(function(d,j){{d.classList.toggle('on',j===i);d.setAttribute('aria-current',j===i?'true':'false')}})}}
set(0);
var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting)set(works.indexOf(e.target))}})}},{{root:hall,threshold:.6}});
works.forEach(function(w){{io.observe(w)}});
dots.forEach(function(d,i){{d.addEventListener('click',function(){{works[i].scrollIntoView({{behavior:rm?'auto':'smooth',inline:'center',block:'nearest'}})}})}});
}})();
</script>'''
    write('index.html', shell('', 'لبنة | معرض تطبيقات عربية', 'معرض أعمال لبنة: ميزان وسنا ومدماك، تطبيقات عربية لآيفون وأندرويد، مع صفحات الدعم والخصوصية وشروط الاستخدام.', body, here='', dark_top=True))

# ---------------- exhibit ----------------
def exhibit(k):
    a = APPS[k]; rel = '../'
    figs = ''.join(
        (f'<figure><div class="phone"><img src="{rel}assets/{s}.webp" alt="{c}" loading="lazy" width="416" height="900"></div><figcaption>{c}</figcaption></figure>' if a['phone'] else
         f'<figure><img src="{rel}assets/{s}.webp" alt="{c}" loading="lazy" width="660" height="1434"><figcaption>{c}</figcaption></figure>')
        for s, c in a['shots'])
    store = (f'<a class="btn" href="{a["store"]}">حمّل من App Store</a>' if a['store']
             else '<span class="btn line" aria-disabled="true">قريبًا على App Store</span>')
    if a.get('play'): store += f'<a class="btn line" href="{a["play"]}">احصل عليه من Google Play</a>'
    elif a.get('play') is None: store += '<span class="btn line" aria-disabled="true">قريبًا على Google Play</span>'
    docs = ''.join(f'<a class="doc" href="{d}/"><b>{DOCNAMES[d][0]}</b><span>{DOCNAMES[d][1]}</span></a>' for d in a['docs'])
    video = ''
    if k == 'mizan':
        video = ('<h2 class="h2" style="margin-top:44px">العمل في حركته</h2>'
                 '<video src="media/mizan.mp4" poster="media/cover.jpg" controls playsinline preload="none" '
                 'style="width:100%;max-width:260px;aspect-ratio:9/16;border-radius:18px;background:#000;margin-top:14px" '
                 'aria-label="عرض قصير لتطبيق ميزان"></video>')
    body = f'''<main id="main">
<section class="exhibit dark" aria-labelledby="ex-h">
  <div class="wrap">
    <p class="crumbs"><a href="{rel}">المعرض</a> ← قاعة {a["name"]}</p>
    <div class="exhibit-head">
      {frame(k, rel)}
      <div class="label"><div class="no">العمل {a["no"]}، {a["year"]}</div><h1 id="ex-h">{a["name"]}</h1>
        <p class="tag">{a["tag"]}</p><p class="meta">{a["meta"]}</p>
        <div class="actions">{store}</div></div>
    </div>
    {f'<div class="strip" tabindex="0" aria-label="لقطات من {a["name"]}">{figs}</div>' if a['shots'] else soon_block('ar', k)}
  </div>
</section>
<section class="reading"><div class="wrap narrow">
  <h2 class="h2">عن العمل</h2>
  {''.join(f'<p>{p}</p>' for p in a['about'])}
  <ul>{''.join(f'<li>{f}</li>' for f in a['features'])}</ul>
  {privacy_card('ar', k, 'privacy/')}
  {video}
  <h2 class="h2" style="margin-top:44px">وثائق {a["name"]}</h2>
  <div class="docs-grid">{docs}</div>
</div></section>
</main>'''
    write(f'{k}/index.html', shell(rel, f'{a["name"]} | معرض لبنة', a['tag'], body, app=k, dark_top=True, path=f'{k}/'))

# ---------------- documents ----------------
def docpage(k, d, inner, desc):
    a = APPS[k]; rel = '../../'
    tabs = f'<a href="../">القاعة</a>' + ''.join(
        f'<a href="../{t}/"' + (' aria-current="page"' if t == d else '') + f'>{DOCNAMES[t][0]}</a>' for t in a['docs'])
    body = f'''<main id="main"><div class="wrap narrow">
<div class="dochead">
  <p class="crumbs"><a href="{rel}">المعرض</a> ← <a href="../">{a["name"]}</a> ← {DOCNAMES[d][0]}</p>
  <div class="who"><img src="{rel}assets/{k}-icon.webp" alt="" width="52" height="52"><div><b>{a["name"]}</b><span>{a["tag"]}</span></div></div>
  <nav class="tabs" aria-label="صفحات {a["name"]}">{tabs}</nav>
</div>
<article class="prose">
{inner.replace('mr.aljohanii@gmail.com', EMAIL).strip()}
</article>
</div></main>'''
    write(f'{k}/{d}/index.html', shell(rel, f'{DOCNAMES[d][0]} | {a["name"]}', desc, body, app=k, path=f'{k}/{d}/'))

def contact_box(subject, line='راسلنا بالبريد، ونرد عادة خلال يومي عمل.'):
    return f'<div class="contact"><p>{line}</p><a class="mail" href="{mailto(subject)}">{EMAIL}</a></div>'

def terms(k):
    a = APPS[k]
    subs = ''
    if a['subs']:
        product = 'ميزان برو' if k == 'mizan' else 'مدماك بلس'
        subs = f'''<h2>الاشتراكات والمشتريات</h2>
<ul>
<li>التطبيق مجاني للتنزيل، ويقدّم مزايا إضافية باسم «{product}» عبر اشتراك متجدد أو شراء داخل التطبيق.</li>
<li>يتم الدفع من حسابك في Apple عند تأكيد الشراء، وتُعرض لك المدة والسعر قبل التأكيد.</li>
<li>الاشتراك يتجدد تلقائيًا ما لم تُلغه قبل نهاية الفترة الحالية بأربع وعشرين ساعة على الأقل، ويُخصم التجديد خلال الأربع والعشرين ساعة السابقة لنهايتها.</li>
<li>تدير اشتراكك وتلغيه من إعدادات حسابك في App Store: إعدادات الآيفون ← اسمك ← الاشتراكات.</li>
<li>إذا وُجدت تجربة مجانية، فأي جزء غير مستخدم منها يسقط عند الاشتراك.</li>
<li>الاسترجاع تديره Apple وفق سياساتها، ويُطلب من <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.</li>
</ul>'''
    nature = {
      'mizan': 'ميزان أداة لتنظيم مصاريفك وميزانيتك. الأرقام والتقديرات فيه، ومنها حساب الزكاة، تُبنى على ما تدخله أنت، وهي مساعدة على الفهم لا استشارة مالية أو فتوى. راجع أهل الاختصاص في القرارات المالية والشرعية المهمة.',
      'sana': 'سنا مرجع تعليمي لأسماء الله الحسنى. اجتهدنا في توثيق المعاني والشواهد، وإن وجدت خطأ فأبلغنا لنصحّحه.',
      'midmak': 'مدماك دفتر لتوثيق بناء بيتك وتنظيمه. ما يعرضه من أرقام وتنبيهات يُبنى على ما تدخله أنت، ولا يُغني عن المهندس المشرف أو المحامي أو العقود الموقّعة.',
    }[k]
    inner = f'''<h1>شروط الاستخدام</h1>
<p class="date">تاريخ السريان: ٩ أكتوبر ٢٠٢٦</p>
<p>باستخدامك تطبيق «{a["name"]}» توافق على هذه الشروط.</p>
<h2>اتفاقية الترخيص</h2>
<p>يخضع استخدام التطبيق لـ<a href="{EULA}">اتفاقية ترخيص المستخدم النهائي القياسية من Apple</a> (Standard EULA)، وتُكمّلها هذه الصفحة. وعند أي تعارض تُقدَّم اتفاقية Apple.</p>
{subs}
<h2>طبيعة التطبيق</h2>
<p>{nature}</p>
<h2>بياناتك</h2>
<p>بياناتك ملكك وتبقى على جهازك. التفاصيل في <a href="../privacy/">سياسة الخصوصية</a>.</p>
<h2>الاستخدام المقبول</h2>
<p>لا تستخدم التطبيق في ما يخالف الأنظمة، ولا تحاول تعطيله أو الالتفاف على مشترياته.</p>
<h2>التغييرات</h2>
<p>قد نحدّث هذه الشروط، ونغيّر تاريخ السريان أعلاه عند ذلك.</p>
<h2>التواصل</h2>
{contact_box('شروط ' + a["name"], 'لأي سؤال عن هذه الشروط')}
<section class="en" dir="ltr" lang="en">
<h2>Terms of Use (English)</h2>
<p>Use of {a["latin"]} is governed by Apple's <a href="{EULA}">Standard End User License Agreement</a>, supplemented by this page; Apple's EULA prevails in case of conflict.{' Optional subscriptions renew automatically unless cancelled at least 24 hours before the end of the current period, are charged to your Apple Account, and can be managed or cancelled in your App Store account settings. Any unused portion of a free trial is forfeited when you subscribe.' if a['subs'] else ''} Your data stays on your device; see the Privacy Policy. Contact: {EMAIL}.</p>
</section>'''
    docpage(k, 'terms', inner, f'شروط استخدام تطبيق {a["name"]}.')

def documents():
    # mizan
    docpage('mizan', 'support', f'''<h1>الدعم</h1>
<p>وجدت خللًا، أو رسالة بنك ما تعرّف عليها ميزان، أو عندك اقتراح؟ راسلنا. وإذا كانت المشكلة مع رسالة بنك، أرسل نصها بعد حذف أي رقم حساب أو بطاقة منه.</p>
{contact_box('دعم ميزان')}
<h2>أسئلة شائعة</h2>
<details><summary>هل يقرأ ميزان رسائلي؟</summary><p>على آيفون لا يقرأ التطبيق رسائلك. أنت تلصق رسالة البنك، أو تنشئ بنفسك أتمتة في تطبيق «الاختصارات» تمرّر نصها إلى ميزان (التسجيل التلقائي من مزايا ميزان برو). وتُعالج الرسالة على جهازك.</p></details>
<details><summary>كيف أنقل بياناتي إلى جهاز جديد؟</summary><p>على آيفون فعّل مزامنة iCloud من الإعدادات فتظهر بياناتك على أجهزتك. أو أنشئ نسخة احتياطية من الإعدادات واحفظ الملف، ثم افتحه على الجهاز الجديد.</p></details>
<details><summary>كيف ألغي اشتراك ميزان برو؟</summary><p>من إعدادات الآيفون ← اسمك ← الاشتراكات ← ميزان ← إلغاء الاشتراك.</p></details>
<details><summary>كيف أحذف بياناتي؟</summary><p>الإعدادات ← منطقة الخطر ← حذف جميع البيانات. وإن كانت مزامنة iCloud مفعّلة فاحذف بيانات التطبيق من إعدادات iCloud في جهازك كذلك.</p></details>
<details><summary>كيف أطلب استرجاع مبلغ؟</summary><p>الاسترجاع تديره Apple. اطلبه من <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a> بحسابك في Apple.</p></details>''',
            'الدعم والأسئلة الشائعة لتطبيق ميزان.')
    s = read('mizan-privacy/index.html')
    main = re.search(r'<main>(.*)</main>', s, re.S).group(1)
    main = re.sub(r'<h1>.*?</h1>', '<h1>سياسة الخصوصية</h1>', main, count=1, flags=re.S)
    main = main.replace('<p class="meta">', '<p class="date">', 1)
    main = re.sub(r'<section([^>]*)>\s*<h2>Privacy Policy', r'<section class="en" dir="ltr" lang="en"\1><h2>Privacy Policy', main)
    docpage('mizan', 'privacy', main, 'سياسة الخصوصية لتطبيق ميزان.')

    # sana
    def sana(f):
        m = re.search(r'<main>(.*)</main>', read(f), re.S).group(1)
        m = re.sub(r'<header>.*?</header>|<footer>.*?</footer>', '', m, flags=re.S)
        return re.sub(r'</?section[^>]*>', lambda x: x.group(0) if 'class="en"' in x.group(0) or x.group(0) == '</section>' and False else '', m)
    sup = sana('sana-support/index.html')
    sup = re.sub(r'<a class="btn" href="mailto:[^"]*">[^<]*</a>', contact_box('دعم سنا'), sup).replace('<h2>تواصل معنا</h2>', '<h1>الدعم</h1>', 1)
    docpage('sana', 'support', sup, 'الدعم والأسئلة الشائعة لتطبيق سنا.')
    raw = re.search(r'<main>(.*)</main>', read('sana-support/privacy.html'), re.S).group(1)
    raw = re.sub(r'<header>.*?</header>|<footer>.*?</footer>', '', raw, flags=re.S)
    en = re.search(r'<section class="en".*?</section>', raw, re.S).group(0)
    pri = re.sub(r'<section class="en".*?</section>', '', raw, flags=re.S)
    pri = re.sub(r'</?section[^>]*>', '', pri)
    pri = pri.replace('<h2>سياسة الخصوصية</h2>', '<h1>سياسة الخصوصية</h1>', 1).replace('<p class="sub" style="margin-bottom:12px">', '<p class="date">', 1)
    pri = re.sub(r'<a class="btn" href="mailto:[^"]*">([^<]*)</a>', lambda m: f'<p><a href="{mailto("خصوصية سنا")}">{m.group(1)}</a></p>', pri)
    docpage('sana', 'privacy', pri + en, 'سياسة الخصوصية لتطبيق سنا.')
    acc = sana('sana-support/accessibility.html').replace('<h2>إمكانية الوصول في سنا</h2>', '<h1>إمكانية الوصول</h1>', 1)
    acc = re.sub(r'<a class="btn" href="mailto:[^"]*">([^<]*)</a>', lambda m: f'<p><a href="{mailto("إمكانية الوصول في سنا")}">{m.group(1)}</a></p>', acc)
    docpage('sana', 'accessibility', acc, 'ما يدعمه تطبيق سنا من خيارات إمكانية الوصول.')

    # midmak
    def midmak(f):
        w = re.search(r'<div class="wrap">(.*)</div>\s*</body>', read(f), re.S).group(1)
        return re.sub(r'<header>.*?</header>|<nav>.*?</nav>|<footer>.*?</footer>', '', w, flags=re.S)
    sup = midmak('midmak/support/index.html')
    sup = re.sub(r'<div class="card">.*?</div>\s*<p[^>]*>.*?</p>\s*</div>', contact_box('دعم مدماك'), sup, count=1, flags=re.S)
    sup = sup.replace('reportaproblem.apple.com باستخدام', '<a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a> باستخدام')
    docpage('midmak', 'support', sup, 'الدعم والأسئلة الشائعة لتطبيق مدماك.')
    pri = midmak('midmak/privacy/index.html')
    pri = re.sub(r'<div class="card">.*?</div>\s*</div>', contact_box('خصوصية مدماك', 'لأي سؤال عن الخصوصية'), pri, count=1, flags=re.S)
    docpage('midmak', 'privacy', pri, 'سياسة الخصوصية لتطبيق مدماك.')

    for k in APPS: terms(k)

# ---------------- docs centre ----------------
def docs_centre():
    rel = '../'
    blocks = ''
    for k, a in APPS.items():
        rows = [('صفحة العمل', 'Marketing URL', f'{DOMAIN}/{k}/')]
        rows += [(DOCNAMES[d][0], {'support': 'Support URL', 'privacy': 'Privacy Policy URL',
                  'terms': 'Terms of Use (EULA)', 'accessibility': 'Accessibility'}[d], f'{DOMAIN}/{k}/{d}/') for d in a['docs']]
        if a['store']: rows.append(('في App Store', 'App Store', a['store']))
        if a.get('play'): rows.append(('في Google Play', 'Google Play', a['play']))
        rh = ''.join(f'<div class="row"><div class="k">{t}<small>{e}</small></div>'
                     f'<a class="v" href="{u}">{u}</a><button class="copy" type="button" data-copy="{u}">نسخ</button></div>' for t, e, u in rows)
        blocks += f'''<section class="ref" style="--app:var(--{k})" aria-labelledby="r-{k}">
  <div class="ref-head"><img src="{rel}assets/{k}-icon.webp" alt="" width="44" height="44"><div><h2 id="r-{k}">{a["name"]}</h2><span>العمل {a["no"]}</span></div></div>
  <div class="rows">{rh}</div>
</section>'''
    body = f'''<main id="main"><div class="wrap narrow">
<div class="dochead"><p class="crumbs"><a href="{rel}">المعرض</a> ← الوثائق</p></div>
<div class="prose" style="padding-bottom:8px">
<h1>الوثائق</h1>
<p>روابط الدعم وسياسات الخصوصية وشروط الاستخدام لكل أعمال لبنة. وهي الروابط المعتمدة لصفحات التطبيقات في المتاجر.</p>
<p>تخضع التطبيقات لـ<a href="{EULA}">اتفاقية ترخيص المستخدم النهائي القياسية من Apple</a>، وتكمّلها صفحة شروط الاستخدام لكل تطبيق.</p>
</div>
{blocks}
<section class="ref"><div class="rows">
  <div class="row"><div class="k">بريد الدعم<small>Support email</small></div><a class="v" href="mailto:{EMAIL}">{EMAIL}</a><button class="copy" type="button" data-copy="{EMAIL}">نسخ</button></div>
  <div class="row"><div class="k">اتفاقية Apple<small>Standard EULA</small></div><a class="v" href="{EULA}">{EULA}</a><button class="copy" type="button" data-copy="{EULA}">نسخ</button></div>
</div></section>
</div></main>
<script>
document.addEventListener('click',function(e){{var b=e.target.closest('.copy');if(!b)return;
var t=b.getAttribute('data-copy');var done=function(){{b.textContent='نُسخ';b.setAttribute('data-done','');setTimeout(function(){{b.textContent='نسخ';b.removeAttribute('data-done')}},1600)}};
if(navigator.clipboard){{navigator.clipboard.writeText(t).then(done,function(){{}})}}}});
</script>'''
    write('docs/index.html', shell(rel, 'الوثائق | لبنة', 'روابط الدعم وسياسات الخصوصية وشروط الاستخدام لتطبيقات لبنة: ميزان وسنا ومدماك.', body, here='docs/', path='docs/'))

def extras():
    write('favicon.svg', FAVICON)
    open(os.path.join(OUT, '.nojekyll'), 'w').close()
    open(os.path.join(OUT, 'CNAME'), 'w').write('labina.app\n')
    write('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
    urls = [''] + ['docs/'] + [f'{k}/' for k in APPS] + [f'{k}/{d}/' for k, a in APPS.items() for d in a['docs']]
    urls += ['press/']
    urls += ['en/' + u for u in urls]
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + ''.join(f'<url><loc>{DOMAIN}/{u}</loc></url>\n' for u in urls) + '</urlset>\n')
    write('404.html', shell('/', 'الصفحة غير موجودة | لبنة', 'الصفحة غير موجودة.', '''<main id="main"><div class="wrap narrow prose" style="padding:80px 0">
<h1>هذه القاعة فارغة</h1><p>ما لقينا الصفحة اللي تبحث عنها، وربما تغيّر رابطها. ارجع إلى <a href="/">المعرض</a> أو افتح <a href="/docs/">الوثائق</a>.</p></div></main>'''))


# ================= English =================
def en_frame(k, rel): return f'<div class="frame"><img src="{rel}assets/{k}-icon.webp" width="512" height="512" alt="{APPS_EN[k]["name"]} icon"></div>'
def en_contact(subject, line='Email us. We usually reply within two working days.'):
    return f'<div class="contact"><p>{line}</p><a class="mail" href="{mailto(subject)}">{EMAIL}</a></div>'

def en_home():
    rel = '../'
    works = ''.join(f"""
    <a class="work" href="{k}/" style="--app-lit:var(--{k}-lit)">
      <i class="cone" aria-hidden="true"><i class="beam"></i></i><i class="lamp" aria-hidden="true"></i>
      <div class="frame"><img src="{rel}assets/{k}-icon.webp" width="512" height="512" alt=""></div>
      <span class="plaque"><span class="no">Work {e['no']}, 2026{notice(APPS[k], en=True)}</span><b>{e['name']}</b><span>{e['tag']}</span></span>
    </a>""" for k, e in APPS_EN.items())
    entries = ''
    for k, e in APPS_EN.items():
        a = APPS[k]
        imgs = ''.join(f'<img src="{rel}assets/{sh}.webp" alt="" loading="lazy" width="660" height="1434">' for sh, _ in a['shots'][:3])
        fan = f'<div class="fan" aria-hidden="true">{imgs}</div>' if a['store'] else f'<div class="fan wallfan">{wall_svg("wall mini")}</div>'
        store = (f'<a class="btn line" href="{a["store"]}">App Store</a>' if a['store'] else '<span class="btn" aria-disabled="true">Coming soon</span>')
        entries += f"""
      <article class="entry" style="--app:var(--{k});--app-lit:var(--{k}-lit)">
        {fan}
        <div>
          <div class="label"><div class="no">Work {e['no']}, 2026{notice(a, en=True)}</div><h3>{e['name']}</h3><p class="meta">{e['meta']}</p></div>
          <p>{e['about'][0]}</p>
          <div class="actions"><a class="btn" href="{k}/">Enter the {e['name']} room</a>{store}</div>
        </div>
      </article>"""
    body = f"""<main id="main">
<section class="gallery dark" aria-labelledby="hall-h"><div class="wrap">
  <h1 id="hall-h">Every app is a piece, and this is its gallery.</h1>
  <p class="lede">Labina is a small studio making Arabic apps for iPhone and Android. Three works are on show today, and the wall has room for more.</p>
  <div class="hall">{works}
  </div>
  <div class="bricks" aria-label="Move between works">{''.join(f'<button type="button" data-i="{i}" aria-label="Work {e["no"]}: {e["name"]}"></button>' for i, e in enumerate(APPS_EN.values()))}<span class="ghost-brick" aria-hidden="true"></span></div>
</div></section>
<section class="section" aria-labelledby="cat-h"><div class="wrap">
  <h2 id="cat-h">Gallery guide</h2>
  <p class="sub">Each work has its own room: its screens, its story and its documents.</p>
  <div class="catalogue">{entries}
  </div>
</div></section>
<section class="section" aria-labelledby="ways-h"><div class="wrap">
  <h2 id="ways-h">What these works share</h2>
  <p class="sub">Three different apps, one way of making them.</p>
  <ul class="principles">
    <li><b>Your data stays on your device</b><span>What you record is stored and processed on your device. We have no server to receive it.</span></li>
    <li><b>No accounts, no ads</b><span>Open the app and start. We do not sell your attention to anyone.</span></li>
    <li><b>Arabic from the first line</b><span>Words, numerals and direction are designed for Arabic, not translated into it.</span></li>
  </ul>
</div></section>
<section class="section"><div class="wrap"><div class="teaser">
  <div><h2>Documents</h2><p>Support, privacy policies and terms of use for every work, on one page.</p></div>
  <a class="btn line" href="docs/">Open documents</a>
</div></div></section>
{visitors_wall('en')}
<section class="section" aria-labelledby="contact-h"><div class="wrap">
  <h2 id="contact-h">Contact</h2>
  <p class="sub">A question, a mistake you spotted, or an idea for a future work? We usually reply within two working days.</p>
  <a class="mail" href="{mailto('Labina')}">{EMAIL}</a>
</div></section>
</main>
<script>
(function(){{var h=document.querySelector('.gallery');if(!h)return;
var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
if(rm){{h.classList.add('lit')}}else{{var o=new IntersectionObserver(function(e){{if(e[0].isIntersecting){{h.classList.add('lit');o.disconnect()}}}},{{threshold:.3}});o.observe(h)}}
/* corridor (phones): light follows the work in front of you */
var hall=h.querySelector('.hall'),works=[].slice.call(hall.querySelectorAll('.work')),dots=[].slice.call(h.querySelectorAll('.bricks button'));
function set(i){{works.forEach(function(w,j){{w.classList.toggle('on',j===i)}});dots.forEach(function(d,j){{d.classList.toggle('on',j===i);d.setAttribute('aria-current',j===i?'true':'false')}})}}
set(0);
var io=new IntersectionObserver(function(es){{es.forEach(function(e){{if(e.isIntersecting)set(works.indexOf(e.target))}})}},{{root:hall,threshold:.6}});
works.forEach(function(w){{io.observe(w)}});
dots.forEach(function(d,i){{d.addEventListener('click',function(){{works[i].scrollIntoView({{behavior:rm?'auto':'smooth',inline:'center',block:'nearest'}})}})}});
}})();
</script>"""
    write('en/index.html', shell(rel, 'Labina | A gallery of Arabic apps', 'The works of Labina: Mizan, Sana and Midmak, Arabic apps for iPhone and Android, with support, privacy and terms pages.', body, here='', dark_top=True, path='en/', lang='en'))

def en_exhibit(k):
    a, e = APPS[k], APPS_EN[k]; rel = '../../'
    figs = ''.join(f'<figure><img src="{rel}assets/{sh}.webp" alt="{c}" loading="lazy" width="660" height="1434"><figcaption>{c}</figcaption></figure>'
                   for (sh, _), c in zip(a['shots'], e['caps']))
    store = (f'<a class="btn" href="{a["store"]}">Download on the App Store</a>' if a['store'] else '<span class="btn line" aria-disabled="true">Coming soon to the App Store</span>')
    if a.get('play'): store += f'<a class="btn line" href="{a["play"]}">Get it on Google Play</a>'
    elif a.get('play') is None: store += '<span class="btn line" aria-disabled="true">Coming soon to Google Play</span>'
    docs = ''.join(f'<a class="doc" href="{d}/"><b>{DOCNAMES_EN[d][0]}</b><span>{DOCNAMES_EN[d][1]}</span></a>' for d in a['docs'])
    video = ''
    if k == 'mizan':
        video = ('<h2 class="h2" style="margin-top:44px">The work in motion</h2><video src="../../mizan/media/mizan.mp4" poster="../../mizan/media/cover.jpg" controls playsinline preload="none" '
                 'style="width:100%;max-width:260px;aspect-ratio:9/16;border-radius:18px;background:#000;margin-top:14px" aria-label="A short demo of Mizan"></video>')
    show = f'<div class="strip" tabindex="0" aria-label="Screens from {e["name"]}">{figs}</div>' if a['shots'] else soon_block('en', k)
    body = f"""<main id="main">
<section class="exhibit dark" aria-labelledby="ex-h"><div class="wrap">
  <p class="crumbs"><a href="../">Gallery</a> / {e['name']} room</p>
  <div class="exhibit-head">{en_frame(k, rel)}
    <div class="label"><div class="no">Work {e['no']}, 2026</div><h1 id="ex-h">{e['name']}</h1>
      <p class="tag">{e['tag']}</p><p class="meta">{e['meta']}</p><div class="actions">{store}</div></div>
  </div>
  {show}
</div></section>
<section class="reading"><div class="wrap narrow">
  <h2 class="h2">About the work</h2>
  {''.join(f'<p>{x}</p>' for x in e['about'])}
  <ul>{''.join(f'<li>{x}</li>' for x in e['features'])}</ul>
  {privacy_card('en', k, 'privacy/')}
  {video}
  <h2 class="h2" style="margin-top:44px">{e['name']} documents</h2>
  <div class="docs-grid">{docs}</div>
</div></section>
</main>"""
    write(f'en/{k}/index.html', shell(rel, f'{e["name"]} | Labina gallery', e['tag'], body, app=k, dark_top=True, path=f'en/{k}/', lang='en'))

def en_docpage(k, d, inner, desc):
    a, e = APPS[k], APPS_EN[k]; rel = '../../../'
    tabs = '<a href="../">Room</a>' + ''.join(f'<a href="../{t}/"' + (' aria-current="page"' if t == d else '') + f'>{DOCNAMES_EN[t][0]}</a>' for t in a['docs'])
    body = f"""<main id="main"><div class="wrap narrow">
<div class="dochead">
  <p class="crumbs"><a href="../../">Gallery</a> / <a href="../">{e['name']}</a> / {DOCNAMES_EN[d][0]}</p>
  <div class="who"><img src="{rel}assets/{k}-icon.webp" alt="" width="52" height="52"><div><b>{e['name']}</b><span>{e['tag']}</span></div></div>
  <nav class="tabs" aria-label="{e['name']} pages">{tabs}</nav>
</div>
<article class="prose">
{inner.strip()}
</article>
</div></main>"""
    write(f'en/{k}/{d}/index.html', shell(rel, f'{DOCNAMES_EN[d][0]} | {e["name"]}', desc, body, app=k, path=f'en/{k}/{d}/', lang='en'))

def en_terms(k):
    a, e = APPS[k], APPS_EN[k]
    subs = ''
    if a['subs']:
        product = 'Mizan Pro' if k == 'mizan' else 'Midmak Plus'
        subs = f"""<h2>Subscriptions and purchases</h2><ul>
<li>The app is free to download and offers extra features as "{product}" through an auto-renewable subscription or an in-app purchase.</li>
<li>Payment is charged to your Apple Account when you confirm the purchase; the period and price are shown before you confirm.</li>
<li>A subscription renews automatically unless cancelled at least 24 hours before the end of the current period, and the renewal is charged within the 24 hours before it ends.</li>
<li>Manage or cancel it in your App Store account settings: iPhone Settings → your name → Subscriptions.</li>
<li>If a free trial is offered, any unused portion is forfeited when you subscribe.</li>
<li>Refunds are handled by Apple under its policies, at <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a>.</li></ul>"""
    inner = f"""<h1>Terms of Use</h1>
<p class="date">Effective: October 9, 2026</p>
<p>By using {e['name']} you agree to these terms.</p>
<h2>License agreement</h2>
<p>Use of the app is governed by Apple's <a href="{EULA}">Standard End User License Agreement</a> (EULA), supplemented by this page. If they conflict, Apple's agreement prevails.</p>
{subs}
<h2>What the app is</h2><p>{NATURE_EN[k]}</p>
<h2>Your data</h2><p>Your data is yours and stays on your device. See the <a href="../privacy/">Privacy Policy</a>.</p>
<h2>Acceptable use</h2><p>Do not use the app against the law, or try to disrupt it or get around its purchases.</p>
<h2>Changes</h2><p>We may update these terms, and will change the effective date above when we do.</p>
<h2>Contact</h2>{en_contact(e['name'] + ' terms', 'Questions about these terms')}"""
    en_docpage(k, 'terms', inner, f'Terms of use for {e["name"]}.')

def en_documents():
    for k in APPS:
        intro, faq = SUPPORT_EN[k]
        en_docpage(k, 'support', f'<h1>Support</h1><p>{intro}</p>{en_contact(APPS_EN[k]["name"] + " support")}<h2>FAQ</h2>'
                   + ''.join(f'<details><summary>{q}</summary><p>{ans}</p></details>' for q, ans in faq), f'Support and FAQs for {APPS_EN[k]["name"]}.')
        en_terms(k)
    # mizan privacy: its English section
    m = re.search(r'<section[^>]*>\s*<h2>Privacy Policy[^<]*</h2>(.*?)</section>', read('mizan-privacy/index.html'), re.S).group(1)
    m = re.sub(r'<p class="meta">', '<p class="date">', m, count=1).replace('mr.aljohanii@gmail.com', EMAIL)
    en_docpage('mizan', 'privacy', '<h1>Privacy Policy</h1>' + m, 'Privacy policy for Mizan.')
    sp = re.search(r'<section class="en"[^>]*>\s*<h2>[^<]*</h2>(.*?)</section>', read('sana-support/privacy.html'), re.S).group(1)
    en_docpage('sana', 'privacy', '<h1>Privacy Policy</h1><p class="date">Last updated: September 25, 2026</p>' + sp
               + f'<p><a href="{mailto("Sana privacy")}">A question about privacy? Email us</a></p>', 'Privacy policy for Sana.')
    en_docpage('midmak', 'privacy', MIDMAK_PRIVACY_EN + en_contact('Midmak privacy', 'Questions about privacy'), 'Privacy policy for Midmak.')
    en_docpage('sana', 'accessibility', SANA_A11Y_EN + f'<p><a href="{mailto("Sana accessibility")}">Suggest an improvement or report a barrier</a></p>', 'Accessibility support in Sana.')

def en_docs_centre():
    rel = '../../'; blocks = ''
    lbl = {'support': 'Support URL', 'privacy': 'Privacy Policy URL', 'terms': 'Terms of Use (EULA)', 'accessibility': 'Accessibility'}
    for k, a in APPS.items():
        e = APPS_EN[k]
        rows = [('Product page', 'Marketing URL', f'{DOMAIN}/en/{k}/')] + [(DOCNAMES_EN[d][0], lbl[d], f'{DOMAIN}/en/{k}/{d}/') for d in a['docs']]
        if a['store']: rows.append(('On the App Store', 'App Store', a['store']))
        if a.get('play'): rows.append(('On Google Play', 'Google Play', a['play']))
        rh = ''.join(f'<div class="row"><div class="k">{t}<small>{x}</small></div><a class="v" href="{u}">{u}</a><button class="copy" type="button" data-copy="{u}">Copy</button></div>' for t, x, u in rows)
        blocks += f'<section class="ref" style="--app:var(--{k})"><div class="ref-head"><img src="{rel}assets/{k}-icon.webp" alt="" width="44" height="44"><div><h2>{e["name"]}</h2><span>Work {e["no"]}</span></div></div><div class="rows">{rh}</div></section>'
    body = f"""<main id="main"><div class="wrap narrow">
<div class="dochead"><p class="crumbs"><a href="../">Gallery</a> / Documents</p></div>
<div class="prose" style="padding-bottom:8px"><h1>Documents</h1>
<p>Support, privacy policies and terms of use for every Labina work. Arabic versions live at the same paths without <span class="latin">/en</span>.</p>
<p>The apps are governed by Apple's <a href="{EULA}">Standard End User License Agreement</a>, supplemented by each app's terms page.</p></div>
{blocks}
<section class="ref"><div class="rows">
<div class="row"><div class="k">Support email<small>Email</small></div><a class="v" href="mailto:{EMAIL}">{EMAIL}</a><button class="copy" type="button" data-copy="{EMAIL}">Copy</button></div>
<div class="row"><div class="k">Apple EULA<small>Standard EULA</small></div><a class="v" href="{EULA}">{EULA}</a><button class="copy" type="button" data-copy="{EULA}">Copy</button></div>
</div></section></div></main>
<script>
document.addEventListener('click',function(e){{var b=e.target.closest('.copy');if(!b)return;var t=b.getAttribute('data-copy');
var done=function(){{b.textContent='Copied';b.setAttribute('data-done','');setTimeout(function(){{b.textContent='Copy';b.removeAttribute('data-done')}},1600)}};
if(navigator.clipboard){{navigator.clipboard.writeText(t).then(done,function(){{}})}}}});
</script>"""
    write('en/docs/index.html', shell(rel, 'Documents | Labina', 'Support, privacy and terms pages for Labina apps: Mizan, Sana and Midmak.', body, here='docs/', path='en/docs/', lang='en'))

# ================= press kit =================
PRESS_TXT = {
 'ar': dict(title='الملف الصحفي', crumb='المعرض', lede='كل ما تحتاجه للكتابة عن لبنة وأعمالها أو الإعلان عنها: الشعار، والأيقونات، واللقطات بدقتها الكاملة، ووصف جاهز لكل تطبيق. استعملها بحرية في المقالات والمراجعات والإعلانات.',
            about_h='عن لبنة', about='لبنة استوديو سعودي صغير يصنع تطبيقات عربية لآيفون وأندرويد. تعمل تطبيقاته على جهاز المستخدم، بلا حسابات ولا إعلانات ولا تتبّع، وأعماله اليوم: ميزان لإدارة المصاريف من رسائل البنك، وسنا لأسماء الله الحسنى، ومدماك لتوثيق بناء البيت.',
            logo_h='الشعار', logo_p='الشعار كلمة «لبنة» مبنية بالخط الكوفي المربّع، كل خلية فيها لبنة، ونقاطها بلون القنديل، وحركاتها لبنات مائلة لم تستقرّ بعد في الجدار. والعلامة المختصرة حرف اللام واللبنة الأولى.',
            on_light='على الفاتح', on_dark='على الداكن', icon='الأيقونة', mono='أحادي اللون',
            rules=['استعمل الملفات كما هي، ولا تكتب الاسم بخط آخر بدلها.', 'اترك حول الشعار مسافة خالية بعرض لبنة على الأقل.', 'لا تمدّ الشعار ولا تميّله ولا تغيّر ألوانه أو تضع عليه ظلًا.'],
            colors_h='الألوان', cn=('ليل', 'جصّ', 'قنديل'),
            all_logo='حمّل الشعار كاملًا', copy='نسخ', copied='نُسخ', shots='اللقطات', soon_shots='تُنشر لقطات مدماك يوم الإطلاق، وأيقونته متاحة الآن.',
            dl_icon='الأيقونة PNG', dl_all='حمّل كل المواد', platforms='المنصات', year='السنة', store='المتجر', soon='قريبًا', short='الوصف القصير', long='الوصف',
            contact_h='للتواصل الإعلامي', contact_p='لطلب مقابلة أو نسخة تجريبية أو مواد إضافية، راسلنا ونرد خلال يومي عمل.', subject='طلب إعلامي'),
 'en': dict(title='Press kit', crumb='Gallery', lede='Everything you need to write about Labina and its works, or to feature them: the logo, icons, full-resolution screenshots, and a ready description of each app. Use them freely in articles, reviews and promotions.',
            about_h='About Labina', about='Labina is a small Saudi studio making Arabic apps for iPhone and Android. Its apps run on the user\'s device, with no accounts, ads or tracking. Its works today: Mizan, for managing spending from bank messages; Sana, on the Beautiful Names of Allah; and Midmak, for documenting the building of a home.',
            logo_h='Logo', logo_p='The logo is the word لبنة (Labina, "a brick") built in square Kufic: every cell is a brick, the dots glow in lantern amber, and the vowel marks are slanted bricks still being laid. The mark is the letter lām with the first brick.',
            on_light='On light', on_dark='On dark', icon='Icon', mono='One colour',
            rules=['Use the files as they are; do not set the name in another typeface instead.', 'Leave clear space of at least one brick around the logo.', 'Do not stretch, tilt, recolour or add shadows to the logo.'],
            colors_h='Colours', cn=('Night', 'Gypsum', 'Lantern'),
            all_logo='Download the full logo set', copy='Copy', copied='Copied', shots='Screenshots', soon_shots='Midmak screenshots will be published on launch day; its icon is available now.',
            dl_icon='Icon PNG', dl_all='Download all materials', platforms='Platforms', year='Year', store='Store', soon='Coming soon', short='Short description', long='Description',
            contact_h='Press contact', contact_p='For interviews, a review copy or more materials, email us. We reply within two working days.', subject='Press request'),
}
def _size(path):
    b = os.path.getsize(path); return f'{b/1048576:.1f} MB' if b > 1048576 else f'{b//1024} KB'

def press(lang):
    t = PRESS_TXT[lang]; en = lang == 'en'
    rel = '../../' if en else '../'
    F = rel + 'press/files/'
    def copyblock(text):
        return f'<div class="quote"><p>{text}</p><button class="copy" type="button" data-copy="{text}">{t["copy"]}</button></div>'
    logos = f"""<div class="kit-logos">
  <figure class="kit-tile light"><img src="{F}labina/wordmark.svg" alt="" width="260" height="220"><figcaption>{t['on_light']} <a href="{F}labina/wordmark.svg" download>SVG</a> <a href="{F}labina/wordmark-2000.png" download>PNG</a></figcaption></figure>
  <figure class="kit-tile dark"><img src="{F}labina/wordmark-light.svg" alt="" width="260" height="220"><figcaption>{t['on_dark']} <a href="{F}labina/wordmark-light.svg" download>SVG</a> <a href="{F}labina/wordmark-light-2000.png" download>PNG</a></figcaption></figure>
  <figure class="kit-tile light"><img src="{F}labina/mark-icon.svg" alt="" width="120" height="120" style="width:96px"><figcaption>{t['icon']} <a href="{F}labina/mark-icon.svg" download>SVG</a> <a href="{F}labina/labina-icon-1024.png" download>PNG</a></figcaption></figure>
  <figure class="kit-tile light"><img src="{F}labina/wordmark-mono.svg" alt="" width="260" height="220"><figcaption>{t['mono']} <a href="{F}labina/wordmark-mono.svg" download>SVG</a> <a href="{F}labina/mark-mono.svg" download>{'العلامة' if not en else 'Mark'}</a></figcaption></figure>
</div>
<ul class="kit-rules">{''.join(f'<li>{r}</li>' for r in t['rules'])}</ul>
<p><a class="btn line" href="{F}labina.zip" download>{t['all_logo']} (ZIP{'، ' if not en else ', '}{_size(os.path.join(PRESS, 'labina.zip'))})</a></p>"""
    colors = ''.join(f'<button class="swatch-chip copy" type="button" data-copy="{h}" style="--c:{h}"><i></i><b>{n}</b><span class="latin">{h}</span></button>'
                     for n, h in zip(t['cn'], ('#0E1110', '#ECEDEA', '#EDB230')))
    apps_html = ''
    for k, a in APPS.items():
        e = APPS_EN[k]
        name = e['name'] if en else a['name']
        tag = e['tag'] if en else a['tag']
        about = (e['about'] if en else a['about'])[0]
        meta = e['meta'] if en else a['meta']
        pdir = os.path.join(PRESS, k)
        files = os.listdir(pdir)  # pair each press file with its shot by name, not by sort order
        shots = [f for sh, _ in a['shots'] for f in files if os.path.splitext(f)[0] == sh]
        thumbs = ''
        if shots:
            caps = e['caps'] if en else [c for _, c in a['shots']]
            for f, (sh, _), c in zip(shots, a['shots'], caps):
                thumbs += f'<a class="kit-shot" href="{F}{k}/{f}" download title="{c}"><img src="{rel}assets/{sh}.webp" alt="{c}" loading="lazy" width="660" height="1434"></a>'
            gallery = f'<div class="kit-shots">{thumbs}</div>'
        else:
            gallery = f'<p class="kit-soon">{t["soon_shots"]}</p>'
        store = f'<a href="{a["store"]}">App Store</a>' if a['store'] else t['soon']
        apps_html += f"""
<section class="kit-app" style="--app:var(--{k})" aria-labelledby="k-{k}">
  <div class="kit-app-head"><img src="{rel}assets/{k}-icon.webp" alt="" width="64" height="64">
    <div><h2 id="k-{k}">{name}</h2><span>{tag}</span></div></div>
  <dl class="kit-facts"><div><dt>{t['platforms']}</dt><dd>{meta}</dd></div><div><dt>{t['store']}</dt><dd>{store}</dd></div><div><dt>{t['year']}</dt><dd>{'2026' if en else '٢٠٢٦'}</dd></div></dl>
  <h3>{t['short']}</h3>{copyblock(tag)}
  <h3>{t['long']}</h3>{copyblock(about)}
  <h3>{t['shots']}</h3>{gallery}
  <div class="actions"><a class="btn" href="{F}{k}/{k}-icon-1024.png" download>{t['dl_icon']}</a>
    <a class="btn line" href="{F}{k}.zip" download>{t['dl_all']} (ZIP{'، ' if not en else ', '}{_size(os.path.join(PRESS, f'{k}.zip'))})</a></div>
</section>"""
    body = f"""<main id="main"><div class="wrap">
<div class="dochead"><p class="crumbs"><a href="{'../' if en else '../'}">{t['crumb']}</a> {'/' if en else '←'} {t['title']}</p></div>
<div class="prose narrowish"><h1>{t['title']}</h1><p class="lede-p">{t['lede']}</p></div>
<section class="kit-sec"><h2 class="h2">{t['about_h']}</h2>{copyblock(t['about'])}</section>
<section class="kit-sec"><h2 class="h2">{t['logo_h']}</h2><p class="sub" style="margin-bottom:20px">{t['logo_p']}</p>{logos}</section>
<section class="kit-sec"><h2 class="h2">{t['colors_h']}</h2><div class="swatches">{colors}</div></section>
{apps_html}
<section class="kit-sec"><h2 class="h2">{t['contact_h']}</h2><p class="sub">{t['contact_p']}</p><a class="mail" href="{mailto(t['subject'])}">{EMAIL}</a></section>
</div></main>
<script>
document.addEventListener('click',function(e){{var b=e.target.closest('.copy');if(!b)return;var t=b.getAttribute('data-copy');
var lbl=b.querySelector('b')?null:b.textContent;var done=function(){{b.setAttribute('data-done','');if(lbl)b.textContent='{t['copied']}';setTimeout(function(){{b.removeAttribute('data-done');if(lbl)b.textContent=lbl}},1600)}};
if(navigator.clipboard){{navigator.clipboard.writeText(t).then(done,function(){{}})}}}});
</script>"""
    path = 'en/press/' if en else 'press/'
    write(path + 'index.html', shell(rel, f'{t["title"]} | {"Labina" if en else "لبنة"}', t['lede'][:150], body, here='press/', path=path, lang=lang))

def build():
    global PRESS
    import tempfile
    _tmp = tempfile.mkdtemp()
    global _press_tmp
    _press_tmp = os.path.join(_tmp, 'press')
    src_press = PRESS if os.path.isdir(PRESS) else os.path.join(ROOT, 'press', 'files')
    shutil.copytree(src_press, _press_tmp)
    PRESS = _press_tmp
    if os.path.exists(OUT):
        for n in os.listdir(OUT):
            if n in ('.git', 'README.md', 'CLAUDE.md', 'brand', 'tools', '_src'): continue
            p = os.path.join(OUT, n); shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(OUT, exist_ok=True)
    shutil.copy(os.path.join(HERE, 'style.css'), os.path.join(OUT, 'style.css'))
    shutil.copytree(ASSETS, os.path.join(OUT, 'assets'))
    for f in os.listdir(os.path.join(BRAND, 'out')): shutil.copy(os.path.join(BRAND, 'out', f), os.path.join(OUT, 'assets', f))
    os.makedirs(os.path.join(OUT, 'mizan/media'), exist_ok=True)
    for f in ('cover.jpg', 'mizan.mp4'):
        shutil.copy(os.path.join(SRC, 'mizan-privacy/video', f), os.path.join(OUT, 'mizan/media', f))
    home(); [exhibit(k) for k in APPS]; documents(); docs_centre()
    en_home(); [en_exhibit(k) for k in APPS]; en_documents(); en_docs_centre()
    shutil.copytree(_press_tmp, os.path.join(OUT, 'press', 'files'))
    press('ar'); press('en'); extras()

build(); print('built', OUT)
