const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const crypto = require('node:crypto');
const { chromium } = require('C:/Users/balla/Documents/agent-office/node_modules/playwright');
const root = path.resolve(__dirname, '..');
const files = ['mancave.png','chainlens.png','magic-money.png','magic-money-icon.svg','afterglow.png',...['duo','poker','pool','swarm','clash','world'].map(n=>`arcade/${n}.png`)];
(async()=>{
 const server=http.createServer((req,res)=>{const p=path.resolve(root,'.'+decodeURIComponent(req.url.split('?')[0])); if(!p.startsWith(root+path.sep)){res.writeHead(403).end();return;} fs.readFile(p,(e,b)=>{if(e){res.writeHead(404).end();return;}res.setHeader('Content-Type',p.endsWith('.svg')?'image/svg+xml':p.endsWith('.png')?'image/png':'text/html');res.end(b);});});
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const browser=await chromium.launch({headless:true});
 try {
 const page=await browser.newPage(); await page.goto(`http://127.0.0.1:${server.address().port}/design/logo-review.html`);
 const results=[];
 for(const file of files){
 const result=await page.evaluate(async file=>{
  const im=new Image();im.src='/assets/logos/'+file;await im.decode(); const c=document.createElement('canvas');c.width=im.naturalWidth;c.height=im.naturalHeight;const ctx=c.getContext('2d',{willReadFrequently:true});ctx.drawImage(im,0,0);const d=ctx.getImageData(0,0,c.width,c.height).data;
  const all=new Map(),colour=new Map();let transparent=0,minX=c.width,minY=c.height,maxX=0,maxY=0;
  for(let i=0;i<d.length;i+=4){const [r,g,b,a]=d.slice(i,i+4);if(a===0)transparent++;if(a<250)continue;const key=[r,g,b].map(v=>v.toString(16).padStart(2,'0')).join('');all.set(key,(all.get(key)||0)+1);if(Math.max(r,g,b)-Math.min(r,g,b)>60){colour.set(key,(colour.get(key)||0)+1);const x=i/4%c.width,y=Math.floor(i/4/c.width);minX=Math.min(x,minX);minY=Math.min(y,minY);maxX=Math.max(x,maxX);maxY=Math.max(y,maxY);}}
  const top=m=>[...m].sort((a,b)=>b[1]-a[1]).slice(0,12).map(([hex,count])=>({hex:'#'+hex,count}));
  const hueModes={};for(const [hex,count] of colour){const r=parseInt(hex.slice(0,2),16),g=parseInt(hex.slice(2,4),16),b=parseInt(hex.slice(4),16);const name=r>g*1.08&&g>b*1.2?'warm':g>r*1.1&&g>b*1.1?'green':r>b*1.2&&b>g*1.1?'pink':b>r*1.2&&r>g*1.1?'violet':null;if(name&&(!hueModes[name]||count>hueModes[name].count))hueModes[name]={hex:'#'+hex,count};}
  return {file,width:c.width,height:c.height,transparentPixels:transparent,topOpaque:top(all),topChromatic:top(colour),hueModes,chromaticBounds:[minX,minY,maxX,maxY]};
 },file);
 result.sha256=crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'assets/logos',file))).digest('hex');results.push(result);
 }
 fs.mkdirSync(path.join(root,'assets/generated'),{recursive:true});fs.writeFileSync(path.join(__dirname,'logo-samples.json'),JSON.stringify(results,null,2));console.log(JSON.stringify(results.map(r=>({file:r.file,size:[r.width,r.height],transparent:r.transparentPixels,colours:r.topChromatic.slice(0,4),neutrals:r.topOpaque.slice(0,2),bounds:r.chromaticBounds})),null,2));
 }finally{await browser.close();server.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
