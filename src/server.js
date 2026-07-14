import crypto from "node:crypto";
import http from "node:http";

const requiredEnv = [
  "LINE_CHANNEL_SECRET",
  "LINE_CHANNEL_ACCESS_TOKEN",
  "OPENAI_API_KEY",
];

const missingEnv = requiredEnv.filter((key) => !process.env[key]);

if (missingEnv.length > 0) {
  throw new Error(`Missing required environment variables: ${missingEnv.join(", ")}`);
}

const port = Number(process.env.PORT || 3000);
const lineChannelSecret = process.env.LINE_CHANNEL_SECRET;
const lineChannelAccessToken = process.env.LINE_CHANNEL_ACCESS_TOKEN;
const openaiApiKey = process.env.OPENAI_API_KEY;
const openaiModel = process.env.OPENAI_MODEL || "gpt-5.6-luna";
const botName = process.env.BOT_NAME || "Codex Line Helper";
const botSystemPrompt =
  process.env.BOT_SYSTEM_PROMPT ||
  "คุณคือผู้ช่วยส่วนตัวใน LINE ของผู้ใช้ ตอบเป็นภาษาไทยเป็นหลัก น้ำเสียงอบอุ่น ฉลาด ใช้งานได้จริง กระชับเมื่อเรื่องง่าย และละเอียดเมื่อผู้ใช้ต้องการ";

const server = http.createServer(async (request, response) => {
  try {
    if (request.method === "GET" && request.url === "/") {
      sendJson(response, 200, {
        ok: true,
        service: botName,
        webhook: "/webhook",
      });
      return;
    }

    if (request.method !== "POST" || request.url !== "/webhook") {
      sendJson(response, 404, { error: "Not found" });
      return;
    }

    const rawBody = await readRequestBody(request);

    if (!isValidLineSignature(request, rawBody)) {
      sendJson(response, 401, { error: "Invalid LINE signature" });
      return;
    }

    const body = JSON.parse(rawBody.toString("utf8"));
    const events = Array.isArray(body?.events) ? body.events : [];

    sendJson(response, 200, { ok: true });

    await Promise.allSettled(events.map(handleLineEvent));
  } catch (error) {
    console.error("Webhook request failed:", error);

    if (!response.headersSent) {
      sendJson(response, 500, { error: "Internal server error" });
    }
  }
});

async function handleLineEvent(event) {
  if (event.type === "follow" && event.replyToken) {
    await replyToLine(event.replyToken, "สวัสดีครับ ผมพร้อมช่วยแล้ว พิมพ์สิ่งที่อยากให้ช่วยมาได้เลยครับ");
    return;
  }

  if (event.type !== "message" || event.message?.type !== "text" || !event.replyToken) {
    return;
  }

  const userText = event.message.text?.trim();

  if (!userText) {
    return;
  }

  try {
    const answer = await generateAnswer(userText);
    await replyToLine(event.replyToken, answer);
  } catch (error) {
    console.error("Failed to handle LINE event:", error);
    await replyToLine(
      event.replyToken,
      "ขอโทษครับ ตอนนี้ผมตอบไม่ได้ชั่วคราว ลองส่งมาอีกครั้งในอีกสักครู่นะครับ",
    );
  }
}

async function generateAnswer(userText) {
  const response = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${openaiApiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: openaiModel,
      instructions: botSystemPrompt,
      input: userText,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(`OpenAI request failed: ${response.status} ${JSON.stringify(data)}`);
  }

  const text = extractOpenAIText(data).trim();

  if (!text) {
    return "ผมยังคิดคำตอบที่ดีไม่ได้ครับ ลองอธิบายเพิ่มอีกนิดได้ไหม";
  }

  return fitLineTextLimit(text);
}

async function replyToLine(replyToken, text) {
  const lineResponse = await fetch("https://api.line.me/v2/bot/message/reply", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${lineChannelAccessToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      replyToken,
      messages: [
        {
          type: "text",
          text,
        },
      ],
    }),
  });

  if (!lineResponse.ok) {
    const body = await lineResponse.text();
    throw new Error(`LINE reply failed: ${lineResponse.status} ${body}`);
  }
}

function isValidLineSignature(request, rawBody) {
  const signature = request.headers["x-line-signature"];

  if (!signature || !rawBody) {
    return false;
  }

  const expectedSignature = crypto
    .createHmac("sha256", lineChannelSecret)
    .update(rawBody)
    .digest("base64");

  const actual = Buffer.from(signature);
  const expected = Buffer.from(expectedSignature);

  return actual.length === expected.length && crypto.timingSafeEqual(actual, expected);
}

function extractOpenAIText(data) {
  if (typeof data.output_text === "string") {
    return data.output_text;
  }

  const chunks = [];

  for (const item of data.output || []) {
    for (const content of item.content || []) {
      if (typeof content.text === "string") {
        chunks.push(content.text);
      }
    }
  }

  return chunks.join("\n").trim();
}

function fitLineTextLimit(text) {
  const maxLength = 4900;

  if (text.length <= maxLength) {
    return text;
  }

  return `${text.slice(0, maxLength - 24)}\n\n(ข้อความยาวเกินไป ผมตัดให้สั้นลงครับ)`;
}

function readRequestBody(request) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    let size = 0;
    const maxSize = 1024 * 1024;

    request.on("data", (chunk) => {
      size += chunk.length;

      if (size > maxSize) {
        reject(new Error("Request body is too large"));
        request.destroy();
        return;
      }

      chunks.push(chunk);
    });

    request.on("end", () => resolve(Buffer.concat(chunks)));
    request.on("error", reject);
  });
}

function sendJson(response, statusCode, body) {
  response.writeHead(statusCode, {
    "Content-Type": "application/json; charset=utf-8",
  });
  response.end(JSON.stringify(body));
}

server.listen(port, () => {
  console.log(`${botName} is running on port ${port}`);
});
