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

FILMS = {
 'mizan': dict(secs=30,
   ar=dict(kicker='العرض', hook='٢٧ الشهر… وين راحت فلوسك؟', body='ميزان في ثلاثين ثانية: من رسالة البنك، إلى كم تقدر تصرف اليوم.', label='العرض الترويجي لتطبيق ميزان'),
   en=dict(kicker='The film', hook='It is the 27th. Where did the money go?', body='Mizan in thirty seconds: from a bank message to what you can spend today.', label='Mizan promo film')),
 'midmak': dict(secs=38,
   ar=dict(kicker='العرض', hook='بيتك يرتفع… وفلوسك وين؟', body='مدماك في ثمانٍ وثلاثين ثانية: كل ريال مسجّل، وكل اتفاق محفوظ، من الحفر إلى المفتاح.', label='العرض الترويجي لتطبيق مدماك'),
   en=dict(kicker='The film', hook='The house is rising. Where is the money going?', body='Midmak in thirty-eight seconds: every riyal recorded, every agreement kept, from excavation to keys.', label='Midmak promo film')),
}

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
   meta='For iPhone and iPad',
   about=['An iPhone and iPad app for owners building their own home: every riyal recorded, every agreement kept, and your rights clear, from excavation to handing over the keys.'],
   features=['Expenses, contractors and daily labour in one logbook.',
             'Site photos, invoices and documents in one place.',
             'Log an expense by voice, with reminders for appointments and payments.',
             'Your data stays on your device and in your own iCloud.'],
   caps=['Every riyal recorded', 'Before you pay', 'The contractor\'s account', 'The house wall', 'Reading the invoice']),
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

# ---------- Sakan: a TV app, shipped as an APK from its releases page (no store) ----------
SAKAN_VER = '3.2.3'   # bump on each release in raljohani/sakan-tv: the APK link and /sakan/apk/ point at this version
SAKAN_REL = 'https://github.com/raljohani/sakan-tv/releases/latest'
SAKAN_APK = f'https://github.com/raljohani/sakan-tv/releases/download/v{SAKAN_VER}/sakan-{SAKAN_VER}.apk'

PRIV['ar']['sakan'] = [('البيانات المجموعة', 'لا شيء'), ('الحساب', 'لا يوجد'), ('الإعلانات والتتبّع', 'لا يوجد'), ('أين تُحفظ', 'على التلفاز أو الحاسوب فقط')]
PRIV['en']['sakan'] = [('Data collected', 'None'), ('Account', 'None'), ('Ads & tracking', 'None'), ('Stored', 'On your TV or PC only')]
PRIV_NOTE['ar']['sakan'] = 'يعمل دون إنترنت، ويتصل في ثلاثة مواضع فقط دون أن يرسل شيئًا عنك: Open-Meteo للطقس، وESPN للمباريات، وصفحة إصداراته على GitHub للتحديث.'
PRIV_NOTE['en']['sakan'] = 'It works offline, and connects in three places only, sending nothing about you: Open-Meteo for weather, ESPN for matches, and its GitHub releases page for updates.'

