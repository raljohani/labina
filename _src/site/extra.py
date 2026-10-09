"""Shared pieces added in round 3: construction wall, privacy card, English content."""

# ---------- the Midmak "coming soon" wall ----------
def wall_svg(cls='wall', courses=7, cols=8, bw=40, bh=17, gap=3, laid_top=4):
    """A brick wall in running bond, its top course still being laid.
    The last brick of the top course is lowered into place (CSS animation)."""
    W = cols * (bw + gap) + gap
    H = courses * (bh + gap) + gap + 70           # headroom for the lowering brick + plumb line
    out = []
    top = 70
    for r in range(courses):                       # r=0 is the TOP course
        y = top + r * (bh + gap) + gap
        off = 0 if r % 2 == 0 else -(bw + gap) / 2
        x = gap + off
        i = 0
        while x < W:
            w = bw
            x0, x1 = max(x, gap), min(x + w, W - gap)
            if x1 - x0 > 6:
                if r == 0:
                    # top course is laid from the right (Arabic reading order)
                    order = cols - 1 - i
                    if order < laid_top:
                        out.append(f'<rect class="b" x="{x0:.1f}" y="{y:.1f}" width="{x1-x0:.1f}" height="{bh}" rx="2"/>')
                    elif order == laid_top:
                        out.append(f'<rect class="b drop" x="{x0:.1f}" y="{y:.1f}" width="{x1-x0:.1f}" height="{bh}" rx="2"/>')
                    else:
                        out.append(f'<rect class="ghost" x="{x0+0.75:.1f}" y="{y+0.75:.1f}" width="{x1-x0-1.5:.1f}" height="{bh-1.5}" rx="2"/>')
                else:
                    shade = ' alt' if (r * 3 + i) % 5 == 0 else ''
                    out.append(f'<rect class="b{shade}" x="{x0:.1f}" y="{y:.1f}" width="{x1-x0:.1f}" height="{bh}" rx="2"/>')
            x += bw + gap; i += 1
    # plumb line (فادن) beside the wall: string + bob
    px = W + 12
    out.append(f'<line class="plumb" x1="{px}" y1="0" x2="{px}" y2="{top+courses*(bh+gap)-40}"/>')
    out.append(f'<path class="bob" d="M{px-6} {top+courses*(bh+gap)-40} h12 l-6 12 z"/>')
    return f'<svg class="{cls}" viewBox="0 0 {W+24} {H}" aria-hidden="true">{"".join(out)}</svg>'

SOON = {
 'ar': dict(kicker='تحت البناء', title='الجدار يرتفع مدماكًا مدماكًا.',
            body='نضع الآن آخر المداميك في مدماك. اللقطات تُعلَّق هنا يوم الافتتاح.',
            badge='قريبًا', notify='أخبرني عند الإطلاق'),
 'en': dict(kicker='Under construction', title='The wall is rising, course by course.',
            body='We are laying the last courses of Midmak. Its screens will hang here on opening day.',
            badge='Coming soon', notify='Tell me when it launches'),
}

# ---------- privacy card ----------
PRIV = {
 'ar': {
  'mizan': [('البيانات المجموعة', 'لا شيء من بياناتك المالية'), ('الحساب', 'لا يوجد'), ('الإعلانات والتتبّع', 'لا يوجد'), ('أين تُحفظ', 'على جهازك، وiCloud اختياري')],
  'sana': [('البيانات المجموعة', 'لا شيء'), ('الإنترنت', 'لا يتصل بأي خادم'), ('الإعلانات والتتبّع', 'لا يوجد'), ('أين تُحفظ', 'على جهازك فقط')],
  'midmak': [('البيانات المجموعة', 'لا شيء'), ('الحساب', 'لا يوجد'), ('الإعلانات والتتبّع', 'لا يوجد'), ('أين تُحفظ', 'على جهازك وفي iCloud الخاص بك')],
 },
 'en': {
  'mizan': [('Data collected', 'None of your financial data'), ('Account', 'None'), ('Ads & tracking', 'None'), ('Stored', 'On your device; iCloud optional')],
  'sana': [('Data collected', 'None'), ('Internet', 'Never contacts a server'), ('Ads & tracking', 'None'), ('Stored', 'On your device only')],
  'midmak': [('Data collected', 'None'), ('Account', 'None'), ('Ads & tracking', 'None'), ('Stored', 'On your device and your own iCloud')],
 },
}
PRIV_NOTE = {
 'ar': {'mizan': 'على أندرويد ترسل مكتبة ML Kit من Google إحصاءات تشخيصية تقنية، لا تشمل بياناتك.'},
 'en': {'mizan': 'On Android, Google\'s ML Kit library sends technical diagnostics that never include your data.'},
}

