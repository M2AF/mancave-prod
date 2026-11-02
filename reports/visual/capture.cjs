const {chromium}=require('C:/Users/balla/Documents/agent-office/node_modules/playwright');
const http=require('node:http'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve('site'),out=__dirname;
const types={'.html':'text/html','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.png':'image/png'};
const server=http.createServer((req,res)=>{const p=path.resolve(root,'.'+decodeURIComponent(req.url.split('?')[0]==='/'?'/index.html':req.url.split('?')[0]));if(!p.startsWith(root+path.sep)){res.writeHead(403).end();return}fs.readFile(p,(err,data)=>{res.writeHead(err?404:200,{'Content-Type':types[path.extname(p)]||'application/octet-stream'});res.end(err?'Not found':data)});});
(async()=>{await new Promise(r=>server.listen(0,'127.0.0.1',r));let browser;try{browser=await chromium.launch({headless:true});}catch(e){console.error('Cannot launch browser in sandbox:',e.message);server.close();process.exitCode=1;return;}
const base=`http://127.0.0.1:${server.address().port}`,results=[];
for(const width of [1440,768,390,320])for(const view of ['home','chainlens','magic-money','afterglow','arcade']){
 const page=await browser.newPage({viewport:{width,height:900},deviceScaleFactor:1,reducedMotion:'reduce'}),errors=[],external=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text())});page.on('request',r=>{if(!r.url().startsWith(base))external.push(r.url())});page.on('response',r=>{if(r.status()>=400)errors.push(`${r.status()} ${r.url()}`)});
 await page.goto(base+'/#'+view,{waitUntil:'networkidle'});
 for(let y=0;y<await page.evaluate(()=>document.documentElement.scrollHeight);y+=700){await page.evaluate(y=>scrollTo(0,y),y);await page.waitForTimeout(40)}
 await page.evaluate(async()=>{await Promise.all([...document.images].filter(i=>i.getClientRects().length).map(i=>i.decode().catch(()=>{})));scrollTo(0,0)});
 await page.screenshot({path:path.join(out,`${view}-${width}.png`),fullPage:true});
 const data=await page.evaluate(()=>{
  const rect=e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height}};
  const css=e=>{const s=getComputedStyle(e);return {color:s.color,background:s.backgroundColor,font:s.fontFamily,size:s.fontSize,weight:s.fontWeight,lineHeight:s.lineHeight,gap:s.gap,padding:s.padding,borderBottom:s.borderBottom,objectFit:s.objectFit}};
  const shown=e=>e.getClientRects().length>0;
  return {scrollWidth:document.documentElement.scrollWidth,height:document.documentElement.scrollHeight,container:rect(document.querySelector('.container')),mark:{rect:rect(document.querySelector('.brand__mark')),css:css(document.querySelector('.brand__mark'))},nav:[...document.querySelectorAll('[role=tab]')].map(e=>({text:e.textContent,selected:e.getAttribute('aria-selected'),rect:rect(e),css:css(e)})),images:[...document.images].filter(shown).map(e=>({src:e.getAttribute('src'),currentSrc:e.currentSrc,complete:e.complete,natural:[e.naturalWidth,e.naturalHeight],rect:rect(e),css:css(e),parent:css(e.parentElement)})),panels:[...document.querySelectorAll('.logo-panel,.logo-inset')].filter(shown).map(e=>({class:e.className,rect:rect(e),css:css(e)})),type:[...document.querySelectorAll('h1,h2,h3,.lead,.caption,.eyebrow')].filter(shown).map(e=>({text:e.textContent,css:css(e)})),overflow:[...document.querySelectorAll('body *')].filter(shown).filter(e=>{let r=e.getBoundingClientRect();return r.x<-.5||r.right>innerWidth+.5}).map(e=>({tag:e.tagName,class:e.className,text:e.textContent.slice(0,70),rect:rect(e)})),grid:[...document.querySelectorAll('*')].filter(shown).filter(e=>getComputedStyle(e).backgroundImage.includes('company-grid')).map(e=>({class:e.className,rect:rect(e)})),text:document.querySelector('[data-view]:not([hidden])').innerText};
 });
 results.push({view,width,errors,external,...data});fs.writeFileSync(path.join(out,'measurements.json'),JSON.stringify({browser:await browser.version(),results},null,2));console.log(`${view} ${width}: height ${data.height}, overflow ${data.overflow.length}, images ${data.images.length}, errors ${errors.length}`);await page.close();
}
await browser.close();await new Promise(r=>server.close(r));})().catch(e=>{console.error(e);server.close();process.exitCode=1});