INSTALL = {
 'ar': dict(h='التحميل والتثبيت',
   intro=f'سَكَن لا يُباع في متجر: يُنزَّل ملفًا (APK) من صفحة إصداراته، ثم يحدّث نفسه من داخله. يعمل على أندرويد ٧ فأحدث (Android TV وGoogle TV)، والإصدار الحالي <bdi dir="ltr">{SAKAN_VER}</bdi>.',
   steps=['ثبّت تطبيق Downloader من Google Play على التلفاز.',
          'افتحه واكتب في خانة العنوان <a href="apk/" class="latin">labina.app/sakan/apk</a>، فيتحمّل سَكَن على التلفاز نفسه ويظهر زر التثبيت. وإن طلب التلفاز السماح بالتثبيت من مصدر غير معروف، فاسمح لـ Downloader وحده.',
          'من إعدادات التلفاز: تفضيلات الجهاز ← شاشة التوقف ← اختر «سَكَن»، واضبط وقت البدء.',
          'بعض التلفزيونات تخفي صفحة شاشة التوقف أو تمنع البرامج المثبّتة من خارج متجرها؛ خطواتها في <a href="support/">صفحة الدعم</a>.'],
   alt='وإن لم يكن في التلفاز Google Play: حمّل الملف على جوالك أو حاسوبك من الرابط نفسه، وانسخه إلى فلاش، وافتحه من مدير الملفات في التلفاز.',
   win='ونسخة ويندوز ١٠ و١١ (شاشة توقف بالواجهة نفسها) نرسلها لمن يطلبها بالبريد.', win_subj='نسخة سكن لويندوز'),
 'en': dict(h='Download and install',
   intro=f'Sakan is not sold in a store: you download it as a file (APK) from its releases page, and it then updates itself from inside. It runs on Android 7 or later (Android TV and Google TV). The current version is {SAKAN_VER}.',
   steps=['Install the Downloader app from Google Play on the TV.',
          'Open it and type <a href="../../sakan/apk/">labina.app/sakan/apk</a> in the address box. Sakan downloads on the TV itself and an Install button appears. If the TV asks to allow installs from unknown sources, allow Downloader only.',
          'In the TV settings: Device Preferences → Screen saver → choose "Sakan", and set when it starts.',
          'Some TVs hide the screen saver page or block apps installed outside their store; see the steps on the <a href="support/">support page</a>.'],
   alt='If the TV has no Google Play: download the file on your phone or computer from the same address, copy it to a USB stick, and open it from a file manager on the TV.',
   win='A Windows 10 and 11 version (a screen saver with the same interface) is sent by email on request.', win_subj='Sakan for Windows'),
}

SAKAN_SUPPORT = '''<h1>الدعم</h1>
<p>وجدت خللًا في مشهد، أو وقتًا لا يطابق مدينتك، أو عندك اقتراح؟ راسلنا، واذكر طراز التلفاز ورقم إصدار سَكَن (من «عن سَكَن» في إعداداته).</p>
{contact}
<h2>أسئلة شائعة</h2>
<details><summary>كيف أثبّت سَكَن على التلفاز؟</summary><p>ثبّت تطبيق Downloader من Google Play على التلفاز، وافتحه واكتب <a href="../apk/">labina.app/sakan/apk</a>، ثم اضغط «تثبيت». وإن طلب التلفاز السماح بالتثبيت من مصدر غير معروف، فاسمح لـ Downloader وحده. ثم اختر سَكَن من الإعدادات ← تفضيلات الجهاز ← شاشة التوقف.</p></details>
<details><summary>ما عندي Downloader، أو التلفاز ما فيه Google Play</summary><p>حمّل الملف على جوالك أو حاسوبك من <a href="../apk/">labina.app/sakan/apk</a> وانسخه إلى فلاش، ثم صِل الفلاش بالتلفاز وافتح الملف من مدير الملفات، واسمح لمدير الملفات وحده بالتثبيت.</p></details>
<details><summary>التلفاز ما فيه صفحة لشاشة التوقف</summary><p>بعض التلفزيونات تخفيها. يحتاج سَكَن حينها إذنًا يُمنح مرة واحدة من حاسوب عليه adb والتلفاز على الشبكة نفسها، بعد تفعيل تصحيح الأخطاء من خيارات المطوّر:</p><p class="latin" dir="ltr">adb connect &lt;TV-IP&gt;:5555<br>adb shell pm grant app.sakan.tv android.permission.WRITE_SECURE_SETTINGS</p><p>ثم من داخل سَكَن: «اجعلها شاشة التوقف». ويُسحب الإذن متى شئت بـ <span class="latin">pm revoke</span>.</p></details>
<details><summary>تلفاز TCL لا يبدأ شاشة التوقف عند الخمول</summary><p>نظامه يمنع البرامج المثبّتة من خارج متجره من العمل تلقائيًا. من الحاسوب نفسه بعد <span class="latin">adb connect</span>:</p><p class="latin" dir="ltr">adb shell appops set app.sakan.tv APP_AUTO_START allow</p></details>
<details><summary>كيف أفعّل التنبيه فوق القنوات ومؤقت المشاهدة؟</summary><p>يحتاجان إذن الظهور فوق التطبيقات، يُمنح مرة واحدة:</p><p class="latin" dir="ltr">adb shell appops set app.sakan.tv SYSTEM_ALERT_WINDOW allow</p><p>ثم فعّلهما من إعدادات سَكَن. وكلاهما متوقف حتى تفعّله.</p></details>
<details><summary>كيف أضيف المواعيد وصور الألبوم والملصقات؟</summary><p>من الإعدادات ← الجوال ← «شغّل رابط الجوال»، ثم امسح الرمز بكاميرا جوالك وهو على شبكة الواي فاي نفسها. تُفتح صفحة سَكَن في المتصفح دون تطبيق ولا حساب، ويُقفل الرابط وحده بعد نصف ساعة دون استخدام.</p></details>
<details><summary>كيف أحدّث سَكَن؟</summary><p>من الإعدادات ← «تحديث البرنامج». أو ثبّت ملف الإصدار الأحدث فوقه، فتبقى إعداداتك ومواعيدك.</p></details>
<details><summary>أوقات الصلاة تختلف عن مسجدنا</summary><p>يحسب سَكَن الأوقات بتقويم أم القرى (الفجر عند ١٨٫٥ درجة، والعشاء بعد المغرب بتسعين دقيقة، ومئة وعشرين في رمضان). ويمكنك تعديل كل صلاة بالدقائق من إعدادات الصلاة.</p></details>
<details><summary>هل توجد نسخة لويندوز؟</summary><p>نعم، شاشة توقف لويندوز ١٠ و١١ بالواجهة نفسها، لا تحتاج صلاحيات مدير. نرسلها لمن يطلبها بالبريد.</p></details>
<details><summary>كيف أحذف سَكَن وبياناته؟</summary><p>إعدادات التلفاز ← التطبيقات ← سَكَن ← إلغاء التثبيت. إعداداتك ومواعيدك وصورك محفوظة في التلفاز وحده، فتُحذف معه.</p></details>'''

