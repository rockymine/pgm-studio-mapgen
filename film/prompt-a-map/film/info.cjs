const { chromium } = require('playwright');
(async () => { const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage();
  await p.goto('file://' + __dirname + '/index.html'); await p.evaluate(() => window.ready);
  require('fs').writeFileSync(__dirname + '/filminfo.json', JSON.stringify(await p.evaluate(() => window.filmInfo()), null, 1)); await b.close(); })();
