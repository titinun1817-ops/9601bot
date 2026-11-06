---
name: "blacklist-project-taste"
description: "อ่านก่อนทุกครั้ง ก่อนเริ่มงานใดๆ ในโปรเจกต์ ติดแบล็คลิสต์ ก็ออกรถได้ (TikTok @blacklist.maneema): สไตล์ที่เจ้าของชอบ, ขั้นตอนบังคับ (สตอรี่ไลน์/สตอรี่บอร์ด/แผนงานเป็นรูป), กฎคำพูดและโลโก้, ตัวอย่างที่ผ่านแล้ว"
---

# Blacklist project: taste + rules (READ FIRST, EVERY TIME)

Use before ANY work in the project "ติดแบล็คลิสต์ ก็ออกรถได้": car clips, educational/viral clips, captions, scripts, thumbnails, ideas. Reply in Thai, casual, short (phone screen). After reading this, read `blacklist-car-clip` for the car-clip build pipeline (voice, render, sound, QA). This file is the owner's taste and the must-do checklist; if the two conflict, the user's latest message wins, then this file.

## 0. Who and why
- Owner sells used cars to people with blacklisted / poor credit through a TikTok page and wants content EVERY DAY. Goal of every clip: viewers DM ("ทักแชทส่งเคส"), not just views.
- Owner works fast and often needs things ready to post now. Don't ask what can be decided from this file; decide, then say in one line what you chose.
- Owner tests clips on the real page and keeps what sells. Treat the proven style below as evidence, not as taste to be improved away.

## 1. MANDATORY before building any clip (owner preference)
For EVERY video clip made or edited, first produce THREE readable images and send them (SendUserFile, display render), then build:
1. **Story line (สตอรี่ไลน์)** - one image: hook -> beats -> price/payoff -> CTA, each with start-end seconds and the exact voice line.
2. **Storyboard (สตอรี่บอร์ด)** - one image: 6-8 frames, one per scene, 9:16 thumbnails (use the real photos / mock text), with on-screen text, the effect, the SFX/beat hit, and the transition into the next scene.
3. **Work plan (แผนงาน)** - one image: steps (script check -> voice -> visuals -> stills check -> render -> sound -> QA -> deliver), what is verified, render time, deliverables (MP4 + caption).
- Every image carries a STYLE header: the fingerprint line (accent / hook device / photo reveal / transition / number reveal / texture / beat), a palette swatch, BPM, and "what changed vs last clip".
- Images must be readable on a phone: Thai text >= 40px on a 1080px-wide canvas, high contrast, max ~6 lines per block, Kanit font, brand red #E3202A + the clip's accent. Render them from HTML with the same fonts (Playwright stills), not as markdown tables.
- Apply the same three images to non-car clips and to edits. If the user already approved the plan in this chat and only asks for a tweak, resend just the changed image(s).
- Never skip because it is "just a small change".

## 2. The style the owner chose and keeps (proven)
- **HYPE is the main style.** 9:16, 1080x1920, ~20-23s: hook (photo strobe -> big slam text with shake -> "<MODEL> ได้!" slam + shockwave) -> 5 photo scenes, one selling point each (keyword box slam, light sweep, speed streaks, corner brackets, fast cuts) -> price card (down payment slam, then the number reveal landing exactly on the spoken number with the biggest SFX hit, hold >= 1.2s) -> CTA (big logo slam + glint, pulsing "ทักแชทส่งเคส", location line).
- **Never repeat a look.** Each clip changes at least 3-4 of 7 slots and shares at most 4 with each of the last 3 clips. Write the fingerprint before building and report it.
- Loud on purpose but with ONE focal moment (the price reveal). Two-font max (Kanit + Bebas Neue / one display face), tabular numbers, no AI-ad clichés (no gradient text, no purple-cyan or orange-pink gradients, no emoji icons inside the video, max 1 white flash).
- Sound: procedural beat that fits the variant, impacts/whooshes/riser, music dips before the price and returns on it, ducked under the voice.
- Safe zone: key content between y~280 and y~1500.

