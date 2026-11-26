"""A room's screens, by platform: the visitor picks a device (or we guess it from their browser)
and sees the work on it. Data comes from _src/gallery/<app>.json (written by tools/sync_shots.py
from each app's labina-shots/); until an app has one, its current shots and fold set stand in."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
GAL_DIR = os.path.join(os.path.dirname(HERE), 'gallery')

# device groups, in dock order: key, platforms inside it, Arabic, English, bezel, icon
GROUPS = [
    ('iphone', ['iphone'], 'آيفون', 'iPhone', 'phone', 'iphone'),
    ('ipad', ['ipad'], 'آيباد', 'iPad', 'tab', 'ipad'),
    ('watch', ['watch'], 'ساعة Apple', 'Apple Watch', 'watch', 'watch'),
    ('iphone-duo', ['iphone-duo-inner', 'iphone-duo-outer'], 'آيفون دو', 'iPhone Duo', 'fold', 'duo'),
    ('android', ['android'], 'أندرويد', 'Android', 'phone', 'android'),
    ('android-fold', ['android-fold', 'android-fold-outer'], 'أندرويد القابل للطي', 'Android foldable', 'fold', 'fold'),
    ('android-tv', ['android-tv'], 'التلفاز', 'TV', 'tv', 'tv'),
    ('windows', ['windows'], 'ويندوز', 'Windows', 'tv', 'pc'),
    ('phone-web', ['phone-web'], 'الجوال', 'Phone', 'phone', 'web'),
]
SUB = {'iphone-duo-inner': ('مفتوحًا', 'Unfolded'), 'iphone-duo-outer': ('مغلقًا', 'Folded'),
       'android-fold': ('مفتوحًا', 'Unfolded'), 'android-fold-outer': ('الشاشة الخارجية', 'Outer screen')}
BEZEL = {'iphone-duo-outer': 'phone', 'android-fold-outer': 'phone'}

ICON = {  # 28×28 line drawings of each device
 'iphone': '<rect x="8" y="2.5" width="12" height="23" rx="3"/><path d="M12.5 5.5h3"/>',
 'ipad': '<rect x="4.5" y="3" width="19" height="22" rx="2.5"/><circle cx="14" cy="22.3" r=".6"/>',
 'watch': '<rect x="8" y="8" width="12" height="12" rx="3.5"/><path d="M10.5 8V3.5h7V8M10.5 20v4.5h7V20"/>',
 'duo': '<path d="M14 5.5v18"/><rect x="3.5" y="5.5" width="21" height="18" rx="2.5"/><path d="M8.5 8.5h2"/>',
 'android': '<rect x="8" y="2.5" width="12" height="23" rx="2"/><circle cx="14" cy="5.3" r=".7"/>',
 'fold': '<path d="M14 6 4 4v20l10 2 10-2V4z"/><path d="M14 6v20"/>',
 'tv': '<rect x="3" y="5" width="22" height="14" rx="1.5"/><path d="M10 23.5h8M14 19v4.5"/>',
 'pc': '<rect x="3" y="4" width="22" height="15" rx="1.5"/><path d="M11 24h6M14 19v5M3 16h22"/>',
 'web': '<rect x="8" y="2.5" width="12" height="23" rx="3"/><circle cx="14" cy="14" r="3.5"/><path d="M10.5 14h7M14 10.5c1.4 2.2 1.4 4.8 0 7"/>',
}

def _num(n, ar):
    s = str(n)
    return s.translate(str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩')) if ar else s

def load(k, a, en_caps, fold):
    """{platform: {'ar': [[src, w, h, cap]], 'en': [...]}, plus 'framed' for store art}"""
    p = os.path.join(GAL_DIR, f'{k}.json')
    synced = json.load(open(p, encoding='utf-8'))['platforms'] if os.path.exists(p) else {}
    # stand-ins: the room's current shots, and its fold set
    seed = {'mizan': 'iphone', 'sana': 'iphone', 'midmak': 'iphone', 'sakan': 'android-tv',
            'mihrab': 'android-tv', 'hamish': 'iphone', 'satr': 'android-fold'}[k]
    w, h = a.get('shape') or ((1280, 720) if a.get('tv') else (660, 1434))
    plats = {}
    if a['shots']:
        plats[seed] = {'ar': [[f'{s}.webp', w, h, c] for s, c in a['shots']],
                       'en': [[f'{s}.webp', w, h, c] for (s, _), c in zip(a['shots'], en_caps)]}
    if fold:
        fp = {'mizan': 'iphone-duo-inner', 'sana': 'android-fold', 'satr': 'android-fold-outer'}[k]
        plats[fp] = {lang: [[f'{s}.webp', sw, sh, c] for s, c, (sw, sh) in zip(fold['shots'], fold[lang]['caps'], fold['size'])]
                     for lang in ('ar', 'en')}
        if k in ('mizan', 'sana'): plats[fp]['framed'] = True     # store art, already in a device frame
    plats.update(synced)          # a session's delivery replaces the stand-in for its platform; the rest stay
    return plats

def groups_of(plats):
    return [g for g in GROUPS if any(p in plats for p in g[1])]

def render(k, lang, rel, plats, name):
    ar = lang == 'ar'
    gs = groups_of(plats)
    if not gs: return ''
    tabs, panels = [], []
    for i, (key, members, n_ar, n_en, bezel, icon) in enumerate(gs):
        count = 0; rows = []
        for p in members:
            if p not in plats: continue
            d = plats[p]
            shots = d.get(lang) or d.get('ar') or []
            count += len(shots)
            dev = 'none' if d.get('framed') else BEZEL.get(p, bezel)
            figs = ''.join(
                f'<figure><div class="dev dev-{dev}"><img src="{rel}assets/{src}" alt="{cap}" loading="lazy" width="{w}" height="{h}"></div>'
                f'<figcaption>{cap}</figcaption></figure>' for src, w, h, cap in shots)
            sub = f'<p class="gal-sub">{SUB[p][0 if ar else 1]}</p>' if p in SUB and sum(m in plats for m in members) > 1 else ''
            if not ar and d.get('ar_ui') and not any('gal-note' in r for r in rows): rows.append('<p class="gal-note">The app\'s interface is in Arabic.</p>')
            rows.append(f'{sub}<div class="strip gal-strip" tabindex="0" aria-label="{(n_ar if ar else n_en)}: {name}">{figs}</div>')
        label = n_ar if ar else n_en
        unit = (('لقطتان' if count == 2 else _num(count, ar) + (' لقطات' if 3 <= count <= 10 else ' لقطة'))) if ar else f'{count} screens'
        sel = 'true' if i == 0 else 'false'
        tabs.append(f'<button type="button" role="tab" id="gt-{key}" aria-controls="gp-{key}" aria-selected="{sel}" tabindex="{0 if i == 0 else -1}" data-os="{key}">'
                    f'<svg viewBox="0 0 28 28" aria-hidden="true">{ICON[icon]}</svg><b>{label}</b><span>{unit}</span></button>')
        panels.append(f'<div class="gal-panel{" on" if i == 0 else ""}" role="tabpanel" id="gp-{key}" aria-labelledby="gt-{key}" data-os="{key}">'
                      f'<h3 class="gal-h">{label}</h3>{"".join(rows)}</div>')
    if len(gs) == 1:   # one device: no dock, just its screens
        only = panels[0].replace(' role="tabpanel"', '')
        return f'<div class="gallery single">{only}</div>'
    ask = 'على أي جهاز تريد أن تراه؟' if ar else 'Which device do you want to see it on?'
    names = {g[0]: (g[2] if ar else g[3]) for g in gs}
    return (f'<div class="gallery" data-names=\'{json.dumps(names, ensure_ascii=False)}\' data-lang="{lang}">'
            f'<p class="gal-ask">{ask}</p><div class="gal-dock" role="tablist" aria-label="{ask}">{"".join(tabs)}</div>'
            f'<p class="gal-hint" aria-live="polite"></p>{"".join(panels)}</div>')

SCRIPT = r'''<script>(function(){
var g=document.querySelector('.gallery:not(.single)');if(!g)return;
var tabs=[].slice.call(g.querySelectorAll('[role=tab]')),names=JSON.parse(g.dataset.names),ar=g.dataset.lang=='ar',hint=g.querySelector('.gal-hint');
function pick(os,why){var t=g.querySelector('[role=tab][data-os="'+os+'"]');if(!t)return false;
 tabs.forEach(function(b){var on=b===t;b.setAttribute('aria-selected',on);b.tabIndex=on?0:-1;
  document.getElementById(b.getAttribute('aria-controls')).classList.toggle('on',on)});
 hint.textContent=why?(ar?'نعرض لك '+names[os]+' لأنك تتصفح منه.':'Showing '+names[os]+' because you are browsing on one.'):'';
 return true}
function guess(){var u=navigator.userAgent,fold=false;
 try{fold=matchMedia('(horizontal-viewport-segments: 2),(vertical-viewport-segments: 2)').matches||!!(navigator.devicePosture&&navigator.devicePosture.type=='folded')}catch(e){}
 if(/Android/.test(u))return fold?['android-fold','android']:/TV|AFT|BRAVIA|SMART-TV/.test(u)?['android-tv']:['android','android-fold'];
 if(/iPad/.test(u)||(/Macintosh/.test(u)&&navigator.maxTouchPoints>1))return['ipad','iphone'];
 if(/iPhone/.test(u))return fold?['iphone-duo','iphone']:['iphone','iphone-duo'];
 if(/Windows/.test(u))return['windows'];return[]}
var saved=null;try{saved=localStorage.getItem('labina-os')}catch(e){}
if(!(saved&&pick(saved)))guess().some(function(os){return pick(os,1)});
tabs.forEach(function(b,i){
 b.addEventListener('click',function(){pick(b.dataset.os);try{localStorage.setItem('labina-os',b.dataset.os)}catch(e){}});
 b.addEventListener('keydown',function(e){var d={ArrowLeft:ar?1:-1,ArrowRight:ar?-1:1,Home:-99,End:99}[e.key];if(d==null)return;e.preventDefault();
  var j=Math.max(0,Math.min(tabs.length-1,d==-99?0:d==99?tabs.length-1:i+d));tabs[j].focus();tabs[j].click()})});
[].slice.call(document.querySelectorAll('[data-show-os]')).forEach(function(b){b.addEventListener('click',function(){
 pick(b.dataset.showOs);g.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'})})});
})()</script>'''
