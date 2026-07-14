# LINE OpenAI Bot

บอท LINE สำเร็จรูปที่รับข้อความจาก LINE Messaging API แล้วให้ OpenAI ช่วยตอบกลับเป็นภาษาไทย

## สิ่งที่ต้องมี

- LINE Official Account
- Messaging API channel ของ LINE
- Channel secret
- Channel access token
- OpenAI API key
- Node.js 20.6 ขึ้นไป

## วิธีเปิดใช้ในเครื่อง

1. ตรวจว่ามี Node.js

```bash
node --version
```

โปรเจกต์นี้ไม่ต้องใช้แพ็กเกจภายนอก แต่ยังใช้ `npm` เพื่อรันคำสั่งให้สะดวก

2. สร้างไฟล์ `.env`

```bash
cp .env.example .env
```

บน Windows PowerShell ใช้:

```powershell
Copy-Item .env.example .env
```

3. ใส่ค่าจริงใน `.env`

```env
LINE_CHANNEL_SECRET=...
LINE_CHANNEL_ACCESS_TOKEN=...
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5.6-luna
```

4. เริ่มบอทแบบโหลด `.env`

```bash
npm run start:local
```

หรือถ้าตั้ง environment variables ไว้ในระบบ/โฮสต์แล้ว:

```bash
npm start
```

## ตั้งค่า LINE Webhook

ใน LINE Developers Console:

1. เข้า Provider และ Messaging API channel
2. ไปที่แท็บ Messaging API
3. ตั้ง Webhook URL เป็น:

```text
https://YOUR-DOMAIN.com/webhook
```

4. กด Verify
5. เปิด Use webhook
6. แนะนำให้ปิด Auto-reply messages ใน LINE Official Account Manager เพื่อไม่ให้ตอบซ้อนกับบอท

LINE ต้องการ webhook ที่เป็น HTTPS และมี certificate ที่เชื่อถือได้ ถ้าทดสอบในเครื่องให้ใช้ tunnel เช่น Cloudflare Tunnel หรือ ngrok แล้วนำ URL ที่ได้ไปใส่ใน LINE

## Deploy บน Render แบบเร็ว

1. อัปโหลดโฟลเดอร์นี้ไป GitHub
2. สร้าง Web Service บน Render
3. ตั้งค่า:

```text
Build Command: npm install
Start Command: npm start
```

4. เพิ่ม Environment Variables:

```text
LINE_CHANNEL_SECRET
LINE_CHANNEL_ACCESS_TOKEN
OPENAI_API_KEY
OPENAI_MODEL
BOT_NAME
BOT_SYSTEM_PROMPT
```

5. นำ URL ของ Render ไปตั้งเป็น Webhook URL โดยเติม `/webhook`

## ปรับบุคลิกบอท

แก้ค่า `BOT_SYSTEM_PROMPT` ใน `.env` ได้เลย เช่น:

```env
BOT_SYSTEM_PROMPT=คุณคือผู้ช่วยฝ่ายขายรถยนต์ ตอบภาษาไทย สุภาพ กระชับ ช่วยเขียนแคปชัน ปิดการขาย และตอบลูกค้าใน LINE
```

## จุดที่ทำไว้แล้ว

- รับ webhook จาก LINE ที่ `/webhook`
- ตรวจ `x-line-signature` ก่อนประมวลผล
- ตอบข้อความตอนผู้ใช้เพิ่มเพื่อน
- รับเฉพาะข้อความ text
- เรียก OpenAI Responses API
- ตัดข้อความให้ไม่ยาวเกินขีดจำกัดของ LINE
- แยกคีย์ลับไว้ใน `.env`

## หมายเหตุเรื่องความปลอดภัย

อย่าอัปโหลดไฟล์ `.env` ขึ้น GitHub และอย่าส่ง API key ให้ใครโดยตรง ถ้าคีย์หลุดให้ revoke แล้วสร้างใหม่ทันที
