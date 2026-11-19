# Clip-3 specifics on top of the retimed clip 1 front.html: track window, pin positions on this building, TRACK data.
import json,re,sys,numpy as np,os
A=json.load(open('tools/anchors_port.json'));xo,xn=zip(*A)
f=lambda t: round(float(np.interp(t,xo,xn)),3)
t0,t1=f(6.75),f(9.8); off=round(t0*30)
p='compositions/front.html'; s=open(p).read()
s=s.replace('const tp = { t: 6.75 };',f'const tp = {{ t: {t0} }};')
s=s.replace('Math.round(tp.t * 30) - 203',f'Math.round(tp.t * 30) - {off}')
s=re.sub(r'tl\.fromTo\(tp, \{ t: 6\.75 \}, \{ t: 9\.8, duration: 3\.05,',f'tl.fromTo(tp, {{ t: {t0} }}, {{ t: {t1}, duration: {round(t1-t0,3)},',s)
R=[("#fr-f2-dot { left: 816px; top: 536px;","#fr-f2-dot { left: 711px; top: 556px;"),
("#fr-f2-pulse { left: 790px; top: 510px;","#fr-f2-pulse { left: 685px; top: 530px;"),
("#fr-f2-line { left: 837px; top: 584px;","#fr-f2-line { left: 732px; top: 604px;"),
("#fr-f2-tag { left: 640px; top: 670px; }","#fr-f2-tag { left: 535px; top: 690px; }"),
("#fr-br-tl { left: 380px; top: 170px;","#fr-br-tl { left: 330px; top: 170px;"),
("#fr-br-tr { left: 720px; top: 170px;","#fr-br-tr { left: 680px; top: 170px;"),
("#fr-br-bl { left: 380px; top: 560px;","#fr-br-bl { left: 330px; top: 560px;"),
("#fr-br-br { left: 720px; top: 560px;","#fr-br-br { left: 680px; top: 560px;"),
("#fr-isz-tag { left: 140px; top: 640px; }","#fr-isz-tag { left: 70px; top: 660px; }"),
("#fr-same { left: 0; top: 800px;","#fr-same { left: 0; top: 790px;")]
# card logo right after the card lands (no empty white card)
R.append(('tl.fromTo("#fr-card-logo", { scale: 1.25, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "expo.out" }, 4.085);','tl.fromTo("#fr-card-logo", { scale: 1.25, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "expo.out" }, 2.95);'))
for a,b in R:
    assert a in s,a; s=s.replace(a,b)
# ---- opening title sits fully above her head (head top >= ~840px): logo 420, branch line 660, no lift in rank section
pb='compositions/behind.html'; b=open(pb).read()
for a,c in [("#bh-logo { position: absolute; left: 90px; top: 530px;","#bh-logo { position: absolute; left: 90px; top: 420px;"),
            ("#bh-l2 { top: 770px;","#bh-l2 { top: 660px;"),
            ('tl.fromTo("#bh-l2", { y: 0 }, { y: -110,','tl.fromTo("#bh-l2", { y: 0 }, { y: 0,')]:
    assert a in b,a; b=b.replace(a,c)
open(pb,'w').write(b)

# ---- floor-2 callout, redesigned as one tidy stack under the ISUZU sign
R2=[("#fr-f2-line { left: 732px; top: 604px; width: 6px; height: 90px;","#fr-f2-line { left: 732px; top: 604px; width: 6px; height: 40px;"),
("#fr-f2-tag { left: 535px; top: 690px; }","#fr-f2-tag { left: 340px; top: 650px; width: 400px; text-align: center; }\n    #fr-f2-dot, #fr-f2-pulse, #fr-f2-line { display: none; }\n    #fr-loc { left: 0; top: 772px; width: 1080px; text-align: center; }\n    #fr-loc-pill { display: inline-flex; align-items: stretch; border-radius: 999px; overflow: hidden; border: 6px solid #fff; font-size: 52px; line-height: 1; }\n    #fr-loc-a { background: #fff; color: var(--ink); font-weight: 700; padding: 14px 26px 18px 34px; }\n    #fr-loc-b { background: var(--red); color: #fff; font-weight: 800; padding: 14px 34px 18px 26px; }"),
('<div id="fr-isz-tag" class="abs"><span id="fr-isz-pill" class="pill shadow">อีซูซุ สยามซิตี้</span></div>',''),
('<div id="fr-same" class="abs"><span id="fr-same-pill" class="pill shadow">ตึกเดียวกัน</span></div>','<div id="fr-loc" class="abs"><span id="fr-loc-pill" class="shadow"><span id="fr-loc-a">ตึกเดียวกับ</span><span id="fr-loc-b">อีซูซุ สยามซิตี้</span></span></div>'),
('{ scale: 0, transformOrigin: "70% 0%" }','{ scale: 0, transformOrigin: "50% 0%" }'),
('ease: "expo.out" }, 9.052);','ease: "expo.out" }, 8.66);'),
('ease: "expo.out" }, 9.204);','ease: "expo.out" }, 8.69);'),
('ease: "expo.out" }, 9.357);','ease: "expo.out" }, 8.72);'),
('ease: "expo.out" }, 9.509);','ease: "expo.out" }, 8.75);'),
('tl.fromTo("#fr-same-pill", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "back.out(2)" }, 9.56);',
 'tl.fromTo("#fr-loc-pill", { y: 40, scale: 0.6, opacity: 0 }, { y: 0, scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)" }, 9.56);'),
('tl.fromTo("#fr-isz-pill", { x: -300, opacity: 0 }, { x: 0, opacity: 1, duration: 0.42, ease: "expo.out" }, 10.46);',
 'tl.fromTo("#fr-loc-b", { scale: 1 }, { scale: 1.1, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1 }, 10.46);'),
('"#fr-isz-pill", "#fr-same-pill", "#fr-br"','"#fr-loc-pill", "#fr-br"')]
for a,c in R2:
    assert a in s,a; s=s.replace(a,c)
tr=sys.argv[1] if len(sys.argv)>1 else 'tools/track3.json'
t=json.load(open(tr)); arr=[t[k] for k in sorted(t,key=int)]
s=re.sub(r'const TRACK=\[.*?\];','const TRACK='+json.dumps(arr,separators=(',',':'))+';',s,count=1,flags=re.S)
open(p,'w').write(s); print('fixups ok',t0,t1,off,len(arr))