def privacy_card(lang, k, href):
    rows = ''.join(f'<div class="pc-cell"><span>{a}</span><b>{b}</b></div>' for a, b in PRIV[lang][k])
    note = PRIV_NOTE[lang].get(k, '')
    head = 'ملصق الخصوصية' if lang == 'ar' else 'Privacy label'
    more = 'اقرأ السياسة كاملة' if lang == 'ar' else 'Read the full policy'
    return (f'<section class="pcard" aria-label="{head}"><div class="pc-head"><b>{head}</b>'
            f'<a href="{href}">{more}</a></div><div class="pc-grid">{rows}</div>'
            + (f'<p class="pc-note">{note}</p>' if note else '') + '</section>')

# ---------- English content ----------
APPS_EN = {
 'mizan': dict(no='1', name='Mizan', tag='Paste a bank SMS, and know what you can spend today.',
   meta='For iPhone and iPad, coming soon to Google Play',
   about=['An Arabic budgeting app. Paste a bank message and Mizan logs the expense for you, then tells you how much you can spend today.'],
   features=['Reads bank messages, statements (PDF and CSV) and receipt photos on your device.',
             'Correct a merchant\'s category once and it becomes a rule you can see and edit any time.',
             'Tracks your budgets, goals and commitments, from instalments and loans to savings circles, plus your zakat.',
             'Ask your ledger the way you think, like "restaurants this month", and export what you see to Excel.',
             'Your financial data never leaves your device; optional iCloud sync goes to your own account.'],
   caps=['What you can spend today', 'From bank message to expense', 'Budget caps', 'Zakat by nisab and hawl', 'Widgets']),
 'sana': dict(no='2', name='Sana', tag='The Beautiful Names of Allah: their meaning, evidence and your share.',
   meta='For iPhone, iPad and Apple Watch, coming soon to Google Play',
   about=['An app about the 99 Names of Allah that helps you know your Lord through His names: the meaning of each name, its evidence, and what it asks of you today.'],
   features=['A sky of names to explore, which turns into an ordered list whenever you need it.',
             'A tasbih counter in the Dynamic Island, on the Lock Screen and in Control Center, plus a Watch app.',
             '99 panels in Thuluth calligraphy; every quoted line carries its source, and verses follow the Madinah Mushaf.',
             'A daily name reminder, and widgets for the Home and Lock Screens.',
             'Works fully offline and collects no data about you.'],
   caps=['The sky of names', 'The name, written before you', 'Your share in practice', 'The mihrab card', 'Tasbih in the Dynamic Island']),
 'midmak': dict(no='3', name='Midmak', tag='The logbook for building your home, from excavation to keys.',
   meta='For iPhone and iPad, coming soon to the App Store',
   about=['An iPhone and iPad app for owners building their own home: every riyal recorded, every agreement kept, and your rights clear, from excavation to handing over the keys.'],
   features=['Expenses, contractors and daily labour in one logbook.',
             'Site photos, invoices and documents in one place.',
             'Log an expense by voice, with reminders for appointments and payments.',
             'Your data stays on your device and in your own iCloud.'],
   caps=[]),
}
DOCNAMES_EN = {'support': ('Support', 'Contact us and FAQs'), 'privacy': ('Privacy Policy', 'What the app collects, and does not'),
               'terms': ('Terms of Use', 'License and subscriptions'), 'accessibility': ('Accessibility', 'What the app supports today')}

SUPPORT_EN = {
 'mizan': ('Found a bug, a bank message Mizan did not recognise, or have a suggestion? Write to us. If it is about a bank message, send its text after removing any account or card number.', [
   ('Does Mizan read my messages?', 'On iPhone the app does not read your messages. You paste a bank message, or build your own Shortcuts automation that passes its text to Mizan (automatic logging is a Mizan Pro feature). The message is processed on your device.'),
   ('How do I move my data to a new device?', 'On iPhone, turn on iCloud sync in Settings and your data appears on your devices. Or create a backup in Settings, save the file, and open it on the new device.'),
   ('How do I cancel Mizan Pro?', 'iPhone Settings → your name → Subscriptions → Mizan → Cancel Subscription.'),
   ('How do I delete my data?', 'Settings → Danger zone → Delete all data. If iCloud sync is on, also remove the app\'s data from iCloud in your device settings.'),
   ('How do I request a refund?', 'Refunds are handled by Apple. Request one at <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a> with your Apple Account.')]),
 'sana': ('Found a mistake in the content, or have a question or suggestion? Write to us and we will reply soon. In the app, Settings → "Report a content error" opens a ready email with the app and content versions.', [
   ('The daily name reminder does not arrive', 'Turn the reminder on in Settings → Notifications, and make sure notifications for Sana are allowed in your device settings.'),
   ('How do I move my progress to a new device?', 'Settings → Your data → "Export progress" saves a file you move yourself; then "Import progress" on the new device. No account or server keeps your data.'),
   ('How do I show the tasbih in the Dynamic Island and Lock Screen?', 'In the Tasbih tab, tap the dotted-circle button in the top bar. Counting from the island needs iOS 17.2 or later.'),
   ('How do I add Sana widgets?', 'Touch and hold the Home Screen or Lock Screen → Edit → Add Widget → "Sana".'),
   ('How do I delete my data?', 'Settings → Your data → "Delete all my data". Everything is erased immediately and cannot be undone.')]),
 'midmak': ('We are here to help you document building your home. We usually reply within two working days.', [
   ('How do I start my real project?', 'More → Settings → Clear sample data and start my home.'),
   ('Is my data safe?', 'Yes. Your data is stored on your device and in your own iCloud account only, and we cannot see it.'),
   ('How do I cancel my subscription?', 'iPhone Settings → your name → Subscriptions → Midmak Plus → Cancel Subscription.'),
   ('I bought on another device. How do I restore?', 'More → Settings → My subscription → Restore Purchases.'),
   ('What happens to my data if my subscription ends?', 'Everything stays visible and exportable. Nothing is deleted.'),
   ('I have a gift code. Where do I use it?', 'More → Settings → My subscription → Have a gift code?'),
   ('How do I request a refund?', 'Refunds are handled by Apple. Request one at <a href="https://reportaproblem.apple.com">reportaproblem.apple.com</a> with your Apple Account.')]),
}