SAKAN_PRIVACY = '''<h1>سياسة الخصوصية</h1>
<p class="date">آخر تحديث: ٢٦ أكتوبر ٢٠٢٦</p>
<p>سَكَن شاشات انتظار للتلفاز والحاسوب، صُنع ليعمل على جهازك. لا حسابات فيه ولا إعلانات ولا تتبّع، ولا نملك خادمًا يستقبل بياناتك.</p>
<h2>ما يُحفظ وأين</h2>
<p>إعداداتك ومواعيدك وملصقاتك وصور الألبوم تُحفظ على التلفاز (أو الحاسوب) نفسه فقط، ولا تُرفع إلى أي خدمة سحابية، وتُحذف بحذف التطبيق. والنسخة الاحتياطية ملف تحفظه أنت على جوالك.</p>
<h2>متى يتصل بالإنترنت</h2>
<p>يعمل سَكَن كاملًا دون إنترنت، ويتصل في ثلاثة مواضع فقط، ولا يرسل فيها شيئًا عنك:</p>
<ul>
<li><b>الطقس:</b> يطلب مشهد الطقس توقعات مدينتك من Open-Meteo بإحداثيات المدينة التي اخترتها، مرة كل ساعة افتراضًا، دون مفتاح ولا ملفات تعريف. وآخر قراءة تُحفظ على الجهاز.</li>
<li><b>الملعب:</b> يجلب جدول المباريات وشعارات الأندية من ESPN حين يُعرض.</li>
<li><b>التحديث:</b> يسأل صفحة إصدارات سَكَن على GitHub عن إصدار جديد حين تفتح سَكَن (مرة كل ست ساعات على الأكثر) وحين تطلبه.</li>
</ul>
<p>هذه الطلبات تصل إلى تلك الجهات كأي تصفح عادي للإنترنت، وتخضع لسياساتها.</p>
<h2>رابط الجوال</h2>
<p>حين تشغّله، يفتح سَكَن خادمًا صغيرًا على شبكة البيت وحدها، برمز عشوائي يتغيّر كل تشغيل، ويُقفل بعد نصف ساعة دون استخدام. ما ترسله من جوالك (مواعيد وصور وملاحظات) يذهب إلى التلفاز مباشرة لا عبر الإنترنت، والصور تُصغَّر على جوالك قبل إرسالها.</p>
<h2>الأذونات على التلفاز</h2>
<ul>
<li><b>الظهور فوق التطبيقات:</b> للتنبيه قبل الأذان ومؤقت المشاهدة، وكلاهما متوقف حتى تفعّله.</li>
<li><b>إعدادات النظام الآمنة</b> (إن منحتها بنفسك): لضبط مدة الخمول والنوم وشاشة التوقف فقط.</li>
<li><b>التشغيل عند الإقلاع وتثبيت الحزم:</b> لإعادة التنبيهات بعد تشغيل التلفاز، ولتثبيت تحديثات سَكَن نفسه.</li>
</ul>
<h2>مؤقت المشاهدة</h2>
<p>الرقم السري لا يُحفظ نفسه، بل بصمته المملّحة على الجهاز.</p>
<h2>الأطفال</h2>
<p>لا نجمع بيانات من أي مستخدم، صغيرًا كان أو كبيرًا.</p>
<h2>التغييرات</h2>
<p>إن تغيّرت هذه السياسة، حدّثنا تاريخها أعلاه قبل نشر أي إصدار يتأثر بها.</p>
<h2>التواصل</h2>'''

