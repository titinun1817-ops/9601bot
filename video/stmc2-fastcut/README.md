# สงวนไทยรถมือสอง · เทมเพลตคลิปแฟสต์คัต (จากคลิป 3)

ผลงานอ้างอิง: `../renders/clip3-spacecab-yommaew.mp4` (9:16, 1080x1920, 30fps, 26 วิ)

## ไฟล์
- `clip3-template.html` – กราฟิก/แอนิเมชันทั้งคลิป ควบคุมด้วย `render(t)` (deterministic ต่อเฟรม)
  - ฉาก: `S=[[id,start,end],...]` · ข้อความอยู่ใน `<section class="scene">`
  - ฟุตเทจเป็นลำดับ JPEG ใน `fr/<shot>/0001.jpg…` (ตั้งใน `frames={...}`)
  - เวลาคำพูด/กระแทก: `HITS`, `BURSTS`, `RINGS`, `STARS` + บล็อก `if(t>=…)` ใน `render`
  - ฟังก์ชัน: `words` (คำเด้งทีละคำ), `slamBox` (กล่องแดงกระแทก+แสงวาบ), `logoSlam` (โลโก้หล่น), `count` (เลขวิ่ง), `popIn`, `slideIn`
- `render.js` – `node render.js stills 1.0 2.5` (ภาพนิ่ง) / `node render.js full [from] [to]` (เฟรมลง `out/`)
- `audio.py` – สร้าง `music.wav` + `sfx.wav`
- `logo-stmc2.png`, `logo-isuzu-st.png` – โลโก้พื้นใส

## ขั้นตอน
1. ตัดฟุตเทจเป็นเฟรม: `ffmpeg -ss S -t T -i in.mp4 -an -vf "fps=30,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=contrast=1.06:saturation=1.12:brightness=0.01,unsharp=5:5:0.4" -q:v 3 fr/<shot>/%04d.jpg`
2. เสียงพากย์ ElevenLabs เสียง Anan `tAV9ucNkXgK2k9TLxWkM` eleven_v4 เจน 1 ครั้ง แล้ว transcribe เอาเวลาคำ
3. แก้ข้อความ/เวลาใน HTML ให้ตรงคำพูด → `node render.js stills ...` เช็ค → `node render.js full`
4. `python3 audio.py 26 "2.5,5,7.5" "1.36:1,10.4:1.1" "0,2.7"`
5. มิกซ์: VO `loudnorm=I=-16`, music `loudnorm=I=-27`, sfx `volume=-6dB` → amix → `loudnorm=I=-14:TP=-1`
6. `ffmpeg -framerate 30 -i out/%04d.jpg -i mix.wav -c:v libx264 -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart out.mp4`