MIDMAK_PRIVACY_EN = '''<h1>Privacy Policy</h1>
<p class="date">Last updated: October 9, 2026</p>
<p>Midmak is an app for documenting the building of your home. Your privacy is part of its foundation, so it was designed to work on your device.</p>
<h2>What we collect</h2>
<p>We collect no personal data and have no server that receives your data. Everything you record (expenses, contractors, photos, documents and more) is stored on your device, and in your own iCloud account if you turn on sync, and we cannot see it.</p>
<h2>Permissions</h2>
<ul>
<li><b>Camera:</b> to photograph invoices, documents and the site.</li>
<li><b>Microphone and speech recognition:</b> to log an expense by voice.</li>
<li><b>Location:</b> to show "Visit mode" when you are at the building site, and to time-stamp photos.</li>
<li><b>Photos:</b> to attach pictures from your library.</li>
<li><b>Notifications:</b> to remind you of appointments and payments.</li>
</ul>
<p>All of this is processed on your device only and is not sent to anyone.</p>
<h2>Purchases</h2><p>Subscriptions and purchases are handled by Apple; we do not receive payment details.</p>
<h2>Sharing</h2><p>We share no data with any third party, show no ads, and do not track you.</p>
<h2>Your rights</h2><p>Your data is yours: you can export or delete it in the app at any time, and deleting the app removes it from your device.</p>
<h2>Children</h2><p>The app is not directed to children, and we collect no data from any user.</p>
<h2>Changes</h2><p>If this policy changes, we update its date above before releasing any version affected by it.</p>'''

SANA_A11Y_EN = '''<h1>Accessibility</h1>
<p>We want everyone to read the Beautiful Names comfortably, whatever their eyesight or way of using the device. This is what the app supports today on iPhone and iPad, and what we are working on.</p>
<h2>Larger text</h2>
<ul><li>The app follows the text size you chose in your device settings, including the larger accessibility sizes.</li>
<li>In Settings → "Text size and reading comfort" you can pick a size for Sana, a line height for Arabic that keeps diacritics from crowding, and an extra boost for reading pages only.</li>
<li>At large sizes the sky of names turns into an easy-to-read list.</li></ul>
<h2>Reduce Motion</h2>
<ul><li>With Reduce Motion on, decorative animations stop and everything appears in place.</li>
<li>The rotating sky of names becomes a fixed list.</li>
<li>You can turn off all haptics, or only the tasbih haptics, in Settings → "Reminders and interaction".</li></ul>
<h2>Night mode</h2>
<ul><li>Sana's colours are dark by default and follow your time of day; you can fix them to "Always night" or "Light paper" in Settings → "Appearance and reading".</li></ul>
<h2>VoiceOver</h2>
<ul><li>Buttons have readable Arabic labels, calligraphy panels are read by name, and the tasbih counts with a "Count" action.</li>
<li>With VoiceOver, names are shown as an ordered list instead of the sky.</li>
<li>We are still testing the whole app with VoiceOver and Voice Control; if you find a spot that is not read, tell us.</li></ul>
<h2>Numerals</h2>
<ul><li>Choose Eastern Arabic (١٢٣) or Western (123) numerals in Settings → "Advanced".</li></ul>
<h2>What we are improving</h2>
<ul><li>Some secondary text, such as footnotes and reference numbers, has lighter contrast than recommended, and we are raising it.</li></ul>'''

NATURE_EN = {
 'mizan': 'Mizan is a tool for organising your spending and budget. Its figures and estimates, including the zakat calculation, are based on what you enter; they help you understand, and are not financial advice or a religious ruling. Consult qualified people for important financial and religious decisions.',
 'sana': 'Sana is an educational reference for the Beautiful Names of Allah. We have worked to document meanings and evidence carefully; if you find a mistake, tell us so we can correct it.',
 'midmak': 'Midmak is a logbook for documenting and organising the building of your home. Its figures and alerts are based on what you enter, and it does not replace your supervising engineer, a lawyer, or signed contracts.',
}
