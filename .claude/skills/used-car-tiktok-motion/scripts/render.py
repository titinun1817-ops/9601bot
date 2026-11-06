"""Render an HTML motion template over pre-extracted background frames.

usage:
  python3 render.py --style templates/sticker_pop_epic.html --bg WORK/bg --fonts WORK/fonts \
      --frames 900 --out WORK/video_noaudio.mp4
  python3 render.py ... --stills 1.0,2.5,7.8      # quick check frames -> WORK/st_<t>.jpg

The style file = DOM/CSS, then a line `<!--JS-->`, then <script> with render(t) (see template).
Background frames are bg/0001.jpg ... (1080x1920, 30 fps) made by build_bg.py.
Fonts dir holds Kanit woff2 files from the npm package @fontsource/kanit (files/kanit-{thai,latin}-{w}-{style}.woff2).
"""
import argparse, glob, subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("--style", required=True)
ap.add_argument("--engine", default=str(Path(__file__).parent.parent / "templates" / "engine.html"))
ap.add_argument("--bg", required=True)
ap.add_argument("--fonts", required=True)
ap.add_argument("--frames", type=int, required=True)
ap.add_argument("--out", default="video_noaudio.mp4")
ap.add_argument("--stills", default="")
a = ap.parse_args()

TH, LA = "U+0E00-0E7F", "U+0000-00FF,U+2000-206F,U+2190-21FF,U+2713,U+00D7"
fonts = Path(a.fonts).resolve()
ff = ""
for w in (300, 400, 500, 700, 800, 900):
    for st in ("normal", "italic"):
        for sub, rng in (("thai", TH), ("latin", LA)):
            f = fonts / f"kanit-{sub}-{w}-{st}.woff2"
            if f.exists():
                ff += f"@font-face{{font-family:K;font-weight:{w};font-style:{st};src:url({f.as_uri()});unicode-range:{rng}}}\n"
eng = Path(a.engine).read_text()
dom, js = Path(a.style).read_text().split("<!--JS-->")
bg = Path(a.bg).resolve().as_uri() + "/"
html = eng.replace("/*FONTS*/", ff).replace("<!--STYLE-->", dom).replace("<!--SCRIPT-->", js + f"\n<script>BGDIR='{bg}';</script>")
page = Path(a.out).resolve().parent / "_page.html"
page.write_text(html, encoding="utf-8")

exe = sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux*/chrome"))
with sync_playwright() as p:
    br = p.chromium.launch(executable_path=exe[-1] if exe else None)
    pg = br.new_page(viewport={"width": 1080, "height": 1920})
    pg.on("pageerror", lambda e: print("PAGEERROR", e))
    pg.goto(page.as_uri())
    pg.evaluate("init()")
    if a.stills:
        for tt in [float(x) for x in a.stills.split(",")]:
            pg.evaluate(f"go({int(round(tt * 30))})")
            pg.screenshot(path=str(page.parent / f"st_{tt:.2f}.jpg"), type="jpeg", quality=80)
    else:
        ffm = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "image2pipe", "-framerate", "30", "-i", "-",
                                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "veryfast",
                                "-movflags", "+faststart", a.out], stdin=subprocess.PIPE)
        for i in range(a.frames):
            pg.evaluate(f"go({i})")
            ffm.stdin.write(pg.screenshot(type="jpeg", quality=90))
        ffm.stdin.close(); ffm.wait()
    br.close()
