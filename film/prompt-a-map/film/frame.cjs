// node frame.cjs <t or shot:offset> [...] -> out/f-<t>.png (quick looks at single frames)
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('ERR', e.message)); p.on('console', m => { if (m.type() === 'error') console.log('console:', m.text()); });
  await p.goto('file://' + __dirname + '/index.html'); await p.evaluate(() => window.ready);
  const info = await p.evaluate(() => window.filmInfo());
  for (const a of process.argv.slice(2)) {
    let T = +a; if (a.includes(':')) { const [id, off] = a.split(':'); T = info.shots.find(s => s.id === id).t0 + +off; }
    await p.evaluate(T => window.seek(T), T);
    const name = `out/f-${a.replace(':', '_')}.jpg`; await p.screenshot({ path: __dirname + '/' + name, type: 'jpeg', quality: 80 }); console.log(name);
  }
  await b.close();
})();
