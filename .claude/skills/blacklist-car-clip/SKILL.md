---
name: "blacklist-car-clip"
description: "Make a TikTok car-sale clip for the page ติดแบล็คลิสต์ มานี่มา from car photos + listing text: proven HYPE style with fresh variations each clip, ElevenLabs voiceover, beat + SFX, MP4 + caption."
---

# Blacklist car clip (ติดแบล็คลิสต์ มานี่มา)

Use when the user sends photos of a used car plus its listing text (model, year, price, down payment, monthly installment x 72, mileage, owners, keys) and wants a TikTok clip. Reply in Thai, casual. Deliver: one vertical MP4 (1080x1920, 30fps, ~18-22s) with voiceover + beat + SFX, then a ready-to-paste TikTok caption. Renders take ~10 min: run the final render in the background, then SendUserFile + PushNotification when done.

**Priority order when rules conflict:** the user's explicit request > the proven HYPE style and the rules in sections 0-1 > the design rules in sections 3b and 6b > general design habits. HYPE is meant to be loud; the design rules make it loud on purpose, not cluttered.

## 0. Style direction (user decision, Oct 2026)
- **HYPE is the main style - it is proven to sell** (user tested the Civic 2018 hype clip). Build every car clip on the HYPE structure and energy, but **vary it every clip so no two look the same**.
- HYPE structure (keep): 9:16 ~20s; hook = fast photo strobe -> big slam text with screen shake -> "<MODEL> ได้!" slam + shockwave; 5 photo scenes each with one selling point (keyword box slam, light sweep, speed streaks, corner brackets, fast wipe cuts); price card = down payment slam, then number reveal landing exactly on the spoken number with a big SFX hit; CTA = LOGO slam + glint + pulsing "ทักแชทส่งเคส" button; driving beat with impacts/whooshes/riser, music ducked under voice.
- Vary per clip (change at least 3-4): accent color / palette (keep brand red, add a new accent: gold, cyan, orange, lime...); hook device (slash split, shatter, stamp, zoom-punch, flip, countdown); photo reveal (strip-slice, iris, shutter, split-panel, push, 3D flip); transition type (diagonal wipe, whip-pan blur, glitch cut, zoom blur, shape mask); number reveal (slot reels, odometer, gauge needle, scramble-decode, flip-board); background texture (speed streaks, grid, rays, particles, asphalt); beat genre/BPM (EDM 120, phonk 100, trap 140, funk 110, amapiano 112, rock 140); hook script line. Note in the reply what changed vs. the last clip.
- Variants already used (Project claude/hype-*-variant-clip.html / -sound.py): red/slot reels/EDM120 (template), gold/slash/slot/trap140 (CR-V), cyan/zoom-punch + stamp/iris/glitch cut/flip-board/phonk105 (Civic FB), lime/shatter/odometer/trap140, blue/card-flip/scramble/amapiano112 (Mazda2), orange/3-2-1 countdown + caution tape/shutter slats/zoom-blur cut/speedometer gauge/funk110 (Yaris), violet/neon-sign flicker/neon-frame panel/whip-pan blur/7-segment LED/neon grid floor (Sienta, Oct 24), mint/tape slap + torn/polaroid drop-in/spin-zoom cut/digit stamp/halftone (Attrage, Oct 25). Full table: blacklist-project-taste section 2. Pick combinations not used recently.
- **Fingerprint line:** before building, write the new clip's fingerprint in one line: `accent / hook device / photo reveal / transition / number reveal / texture / beat`. Compare it with the variants above; at least 3 of the 7 slots must differ from each of the last 3 clips. Put the fingerprint in the reply so the user can add it to the list above.
- Alternative themed concepts already built (use occasionally for testing, or for brand clips; borrow their tricks inside HYPE): CREDIT SCAN/GLITCH HUD (Mazda2), IGNITION/GEAR SHIFT gauges (Ranger), BOARDING PASS/airport (CR-V), BREAKING NEWS TV (CR-V), KEY UNLOCK brand clip (เงินดาวน์ = กุญแจ). Unused ideas: game level-up, comic panels, receipt printer, gacha capsule, GPS map route, polaroid scrapbook, neon night city.
- **Idea bank (from the ui-ux-pro-max skill):** `python3 $HOME/.cache/ui-ux-pro-max/.claude/skills/ui-ux-pro-max/scripts/search.py "<mood words>" --domain style -n 5` (if `$HOME/.cache/ui-ux-pro-max` is missing, run the Setup block of the ui-ux-pro-max skill first) lists visual languages with their colours and effects (e.g. Bauhaus, Memphis, Y2K, Neubrutalism, Retro film, HUD / Sci-Fi, Kinetic typography, Editorial magazine, Pixel art, Chromatic aberration). The data is written for web/app screens, so borrow ONE device per clip (a shape language, a texture, a reveal, a colour block), never a page layout. Skip results that fail the slop test (aurora/mesh gradients, gradient text, glassmorphism over photos, neon unrelated to the brand).
- If the same car is sent again after a clip was already made, ask whether they want a new version, the old file resent, or edits.

