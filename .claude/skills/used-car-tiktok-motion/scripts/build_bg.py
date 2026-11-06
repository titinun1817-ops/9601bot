"""Cut vertical phone clips into one 1080x1920 30fps background frame sequence.

usage: python3 build_bg.py shots.json CLIPDIR OUTDIR
shots.json: [["20260918_143448.mp4", start_sec, n_frames, zoom, speed], ...]
  zoom  = slow push-in amount over the shot (0.04-0.06; 0 = none)
  speed = setpts factor (1.12 = 12% slower, to stretch a short clip)
Each shot is rendered separately; if a clip runs out, its last frame is held so the total
frame count is exact (timeline must match the voiceover).
"""
import json, subprocess, glob, shutil, os, sys, tempfile

shots = json.load(open(sys.argv[1])); src = sys.argv[2]; out = sys.argv[3]
os.makedirs(out, exist_ok=True)
tmp = tempfile.mkdtemp()
k = 1
for i, (clip, ss, n, z, sp) in enumerate(shots):
    d = f"{tmp}/{i:02d}"; os.makedirs(d)
    zf = f",scale=w='2*trunc(540*(1+{z}*t/{n/30:.3f}))':h=-2:eval=frame,crop=1080:1920" if z else ""
    subprocess.run(["ffmpeg", "-v", "error", "-ss", str(ss), "-i", os.path.join(src, clip), "-an", "-vf",
                    f"setpts={sp}*(PTS-STARTPTS),fps=30,scale=1080:1920,setsar=1{zf},eq=saturation=1.12:contrast=1.04",
                    "-frames:v", str(n), "-q:v", "3", f"{d}/%04d.jpg"], check=True)
    fs = sorted(glob.glob(d + "/*.jpg"))
    print(clip, "want", n, "got", len(fs))
    for j in range(n):
        shutil.copy(fs[min(j, len(fs) - 1)], f"{out}/{k:04d}.jpg"); k += 1
print("total frames", k - 1)
