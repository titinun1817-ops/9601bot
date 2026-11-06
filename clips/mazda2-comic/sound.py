import numpy as np, wave
SR=44100; D=24.2; N=int(SR*D)
R=dict(R1=0.30,R2=3.55,R3=5.70,R4=8.60,R5=14.60,R6=18.20,R7=21.10); LAND=R['R6']+1.25
rng=np.random.default_rng(7)
def lp(x,a):
    A=np.broadcast_to(np.asarray(a,float),x.shape); y=np.zeros_like(x); s=0.
    for i in range(len(x)): s+=A[i]*(x[i]-s); y[i]=s
    return y
def env(n,a,d): t=np.arange(n)/SR; return np.minimum(t/a,1)*np.exp(-t/d)
def kick(): n=int(.35*SR);t=np.arange(n)/SR; f=45+120*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,.002,.12)
def snare(): n=int(.25*SR);t=np.arange(n)/SR; return (0.6*rng.standard_normal(n)*env(n,.001,.07)+0.5*np.sin(2*np.pi*190*t)*env(n,.001,.05))
def hat(): n=int(.05*SR); x=rng.standard_normal(n); x=x-lp(x,.5); return x*env(n,.0005,.012)*.5
def add(buf,x,t,g=1.):
    i=int(t*SR); j=min(len(buf),i+len(x)); 
    if i<len(buf) and j>i: buf[i:j]+=g*x[:j-i]
music=np.zeros(N); sfx=np.zeros(N)
bpm=172; b=60/bpm; K,S,H=kick(),snare(),hat()
# DnB two-step pattern per bar (8 eighths): K . . . S . . K? classic: K on 1, S on 2&4 (eighth 2,6), K on eighth 5(3.5)
t0=0.6; bar=4*b
drop0,drop1=LAND-1.3,LAND
bars=int((D-t0)/bar)+2
for k in range(bars):
    s=t0+k*bar
    for e,kind in [(0,'K'),(2,'S'),(5,'K'),(6,'S')]:
        tt=s+e*b/2
        if drop0<=tt<drop1 or tt>D-0.3: continue
        add(music,K if kind=='K' else S,tt,0.9 if kind=='K' else 0.6)
    for e in range(8):
        tt=s+e*b/2+(b/4 if e%2 else 0)*0
        if not(drop0<=tt<drop1): add(music,H,tt,0.35 if e%2 else 0.2)
# reese bass: detuned saws following root notes
t=np.arange(N)/SR
roots=[41.2,41.2,49.0,36.7]
f=np.array([roots[int(max(0,x-t0)//bar)%4] for x in t[::441]]).repeat(441)[:N]
f=np.pad(f,(0,N-len(f)),'edge')
ph1=np.cumsum(f)/SR; ph2=np.cumsum(f*1.012)/SR
saw=lambda p:2*(p%1)-1
bass=(saw(ph1)+saw(ph2))*0.5
cut=0.02+0.03*(0.5+0.5*np.sin(2*np.pi*t*bpm/60/2))
bass=lp(bass,cut)*0.55
gate=np.ones(N); gate[t<t0]=0; gate[(t>=drop0)&(t<drop1)]=0
music+=bass*gate
# stab chords on hook
# SFX
def impact(g=1.,dec=.5):
    n=int(1.2*SR); tt=np.arange(n)/SR; f=60*np.exp(-tt*4)+30
    return (np.sin(2*np.pi*np.cumsum(f)/SR)*env(n,.001,dec)+lp(rng.standard_normal(n),.15)*env(n,.001,.15))*g
def whoosh(dur=.35):
    n=int(dur*SR); x=rng.standard_normal(n); c=np.linspace(.02,.4,n)**1.5; e=np.sin(np.linspace(0,np.pi,n))**2
    return lp(x,c)*e*.6
def riser(dur):
    n=int(dur*SR); x=rng.standard_normal(n); c=np.linspace(.01,.5,n)**2; return lp(x,c)*np.linspace(0,1,n)**2*.5
def tear(): n=int(.3*SR); x=rng.standard_normal(n)*(rng.random(n)<.35); return (x-lp(x,.3))*env(n,.003,.09)*.8
def printer(dur):
    n=int(dur*SR); tt=np.arange(n)/SR; x=np.sign(np.sin(2*np.pi*22*tt))*0.5+0.5; return lp(rng.standard_normal(n),.2)*x*.35+np.sin(2*np.pi*900*tt)*x*.04
add(sfx,impact(1.,.6),0.6); add(sfx,impact(.7,.4),1.85)
for k in range(6): add(sfx,whoosh(.12),k*0.1,0.5)
add(sfx,impact(.9,.5),3.6); add(sfx,whoosh(.4),3.3)
for s in [5.6,8.4,10.4,12.4,13.4,14.5]: add(sfx,tear(),s); add(sfx,whoosh(.3),s-0.05,.7)
for s in [5.6,8.4,10.4,12.4,13.4]: add(sfx,impact(.45,.25),s+0.38)
add(sfx,impact(.6,.35),14.65)
add(sfx,riser(LAND-(R['R6']-0.5)),R['R6']-0.5,1.)
add(sfx,printer(LAND-(R['R6']-0.5)),R['R6']-0.5,1.)
add(sfx,impact(1.6,.9),LAND); add(sfx,whoosh(.6),LAND-0.1,.6)
add(sfx,impact(1.,.6),21.05); add(sfx,whoosh(.4),20.8)
def save(n,x):
    x=x/ (np.abs(x).max()+1e-9)*0.9
    w=wave.open(n,'wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes((x*32767).astype('<i2').tobytes());w.close()
save('music.wav',music); save('sfx.wav',sfx)
print('LAND',LAND)