SAKAN_PRIVACY_EN = '''<h1>Privacy Policy</h1>
<p class="date">Last updated: October 26, 2026</p>
<p>Sakan is a set of ambient screens for the TV and PC, made to work on your device. It has no accounts, no ads and no tracking, and we have no server that receives your data.</p>
<h2>What is stored, and where</h2>
<p>Your settings, appointments, notes and album photos are stored on the TV (or PC) itself only, are never uploaded to any cloud service, and are deleted when you remove the app. A backup is a file you keep on your own phone.</p>
<h2>When it goes online</h2>
<p>Sakan works fully offline, and connects in three places only, sending nothing about you:</p>
<ul>
<li><b>Weather:</b> the weather scene requests your city's forecast from Open-Meteo using the coordinates of the city you chose, once an hour by default, with no key and no cookies. The last reading is kept on the device.</li>
<li><b>Matches:</b> the stadium scene fetches fixtures and club crests from ESPN when it is shown.</li>
<li><b>Updates:</b> it asks Sakan's GitHub releases page for a new version when you open Sakan (at most once every six hours) and when you ask it to.</li>
</ul>
<p>These requests reach those services like any ordinary web browsing, under their own policies.</p>
<h2>Phone link</h2>
<p>When you turn it on, Sakan opens a small server on your home network only, with a random code that changes each time and that closes after thirty minutes without use. What you send from your phone (appointments, photos, notes) goes straight to the TV, not over the internet, and photos are resized on your phone before sending.</p>
<h2>Permissions on the TV</h2>
<ul>
<li><b>Display over other apps:</b> for the prayer alert and the viewing timer, both off until you turn them on.</li>
<li><b>Secure system settings</b> (only if you grant it yourself): to set the idle, sleep and screen saver timings only.</li>
<li><b>Start at boot and install packages:</b> to restore alerts after the TV starts, and to install Sakan's own updates.</li>
</ul>
<h2>Viewing timer</h2><p>The PIN itself is never stored, only its salted hash on the device.</p>
<h2>Children</h2><p>We collect no data from any user, young or old.</p>
<h2>Changes</h2><p>If this policy changes, we update its date above before releasing any version affected by it.</p>'''

