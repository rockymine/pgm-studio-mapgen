// One look: render out/index.html inside the publish skeleton at desktop and phone, light and dark.
const { chromium } = require('playwright'); const fs = require('fs'); const http = require('http'); const path = require('path');
const OUT = path.join(__dirname, 'out');
const page = fs.readFileSync(OUT + '/index.html', 'utf8');
const skel = `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{color-scheme:light}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style></head><body>${page}</body></html>`;
const srv = http.createServer((q, r) => { const u = decodeURIComponent(q.url.split('?')[0]); if (u === '/') { r.setHeader('content-type', 'text/html'); return r.end(skel); } const f = path.join(OUT, u); if (f.startsWith(OUT) && fs.existsSync(f)) { r.setHeader('content-type', 'image/jpeg'); return r.end(fs.readFileSync(f)); } r.statusCode = 404; r.end(); }).listen(4180);
(async () => {
  const b = await chromium.launch(); const shots = process.argv.slice(2);
  for (const s of shots) { const [view, w, scheme, full] = s.split(':');
    const p = await b.newPage({ viewport: { width: +w, height: +w > 600 ? 950 : 800 }, colorScheme: scheme, deviceScaleFactor: 1 });
    const errs = []; p.on('pageerror', e => errs.push(String(e).slice(0, 150)));
    await p.goto('http://127.0.0.1:4180/#' + view, { waitUntil: 'load' }); await p.waitForTimeout(1200);
    const over = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    if (full === 'cards') { await p.evaluate(() => document.querySelector('.scenes').scrollIntoView()); await p.waitForTimeout(500); } await p.screenshot({ path: `look-${view}-${w}-${scheme}${full||''}.png`, fullPage: full === 'full' });
    console.log(s, 'overflow-x', over, errs.join(' | ')); await p.close(); }
  await b.close(); srv.close();
})();
