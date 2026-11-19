# Footage prep (run before HyperFrames)

Source: Drive `IMG_7754.MOV` (4K HEVC, vertical). Generated media is git-ignored.

1. `tx.py audio.wav large-v3 words.json` — Thai word timings (faster-whisper).
2. `bake2.py camera.json IMG_7754.MOV cam.mp4` — punch-ins cropped from the 4K source (out t = src t − 0.7 s), then mux audio + 2.5 s freeze → `assets/footage.mp4`.
3. Extract `cam.mp4` to `frames/%04d.jpg`; `seg.py u2net_human_seg frames masks 0 390` — person mattes.
4. `cut.py` → `cut/` (RGBA presenter) and `ring/` (white glow outline) → VP9-alpha `assets/cut.webm`, `assets/ring.webm` (+2.5 s freeze).
5. `track.py` — building tracking for the "ชั้น 2" / "อีซูซุ สยามซิตี้" pins (pasted into `compositions/front.html` as `TRACK`).
