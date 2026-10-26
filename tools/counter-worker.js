// عدّاد زوار لبنة — Cloudflare Worker
// يحفظ أرقامًا فقط: عدد زيارات الموقع (جدار الزوار)، وعدد زيارات قاعة كل تطبيق.
// لا يحفظ عنوان IP ولا أي معلومة عن الزائر.
//
// الربط المطلوب (Bindings):
//   KV namespace باسم المتغير COUNTER
//
// المسارات:
//   GET  /             → {"visits": 1234}                     قراءة عدد زيارات الموقع
//   POST /hit          → {"visits": 1235}                     لبنة في جدار الزوار (الصفحة الرئيسية)
//   GET  /room/<app>   → {"visits": 42, "room": "<app>"}                     قراءة عدد زوار قاعة تطبيق: mizan | sana | midmak | sakan
//   POST /hit/<app>    → {"visits": 43, "room": "<app>"}                     لبنة في جدار قاعة التطبيق
//   GET  /stats        → {"visits": …, "pages": {…}, "since": "…"}   كل الأرقام
//
// حدّ العدّ: كل جهاز يُعدّ مرة واحدة في اليوم لكل عدّاد، ومهما أرسل من طلبات بعدها
// يبقى الرقم كما هو. يُعرف الجهاز ببصمة SHA-256 من عنوانه مع ملح عشوائي يتجدّد كل يوم
// (يُحفظ في KV ويُحذف بعد يومين)، فلا يُحفظ العنوان نفسه، ولا يمكن استرجاعه من البصمة.
// وتُحفظ البصمة في الذاكرة المؤقتة لـ Cloudflare (Cache API) حتى نهاية اليوم فقط، لا في KV.

const ALLOWED = ['https://labina.app', 'https://www.labina.app'];
const PAGES = ['mizan', 'sana', 'midmak', 'sakan'];

const json = (body, headers, status = 200) => new Response(JSON.stringify(body), { status, headers });
const today = () => new Date().toISOString().slice(0, 10);
const num = async (env, key) => parseInt((await env.COUNTER.get(key)) || '0', 10) || 0;

async function dailySalt(env, day) {
  const key = 'salt:' + day;
  let salt = await env.COUNTER.get(key);
  if (!salt) {
    const b = new Uint8Array(16); crypto.getRandomValues(b);
    salt = [...b].map((x) => x.toString(16).padStart(2, '0')).join('');
    await env.COUNTER.put(key, salt, { expirationTtl: 172800 });
  }
  return salt;
}

// true أول مرة يُعدّ فيها هذا الجهاز لهذا العدّاد اليوم، وfalse بعدها
async function firstToday(request, env, counter) {
  const ip = request.headers.get('CF-Connecting-IP') || '';
  if (!ip) return false;
  const day = today();
  const salt = await dailySalt(env, day);
  const data = new TextEncoder().encode(`${salt}|${ip}|${counter}`);
  const hash = [...new Uint8Array(await crypto.subtle.digest('SHA-256', data))]
    .map((x) => x.toString(16).padStart(2, '0')).join('');
  const cache = caches.default;
  const mark = new Request(`https://count.labina.app/__seen/${day}/${hash}`);
  if (await cache.match(mark)) return false;
  const left = Math.max(60, Math.floor((Date.parse(day + 'T24:00:00Z') - Date.now()) / 1000));
  await cache.put(mark, new Response('1', { headers: { 'Cache-Control': `max-age=${left}` } }));
  return true;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = request.headers.get('Origin') || '';
    const headers = {
      'Access-Control-Allow-Origin': ALLOWED.includes(origin) ? origin : ALLOWED[0],
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Cache-Control': 'no-store',
      'Content-Type': 'application/json; charset=utf-8',
      'Vary': 'Origin',
    };
    if (request.method === 'OPTIONS') return new Response(null, { headers });

    const path = url.pathname.replace(/\/+$/, '') || '/';

    if (request.method === 'GET' && path === '/') {
      return json({ visits: await num(env, 'visits') }, headers);
    }

    if (request.method === 'GET' && path.startsWith('/room/')) {
      const page = path.slice(6);
      if (!PAGES.includes(page)) return json({ error: 'unknown page' }, headers, 404);
      return json({ visits: await num(env, 'page:' + page), room: page }, headers);
    }

    if (request.method === 'GET' && path === '/stats') {
      const pages = {};
      for (const p of PAGES) pages[p] = await num(env, 'page:' + p);
      return json({ visits: await num(env, 'visits'), pages, since: (await env.COUNTER.get('pages-since')) || null }, headers);
    }

    if (request.method === 'POST' && (path === '/hit' || path.startsWith('/hit/'))) {
      const page = path === '/hit' ? null : path.slice(5);
      if (page !== null && !PAGES.includes(page)) return json({ error: 'unknown page' }, headers, 404);
      const key = page ? 'page:' + page : 'visits';
      // يُقبل العدّ فقط من صفحات الموقع نفسه
      if (!ALLOWED.includes(origin)) return json({ visits: await num(env, key) }, headers, 403);

      let n = await num(env, key);
      if (await firstToday(request, env, key)) {
        n += 1;
        await env.COUNTER.put(key, String(n));
        if (page && !(await env.COUNTER.get('pages-since'))) await env.COUNTER.put('pages-since', today());
      }
      return json(page ? { visits: n, room: page } : { visits: n }, headers);
    }

    return json({ error: 'not found' }, headers, 404);
  },
};
