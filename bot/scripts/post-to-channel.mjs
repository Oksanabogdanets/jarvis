#!/usr/bin/env node
/**
 * post-to-channel.mjs — публікація поста в Telegram-канал через постинг-бота.
 *
 * Конфіг (токен + ID каналу) береться з bot/.channel.json (він у .gitignore).
 *
 * Використання:
 *   node scripts/post-to-channel.mjs --text "Текст поста <b>жирним</b>"
 *   node scripts/post-to-channel.mjs --file /шлях/пост.html
 *   node scripts/post-to-channel.mjs --photo /шлях/фото.jpg --caption "Підпис"
 *   node scripts/post-to-channel.mjs --file пост.html --dry      # показати, НЕ відправляти
 *
 * Прапорці:
 *   --text "..."     текст поста (Telegram-HTML: <b> <i> <a href> <code> <pre>)
 *   --file PATH      взяти текст/підпис з файлу
 *   --photo PATH|URL фото до поста (локальний файл або посилання)
 *   --caption "..."  підпис до фото (альтернатива --file для фото)
 *   --plain          вимкнути HTML-розмітку (parse_mode: без форматування)
 *   --silent         опублікувати без звуку (без сповіщення підписникам)
 *   --dry            нічого не публікувати, лише показати що буде відправлено
 */

import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, basename } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const CONFIG_PATH = join(__dirname, "..", ".channel.json");

// ─── Конфіг ─────────────────────────────────────────────────────────────────
let cfg;
try {
  cfg = JSON.parse(readFileSync(CONFIG_PATH, "utf8"));
} catch {
  console.error(`❌ Не знайдено конфіг каналу: ${CONFIG_PATH}\n   Створи bot/.channel.json з полями token і channelId.`);
  process.exit(1);
}
if (!cfg.token || !cfg.channelId) {
  console.error("❌ У .channel.json відсутній token або channelId.");
  process.exit(1);
}

// ─── Аргументи ──────────────────────────────────────────────────────────────
function parseArgs(argv) {
  const a = { plain: false, silent: false, dry: false };
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    if (k === "--text") a.text = argv[++i];
    else if (k === "--file") a.file = argv[++i];
    else if (k === "--photo") a.photo = argv[++i];
    else if (k === "--caption") a.caption = argv[++i];
    else if (k === "--plain") a.plain = true;
    else if (k === "--silent") a.silent = true;
    else if (k === "--dry") a.dry = true;
    else { console.error(`Невідомий прапорець: ${k}`); process.exit(1); }
  }
  return a;
}
const args = parseArgs(process.argv.slice(2));

// Тіло поста: пріоритет --text, потім --file, потім --caption
let body = args.text;
if (body === undefined && args.file) body = readFileSync(args.file, "utf8");
if (body === undefined && args.caption) body = args.caption;
if (args.photo && body === undefined && args.caption) body = args.caption;

if (!args.photo && (body === undefined || body.trim() === "")) {
  console.error("❌ Нема що публікувати. Додай --text, --file або --photo.");
  process.exit(1);
}

const isUrl = (s) => /^https?:\/\//i.test(s || "");
const api = (method) => `https://api.telegram.org/bot${cfg.token}/${method}`;
const parseMode = args.plain ? undefined : "HTML";

// ─── Прев'ю ─────────────────────────────────────────────────────────────────
console.log(`Канал:  ${cfg.channelTitle || cfg.channelId} (${cfg.channelId})`);
console.log(`Бот:    @${cfg.botUsername || "?"}`);
console.log(`Тип:    ${args.photo ? "фото" + (body ? " + підпис" : "") : "текст"}`);
console.log(`Розмітка: ${parseMode || "без форматування"}${args.silent ? ", без звуку" : ""}`);
if (body) console.log(`\n─── текст ───\n${body}\n─────────────`);
if (args.photo) console.log(`Фото:   ${args.photo}`);

if (args.dry) {
  console.log("\n🟡 --dry: нічого не опубліковано.");
  process.exit(0);
}

// ─── Публікація ─────────────────────────────────────────────────────────────
async function sendText() {
  const r = await fetch(api("sendMessage"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chat_id: cfg.channelId,
      text: body,
      ...(parseMode ? { parse_mode: parseMode } : {}),
      disable_notification: args.silent,
      link_preview_options: { is_disabled: false },
    }),
  });
  return r.json();
}

async function sendPhoto() {
  const caption = body ? (body.length > 1024 ? body.slice(0, 1024) : body) : undefined;
  if (isUrl(args.photo)) {
    const r = await fetch(api("sendPhoto"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_id: cfg.channelId,
        photo: args.photo,
        ...(caption ? { caption } : {}),
        ...(parseMode && caption ? { parse_mode: parseMode } : {}),
        disable_notification: args.silent,
      }),
    });
    return r.json();
  }
  // Локальний файл — завантажуємо як multipart
  const buf = readFileSync(args.photo);
  const form = new FormData();
  form.append("chat_id", String(cfg.channelId));
  form.append("photo", new Blob([buf]), basename(args.photo));
  if (caption) form.append("caption", caption);
  if (parseMode && caption) form.append("parse_mode", parseMode);
  if (args.silent) form.append("disable_notification", "true");
  const r = await fetch(api("sendPhoto"), { method: "POST", body: form });
  return r.json();
}

const res = args.photo ? await sendPhoto() : await sendText();

if (!res.ok) {
  console.error(`\n❌ Помилка Telegram: ${res.error_code} — ${res.description}`);
  process.exit(1);
}

const mid = res.result.message_id;
const link = cfg.channelUsername ? `https://t.me/${cfg.channelUsername}/${mid}` : `(приватний канал, message_id=${mid})`;
console.log(`\n✅ Опубліковано в «${cfg.channelTitle || cfg.channelId}». Посилання: ${link}`);
