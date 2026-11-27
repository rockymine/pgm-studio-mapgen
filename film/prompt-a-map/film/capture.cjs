// node capture.cjs <outDir> <fromFrame> <toFrame>   -> outDir/000000.jpg ...
const { chromium } = require('playwright');
(async () => {
  const [, , out, from, to] = process.argv;
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.log('ERR', e.message));
  await p.goto('file://' + __dirname + '/index.html'); await p.evaluate(() => window.ready);
  const info = await p.evaluate(() => window.filmInfo());
  const last = Math.min(+to, Math.ceil(info.total * info.fps) - 1);
  for (let f = +from; f <= last; f++) {
    await p.evaluate(T => window.seek(T), f / info.fps);
    await p.screenshot({ path: `${out}/${String(f).padStart(6, '0')}.jpg`, type: 'jpeg', quality: 93 });
    if (f % 150 === 0) console.log('frame', f);
  }
  await b.close();
})();
