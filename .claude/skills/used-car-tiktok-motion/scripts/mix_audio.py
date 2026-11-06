"""Synth beat + SFX + voiceover mix (all generated locally, no music licensing issues).

usage: python3 mix_audio.py cues.json vo.mp3 out.wav
cues.json example (times in seconds on the video timeline):
{
 "dur": 30.0, "vo_at": 0.15,
 "vo_lines": null,            // or [[src_a, src_b, place_at, tempo], ...] to split/move/speed lines (tempo<=1.3)
 "whoosh_big": [2.85, 10.0], "whoosh_small": [15.88],
 "pop": [0.12, 1.9], "boom": [[2.35, 0.9], [23.65, 1.0]], "sparkle": [7.7, 23.65],
 "riser": [[23.65, 1.9]],     // [hit_time, length] riser ends exactly on the hit
 "ticks": [[22.0, 23.6, 0.07]], "clicks": [22.55, 22.95, 23.3],
 "music_mute_before": 2.8     // half-time beat during the hook
}
Then mux: ffmpeg -i video_noaudio.mp4 -i out.wav -filter_complex "[1:a]loudnorm=I=-14:TP=-1.5[a]"
          -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart final.mp4
"""
import numpy as np, wave, sys, json, subprocess
cfg = json.load(open(sys.argv[1])); VO = sys.argv[2]; OUT = sys.argv[3]
SR = 48000; DUR = cfg["dur"]; BPM = 120; beat = 60 / BPM
rng = np.random.default_rng(3)
N = int(SR * DUR)
def env(n, a=0.002, d=0.2):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-t / d)

def add(buf, sig, at):
    i = int(at * SR); j = min(len(buf), i + len(sig))
    if i < len(buf): buf[i:j] += sig[:j - i]

def kick(n=int(.35 * SR)):
    t = np.arange(n) / SR; f = 50 + 110 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)

def noise(n, d):
    return rng.standard_normal(n) * env(n, .001, d)

def hp(x, k=0.95):
    y = np.zeros_like(x); p = 0
    for i in range(1, len(x)): p = k * (p + x[i] - x[i - 1]); y[i] = p
    return y

def tone(f, n, d, wave_="saw"):
    t = np.arange(n) / SR
    s = 2 * ((t * f) % 1) - 1 if wave_ == "saw" else np.sin(2 * np.pi * f * t)
    return s * env(n, .005, d)

def whoosh(n=int(.45 * SR)):
    x = rng.standard_normal(n); t = np.arange(n) / SR
    e = np.sin(np.pi * t / t[-1]) ** 2
    # crude band sweep via moving-average difference
    out = np.convolve(x, np.ones(6) / 6, "same") - np.convolve(x, np.ones(40) / 40, "same")
    return out * e * 0.9

def pop(n=int(.12 * SR)):
    t = np.arange(n) / SR; f = 900 * np.exp(-t * 25) + 300
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 35)

def boom(n=int(1.4 * SR)):
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * np.cumsum(40 + 60 * np.exp(-t * 8)) / SR) * np.exp(-t * 2.5) * 1.2
            + noise(n, .25) * .35)

def sparkle(n=int(1.0 * SR)):
    s = np.zeros(n)
    for k in range(9):
        f = 2400 + 300 * k; m = int(.08 * SR)
        add(s, tone(f, m * 4, .12, "sin") * .25, k * .07)
    return s

def tick(n=int(.03 * SR)):
    return noise(n, .006)

def riser(d):
    n=int(d*SR); t=np.arange(n)/SR; x=rng.standard_normal(n)
    y=np.convolve(x,np.ones(4)/4,'same')*(t/d)**2*.8
    f=200+1800*(t/d)**2; y+=np.sin(2*np.pi*np.cumsum(f)/SR)*(t/d)**2*.25
    return y

music=np.zeros(N); sfx=np.zeros(N)
hat=hp(noise(int(.06*SR),.02)); clap=hp(noise(int(.25*SR),.08)); bass=[55,55,65.4,49]
for b in range(int(DUR/beat)+1):
    t0=b*beat
    if t0>=DUR-.6: break
    if t0<cfg.get("music_mute_before",0) and b%2==1: continue
    add(music,kick()*.9,t0)
    if b%2==1: add(music,clap*.45,t0)
    add(music,hat*.25,t0+beat/2); add(music,hat*.12,t0+beat*.75)
    f=bass[(b//4)%4]; add(music,tone(f,int(beat*.9*SR),.25)*.28,t0)
    if b%4==0: add(music,tone(f*4,int(.6*SR),.3,"sin")*.12,t0+beat/2)
for c in cfg.get("whoosh_big",[]): add(sfx,whoosh()*.55,c-.22)
for c in cfg.get("whoosh_small",[]): add(sfx,whoosh()*.25,c-.15)
for a in cfg.get("pop",[]): add(sfx,pop()*.35,a)
for at,amp in cfg.get("boom",[]): add(sfx,boom()*amp,at)
for at in cfg.get("sparkle",[]): add(sfx,sparkle()*.7,at)
for at,d in cfg.get("riser",[]): add(sfx,riser(d),at-d)
for l in cfg.get("clicks",[]): add(sfx,pop()*.5,l); add(sfx,tick()*.6,l)
for a,b,step in cfg.get("ticks",[]):
    t=a
    while t<b: add(sfx,tick()*.2,t); t+=step

raw=subprocess.run(['ffmpeg','-v','error','-i',VO,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout
vo=np.frombuffer(raw,np.float32).astype(float)
V=np.zeros(N)
def seg(a,b,tempo=1.0):
    x=vo[int(a*SR):int(b*SR)].astype(np.float32)
    if tempo!=1.0:
        x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-f','f32le','-ar',str(SR),'-ac','1','-i','-','-af',f'atempo={tempo}','-f','f32le','-'],input=x.tobytes(),capture_output=True).stdout,np.float32)
    x=x.astype(float); f=int(.01*SR); x[:f]*=np.linspace(0,1,f); x[-f:]*=np.linspace(1,0,f); return x
if cfg.get("vo_lines"):
    for a,b,at,tp in cfg["vo_lines"]: add(V,seg(a,b,tp),at)
else:
    add(V,vo,cfg.get("vo_at",0.15))
V/=np.max(np.abs(V))
envv=np.convolve(np.abs(V),np.ones(int(.15*SR))/int(.15*SR),'same'); duck=1-.55*np.clip(envv/.08,0,1)
mix=music*.5*duck+sfx*.55+V
fade=np.ones(N); fs=int(.5*SR); fade[-fs:]=np.linspace(1,0,fs); mix*=fade; mix/=np.max(np.abs(mix))*1.05
st=np.stack([mix,mix],1)
with wave.open(OUT,'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes())
print('wrote',OUT)