SAKAN_TERMS = '''<h1>شروط الاستخدام</h1>
<p class="date">تاريخ السريان: ٢٦ أكتوبر ٢٠٢٦</p>
<p>باستخدامك «سَكَن» توافق على هذه الشروط.</p>
<h2>الترخيص</h2>
<p>سَكَن مجاني للاستخدام الشخصي في البيت، ويُقدَّم كما هو دون ضمان. لا تبعه، ولا تُعِد توزيعه معدّلًا.</p>
<h2>التحميل</h2>
<p>نزّله من labina.app أو من صفحة إصداراته الرسمية فقط. النسخ من مصادر أخرى قد تكون معدّلة، والتلفاز لا يقبل تحديثًا لا يحمل توقيع سَكَن.</p>
<h2>طبيعة التطبيق</h2>
<p>أوقات الصلاة تُحسب بتقويم أم القرى وقد تختلف عن أذان مسجدك، والتاريخ الهجري قد يختلف بيوم عن الرؤية، والطقس والمباريات تأتي من مصادرها ولا نضمن دقتها.</p>
<h2>الأذونات وإعدادات التلفاز</h2>
<p>ما تمنحه لسَكَن من أذونات عبر adb تمنحه باختيارك، ويمكنك سحبه متى شئت. ونصائح التثبيت في صفحة الدعم إرشادية؛ اتبعها على مسؤوليتك.</p>
<h2>بياناتك</h2>
<p>بياناتك ملكك وتبقى على جهازك. التفاصيل في <a href="../privacy/">سياسة الخصوصية</a>.</p>
<h2>الاستخدام المقبول</h2>
<p>لا تستخدم التطبيق في ما يخالف الأنظمة، ولا تحاول تعطيله.</p>
<h2>التغييرات</h2>
<p>قد نحدّث هذه الشروط، ونغيّر تاريخ السريان أعلاه عند ذلك.</p>
<h2>التواصل</h2>'''

SAKAN_TERMS_EN = '''<h1>Terms of Use</h1>
<p class="date">Effective: October 26, 2026</p>
<p>By using Sakan you agree to these terms.</p>
<h2>License</h2><p>Sakan is free for personal use at home and is provided as is, without warranty. Do not sell it or redistribute modified copies.</p>
<h2>Downloads</h2><p>Download it only from labina.app or its official releases page. Copies from elsewhere may be modified, and the TV will not accept an update that does not carry Sakan's signature.</p>
<h2>What the app is</h2><p>{nature}</p>
<h2>Permissions and TV settings</h2><p>Any permission you grant Sakan through adb is your choice, and you can revoke it at any time. The installation tips on the support page are guidance; follow them at your own risk.</p>
<h2>Your data</h2><p>Your data is yours and stays on your device. See the <a href="../privacy/">Privacy Policy</a>.</p>
<h2>Acceptable use</h2><p>Do not use the app against the law, or try to disrupt it.</p>
<h2>Changes</h2><p>We may update these terms, and will change the effective date above when we do.</p>
<h2>Contact</h2>'''

APPS_EN['sakan'] = dict(no='4', name='Sakan', tag='The home screen for when nobody is watching.',
   meta='For Android TV and Windows',
   about=['A screen saver for Android TVs that knows your day: its scenes change with the prayer times in your city, show the Hijri and Gregorian calendar, the weather, the matches and family photos, and a calm alert appears over any channel when the adhan is near. It also comes as a screen saver for Windows.'],
   features=['Scenes for your day: the city panel and prayer times, the day dial, the Hijri and Gregorian calendar, the weather, the verse of the day, Ramadan, and the quiet night.',
             'A 24-hour ring: each part of the day has its scenes, and the parts move with the prayer times without you setting them.',
             'The stadium: your team\'s matches and the league table, and "On air" when matches overlap.',
             'A home album, notes and appointments you write from your phone over a link on your home network, with no app and no account.',
             'A calm alert over any channel before the adhan, and a viewing timer with a PIN; both are off until you turn them on.',
             'Prayer times by the Umm al-Qura calendar, calculated on the device itself. No ads, no accounts, no tracking.'],
   caps=['The city panel', 'The day dial', 'The calendar', 'The weather', 'Ramadan', 'The verse of the day'])
