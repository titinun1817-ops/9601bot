# Synth music (120 BPM) + SFX for the fast-cut template, then mix with a VO wav.
# Usage: python3 audio.py <duration_s> <cuts comma list> <hits "t:amp,..."> <pops comma list>
# Writes music.wav and sfx.wav; mix with ffmpeg (see README).
import sys, numpy as np, wave
SR=48000; D=float(sys.argv[1]); n=int(SR*D)
cuts=[float(x) for x in sys.argv[2].split(',') if x]
hits=[tuple(map(float,h.split(':'))) for h in sys.argv[3].split(',') if h]
pops=[float(x) for x in sys.argv[4].split(',') if x] if len(sys.argv)>4 else []
rng=np.random.default_rng(1); mus=np.zeros(n); sfx=np.zeros(n)
def add(buf,start,sig,a=1):
    i=int(start*SR); j=min(n,i+len(sig))
    if i<n: buf[i:j]+=sig[:j-i]*a
kt=np.arange(int(.35*SR))/SR; kick=np.sin(2*np.pi*(45+90*np.exp(-kt*28))*kt)*np.exp(-kt*9)
hat=rng.normal(0,1,int(.06*SR)); hat=np.diff(np.concatenate([[0],hat]))*np.exp(-np.arange(len(hat))/SR*70)*.25
duck=np.ones(n)
for b in range(int(D/.5)):
    s=b*.5
    if s>=D-1.0: break
    add(mus,s,kick*.9); add(mus,s+.25,hat)
    i=int(s*SR); L=min(int(.3*SR),n-i); duck[i:i+L]=np.minimum(duck[i:i+L],1-.6*np.exp(-np.arange(L)/SR*12))
for k in range(int(D/2)+1):
    L=int(2*SR); tt=np.arange(L)/SR; f=[55,55,65.4,49][k%4]
    add(mus,k*2,(np.sin(2*np.pi*f*tt)+.3*np.sin(2*np.pi*2*f*tt))*.35)
    f2=[220,261.6,329.6,196][k%4]; env=np.minimum(1,tt/.3)*np.minimum(1,(2-tt)/.3)
    add(mus,k*2,(np.sin(2*np.pi*f2*tt)+np.sin(2*np.pi*f2*1.5*tt)*.5)*.06*env)
mus*=duck; fe=int((D-1.2)*SR); mus[fe:]*=np.linspace(1,0,n-fe)
rng=np.random.default_rng(3)
def whoosh(L=.34):
    m=int(L*SR); x=rng.normal(0,1,m); tt=np.arange(m)/SR; env=np.sin(np.pi*tt/L)**2
    return (np.convolve(x,np.ones(5)/5,'same')-np.convolve(x,np.ones(50)/50,'same'))*env*.55
def hit(f=60,L=.6):
    m=int(L*SR); tt=np.arange(m)/SR
    return np.sin(2*np.pi*(f+140*np.exp(-tt*30))*tt)*np.exp(-tt*6)+rng.normal(0,1,m)*np.exp(-tt*35)*.35
def pop(L=.09):
    m=int(L*SR); tt=np.arange(m)/SR; return np.sin(2*np.pi*(900-5000*tt)*tt)*np.exp(-tt*45)*.5
def sparkle(L=.7):
    m=int(L*SR); tt=np.arange(m)/SR; y=np.zeros(m)
    for k in range(14):
        s=int(rng.random()*m*.7); f=2500+rng.random()*3000; l=int(.05*SR)
        seg=np.sin(2*np.pi*f*np.arange(l)/SR)*np.exp(-np.arange(l)/SR*60); y[s:s+l]+=seg[:max(0,min(l,m-s))]
    return y*.18*np.exp(-tt*2)
for c in cuts: add(sfx,c-.17,whoosh())
for t0,a in hits: add(sfx,t0,hit(),a); add(sfx,t0+.02,sparkle(),a)
for t0 in pops: add(sfx,t0,pop(),.6)
def w(name,x):
    x=x/(np.max(np.abs(x))+1e-9)*.8
    with wave.open(name,'wb') as f:
        f.setnchannels(1);f.setsampwidth(2);f.setframerate(SR);f.writeframes((x*32767).astype('<i2').tobytes())
w('music.wav',mus); w('sfx.wav',sfx)
