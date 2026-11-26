#!/usr/bin/env python3
"""Bring an app's screenshots into the site.

    python3 tools/sync_shots.py <app> <path to the app project's labina-shots/>

The app session delivers labina-shots/<platform>/<ar|en>/NN-slug.png plus captions.tsv
(platform, NN-slug, Arabic caption, English caption). This converts each PNG to a webp in
_src/assets/g/<app>/<platform>/<lang>/ and writes _src/gallery/<app>.json, which build.py
reads to draw the room's platform switcher. Re-running replaces that app's set.
"""
import csv, json, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORDER = ['iphone', 'ipad', 'watch', 'iphone-duo-inner', 'iphone-duo-outer', 'android', 'android-fold',
         'android-fold-outer', 'android-tv', 'windows', 'phone-web']
WIDE = {'ipad', 'iphone-duo-inner', 'android-fold', 'android-tv', 'windows'}   # landscape-ish screens


def size(p):
    w, h = subprocess.check_output(['magick', 'identify', '-format', '%w %h', p], text=True).split()
    return int(w), int(h)


def main(app, src, skip=()):
    caps = {}
    tsv = os.path.join(src, 'captions.tsv')
    with open(tsv, encoding='utf-8') as f:
        for row in csv.reader(f, delimiter='\t'):
            if len(row) < 4 or row[0].strip().startswith(('#', 'platform', 'system', 'النظام')): continue
            plat, name = row[0].strip(), os.path.splitext(row[1].strip())[0]
            caps[(plat, name)] = (row[2].strip(), row[3].strip())
    out_assets = os.path.join(ROOT, '_src', 'assets', 'g', app)
    shutil.rmtree(out_assets, ignore_errors=True)
    data = {'platforms': {}}
    for plat in ORDER + sorted(set(os.listdir(src)) - set(ORDER)):
        pdir = os.path.join(src, plat)
        if not os.path.isdir(pdir) or plat in skip: continue
        entry = {}
        for lang in ('ar', 'en'):
            ldir = os.path.join(pdir, lang)
            if not os.path.isdir(ldir): continue
            shots = []
            for fn in sorted(os.listdir(ldir)):
                if not fn.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')): continue
                name = os.path.splitext(fn)[0]
                dest_rel = f'g/{app}/{plat}/{lang}/{name}.webp'
                dest = os.path.join(ROOT, '_src', 'assets', dest_rel)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                box = '1600x1000>' if plat in WIDE else '700x1100>'
                subprocess.check_call(['magick', os.path.join(ldir, fn), '-resize', box, '-quality', '80', dest])
                w, h = size(dest)
                cap = caps.get((plat, name), ('', ''))[0 if lang == 'ar' else 1]
                shots.append([dest_rel, w, h, cap])
            if shots: entry[lang] = shots
        if 'ar' in entry and 'en' not in entry:   # no English UI: the Arabic screens, with English captions
            entry['en'] = [[src, w, h, caps.get((plat, os.path.splitext(os.path.basename(src))[0]), ('', ''))[1]]
                           for src, w, h, _ in entry['ar']]
            entry['ar_ui'] = True
        if entry:
            data['platforms'][plat] = entry
            print(plat, {l: len(v) for l, v in entry.items() if isinstance(v, list)})
    os.makedirs(os.path.join(ROOT, '_src', 'gallery'), exist_ok=True)
    with open(os.path.join(ROOT, '_src', 'gallery', f'{app}.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    # optional: --skip platform,platform  (a platform the app does not really support)
    args = sys.argv[1:]; skip = ()
    if '--skip' in args:
        i = args.index('--skip'); skip = tuple(args[i + 1].split(',')); del args[i:i + 2]
    if len(args) != 2: sys.exit(__doc__)
    main(args[0], os.path.expanduser(args[1]), skip)
