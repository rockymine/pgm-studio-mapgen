// Screenshots of the viewer, served locally, for checking a change before it is published.
//   node check.js <three.min.js> <OrbitControls.js> [out-dir]
// The two library files come from `npm pack three@0.128.0`; the page loads them from a CDN, which the harness
// answers from these local copies. Needs Playwright with Chromium installed globally.
const { chromium } = require('playwright');
const http = require('http'), fs = require('fs'), path = require('path');
const [three, orbit, out = __dirname] = process.argv.slice(2);
const server = http.createServer((req, res) => {
  const file = path.join(__dirname, decodeURIComponent(req.url.split('?')[0]) === '/' ? 'index.html' : decodeURIComponent(req.url.split('?')[0]));
  fs.readFile(file, (err, data) => {
    if (err) { res.writeHead(404); return res.end(); }
    res.writeHead(200, {'content-type': file.endsWith('.html') ? 'text/html; charset=utf-8' : 'application/json'}); res.end(data);
  });
}).listen(8765, async () => {
  const browser = await chromium.launch({args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader']});
  for (const [w, h, name, click] of [[1400, 860, 'mesh', null], [1400, 860, 'blocks', '#mBlocks'], [1400, 860, 'inside', '[data-p=inside]'], [400, 860, 'phone', null]]) {
    const page = await browser.newPage({viewport: {width: w, height: h}});
    page.on('pageerror', e => console.log(name, 'ERROR', e.message));
    await page.route('https://cdnjs.cloudflare.com/**', r => r.fulfill({path: three, contentType: 'text/javascript'}));
    await page.route('https://cdn.jsdelivr.net/**', r => r.fulfill({path: orbit, contentType: 'text/javascript'}));
    await page.route('https://fonts.googleapis.com/**', r => r.fulfill({body: '', contentType: 'text/css'}));
    await page.goto('http://localhost:8765/');
    await page.waitForSelector('#load[hidden]', {timeout: 60000});
    if (click) await page.click(click);
    await page.waitForTimeout(1500);
    await page.screenshot({path: path.join(out, `check_${name}.png`), fullPage: name === 'phone'});
    console.log(name, (await page.textContent('.figs')).replace(/\s+/g, ' '));
  }
  await browser.close(); server.close();
});
