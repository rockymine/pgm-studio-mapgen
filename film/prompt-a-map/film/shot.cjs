const { chromium } = require('playwright');
(async()=>{
const [,, page_, out, w='1920', h='1080', t] = process.argv;
const b = await chromium.launch();
const p = await b.newPage({viewport:{width:+w,height:+h}});
p.on('console',m=>console.log('console:',m.text())); p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+process.cwd()+'/'+page_); await p.waitForTimeout(600);
if(t!==undefined){ await p.evaluate(async t=>{await window.seek(+t)}, t); }
await p.screenshot({path:out}); await b.close();
})();
