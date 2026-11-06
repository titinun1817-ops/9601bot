const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:800},deviceScaleFactor:1});
for(const n of ['1_storyline','2_storyboard','3_workplan']){await p.goto('file://'+process.cwd()+'/'+n+'.html');await p.evaluate(()=>document.fonts.ready);await p.screenshot({path:n+'.png',fullPage:true});}await b.close();})();
