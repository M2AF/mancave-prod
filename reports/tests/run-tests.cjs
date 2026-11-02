const fs = require('fs');
const path = require('path');
const http = require('http');
const crypto = require('crypto');
const { chromium } = require('C:/Users/balla/Documents/agent-office/node_modules/playwright');
const root = path.resolve(__dirname, '../../site');
const out = __dirname;
process.chdir(out); // Keep Chromium process diagnostics in the authorized artifact directory.
const ids = ['home','chainlens','magic-money','afterglow','arcade'];
const widths = [1440,768,390,320];
const results = [];
const requests = [];
const snapshots = [];
function walk(dir) { return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name)):[path.join(dir,e.name)]); }
function manifest() { return Object.fromEntries(['site','content','brief'].flatMap(d=>fs.existsSync(path.resolve(root,'..',d))?walk(path.resolve(root,'..',d)):[]).map(f=>[path.relative(path.resolve(root,'..'),f),crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex')])); }
const before=manifest();
function check(width,view,name,ok,evidence) {results.push({width,view,check:name,status:ok?'PASS':'FAIL',evidence});}
const mime={'.html':'text/html','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.png':'image/png'};
const server=http.createServer((req,res)=>{let file;try {file=path.resolve(root,'.'+decodeURIComponent(new URL(req.url,'http://localhost').pathname));if(file===root)file=path.join(root,'index.html');if(!file.startsWith(root+path.sep))throw Error();const data=fs.readFileSync(file);res.writeHead(200,{'Content-Type':mime[path.extname(file)]||'application/octet-stream','Cache-Control':'no-store'});res.end(data);}catch{res.writeHead(404);res.end('Not found');}});
async function settleImages(page) {
  await page.evaluate(async()=>{for(let y=0;y<document.documentElement.scrollHeight;y+=600)window.scrollTo(0,y);});
  // Visit each lazy image individually, without changing its loading attribute.
  for (const img of await page.locator('img:visible').all()) await img.scrollIntoViewIfNeeded();
  await page.waitForFunction(()=>Array.from(document.images).filter(i=>i.getClientRects().length).every(i=>i.complete),{},{timeout:15000});
  await page.evaluate(()=>window.scrollTo(0,0));
}
async function state(page,id) {
 return page.evaluate(id=>{
  const tabs=[...document.querySelectorAll('[role=tab]')],panels=[...document.querySelectorAll('[data-view]')];
  return tabs.length===5&&document.querySelectorAll('[role=tablist]').length===1&&tabs.every(t=>t.closest('[role=tablist]')&&t.getAttribute('aria-selected')===String(t.getAttribute('aria-controls')===id)&&t.tabIndex===(t.getAttribute('aria-controls')===id?0:-1)&&document.getElementById(t.getAttribute('aria-controls'))?.getAttribute('aria-labelledby')===t.id)&&panels.every(p=>p.getAttribute('role')==='tabpanel'&&p.hidden===(p.id!==id));
 },id);
}
async function keyboard(page,id) {
 const errors=[];const index=ids.indexOf(id);await page.locator('#tab-'+id).focus();
 const steps=[['ArrowRight',ids[(index+1)%5]],['ArrowLeft',id],['Home','home'],['ArrowLeft','arcade'],['ArrowRight','home'],['End','arcade'],['Home','home']];
 for(const [key,want] of steps){await page.keyboard.press(key);if(!await state(page,want)||await page.evaluate(()=>document.activeElement.id)!=='tab-'+want)errors.push(key+' expected '+want);}
 // Activate each unselected button using native Enter and Space, without clicking it.
 for(const key of ['Enter','Space']){await page.locator('#tab-'+id).focus();await page.keyboard.press(key);if(!await state(page,id)||new URL(page.url()).hash!=='#'+id)errors.push(key+' activation');if(id==='home'){await page.locator('#tab-chainlens').focus();await page.keyboard.press(key);if(!await state(page,'chainlens'))errors.push(key+' unselected activation');}}
 await fresh(page,id);return errors;
}
let base;
let loadIndex=0;
async function fresh(page,id) { await page.goto(base+'/?test='+(++loadIndex)+'#'+id); await page.evaluate(()=>{document.body.setAttribute('tabindex','-1');document.body.focus();document.body.removeAttribute('tabindex');}); }
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));base='http://127.0.0.1:'+server.address().port;
 const browser=await chromium.launch({headless:true});
 fs.writeFileSync(path.join(out,'environment.json'),JSON.stringify({time:new Date().toISOString(),browser:browser.version(),playwright:require('C:/Users/balla/Documents/agent-office/node_modules/playwright/package.json').version,base,height:900},null,2));
 for(const width of widths){
  const context=await browser.newContext({viewport:{width,height:900}});
  await context.route('**/*',route=>{const url=route.request().url();if(new URL(url).origin!==base){requests.push({width,url,blocked:true});return route.abort();}return route.continue();});
  const page=await context.newPage();let consoleErrors=[],pageErrors=[],badResponses=[],failedRequests=[];
  page.on('console',m=>{if(m.type()==='error')consoleErrors.push(m.text());});page.on('pageerror',e=>pageErrors.push(e.message));
  page.on('response',r=>{requests.push({width,url:r.url(),status:r.status()});if(r.status()>=400)badResponses.push({url:r.url(),status:r.status()});});
  page.on('requestfailed',r=>failedRequests.push({url:r.url(),error:r.failure()}));
  for(const id of ids){
   const start=requests.length;consoleErrors=[];pageErrors=[];badResponses=[];failedRequests=[];
   await fresh(page,id);await settleImages(page);
   check(width,id,'Tab semantics and selection',await state(page,id),'Five labelled tabs, reciprocal controls/labelledby, one tabindex=0; selected panel only visible.');
   const cdp=await context.newCDPSession(page);await cdp.send('DOM.enable');await cdp.send('Accessibility.enable');
   const ax=[];
   const {root:dom}=await cdp.send('DOM.getDocument');
   for(const hidden of ids.filter(x=>x!==id)){
    const {nodeId}=await cdp.send('DOM.querySelector',{nodeId:dom.nodeId,selector:'#'+hidden});
    const tree=await cdp.send('Accessibility.getPartialAXTree',{nodeId,fetchRelatives:false});
    ax.push({id:hidden,nodes:tree.nodes.map(n=>({ignored:n.ignored,role:n.role?.value,name:n.name?.value}))});
   }
   await cdp.detach();
   const hiddenFocus=await page.evaluate(()=>[...document.querySelectorAll('[data-view][hidden]')].every(p=>[p,...p.querySelectorAll('a,button,[tabindex]')].every(e=>{e.focus();return document.activeElement!==e;})));
   check(width,id,'Inactive panels excluded',hiddenFocus&&ax.every(p=>p.nodes.every(n=>n.ignored)),{programmaticFocusRejected:hiddenFocus,accessibility:ax});
   const errors=await keyboard(page,id);check(width,id,'Keyboard arrows/wrap/Home/End/Enter/Space',!errors.length,errors);
   // Traverse actual tab stops from a fresh document; do not activate outbound links.
   await fresh(page,id);await page.keyboard.press('Tab');
   const skip=await page.evaluate(()=>{const e=document.activeElement,r=e.getBoundingClientRect(),s=getComputedStyle(e);return {text:e.textContent,href:e.getAttribute('href'),visible:r.y>=0&&r.bottom<=innerHeight&&r.x>=0&&r.right<=innerWidth,outline:s.outline};});
   await page.screenshot({path:path.join(out,`${width}-${id}-skip-focus.png`)});
   if(skip.href==='#main') await page.keyboard.press('Enter');
   check(width,id,'Skip link',skip.href==='#main'&&skip.visible&&await page.evaluate(()=>document.activeElement.id==='main'),skip);
   await fresh(page,id);await settleImages(page);
   // All interactive elements, including non-tabstop tabs, receive keyboard focus mode.
   await page.keyboard.press('Tab');const focusDetails=[];
   for(const el of await page.locator('a:visible,button:visible,input:visible,select:visible,textarea:visible,[role=button]:visible').all()){
    await el.focus();await page.waitForTimeout(160);
    focusDetails.push(await el.evaluate(e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return {text:e.textContent.trim(),id:e.id,href:e.getAttribute('href'),width:r.width,height:r.height,focusVisible:e.matches(':focus-visible'),outlineStyle:s.outlineStyle,outlineWidth:s.outlineWidth,outlineColor:s.outlineColor,outlineOffset:s.outlineOffset,boxShadow:s.boxShadow};}));
    if((await el.getAttribute('class')||'').includes('btn--primary'))await page.screenshot({path:path.join(out,`${width}-${id}-action-focus.png`)});
   }
   check(width,id,'Focus rings',focusDetails.every(e=>e.focusVisible&&e.outlineStyle!=='none'&&parseFloat(e.outlineWidth)>=2),focusDetails);
   check(width,id,'Tap targets >=44px',focusDetails.every(e=>e.width>=44&&e.height>=44),focusDetails.filter(e=>e.width<44||e.height<44));
   await fresh(page,id);const visited=[];
   for(let i=0;i<30;i++){await page.keyboard.press('Tab');visited.push(await page.evaluate(()=>({id:document.activeElement.id,panel:document.activeElement.closest('[data-view]')?.id,role:document.activeElement.getAttribute('role')})));if(i>0&&visited.at(-1).id===''&&await page.evaluate(()=>document.activeElement.classList.contains('skip-link')))break;}
   check(width,id,'Keyboard tab order isolation',visited.filter(v=>v.role==='tab').length===1&&visited.every(v=>!v.panel||v.panel===id),visited);
   await settleImages(page);
   const geometry=await page.evaluate(()=>({viewport:innerWidth,document:document.documentElement.scrollWidth,body:document.body.scrollWidth,offenders:[...document.querySelectorAll('body *')].filter(e=>e.getClientRects().length&&getComputedStyle(e).position!=='absolute').map(e=>({tag:e.tagName,id:e.id,class:e.className,x:e.getBoundingClientRect().x,right:e.getBoundingClientRect().right})).filter(e=>e.x<-.5||e.right>innerWidth+.5)}));
   check(width,id,'No horizontal overflow',geometry.document<=width&&geometry.body<=width,geometry);
   const broken=await page.locator('img:visible').evaluateAll(imgs=>imgs.filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.currentSrc));
   check(width,id,'No broken images',!broken.length,broken);
   await page.screenshot({path:path.join(out,`${width}-${id}.png`),fullPage:true});
   // Click two local tabs, then exercise real session history.
   const other=ids[(ids.indexOf(id)+1)%5];await page.locator('#tab-'+other).click();await page.locator('#tab-'+id).click();await page.goBack();await page.waitForTimeout(50);const back=await state(page,other);await page.goForward();await page.waitForTimeout(50);const forward=await state(page,id);
   check(width,id,'Deep links and back/forward',back&&forward&&new URL(page.url()).hash==='#'+id,{back,forward});
   await page.emulateMedia({reducedMotion:'reduce'});await page.locator('#tab-'+id).hover();await page.keyboard.press('Tab');
   const motion=await page.evaluate(()=>({reduced:matchMedia('(prefers-reduced-motion: reduce)').matches,running:document.getAnimations().filter(a=>a.playState==='running').length,styles:[...document.querySelectorAll('*')].flatMap(e=>['', '::before','::after'].map(p=>{const s=getComputedStyle(e,p||null);return {element:e.id||e.tagName,pseudo:p,transition:s.transitionDuration,animation:s.animationName,duration:s.animationDuration};})).filter(s=>s.transition.split(',').some(t=>parseFloat(t)>0)||s.animation!=='none')}));
   check(width,id,'Reduced motion',motion.reduced&&!motion.running&&!motion.styles.length,motion);await page.emulateMedia({reducedMotion:'no-preference'});
   check(width,id,'No console/page errors',!consoleErrors.length&&!pageErrors.length,{consoleErrors,pageErrors});
   check(width,id,'Loopback-only requests',requests.slice(start).every(r=>new URL(r.url).origin===base),requests.slice(start).filter(r=>new URL(r.url).origin!==base));
   check(width,id,'No HTTP errors or failed requests',!badResponses.length&&!failedRequests.length,{badResponses,failedRequests});
   console.log(`Completed ${width} ${id}`);
  }
  await context.close();
  const nojs=await browser.newContext({viewport:{width,height:900},javaScriptEnabled:false});const p=await nojs.newPage();const nojsRequests=[],nojsErrors=[];
  await nojs.route('**/*',r=>{nojsRequests.push(r.request().url());return new URL(r.request().url()).origin===base?r.continue():r.abort();});p.on('response',r=>{if(r.status()>=400)nojsErrors.push({url:r.url(),status:r.status()});});
  await p.goto(base);await settleImages(p);
  for(const id of ids){
   const allVisible=await p.locator('[data-view]').evaluateAll(es=>es.length===5&&es.every(e=>!e.hidden&&getComputedStyle(e).display!=='none'&&e.getBoundingClientRect().height>0));
   await p.locator('[data-fallback-nav] a[href="#'+id+'"]').click();
   const destination=await p.evaluate(id=>({hash:location.hash,y:document.getElementById(id).getBoundingClientRect().y,scrollY}),id);
   check(width,id,'JavaScript disabled: content and header anchors',allVisible&&destination.hash==='#'+id&&Math.abs(destination.y)<2,{allVisible,destination});
   const geometry=await p.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth}));
   check(width,id,'JavaScript disabled: overflow/network/images',geometry.scrollWidth<=width&&nojsRequests.every(u=>new URL(u).origin===base)&&!nojsErrors.length&&await p.locator('img').evaluateAll(es=>es.every(e=>e.complete&&e.naturalWidth>0)),{geometry,nojsErrors});
  }
  await p.screenshot({path:path.join(out,`${width}-no-javascript.png`),fullPage:true});await nojs.close();
 }
 const ctx=await browser.newContext();const p=await ctx.newPage();await p.goto(base);
 const links=await p.locator('a[href^="https:"]').evaluateAll(es=>es.map(e=>({href:e.getAttribute('href'),text:e.textContent.trim(),location:e.closest('[data-view]')?.id||(e.closest('footer')?'footer':'other')})));
 const expected=['https://www.chainlensnft.info','https://github.com/M2AF/Magic-Money-Wallet','https://github.com/M2AF/Magic-Money-Wallet/releases/latest','https://duo.magicmoney.dev','https://discord.gg/26uxjad8uT'];
 check('all','all','Exact outbound links',JSON.stringify([...new Set(links.map(l=>l.href))].sort())===JSON.stringify([...expected].sort())&&links.filter(l=>l.href===expected[4]).length===2&&links.some(l=>l.href===expected[4]&&l.location==='home')&&links.some(l=>l.href===expected[4]&&l.location==='footer'),links);
 check('all','afterglow','AfterGlow has no link/button',await p.locator('#afterglow a,#afterglow button,#afterglow [role=button],#afterglow [role=link]').count()===0,{scope:'#afterglow content panel; shared header/footer excluded'});
 const occurrences=walk(root).flatMap(f=>{const s=fs.readFileSync(f).toString('utf8');return [...s.matchAll(/duo arcade/gi)].map(m=>({file:path.relative(root,f),line:s.slice(0,m.index).split('\n').length,text:m[0]}));});
 await p.goto(base+'/#arcade');const beside=await p.locator('#arcade .actions').evaluate(e=>{const a=e.querySelector('a'),n=e.querySelector('.action-note');return !!a&&!!n&&a.getAttribute('href')==='https://duo.magicmoney.dev'&&/duo arcade/i.test(n.textContent);});
 check('all','arcade','DUO Arcade exactly once beside Play',occurrences.length===1&&beside,{occurrences,sameActionsContainer:beside});
 await ctx.close();await browser.close();server.close();
 const after=manifest();check('all','all','Protected files unchanged',JSON.stringify(before)===JSON.stringify(after),{before,after});
 fs.writeFileSync(path.join(out,'results.json'),JSON.stringify(results,null,2));fs.writeFileSync(path.join(out,'requests.json'),JSON.stringify(requests,null,2));
 const names=[...new Set(results.map(r=>r.check))];
 const lines=['# Static site test pass','',`Run: ${new Date().toISOString()}. Chromium headless; widths 1440, 768, 390, 320 CSS px, viewport height 900. Existing Playwright installation only. Loopback server: ${base}.`,'','## Check summary','','| Check | Result | Cases |','|---|---|---|',...names.map(n=>{const rs=results.filter(r=>r.check===n);return `| ${n} | ${rs.every(r=>r.status==='PASS')?'PASS':'FAIL'} | ${rs.filter(r=>r.status==='PASS').length}/${rs.length} |`;}),'','## Per-view / width matrix','','| View | Width | Result | Failures |','|---|---:|---|---|',...widths.flatMap(w=>ids.map(id=>{const rs=results.filter(r=>r.width===w&&r.view===id),fails=rs.filter(r=>r.status==='FAIL');return `| ${id} | ${w} | ${fails.length?'FAIL':'PASS'} | ${fails.map(r=>r.check).join('; ')||'None'} |`;})),'','## Failures','',...results.filter(r=>r.status==='FAIL').map(r=>`- **${r.width} / ${r.view} / ${r.check}**: ${JSON.stringify(r.evidence)}`),'','## Evidence and scope','','- Detailed assertions and measured evidence: [results.json](results.json). HTTP response log: [requests.json](requests.json). Browser/version/time: [environment.json](environment.json). Re-run with `node reports/tests/run-tests.cjs`.','- Full-page screenshots: `<width>-<view>.png`; skip-focus and action-focus screenshots also saved for every applicable combination. No-JavaScript full-page screenshots: `<width>-no-javascript.png`.','- Tabs tested with real key events, automatic selection, both wrap directions, Home/End, Enter/Space; actual Tab traversal confirms one tab stop. CDP accessibility inspection confirms inactive panels are ignored; focus attempts into hidden panels fail.','- All visible links/buttons measured and checked in keyboard focus mode for a >=2px non-none focus outline. View panels and main use the same global focus rule; focus screenshots require visual review.','- All five panels render together without JavaScript. Every fallback header link tested at each width. Lazy images scrolled into view before checking load completion. Reduced-motion computed styles checked including pseudo-elements, plus running animation inspection after hover/focus.','- Outbound URLs inspected only; never followed. A route guard blocks unexpected external requests and records them as failures.','- No dependencies installed and no commits made. Protected folder file hashes compared before/after.','', '## Not tested / limitations','','- Chromium only: Firefox, WebKit, physical touch devices, operating-system assistive technology and manual screen-reader output were not tested. Accessibility-tree results are Chromium CDP evidence.','- Target-size measurements use CSS pixels at device scale factor 1. Focus checks combine computed outlines with screenshot review; they are not a formal contrast audit. External site availability intentionally not tested.','- History tested by clicking tabs then Back/Forward for every starting view and width. No browser-extension or production-host behavior is implied.'];
 fs.writeFileSync(path.join(out,'test-pass.md'),lines.join('\n')+'\n');
 console.log(JSON.stringify({assertions:results.length,failures:results.filter(r=>r.status==='FAIL').map(({width,view,check,evidence})=>({width,view,check,evidence}))},null,2));
})().catch(e=>{console.error(e);fs.writeFileSync(path.join(out,'run-error.txt'),e.stack||String(e));server.close();process.exit(1);});