## 1. Rules
- **Logo is required in every clip.** The official shield logo is stored in the Project as claude/logo-maneema-720.png.b64.txt (base64 PNG, transparent bg) -> `base64 -d > logo_full.png`. If the user sends a new logo with a white background, remove the bg by flood-fill from the corners. Use it as a small badge top-right (~190px wide, hidden during the opening strobe) and as the big CTA slam (~560px) with a masked glint. Never replace it with a typed wordmark.
- Colors: red #E3202A, black, plus one accent.
- **Copy tone (user decision):** never call buyers "สายแบล็คลิสต์" - nobody chooses to be blacklisted. The message is "ใครติดแบล็คลิสต์ก็ออกรถได้": they didn't want it, but now that they're blacklisted, we can help. Verified voice line: "ใครติดแบล็คลิสต์ เราช่วยได้... ดาวน์แค่"; on screen: "ติดแบล็คลิสต์ เราช่วยได้!".
- Facts: only what the listing says (e.g. don't claim leather seats unless listed). Show "*ผลอนุมัติขึ้นอยู่กับการพิจารณาของไฟแนนซ์" on the price card. Never say "ผ่านแน่นอน"/"ขอแค่มีเงินดาวน์ก็ออกได้"; use "มีโอกาสออกรถ" / "ส่งเคสมาให้เช็กก่อน".
- If the listing's monthly payment is for "เครดิตดี" only (blacklist gets only a down payment), make the blacklist down payment + price the hero and show the good-credit installment small and clearly labelled.
- Do NOT include the "เจ้าบ้าน" (homeowner buyer/guarantor) condition in clips or captions - the user removes it from ads.
- Keep important content between y≈280 and y≈1500 (TikTok UI covers the rest).

## 2. Voiceover (ElevenLabs via Speko MCP)
- mcp__Speko__audio_synthesize body {text, intent:{language:'th',optimizeFor:'accuracy'}, model:'eleven_v3', voice:'tAV9ucNkXgK2k9TLxWkM', constraints:{allowedProviders:{tts:['elevenlabs']}}}. One call per line, in parallel. Emotion tag first: [excited] [cheerfully] [playfully] [impressed] [warmly] [curious].
- Output is saved to a tool-results file: `jq -r .audio_base64 FILE | base64 -d > rN.wav`; trim with ffmpeg silenceremove; measure; find pauses with silencedetect.
- Script rules: NO ending particles (คะ/ค่ะ/นะ/น้า). Say "ผ่อนต่อเดือน" (never "ผ่อนเดือนละ"). Never start a line with "ติด..." - use "ใครติดแบล็คลิสต์...". Numbers as Thai words. Keep tricky trim names on screen only ("ไฮพลัส" -> heard as "ไฮบริด"). New hook line each clip. Lines already verified for the same car can be reused.
- Known pitfalls with this voice: "ไมล์" is heard as "ไม่" (keep mileage on screen only); "ถึงจะ..." is heard as "ฉันจะ..." (avoid).
- Verify hook/model/number and any meaning-critical lines with mcp__Speko__audio_transcribe (signed url from jq -r .url, 15 min, language 'th'); check meaning not spelling; regenerate or rephrase wrong lines. Don't use eleven_multilingual_v2 with this voice.

### 2b. Copy pass (Thai, adapted from the humanizer skill) - run on the script BEFORE synthesizing
Voice credits are limited, so fix the words first. Each line must say one concrete thing a buyer cares about.
- Cut contrasts with a claim nobody made ("ไม่ใช่แค่...แต่..."), staged run-ups ("บอกเลยว่า", "ต้องบอกว่า", "เอาจริงๆ"), and empty hype words with no fact behind them (สุดยอด, ที่สุด, ครบจบ, ตอบโจทย์ทุกไลฟ์สไตล์, คุ้มเกินราคา). Replace with the listing's number or detail.
- No three-adjective strings by habit ("สวย หรู คุ้ม"); one real detail beats three adjectives.
- HYPE energy comes from rhythm, short lines and the beat, not from superlatives.

## 3. Visuals - one self-contained HTML
- Fonts via npm (GitHub blocked): `npm pack @fontsource/kanit` (+ bebas-neue, jetbrains-mono etc.) into fonts/.
- Photos: 3:2 crops at 1300x867 for panels; 9:16 full-bleed only for quick strobes or blurred backdrops (upscaled - never hold sharp).
- `window.render(t)` pure function of time + `window.DURATION`; scenes [id,start,end]; sin-hash randomness. Time every hit to the voice (adelay offsets + silencedetect pauses); keep a LAND constant for the price reveal and derive visual + sound hits from it. Switch scenes/images with display:none, not visibility.
- References in the Project: claude/hype-template-clip.html + claude/hype-template-sound.py (main style), claude/hype-*-variant-clip.html / -sound.py, other concepts claude/*-concept-clip.html / *-concept-sound.py, claude/render.py.

### 3b. Design rules inside HYPE (adapted from the Hallmark and Impeccable skills)
- **One focal moment:** the price reveal (LAND) is the clip's biggest beat: biggest scale, biggest SFX hit, longest hold (>=1.2s after the number lands). The hook slam is second. Scene effects (light sweep, streaks, brackets) stay smaller than both. If two things shout at once, cut one.
- **Tokens:** define red, black, the accent, fonts, easings and durations once as CSS variables at the top; use only those below. No one-off colours or fonts mid-file.
- **Fonts:** max 2 families (a Thai face + one Latin/number display face). Hierarchy by size steps of at least 1.5x, not by piling on stroke + glow + shadow on the same word.
- **Accent discipline:** the accent marks the keyword and the number; red marks the brand, the price box and the CTA. Neither colour is used as background decoration.
- **Numbers:** tabular figures (`font-variant-numeric: tabular-nums`) for slot/odometer/scramble reveals so digits don't jiggle; thousands separators; lock the number's width to its final value.
- **Easing:** entrances expoOut, exits expoIn at ~75% of the entrance time, slams may overshoot once. Never browser-default `ease`.
- **No AI-ad clichés:** no purple-to-cyan or orange-to-pink gradients, no gradient text, no emoji as icons inside the video (draw SVG icons), no lens-flare filler, max 1 white flash.
- **Icons:** Phosphor SVGs via npm (about 1,500 icons): `npm pack @phosphor-icons/core && tar xzf phosphor-icons-core-*.tgz`, then inline files such as `package/assets/bold/car-bold.svg`, `wallet-bold.svg`, `key-bold.svg`, `warning-bold.svg`, `check-circle-bold.svg`, `chat-circle-dots-bold.svg` (weights: regular, bold, fill, duotone...). One weight per clip, recoloured with the clip's colour tokens. Use these instead of emoji or one-off hand-drawn icons.

## 4. Render
- claude/render.py stills mode first -> contact sheet -> LOOK (overflow, Thai marks, safe zone, readability, numbers legible over graphics, nothing leaking between scenes). Also view the contact sheet shrunk to ~180px wide: the hook text, the model name and the down payment must still read. Then video mode as a background job (~10 min).

### When a render or tool step fails (adapted from the superpowers systematic-debugging skill)
- Read the whole error and find the first real failure, not just the last line.
- Reproduce it small before touching the full job: render only the failing frame (`render(t)` at that time, stills mode) or run ffmpeg on a 2-second piece.
- Change one thing at a time and re-check the small case; start the full render again only when the small case passes.
- Never re-generate voice lines to debug timing or the mix (credits are limited); work from the audio files already made.
- After two fixes that don't work, stop and tell the user in one line what is failing and what you tried.

## 5. Sound
- numpy synth -> music.wav + sfx.wav. In lp() filters broadcast the coefficient (`A=np.broadcast_to(np.asarray(a,float),x.shape)`) so time-varying cutoffs work. Music drops right before the price reveal and returns on it.
- Voice: amix of delayed lines, highpass 90, compressor, loudnorm I=-15. Mix: music ~0.32 sidechained by voice, sfx ~0.5, alimiter, loudnorm I=-14 TP=-1. Mux with -c:v copy, aac 192k, -shortest, +faststart.

## 6. QA + deliver
- Frame strip from the final MP4, confirm duration. SendUserFile (display render) + PushNotification.
- **Evidence before "done" (adapted from superpowers verification-before-completion):** call a clip finished, fixed or "Slop test: pass" only after running the checks in this turn on the FINAL file: the ffprobe line (resolution, fps, duration), the frame strip you actually looked at, and the transcribe result for meaning-critical voice lines. If a check could not run, name it instead of claiming pass.
- Reply in Thai: what's in the clip, the fingerprint line and what changed vs last clip, what was verified, anything to listen to.
- TikTok caption in a code block: hook line, model/year/gear/color, ✅ points, 💰 price (ซื้อสดไม่มี VAT), 💳 ติดแบล็คลิสต์ ดาวน์ X (ผ่อน Y x 72 งวด if it applies), 📍 ดูรถที่ บ้านรถสวย รัชดา-พระราม 9, 💬 ทักแชทส่งเคส, disclaimer, ~10 hashtags. Same copy tone rule: no "สายแบล็คลิสต์". The emoji line format is the user's approved caption format; keep it, but run the hook line and ✅ points through the copy pass in 2b (each ✅ = one listed fact, no empty hype).
- Save notable new variations/concepts to the Project (claude/<name>-clip.html / -sound.py).

### 6b. Slop test before sending (fail any = fix first)
1. Down payment / offer not readable with the sound off by the end of the hook.
2. The price reveal is not clearly the biggest moment, or another effect competes with it.
3. Fingerprint shares 5+ slots with any of the last 3 clips.
4. More than 2 fonts, or stroke + glow + shadow stacked on one word.
5. An AI-ad cliché from 3b (gradient text, purple-cyan, emoji icons, flare filler, 2+ white flashes).
6. Any claim not in the listing, any "ผ่านแน่นอน"-type promise, missing finance disclaimer, "สายแบล็คลิสต์" or "เจ้าบ้าน" anywhere.
7. Text or logo outside y≈280-1500, or clipped Thai marks.
Report "Slop test: pass" or what was fixed, in one line of the reply.