### Variants already used (do not reuse a combination within the last 3 clips)
| Clip | Accent | Hook device | Photo reveal | Transition | Number reveal | Texture | Beat |
|---|---|---|---|---|---|---|---|
| template (Civic) | red | strobe + slash split | strip-slice | diagonal wipe | slot reels | rays/streaks | EDM 120 |
| gold (CR-V) | gold | slash split | - | - | slot | - | trap 140 |
| cyan (Civic FB) | cyan | zoom-punch + stamp | iris | glitch cut | flip-board | - | phonk 105 |
| lime | lime | shatter | - | - | odometer | - | trap 140 |
| blue (Mazda2) | blue | card flip | - | - | scramble-decode | - | amapiano 112 |
| orange (Yaris) | orange | 3-2-1 countdown + caution tape | shutter slats | zoom-blur cut | speedometer gauge | - | funk 110 |
| violet-neon (Sienta, Oct 24) | violet | neon-sign flicker + strobe | single panel with neon frame + counter tag | whip-pan horizontal blur | 7-segment LED roll | perspective neon grid floor + grain | see sound.py |
| mint-tape (Attrage, Oct 25) | mint | tape slap then torn in half | polaroid drop-in with tape | spin-zoom cut | digit-by-digit stamp | halftone dots | see sound.py |
| yellow-comic (Mazda2 1.5XD, Nov 6) | yellow | comic POW burst + shake | comic-panel split (3 panels fly in) | page-tear jagged wipe | receipt-printer roll + scramble | ink focus-lines + paper grain | drum&bass 172 |
Unused ideas: game level-up, comic panels, receipt printer, gacha capsule, GPS route, polaroid scrapbook (partly used), neon night city (partly used). After each new clip, give the fingerprint so the user can save it here.
- More fresh ideas: search the ui-ux-pro-max style data (`python3 $HOME/.cache/ui-ux-pro-max/.claude/skills/ui-ux-pro-max/scripts/search.py "<mood words>" --domain style -n 5`) and borrow ONE device per clip (shape language, texture, reveal, colour block); skip anything that breaks the no-cliché rules above. Details in `blacklist-car-clip` section 0.

## 3. Non-car content (educational / viral, built to get DMs)
- Owner wants content beyond car listings, fully AI-generated, no new filming. Built so far: scam warning ("4 สัญญาณอันตราย"), myth bureau, FAQ. Files in the Project: claude/edu-common.css/js, edu-sound.py, edu-*-clip.html.
- Pattern: hook "ใครติดแบล็คลิสต์อยู่" + red slam statement -> numbered items (chip "#n", red title box, SVG icon card, short quote line, stamp) -> 3-word summary slam (e.g. ไม่เชื่อ / ไม่รีบ / ไม่โอน) -> CTA with logo, "มาดูรถจริงก่อนตัดสินใจ", location, disclaimer.
- Same rules as cars: logo, copy tone, safe zone, one focal moment, fingerprint variation, the three planning images.
- Icon cards use Phosphor SVG icons from npm (`npm pack @phosphor-icons/core`, e.g. warning, wallet, key, phone, chat-circle-dots), one weight per clip, recoloured with the clip tokens. No emoji.

## 4. Words and claims (hard rules)
- Message: "ใครติดแบล็คลิสต์ก็ออกรถได้ / เราช่วยได้". NEVER "สายแบล็คลิสต์". Empathetic, never shaming, friend-to-friend tone, no jargon, no hard sell.
- Never promise approval ("ผ่านแน่นอน", "ขอแค่มีเงินดาวน์ก็ออกได้", "การันตีผ่าน"). Use "มีโอกาสออกรถ" / "ส่งเคสมาให้เช็กก่อน". Always show "*ผลอนุมัติขึ้นอยู่กับการพิจารณาของไฟแนนซ์" on the price card/CTA.
- Facts only from the listing (model, year, price, down payment, installment x 72, mileage, owners, keys). Do not add features not listed.
- If installment is for good credit only, make the blacklist down payment the hero; show the good-credit installment small and labelled.
- Do NOT mention "เจ้าบ้าน" anywhere.
- Price line: "ซื้อสดไม่มี VAT". Location: "บ้านรถสวย รัชดา-พระราม 9". CTA: "ทักแชทส่งเคส".
- Official logo (red/black shield "ติดแบล็คลิสต์ มานี่มา") is REQUIRED in every clip: small badge top-right + big CTA slam. Source: Project doc claude/logo-maneema-720.png.b64.txt (base64 PNG) -> `base64 -d > logo_full.png`. Never retype it as text.

## 5. Voice (ElevenLabs, chosen by owner)
- Voice ID tAV9ucNkXgK2k9TLxWkM via Speko audio_synthesize, model eleven_v3, one call per line, emotion tag first. Cute, natural, human - not AI-sounding.
- Script: no ending particles (คะ/ค่ะ/นะ/น้า); "ผ่อนต่อเดือน" not "ผ่อนเดือนละ"; open with "ใครติดแบล็คลิสต์..." (the voice drops a leading "ติด"); numbers as Thai words; mileage and tricky trim names stay on screen only; new hook line every clip.
- Credits are limited: run the copy pass (cut filler like "บอกเลยว่า", "สุดยอด", "คุ้มเกินราคา"; one concrete fact per line) BEFORE synthesizing, and verify meaning-critical lines with audio_transcribe.

## 6. Deliver (every time)
1. The three planning images (section 1) first.
2. The final MP4 (1080x1920, voice + beat + SFX) + frame strip check + slop test result in one line. Say "pass" only for checks actually run on the final file in this turn.
3. TikTok caption in a code block: hook line, model/year/gear/color, check-mark facts (each = one listed fact), price, blacklist down payment, location, "ทักแชทส่งเคส", disclaimer, ~10 hashtags.
4. One short line: what changed vs the last clip + the fingerprint.
- If the same car comes again after a clip exists, ask: new version, resend old file, or edit?
- Save notable new variants to the Project (claude/<name>-clip.html and -sound.py).