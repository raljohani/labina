# سياسة الخصوصية لتطبيق «سطر»

آخر تحديث: ١٣ نوفمبر ٢٠٢٦

## الخلاصة

«سطر» دفتر يعمل على جهازك. كل ما تكتبه وترسمه وتلصقه وتسجّله يبقى على جهازك، ولا حساب فيه، ولا إعلانات، ولا خوادم لنا. يتصل التطبيق بالإنترنت في حالة واحدة تختارها أنت: تنزيل ملفات التعرّف على خط اليد من Google، كما هو مفصّل أدناه.

## ما يحفظه التطبيق، وأين

- **ما تكتبه وترسمه، والصور التي تلصقها، وإعدادات دفاترك:** تُحفظ في مساحة التطبيق الخاصة على جهازك فقط.
- **التسجيل الصوتي (اختياري):** حين تختار «تسجيل صوتي» يطلب التطبيق إذن الميكروفون، ويسجّل ما دمت ترى شريط التسجيل على الشاشة. يُحفظ التسجيل ملفًّا على جهازك ملصقًا في صفحته، ولا يُرسل إلى أي جهة. لا يسجّل التطبيق شيئًا في الخلفية.
- **مكان كتابة الصفحة (اختياري):** إن فعّلت «حفظ مكان كتابة الصفحات»، يقرأ التطبيق موقعك التقريبي (على مستوى الحي أو المدينة) لحظة الكتابة. ثم يحفظ اسم المكان مع الصفحة على جهازك. تحويل الإحداثيات إلى اسم مكان تجريه خدمة الأماكن المدمجة في نظام Android، وتخضع لسياسة الجهة المزوّدة لها. التطبيق نفسه لا يرسل موقعك إلى أي جهة. ويمكنك إيقاف هذا الخيار في أي وقت.
- **الكاميرا (اختيارية):** إن فعّلت «ضوء الغرفة الحقيقي» وأذنت باستخدام الكاميرا، تلتقط الكاميرا الأمامية صورة صغيرة جدًا مرتين في الثانية ما دام التطبيق ظاهرًا. لا يقرأ التطبيق منها إلا سطوعها ليعرف جهة الضوء، ثم يمحوها فورًا. لا تُحفظ أي صورة ولا تُرسل إلى أي جهة، ولا يُتعرَّف على الوجوه. ويتوقف ذلك عند إيقاف الخيار أو مغادرة التطبيق.
- **البصمة:** عند قفل دفتر يطلب التطبيق من النظام التحقق منك. لا يرى التطبيق بصمتك ولا يحفظها.
- **قراءة النص من الصور:** تجري على جهازك بمحرّك مضمَّن في التطبيق، بلا اتصال.

## متى يتصل التطبيق بالإنترنت

التطبيق يحمل إذن الإنترنت لسبب واحد: **التعرّف على خط اليد** (خيار «اجعل خط يدي قابلًا للبحث» و«ذكاء الحبر»)، وهو مطفأ إلى أن تفعّله.

- **تنزيل النماذج بطلبك:** حين تفعّل الخيار ينزّل التطبيق ملف التعرّف لكل لغة مرة واحدة من خوادم Google (مكتبة ML Kit). لا يُنزَّل شيء قبل ذلك.
- **التعرّف نفسه على الجهاز:** خطّك وصفحاتك لا تُرسل إلى Google ولا إلى أي جهة. ما يُقرأ من خطك يُحفظ مع الصفحة على جهازك للبحث فقط.
- **ما ترسله مكتبة ML Kit إلى Google:** المكتبة ترسل إلى Google بيانات تشغيل عن استعمالها هي، لا عن محتواك: معلومات عن الجهاز والتطبيق (مثل الطراز وإصدار النظام وإصدار التطبيق)، ومعرّفًا خاصًّا بتثبيت المكتبة، وأحداث التنزيل والتشغيل، ومقاييس الأداء، ورموز الأخطاء. تستعملها Google لتشخيص المكتبة وتحسينها، وتخضع لسياسة خصوصية Google. تفصيلها في صفحة «ML Kit Android data disclosure» لدى Google.
- إن لم تفعّل التعرّف على خط اليد فلا يتصل التطبيق بالإنترنت.

## الأذونات التي يحملها التطبيق

| الإذن | لماذا |
|---|---|
| الإنترنت، وحالة الشبكة | تنزيل ملفات التعرّف على خط اليد بطلبك، ومعرفة أن الجهاز متصل ليُقال لك «ينتظر الاتصال» |
| الميكروفون | التسجيل الصوتي، حين تختاره |
| الكاميرا | «ضوء الغرفة الحقيقي»، حين تفعّله |
| الموقع التقريبي | «حفظ مكان كتابة الصفحات»، حين تفعّله |
| البصمة | قفل الدفاتر |
| الاهتزاز | ملمس الورق والنقرات |
| البقاء مستيقظًا، والتشغيل بعد الإقلاع، والخدمة الأمامية | تطلبها مكتبات النظام التي يعتمد عليها ودجت الشاشة الرئيسية (WorkManager وGlance) لتحديث الودجت. لا يشغّل التطبيق بها شيئًا آخر |

## ما لا يفعله التطبيق

- لا إعلانات، ولا أدوات تحليل لنا، ولا تتبع.
- لا حساب، ولا خوادم لنا: لا نستقبل منك أي بيانات.
- لا يبيع أي بيانات ولا يشاركها مع أي طرف، سوى ما ترسله مكتبة ML Kit إلى Google عن تشغيلها، كما سبق.

