import os, sys, json, shutil, subprocess, numpy as np
import pycapcut as cc
from pycapcut import TrackType, TextSegment, TextStyle, TextBorder, TextBackground, ClipSettings, VideoSegment, AudioSegment, Timerange

ROOT, MOB, SX, CUES, WINROOT = sys.argv[1:6]   # staging root, mobile files dir, sfx dir, SFX_timing.txt, "C:/ISUZU_NLR"
MEDIA = os.path.join(ROOT, "media"); PROJ = os.path.join(ROOT, "CapCut_Projects")
shutil.rmtree(ROOT, ignore_errors=True); os.makedirs(MEDIA); os.makedirs(PROJ)
END = 25.4
def us(s): return int(round(s * 1e6))
def tr(a, b): return Timerange(us(a), us(b - a))

# ---- media (ASCII names so Windows paths are safe)
m = {"footage": "footage.mp4", "gfx": "graphics_bluescreen.mp4", "vo": "voiceover.mp3", "music": "music.mp3", "sfxmix": "sfx_mix.mp3"}
shutil.copy(f"{MOB}/1_ฟุตเทจ.mp4", f"{MEDIA}/footage.mp4")
shutil.copy(f"{MOB}/2_ตัวหนังสือ_จอฟ้า.mp4", f"{MEDIA}/graphics_bluescreen.mp4")
shutil.copy(f"{MOB}/3_เสียงพากย์.mp3", f"{MEDIA}/voiceover.mp3")
shutil.copy(f"{MOB}/5_เพลง.mp3", f"{MEDIA}/music.mp3")
shutil.copy(f"{MOB}/4_เสียงเอฟเฟค.mp3", f"{MEDIA}/sfx_mix.mp3")

# ---- SFX cues: parse timing sheet, copy each file with ASCII name, compute volume to match the mix
cues = []
for ln in open(CUES, encoding="utf-8").read().splitlines()[1:]:
    p = ln.split()
    if not p: continue
    start = float(p[0]); name = ln.split("วิ  ")[1].split("  (")[0]; lvl = int(ln.split("ระดับ ")[1].split("%")[0]) / 100
    cues.append((start, name, lvl))
sfx_files = {}
for i, (st, name, lvl) in enumerate(cues):
    if name not in sfx_files:
        dst = f"sfx_{len(sfx_files)+1:02d}.mp3"; shutil.copy(f"{SX}/{name}", f"{MEDIA}/{dst}")
        a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f"{SX}/{name}", "-f", "f32le", "-ac", "1", "-"], capture_output=True).stdout, np.float32)
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{SX}/{name}"], capture_output=True, text=True).stdout)
        sfx_files[name] = (dst, float(np.abs(a).max()), dur)
open(f"{ROOT}/sfx_names.txt", "w", encoding="utf-8").write("\n".join(f"{v[0]} = {k}" for k, v in sfx_files.items()) + "\n")

def add_audio(sc, with_individual_sfx):
    sc.add_track(TrackType.audio, "เสียงพากย์")
    sc.add_segment(AudioSegment(f"{MEDIA}/voiceover.mp3", tr(0, END)), "เสียงพากย์")
    sc.add_track(TrackType.audio, "เพลง")
    sc.add_segment(AudioSegment(f"{MEDIA}/music.mp3", tr(0, END)), "เพลง")
    if not with_individual_sfx:
        sc.add_track(TrackType.audio, "เอฟเฟคเสียง")
        sc.add_segment(AudioSegment(f"{MEDIA}/sfx_mix.mp3", tr(0, END)), "เอฟเฟคเสียง"); return
    lanes = []  # greedy non-overlapping lanes
    for st, name, lvl in sorted(cues):
        dst, pk, dur = sfx_files[name]
        en = min(st + int(dur * 1000) / 1000 - 0.002, END)
        for li, last in enumerate(lanes):
            if last <= st - 0.01: lanes[li] = en; break
        else:
            lanes.append(en); li = len(lanes) - 1; sc.add_track(TrackType.audio, f"SFX_{li+1}")
        vol = min(2.0, 0.55 * lvl * (10 ** (-3 / 20)) / max(pk, 1e-3) * 1.25)  # 1.25 ≈ loudnorm makeup in final mix
        sc.add_segment(AudioSegment(f"{MEDIA}/{dst}", tr(st, en), volume=round(vol, 3)), f"SFX_{li+1}")

def footage(sc):
    sc.add_track(TrackType.video, "ฟุตเทจ")
    sc.add_segment(VideoSegment(f"{MEDIA}/footage.mp4", tr(0, END)), "ฟุตเทจ")

folder = cc.DraftFolder(PROJ)

