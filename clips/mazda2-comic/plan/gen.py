F="../fonts/fontsource-kanit/files/"
css=f"""
@font-face{{font-family:K;font-weight:400;src:url({F}kanit-thai-400-normal.woff2)}}
@font-face{{font-family:K;font-weight:400;src:url({F}kanit-latin-400-normal.woff2);unicode-range:U+0000-00FF}}
@font-face{{font-family:K;font-weight:800;src:url({F}kanit-thai-800-normal.woff2)}}
@font-face{{font-family:K;font-weight:800;src:url({F}kanit-latin-800-normal.woff2);unicode-range:U+0000-00FF}}
:root{{--red:#E3202A;--acc:#FFD400;--ink:#0B0B0B;--paper:#F4EFE3}}
*{{box-sizing:border-box;margin:0}} body{{width:1080px;background:var(--ink);color:#fff;font-family:K;font-weight:400;font-size:40px;padding:48px}}
h1{{font-weight:800;font-size:72px;line-height:1.1}} h2{{font-weight:800;font-size:52px;margin:28px 0 12px;color:var(--acc)}}
.style{{border:4px solid var(--acc);padding:24px;font-size:34px;line-height:1.35;margin:24px 0}}
.sw{{display:inline-block;width:60px;height:60px;border:3px solid #fff;vertical-align:middle;margin-right:8px}}
.row{{display:flex;gap:24px;border-bottom:2px solid #333;padding:18px 0;align-items:flex-start}}
.t{{font-weight:800;color:var(--acc);min-width:210px}} .v{{color:#ddd}} b{{color:#fff;font-weight:800}}
.red{{color:var(--red)}} .grid{{display:grid;grid-template-columns:1fr 1fr;gap:28px}}
.fr{{background:#1a1a1a;border:3px solid #444}} .th{{width:100%;aspect-ratio:9/16;background-size:cover;background-position:center;position:relative;display:flex;align-items:center;justify-content:center}}
.th span{{background:var(--red);font-weight:800;font-size:44px;padding:6px 16px;transform:rotate(-4deg);text-align:center;line-height:1.15}}
.th .y{{background:var(--acc);color:var(--ink)}}
.cap{{padding:14px;font-size:30px;line-height:1.3}} .cap b{{color:var(--acc)}}
"""
head="""<div class=style><b>STYLE:</b> yellow / comic POW burst / comic-panel split / page-tear cut / receipt-printer roll / ink speed-lines + paper grain / drum&bass 172 (half-time)<br>
<span class=sw style="background:#E3202A"></span><span class=sw style="background:#FFD400"></span><span class=sw style="background:#0B0B0B"></span><span class=sw style="background:#F4EFE3"></span> BPM 172<br>
<b>ต่างจากคลิปก่อน:</b> เปลี่ยนครบ 7 ช่อง vs Yaris / Sienta / Attrage (คอนเซปต์การ์ตูน comic + ใบเสร็จ ยังไม่เคยใช้)</div>"""
def page(n,body): open(f"{n}.html","w").write(f"<html><head><meta charset=utf-8><style>{css}</style></head><body>{body}</body></html>")
story=[("0.0–3.2","HOOK","แฟลชรูปเร็ว → ระเบิด POW สีเหลือง + จอสั่น","[excited] ใครติดแบล็คลิสต์ เราช่วยได้... ดาวน์แค่เจ็ดหมื่นสี่!"),
("3.2–4.8","รุ่น","“MAZDA2 ได้!” สแลม + คลื่นกระแทก","[playfully] มาสด้าสอง ดีเซล ได้!"),
("4.8–7.2","จุดขาย 1","ปี 2016/17 · ออโต้ · สีแดง","[cheerfully] ปีสองพันสิบหก เกียร์ออโต้ สีแดงสด"),
("7.2–11.6","จุดขาย 2-3","1.5XD Hi Connect ดีเซล → มือเดียว กุญแจ 2 ดอก","[impressed] รถมือเดียว กุญแจครบสองดอก มีบุ๊คเซอร์วิสครบ"),
("11.6–14.6","จุดขาย 4-5","ไมล์ 10x,xxx กม. + Book Service → ไม่มีชนหนัก ไม่มีน้ำท่วม","(ดนตรี + ตัวหนังสือ)"),
("14.6–19.6","ราคา ★","258,000 ซื้อสดไม่มี VAT → ใบเสร็จพิมพ์ “ดาวน์ 74,000” ลงตรงคำพูด (จุดใหญ่สุด ค้าง ≥1.2 วิ)","[excited] ราคาสองแสนห้าหมื่นแปดพันบาท ซื้อสดไม่มีแวต / ใครติดแบล็คลิสต์ ดาวน์เจ็ดหมื่นสี่พันบาท"),
("19.6–23","CTA","โลโก้สแลม + ประกาย, ปุ่ม “ทักแชทส่งเคส” เต้น, บ้านรถสวย รัชดา-พระราม 9","[warmly] ทักแชทส่งเคสมาให้เช็กก่อนได้เลย")]
page("1_storyline","<h1>สตอรี่ไลน์ · MAZDA2 1.5XD 2016</h1>"+head+"".join(f"<div class=row><div class=t>{a}<br><span style='color:#fff'>{b}</span></div><div class=v><b>{c}</b><br>🎙 {d}</div></div>".replace("🎙","เสียง:") for a,b,c,d in story))
fr=[("p1","y","ติดแบล็คลิสต์<br>เราช่วยได้!","POW burst + สั่น","ฮิต: impact + crash","ฉีกกระดาษ →"),
("p3","","MAZDA2<br>ได้!","สแลม + shockwave","ฮิต: boom","ฉีกกระดาษ →"),
("p2","y","2016/17<br>ออโต้","แผงการ์ตูน 3 ช่อง","ฮิต: whoosh","ฉีก →"),
("p6","","ดีเซล 1.5XD<br>Hi Connect","กรอบหมึก + speed-lines","ฮิต: snare roll","ฉีก →"),
("p8","y","มือเดียว<br>กุญแจ 2 ดอก","ป้ายคำพูด slam","ฮิต: impact","ฉีก →"),
("p5","","ไมล์ 10x,xxx<br>Book Service","แผงแตกเฉียง","ฮิต: riser เริ่ม","ฉีก →"),
("p7","y","ดาวน์<br>74,000","ใบเสร็จพิมพ์ออก ★","ฮิต: เงียบ → BOOM ใหญ่สุด","ตัดดำ →"),
("p4","","[โลโก้]<br>ทักแชทส่งเคส","โลโก้สแลม + glint","ฮิต: impact + จบบีต","จบ")]
page("2_storyboard","<h1>สตอรี่บอร์ด</h1>"+head+"<div class=grid>"+"".join(f"<div class=fr><div class=th style=\"background-image:linear-gradient(#0006,#0006),url(../photos/{p}.jpg)\"><span class='{c}'>{t}</span></div><div class=cap><b>{i+1}.</b> {e}<br>{s}<br>{tr}</div></div>" for i,(p,c,t,e,s,tr) in enumerate(fr))+"</div>")
steps=[("1 สคริปต์","copy pass แล้ว 7 บรรทัด ไม่มีคำลงท้าย ไม่มีคำโฆษณาลอย"),("2 เสียง","ElevenLabs v3 · 7 ไฟล์ · ตรวจ hook / รุ่น / ตัวเลขด้วย transcribe"),("3 ภาพ","HTML 1080×1920 · Kanit + Bebas · โลโก้จริง (รอไฟล์)"),("4 เช็กภาพนิ่ง","contact sheet + ย่อ 180px ต้องอ่านดาวน์ออก"),("5 เรนเดอร์","วิดีโอ 30fps ~10 นาที (เบื้องหลัง)"),("6 เสียงบีต","DnB 172 + SFX · ดนตรีเงียบก่อนราคา"),("7 QA","ffprobe · frame strip · slop test 7 ข้อ"),("8 ส่ง","MP4 + แคปชั่น TikTok + fingerprint")]
page("3_workplan","<h1>แผนงาน</h1>"+head+"".join(f"<div class=row><div class=t>{a}</div><div class=v>{b}</div></div>" for a,b in steps)+"<h2>ไม่ใช้ในคลิป</h2><div class=v>“การันตีเครื่อง/เกียร์” (เป็นคำสัญญา) · ไมล์ในเสียง · “เจ้าบ้าน”</div>")
