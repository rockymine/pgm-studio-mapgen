const { chromium } = require('playwright'); const fs = require('fs');
(async () => { const b = await chromium.launch(); 
  for (const [w, h, name] of [[1280, 900, 'desk'], [400, 800, 'phone']]) {
    const p = await b.newPage({ viewport: { width: w, height: h } });
    p.on('pageerror', e => console.log('ERR', e.message));
    await p.setContent('<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1"></head><body style="margin:0">' + fs.readFileSync(__dirname + '/../prompt-a-map.html', 'utf8') + '</body></html>');
    await p.waitForTimeout(1500);
    const sw = await p.evaluate(() => document.documentElement.scrollWidth); console.log(name, 'scrollWidth', sw, 'viewport', w);
    await p.screenshot({ path: __dirname + `/out/page-${name}.jpg`, type: 'jpeg', quality: 70, fullPage: true });
  } await b.close(); })();
