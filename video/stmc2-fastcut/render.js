const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [,,mode,...rest]=process.argv;const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+__dirname+'/clip3-template.html');await p.evaluate(()=>window.ready);await p.waitForTimeout(500);
if(mode==='stills'){for(const t of rest){await p.evaluate(t=>render(+t),t);await p.screenshot({path:`s4_${t}.jpg`,type:'jpeg',quality:85});}}
else{fs.mkdirSync('out',{recursive:true});const N=Math.round(26*30);const a=+(rest[0]||0),z=+(rest[1]||N);for(let i=a;i<z;i++){await p.evaluate(t=>render(t),i/30);await p.screenshot({path:`out/${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});if(i%100==0)console.log(i)}}
await b.close();})();
