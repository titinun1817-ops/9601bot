# Video tools: HyperFrames + Remotion

โฟลเดอร์นี้แยกจากบอท LINE ไม่กระทบการ deploy (Render/Docker ไม่ติดตั้งของในนี้)

ต้องมี Node.js 22.13 ขึ้นไป (หรือ 20.19+) และ Chrome/Chromium กับ ffmpeg ในเครื่อง

## HyperFrames — เขียน HTML + GSAP แล้วเรนเดอร์เป็น MP4

```bash
cd video/hyperframes
npm install
npm run dev      # เปิด studio พรีวิวในเบราว์เซอร์
npm run check    # ตรวจ composition
npm run render   # เรนเดอร์ MP4 ลง renders/
```

- แก้วิดีโอที่ `index.html` (ตั้งไว้แนวตั้ง 1080x1920 สำหรับ TikTok/Reels)
- GSAP ถูกเก็บไว้ที่ `vendor/gsap.min.js` จึงเรนเดอร์ได้แม้ไม่มีอินเทอร์เน็ต
- เอกสาร: https://hyperframes.heygen.com

## Remotion — เขียนวิดีโอด้วย React

```bash
cd video/remotion
npm install
npm run dev                                  # เปิด Remotion Studio
npx remotion render HelloWorld out/video.mp4 # เรนเดอร์ MP4 ลง out/
```

- composition อยู่ที่ `src/Root.tsx` ตัวอย่างอยู่ใน `src/HelloWorld/`
- ใช้ฟรีสำหรับบุคคลและทีมไม่เกิน 3 คน ถ้าเป็นบริษัทที่ใหญ่กว่านั้นต้องซื้อ license: https://www.remotion.pro/license
- เอกสาร: https://www.remotion.dev/docs
