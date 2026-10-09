// عدّاد زوار لبنة — Cloudflare Worker
// يحفظ رقمًا واحدًا فقط (عدد الزيارات). لا يحفظ عنوان IP ولا أي معلومة عن الزائر.
//
// الربط المطلوب (Bindings):
//   KV namespace باسم المتغير COUNTER
//
// المسارات:
//   GET  /      → {"visits": 1234}           قراءة العدد
//   POST /hit   → {"visits": 1235}           إضافة لبنة وقراءة العدد

const ALLOWED = ['https://labina.app', 'https://www.labina.app'];

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

    let visits = parseInt((await env.COUNTER.get('visits')) || '0', 10) || 0;

    if (request.method === 'POST' && url.pathname === '/hit') {
      // يُقبل العدّ فقط من صفحات الموقع نفسه
      if (!ALLOWED.includes(origin)) {
        return new Response(JSON.stringify({ visits }), { status: 403, headers });
      }
      visits += 1;
      await env.COUNTER.put('visits', String(visits));
    }

    return new Response(JSON.stringify({ visits }), { headers });
  },
};
