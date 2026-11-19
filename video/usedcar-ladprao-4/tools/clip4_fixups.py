# Clip-4 (IMG_7745) specifics on top of clip 1's retimed compositions:
# title above her head, card logo early, floor-2 callout as a centred stack under the ISUZU sign, building track.
import json,re,sys,numpy as np
A=json.load(open('tools/anchors_port.json'));xo,xn=zip(*A)
f=lambda t: round(float(np.interp(t,xo,xn)),3)
T=dict(card_logo=2.85, floor=7.85, loc=8.62, isz=9.5)   # speech-locked times (s): ชั้น 7.88, ตึก 8.62, อีซูซุ สยามซิตี้ 9.5
CX=565                                                  # centre x of the ISUZU sign in this shot
t0,t1=f(6.75),f(9.8); off=round(t0*30)
p='compositions/front.html'; s=open(p).read()
def sub(pat,rep,n=1):
    global s; s2,k=re.subn(pat,rep,s,count=n); assert k==n,(pat,k); s=s2
sub(r'const tp = \{ t: 6\.75 \};',f'const tp = {{ t: {t0} }};')
sub(r'Math\.round\(tp\.t \* 30\) - 203',f'Math.round(tp.t * 30) - {off}')
sub(r'tl\.fromTo\(tp, \{ t: 6\.75 \}, \{ t: 9\.8, duration: 3\.05,',f'tl.fromTo(tp, {{ t: {t0} }}, {{ t: {t1}, duration: {round(t1-t0,3)},')
# card logo right after the card lands
sub(r'(tl\.fromTo\("#fr-card-logo".*?\}, )[\d.]+\);',rf'\g<1>{T["card_logo"]});')
# brackets around the sign + centred stack
css=f'''#fr-br-tl {{ left: {CX-205}px; top: 90px; border-top-width: 12px; border-left-width: 12px; }}
    #fr-br-tr {{ left: {CX+135}px; top: 90px; border-top-width: 12px; border-right-width: 12px; }}
    #fr-br-bl {{ left: {CX-205}px; top: 520px; border-bottom-width: 12px; border-left-width: 12px; }}
    #fr-br-br {{ left: {CX+135}px; top: 520px; border-bottom-width: 12px; border-right-width: 12px; }}
    #fr-f2-tag {{ left: {CX-200}px; top: 605px; width: 400px; text-align: center; }}
    #fr-f2-dot, #fr-f2-pulse, #fr-f2-line {{ display: none; }}
    #fr-loc {{ left: {CX-540}px; top: 727px; width: 1080px; text-align: center; }}
    #fr-loc-pill {{ display: inline-flex; align-items: stretch; border-radius: 999px; overflow: hidden; border: 6px solid #fff; font-size: 52px; line-height: 1; }}
    #fr-loc-a {{ background: #fff; color: var(--ink); font-weight: 700; padding: 14px 26px 18px 34px; }}
    #fr-loc-b {{ background: var(--red); color: #fff; font-weight: 800; padding: 14px 34px 18px 26px; }}'''
sub(r'#fr-br-tl \{[^}]*\}\s*#fr-br-tr \{[^}]*\}\s*#fr-br-bl \{[^}]*\}\s*#fr-br-br \{[^}]*\}',css)
sub(r'#fr-f2-tag \{[^}]*\}\n','')
sub(r'<div id="fr-isz-tag".*?</div>\n','')
sub(r'<div id="fr-same" .*?</div>','<div id="fr-loc" class="abs"><span id="fr-loc-pill" class="shadow"><span id="fr-loc-a">ตึกเดียวกับ</span><span id="fr-loc-b">อีซูซุ สยามซิตี้</span></span></div>')
sub(r'(tl\.fromTo\("#fr-f2-pill", \{ scale: 0, transformOrigin: )"70% 0%"( \}.*?\}, )[\d.]+\);',rf'\1"50% 0%"\g<2>{T["floor"]});')
sub(r'(tl\.fromTo\("#fr-f2-num".*?\}, )[\d.]+\);',rf'\g<1>{round(T["floor"]+0.12,3)});')
for i,c in enumerate(['tl','tr','bl','br']):
    sub(rf'(tl\.fromTo\("#fr-br-{c}".*?\}}, )[\d.]+\);',rf'\g<1>{round(T["floor"]-0.1+i*0.03,3)});')
sub(r'tl\.fromTo\("#fr-same-pill".*?\);',f'tl.fromTo("#fr-loc-pill", {{ y: 40, scale: 0.6, opacity: 0 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)" }}, {T["loc"]});')
sub(r'tl\.fromTo\("#fr-isz-pill".*?\);',f'tl.fromTo("#fr-loc-b", {{ scale: 1 }}, {{ scale: 1.1, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1 }}, {T["isz"]});')
sub(r'"#fr-isz-pill", "#fr-same-pill", "#fr-br"','"#fr-loc-pill", "#fr-br"')
tr=sys.argv[1] if len(sys.argv)>1 else 'tools/track4.json'
t=json.load(open(tr)); arr=[t[k] for k in sorted(t,key=int)]
sub(r'const TRACK=\[.*?\];','const TRACK='+json.dumps(arr,separators=(',',':'))+';')
open(p,'w').write(s)
# opening title fully above her head (head top >= ~850px)
pb='compositions/behind.html'; b=open(pb).read()
for a,c in [("#bh-logo { position: absolute; left: 90px; top: 530px;","#bh-logo { position: absolute; left: 90px; top: 420px;"),
            ("#bh-l2 { top: 770px;","#bh-l2 { top: 660px;"),
            ('tl.fromTo("#bh-l2", { y: 0 }, { y: -110,','tl.fromTo("#bh-l2", { y: 0 }, { y: 0,')]:
    assert a in b,a; b=b.replace(a,c)
open(pb,'w').write(b)
print('fixups ok',t0,t1,off,len(arr))