APPS_EN['mihrab'] = dict(no='5', name='Mihrab', tag='Prayer times and iqama on the mosque screen, read from the back row.',
   meta='Coming soon to Android TV, Fire TV and Windows',
   about=['A TV app that shows the prayer times, the adhan and the iqama in mosques, homes and organisations. It reads from the back of the mosque in a second, works offline once set up, and is managed from a phone.'],
   features=['Umm al-Qura prayer times, and an iqama rule for each prayer: minutes after the adhan, or a fixed time.',
             'Every moment of the day on screen: the adhan approaching, the adhan, the countdown to the iqama, the prayer, and Friday with both adhans and the sermon.',
             'The seasons: Ramadan with iftar, imsak and taraweeh, both Eids, the day of Arafah, and Ashura.',
             'Mosque announcements, funerals by name, and the eclipse and rain prayers at their time.',
             'Themes in the spirit of mosques: Madani, Najdi, Andalusi, Ottoman and Modern, or one built from your organisation\'s colour.',
             'Set it up from a phone, with the remote on the TV itself, or from a USB stick for a mosque with no network.'],
   caps=['The adhan approaching', 'The adhan', 'Countdown to the iqama', 'Mosque announcements', 'Ramadan', 'Eid'])
DOCNAMES_EN_SUB = {'sakan': {'terms': 'License and downloads'}}
SUPPORT_EN['sakan'] = ('Found a glitch in a scene, a time that does not match your city, or have a suggestion? Write to us, and mention your TV model and Sakan\'s version (from "About Sakan" in its settings).', [
   ('How do I install Sakan on the TV?', 'Install the Downloader app from Google Play on the TV, open it, type <a href="../../../sakan/apk/">labina.app/sakan/apk</a>, then press Install. If the TV asks to allow installs from unknown sources, allow Downloader only. Then choose Sakan in Settings → Device Preferences → Screen saver.'),
   ('I do not have Downloader, or the TV has no Google Play', 'Download the file on your phone or computer from <a href="../../../sakan/apk/">labina.app/sakan/apk</a> and copy it to a USB stick, then plug it into the TV and open the file from a file manager, allowing that file manager alone to install.'),
   ('My TV has no screen saver page', 'Some TVs hide it. Sakan then needs a permission granted once from a computer with adb on the same network, after turning on debugging in Developer options:<br><span class="latin">adb connect &lt;TV-IP&gt;:5555<br>adb shell pm grant app.sakan.tv android.permission.WRITE_SECURE_SETTINGS</span><br>Then, inside Sakan, choose to make it the screen saver. You can revoke the permission any time with <span class="latin">pm revoke</span>.'),
   ('A TCL TV does not start the screen saver when idle', 'Its system blocks apps installed outside its store from starting on their own. From the same computer, after <span class="latin">adb connect</span>:<br><span class="latin">adb shell appops set app.sakan.tv APP_AUTO_START allow</span>'),
   ('How do I turn on the alert over channels and the viewing timer?', 'They need the display-over-other-apps permission, granted once:<br><span class="latin">adb shell appops set app.sakan.tv SYSTEM_ALERT_WINDOW allow</span><br>Then turn them on in Sakan\'s settings. Both are off until you do.'),
   ('How do I add appointments, album photos and notes?', 'Settings → Phone → "Start the phone link", then scan the code with your phone camera while on the same Wi-Fi. Sakan\'s page opens in the browser with no app and no account, and the link closes itself after thirty minutes without use.'),
   ('How do I update Sakan?', 'Settings → "Update the app". Or install the newer file over it; your settings and appointments stay.'),
   ('Prayer times differ from our mosque', 'Sakan uses the Umm al-Qura calendar (Fajr at 18.5°, Isha ninety minutes after Maghrib, and one hundred and twenty in Ramadan). You can adjust each prayer by minutes in the prayer settings.'),
   ('Is there a Windows version?', 'Yes: a screen saver for Windows 10 and 11 with the same interface, needing no administrator rights. We send it by email on request.'),
   ('How do I remove Sakan and its data?', 'TV Settings → Apps → Sakan → Uninstall. Your settings, appointments and photos live on the TV only, so they go with it.')])
NATURE_EN['sakan'] = 'Prayer times are calculated by the Umm al-Qura calendar and may differ from your mosque\'s adhan; the Hijri date may differ by a day from the sighting; and weather and match data come from their sources, whose accuracy we cannot guarantee.'
