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
for a,b in R:
    assert a in s,a; s=s.replace(a,b)
tr=sys.argv[1] if len(sys.argv)>1 else 'tools/track3.json'
t=json.load(open(tr)); arr=[t[k] for k in sorted(t,key=int)]
s=re.sub(r'const TRACK=\[.*?\];','const TRACK='+json.dumps(arr,separators=(',',':'))+';',s,count=1,flags=re.S)
open(p,'w').write(s); print('fixups ok',t0,t1,off,len(arr))