## التصدير والمشاركة

- حين تصدّر صفحة ملفَّ PDF وتختار مشاركته، يُسلَّم الملف إلى التطبيق الذي تختاره أنت. وما يحدث له بعد ذلك يخضع لذلك التطبيق.
- حين تشارك صورة أو نصًّا من تطبيق آخر إلى «سطر»، يُلصق في الدفتر الذي تختاره ويبقى على جهازك.

## النسخ الاحتياطي

- **نسخة «سطر» بملف:** من الإعدادات تحفظ نسخة من دفاترك في ملف واحد مشفَّر بكلمة تختارها، حيث تشاء. التطبيق لا يرفعه إلى أي مكان.
- **نسخة النظام:** قد ينسخ نظام Android بيانات التطبيق ضمن نسخة الجهاز الاحتياطية، إن كانت مفعّلة في إعدادات جهازك. وهذا يتم وفق إعداداتك وحسابك لدى مزوّد النظام.
- **الدفاتر المختومة مستثناة:** صفحات أي دفتر مختوم بالشمع، وصوره وتسجيلاته، لا تدخل النسخة الاحتياطية السحابية ولا النقل إلى جهاز جديد، فتبقى على جهازك وحده. الختم يمنع فتح الدفتر في التطبيق ويبقيه خارج نسخ النظام، وليس تشفيرًا لملفاته على الجهاز.

## حذف بياناتك

حذف التطبيق يحذف كل ما حفظه، ومنه ملفات التعرّف المنزَّلة. ويمكنك حذف دفتر بعينه من «تعديل الغلاف»، وإيقاف التعرّف على خط اليد من الإعدادات.

## الأطفال

التطبيق مناسب للجميع، وليس موجَّهًا للأطفال خصوصًا. لا نجمع بيانات من أحد.

## التواصل

للأسئلة عن هذه السياسة: [يُضاف بريد المطوّر قبل النشر].

---

# Satr Privacy Policy

Last updated: 13 November 2026

**In short:** Satr is a notebook that lives on your device. Everything you write, draw, paste and record stays on your device. There is no account, no advertising and we run no servers. The app connects to the internet in one case that you choose: downloading handwriting-recognition files from Google, as described below.

- **Your writing, drawings, photos and notebook settings** are stored only in the app's private storage on your device.
- **Voice notes (optional):** when you choose "Voice note" the app asks for the microphone permission and records while the recording bar is on screen. The recording is saved as a file on your device, attached to its page, and is never sent anywhere. Nothing is recorded in the background.
- **Where you wrote a page (optional):** if you turn on "Remember where pages were written", the app reads your approximate location (neighbourhood or city level) when you write. It then saves the place name with the page on your device. Turning coordinates into a place name is done by Android's built-in geocoding service, under its provider's policy. The app itself never sends your location anywhere. You can turn this off at any time.
- **Camera (optional):** if you turn on "Real room light" and allow the camera, the front camera takes a tiny picture twice a second while the app is visible. The app reads only its brightness to tell where the light comes from, then discards it at once. No picture is saved or sent, and no faces are recognised.
- **Fingerprint:** when you lock a notebook, the app asks the system to verify you. The app never sees or stores your fingerprint.
- **Text in pictures** is read on your device by an engine bundled with the app, with no connection.

**When the app uses the internet.** The app holds the internet permission for one reason: **handwriting recognition** ("Make my handwriting searchable" and smart ink), which is off until you turn it on.

- **Models are downloaded at your request:** when you turn the option on, the app downloads the recognition file for each language once from Google's servers (the ML Kit library). Nothing is downloaded before that.
- **Recognition itself runs on the device:** your handwriting and pages are not sent to Google or to anyone. The recognised text is stored with the page on your device, for search only.
- **What the ML Kit library sends to Google:** the library sends Google operational data about its own use, not about your content: device and app information (such as model, OS version and app version), an identifier specific to the library's installation, download and usage events, performance metrics and error codes. Google uses these to diagnose and improve the library, under Google's privacy policy. See Google's "ML Kit Android data disclosure" page.
- If you never turn handwriting recognition on, the app does not connect to the internet.

**Permissions the app holds:** internet and network state (downloading recognition files at your request, and telling you "waiting for a connection"); microphone (voice notes, when you choose them); camera ("Real room light", when you turn it on); approximate location ("Remember where pages were written", when you turn it on); biometrics (locking notebooks); vibration (paper feel); wake lock, run at startup and foreground service (required by the system libraries behind the home-screen widget, WorkManager and Glance, to refresh the widget; the app runs nothing else with them).

- **No ads, no analytics of ours, no tracking.** No account and no servers of ours. The app sells no data and shares none, other than the operational data the ML Kit library sends to Google as described above.
- **Exported PDFs** go only to the app you choose to share them with. Pictures or text you share into Satr from another app are pasted into the notebook you pick and stay on your device.
- **Backup:** from Settings you can save your notebooks into a single file encrypted with a password you choose, wherever you like; the app uploads it nowhere. Android may also include the app's data in your device backup, if you have enabled it. Pages, pictures and recordings of sealed notebooks are excluded from cloud backup and device transfer, so they stay on your device only. Sealing keeps a notebook closed inside the app and out of system backups; it does not encrypt its files on the device.
- **Deleting:** uninstalling the app deletes everything it stored, including downloaded recognition files.
- **Children:** the app is suitable for everyone and is not directed at children. We collect data from no one.
- **Contact:** [developer email to be added before publishing].