# ===== Project A: full graphics (chroma-keyed overlay) =====
A = folder.create_draft("ISUZU_NLR_กราฟิกเต็ม", 1080, 1920, 30)
footage(A)
A.add_track(TrackType.video, "กราฟิก", relative_index=1)
g = VideoSegment(f"{MEDIA}/graphics_bluescreen.mp4", tr(0, END)); g.add_chroma("#0000FFFF", intensity=25, shadow=10)
A.add_segment(g, "กราฟิก")
add_audio(A, with_individual_sfx=True)
A.save()

# ===== Project B: native editable CapCut text =====
B = folder.create_draft("ISUZU_NLR_แก้คำได้", 1080, 1920, 30)
footage(B)
Y = lambda py: round((960 - py) / 960, 3)   # pixel y (top=0) -> CapCut transform_y
YEL, BLK, WHT = (1.0, 0.831, 0.0), (0.067, 0.067, 0.067), (1, 1, 1)
STY = {
  "lead":  dict(style=TextStyle(size=9,  bold=True, italic=True, color=WHT, align=1), background=TextBackground(color="#111111", alpha=0.95)),
  "kb":    dict(style=TextStyle(size=15, bold=True, italic=True, color=BLK, align=1), background=TextBackground(color="#FFD400")),
  "cap":   dict(style=TextStyle(size=7.5, bold=True, italic=True, color=YEL, align=1), background=TextBackground(color="#111111")),
  "name":  dict(style=TextStyle(size=19, bold=True, italic=True, color=YEL, align=1), border=TextBorder(color=BLK, width=60)),
  "badge": dict(style=TextStyle(size=10, bold=True, italic=True, color=YEL, align=1), background=TextBackground(color="#111111")),
  "stamp": dict(style=TextStyle(size=15, bold=True, italic=True, color=BLK, align=1), background=TextBackground(color="#FFD400"), border=TextBorder(color=BLK, width=25)),
}
S = [
 ('lead','// สี่ล้อจัมโบ้ //',0.20,4.32,265), ('kb','ตู้รั่วไหม?',1.62,4.32,480), ('cap','พิสูจน์ให้ดูกันจะๆ!',2.75,4.32,720),
 ('name','ISUZU NLR',5.15,7.38,370), ('badge','EURO 5',6.1,7.38,570),
 ('lead','// จับเข้าจุดทดสอบน้ำ //',7.55,11.78,265), ('kb','ฝนกระหน่ำ',9.0,11.78,480), ('cap','ลุยให้ดูทุกมุม',10.55,11.78,720),
 ('lead','// ยังไม่พอ! //',11.92,15.42,265), ('kb','ฉีดน้ำแรงดันสูง',12.78,15.42,480), ('cap','อัดเข้าไปอีก!',14.55,15.42,720),
 ('lead','// ถ้าตู้ดีจริง //',15.6,17.88,265), ('kb','น้ำต้องไม่เข้า!',16.68,17.88,480),
 ('kb','ของสด',18.0,19.25,300), ('kb','ของแห้ง',18.8,19.25,500),
 ('stamp','วิ่งไม่ติดเวลา!',19.32,21.85,430), ('cap','ขนได้หายห่วง',19.9,21.85,720),
 ('lead','// สนใจสี่ล้อจัมโบ้ //',21.95,END,265), ('kb','ทักแชท',22.1,END,480), ('cap','อีซูซุ สงวนไทย',22.85,END,730),
]
INTRO = {"lead": "向右滑动", "kb": "弹出", "cap": "放大", "name": "弹出", "badge": "放大", "stamp": "弹出"}
# one text track per role so overlapping lines never collide
roles = []
for ty, *_ in S:
    if ty not in roles: roles.append(ty)
for i, r in enumerate(roles): B.add_track(TrackType.text, f"ข้อความ_{r}", relative_index=i + 1)
# the two kb lines in the ของสด/ของแห้ง scene overlap -> put the second on its own track
B.add_track(TrackType.text, "ข้อความ_kb2", relative_index=len(roles) + 1)
for ty, txt, a, b, y in S:
    seg = TextSegment(txt, tr(a, b), clip_settings=ClipSettings(transform_y=Y(y)), **STY[ty])
    try: seg.add_animation(getattr(cc.TextIntro, INTRO[ty]), duration=us(0.3))
    except Exception as e: print("intro skip", ty, e)
    track = "ข้อความ_kb2" if txt == "ของแห้ง" else f"ข้อความ_{ty}"
    B.add_segment(seg, track)
add_audio(B, with_individual_sfx=True)
B.save()

# ---- rewrite local staging paths -> Windows path
for d in os.listdir(PROJ):
    for fn in ("draft_content.json", "draft_meta_info.json"):
        p = os.path.join(PROJ, d, fn)
        if not os.path.exists(p): continue
        s = open(p, encoding="utf-8").read().replace(MEDIA, WINROOT + "/media")
        s = s.replace(json.dumps(MEDIA)[1:-1], WINROOT + "/media")
        open(p, "w", encoding="utf-8").write(s)
print("ok", os.listdir(PROJ))
