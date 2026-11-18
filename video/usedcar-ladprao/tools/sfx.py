# Synthesized SFX track (deterministic). Writes assets/sfx.wav (48 kHz stereo, 13 s).
import numpy as np, scipy.signal as sg, scipy.io.wavfile as wf, sys
SR=48000; DUR=13.0; rng=np.random.default_rng(3)
L=np.zeros(int(SR*DUR)); R=np.zeros_like(L)
def t_(d): return np.arange(int(SR*d))/SR
def place(x,t,g=1.0,pan=0.0):
    i=int(t*SR); n=min(len(x),len(L)-i)
    if n<=0: return
    L[i:i+n]+=x[:n]*g*np.sqrt(0.5*(1-pan)); R[i:i+n]+=x[:n]*g*np.sqrt(0.5*(1+pan))
def bp(x,lo,hi): b,a=sg.butter(2,[lo/(SR/2),hi/(SR/2)],'band'); return sg.lfilter(b,a,x)
def lp(x,f): b,a=sg.butter(2,f/(SR/2)); return sg.lfilter(b,a,x)
def hp(x,f): b,a=sg.butter(2,f/(SR/2),'high'); return sg.lfilter(b,a,x)
def norm(x): return x/ (np.max(np.abs(x))+1e-9)
def whoosh(d=0.45,f0=300,f1=3000,rev=False):
    n=int(SR*d); x=rng.standard_normal(n); out=np.zeros(n); seg=512
    fs=np.geomspace(f0,f1,n//seg+1)
    for k in range(0,n,seg):
        f=fs[k//seg]; out[k:k+seg]=bp(x[k:k+seg+0],max(f*0.6,40),min(f*1.6,20000))[:len(out[k:k+seg])]
    env=np.sin(np.linspace(0,np.pi,n))**2
    if rev: env=np.linspace(0,1,n)**2.5
    out=lp(out*env,9000); return norm(out)
def pop(f0=900,f1=320,d=0.09):
    t=t_(d); f=np.geomspace(f0,f1,len(t)); ph=2*np.pi*np.cumsum(f)/SR
    return norm(np.sin(ph)*np.exp(-t*38))
def tick(f=2600,d=0.025): t=t_(d); return norm(np.sin(2*np.pi*f*t)*np.exp(-t*220))
def boom(d=1.1,f0=95,f1=38):
    t=t_(d); f=np.geomspace(f0,f1,len(t)); s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*3.2)
    n=lp(rng.standard_normal(len(t)),900)*np.exp(-t*14)*0.8
    c=hp(rng.standard_normal(len(t)),2500)*np.exp(-t*40)*0.35
    return norm(s+n+c)
def crash(d=1.6): t=t_(d); return norm(hp(rng.standard_normal(len(t)),5000)*np.exp(-t*2.6))
def riser(d=0.7):
    t=t_(d); f=np.geomspace(180,1500,len(t)); s=np.sin(2*np.pi*np.cumsum(f)/SR)*0.4
    n=whoosh(d,400,7000,rev=True); env=np.linspace(0,1,len(t))**2
    return norm((s*env)+n*0.8)
def sparkle(d=0.7,k=10):
    out=np.zeros(int(SR*d))
    for i in range(k):
        f=rng.uniform(3500,8500); st=int(rng.uniform(0,d*0.6)*SR); tt=t_(0.25)
        x=np.sin(2*np.pi*f*tt)*np.exp(-tt*18); n=min(len(x),len(out)-st); out[st:st+n]+=x[:n]
    return norm(out)
def thud(d=0.25): t=t_(d); return norm(np.sin(2*np.pi*np.geomspace(160,60,len(t)).cumsum()/SR)*np.exp(-t*16))
def ring(d=0.45):
    t=t_(d); s=(np.sin(2*np.pi*1400*t)+np.sin(2*np.pi*1750*t))*(0.5+0.5*np.sign(np.sin(2*np.pi*18*t)))
    return norm(s*np.exp(-t*3))
def click(): return tick(4200,0.012)

# ---- cue sheet (seconds, matches compositions) ----
place(whoosh(0.5,3000,300),0.0,0.35)
place(pop(700,260,0.12),0.22,0.5); place(thud(),0.22,0.45)
place(click(),0.55,0.25)
place(pop(1000,420),1.46,0.45)
place(whoosh(0.25,500,4000),1.85,0.35,0.2)
place(whoosh(0.5,250,5000),2.33,0.6,-0.3)
place(pop(800,300),2.6,0.45)
place(thud(),3.56,0.6); place(pop(600,200,0.12),3.56,0.35)
place(sparkle(0.6,8),3.8,0.25)
place(riser(0.75),4.0,0.35)
place(boom(0.9),4.74,0.7); place(whoosh(0.3,4000,400),4.7,0.3)
place(pop(500,180,0.14),4.76,0.35)
place(boom(0.7,120,50),5.34,0.6)
for i in range(10): place(tick(2200+i*180),5.84+i*0.032,0.28,(-1)**i*0.3)
place(riser(0.3),5.86,0.3)
place(boom(1.3,80,32),6.15,1.0); place(crash(1.8),6.15,0.35)
place(sparkle(0.9,16),6.2,0.35,-0.2); place(sparkle(0.9,14),6.3,0.3,0.3)
place(pop(900,300),6.06,0.4)
place(whoosh(0.5,5000,250),6.48,0.55,0.3)
place(tick(1800,0.04),7.0,0.35); place(pop(900,350),7.24,0.45); place(pop(1100,500),7.5,0.4)
place(whoosh(0.22,400,3000),7.5,0.25)
for i in range(4): place(click(),7.9+i*0.03,0.3,(-1)**i*0.4)
place(whoosh(0.35,3000,400),7.88,0.3)
place(pop(800,300),8.1,0.35); place(whoosh(0.3,600,4500),8.56,0.4,-0.4)
place(whoosh(0.25,3000,600),9.48,0.3)
place(pop(700,260,0.12),9.7,0.45); place(whoosh(0.45,300,2500),9.8,0.22,0.3)
place(whoosh(0.4,3500,300),10.22,0.25); place(thud(),10.42,0.6)
for i in range(8): place(pop(1200-i*40,500,0.05),9.86+i*0.035,0.18,(-1)**i*0.3)
place(whoosh(0.4,3000,300),10.85,0.4)
place(pop(700,250,0.12),10.9,0.45); place(pop(900,330),11.0,0.4)
place(thud(),11.4,0.45); place(pop(1000,400),11.14,0.35); place(pop(900,350),11.25,0.35)
for i in range(12): place(tick(2400+(i%3)*300,0.02),11.42+i*0.035,0.22,(-1)**i*0.25)
place(pop(800,280),11.2,0.4)
place(ring(0.45),12.0,0.22)
place(sparkle(0.6,8),12.1,0.25)
mix=np.stack([L,R],1); peak=np.max(np.abs(mix)); mix=mix/peak*0.89
wf.write(sys.argv[1],SR,(mix*32767).astype(np.int16)); print('ok',peak)
