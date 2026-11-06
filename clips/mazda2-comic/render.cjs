// usage: node render.cjs stills t1,t2,...  |  node render.cjs video out.mp4
const {chromium}=require('playwright');const {spawn}=require('child_process');const fs=require('fs');
(async()=>{const mode=process.argv[2];const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
await p.goto('file://'+process.cwd()+'/clip.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
if(mode=='stills'){fs.mkdirSync('stills',{recursive:true});for(const t of process.argv[3].split(',')){await p.evaluate(t=>render(+t),t);await p.waitForTimeout(40);await p.screenshot({path:`stills/t${(+t).toFixed(2)}.png`})}}
else{const D=await p.evaluate(()=>DURATION);const N=Math.round(D*30);
 const ff=spawn('ffmpeg',['-v','error','-y','-f','image2pipe','-framerate','30','-c:v','png','-i','-','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p',process.argv[3]],{stdio:['pipe','inherit','inherit']});
 for(let i=0;i<N;i++){await p.evaluate(t=>render(t),i/30);const buf=await p.screenshot({type:'png'});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));if(i%60==0)console.log('frame',i,'/',N)}
 ff.stdin.end();await new Promise(r=>ff.on('close',r))}
await b.close()})();
