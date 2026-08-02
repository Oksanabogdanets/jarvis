/**
 * channel.js — публікація постів у Telegram-канал через окремого постинг-бота.
 *
 * Агент (Claude) у своїй відповіді ставить тег:
 *   [КАНАЛ]текст поста (Telegram-HTML)[/КАНАЛ]
 *   [КАНАЛ ФОТО=/шлях/фото.jpg]підпис[/КАНАЛ]
 *   [КАНАЛ ТИХО]без сповіщення[/КАНАЛ]
 * bot/index.js перехоплює ці теги через parseChannelTags() і публікує postToChannel().
 *
 * Конфіг каналу (token постинг-бота + channelId) — у ~/.agent/channel.json
 * (fallback: змінні оточення CHANNEL_BOT_TOKEN / CHANNEL_ID / CHANNEL_USERNAME).
 * Токен постинг-бота — секрет, у git не потрапляє.
 */

import { readFileSync, writeFileSync, existsSync, unlinkSync } from "node:fs";
import { basename } from "node:path";

// ─── Конфіг ─────────────────────────────────────────────────────────────────

export function loadChannel(channelFile) {
  if (channelFile && existsSync(channelFile)) {
    try {
      const c = JSON.parse(readFileSync(channelFile, "utf8"));
      if (c.token && c.channelId) return normalizeCfg(c);
    } catch {}
  }
  const token = process.env.CHANNEL_BOT_TOKEN;
  const id = process.env.CHANNEL_ID;
  if (token && id) {
    return normalizeCfg({
      token,
      channelId: id,
      channelUsername: process.env.CHANNEL_USERNAME || null,
      channelTitle: process.env.CHANNEL_TITLE || null,
    });
  }
  return null;
}

function normalizeCfg(c) {
  const id = typeof c.channelId === "string" && /^-?\d+$/.test(c.channelId.trim())
    ? Number(c.channelId.trim())
    : c.channelId;
  let username = c.channelUsername || null;
  if (username) username = String(username).replace(/^@/, "").trim() || null;
  return { ...c, channelId: id, channelUsername: username };
}

export function saveChannel(channelFile, cfg) {
  writeFileSync(channelFile, JSON.stringify(cfg, null, 2));
}

export function clearChannel(channelFile) {
  if (existsSync(channelFile)) unlinkSync(channelFile);
}

// ─── Парсинг тегів ──────────────────────────────────────────────────────────

// Увага: \b не працює з кирилицею — атрибути відділяємо явним пробілом/табом.
const CHANNEL_TAG_RE = /\[КАНАЛ(?:[ \t]([^\]]*))?\]([\s\S]*?)\[\/КАНАЛ\]/gi;

/**
 * Витягує теги [КАНАЛ]...[/КАНАЛ] з тексту.
 * @returns {{cleaned: string, posts: Array<{body:string, photo:string|null, silent:boolean}>}}
 */
export function parseChannelTags(text) {
  const posts = [];
  const cleaned = text.replace(CHANNEL_TAG_RE, (_, attrs, body) => {
    const photoMatch = /(?:ФОТО|PHOTO)\s*=\s*(?:"([^"]+)"|(\S+))/i.exec(attrs || "");
    const photo = photoMatch ? (photoMatch[1] || photoMatch[2]) : null;
    const silent = /(?:^|\s)(?:ТИХО|SILENT)(?:\s|$)/i.test(attrs || "");
    posts.push({ body: (body || "").trim(), photo, silent });
    return "";
  });
  return { cleaned: cleaned.trim(), posts };
}

// ─── Telegram API ─────────────────────────────────────────────────────────────

const api = (token, method) => `https://api.telegram.org/bot${token}/${method}`;
const isUrl = (s) => /^https?:\/\//i.test(s || "");

/**
 * Посилання на опублікований пост.
 */
export function postLink(cfg, messageId) {
  if (cfg.channelUsername) return `https://t.me/${cfg.channelUsername}/${messageId}`;
  const idStr = String(cfg.channelId);
  if (idStr.startsWith("-100")) return `https://t.me/c/${idStr.slice(4)}/${messageId}`;
  return null;
}

async function tgCall(token, method, payload) {
  const r = await fetch(api(token, method), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return r.json();
}

/**
 * Публікує один пост у канал.
 * @returns {{ok:boolean, messageId?:number, link?:string|null, error?:string}}
 */
export async function postToChannel(cfg, post) {
  try {
    const { body = "", photo = null, silent = false } = post;
    let res;

    if (photo) {
      const caption = body ? body.slice(0, 1024) : undefined;
      if (isUrl(photo)) {
        res = await tgCall(cfg.token, "sendPhoto", {
          chat_id: cfg.channelId,
          photo,
          ...(caption ? { caption, parse_mode: "HTML" } : {}),
          disable_notification: silent,
        });
      } else {
        if (!existsSync(photo)) return { ok: false, error: `фото не знайдено: ${photo}` };
        const buf = readFileSync(photo);
        const form = new FormData();
        form.append("chat_id", String(cfg.channelId));
        form.append("photo", new Blob([buf]), basename(photo));
        if (caption) { form.append("caption", caption); form.append("parse_mode", "HTML"); }
        if (silent) form.append("disable_notification", "true");
        const r = await fetch(api(cfg.token, "sendPhoto"), { method: "POST", body: form });
        res = await r.json();
      }
    } else {
      if (!body) return { ok: false, error: "порожній текст поста" };
      res = await tgCall(cfg.token, "sendMessage", {
        chat_id: cfg.channelId,
        text: body,
        parse_mode: "HTML",
        disable_notification: silent,
      });
      // Якщо HTML не парситься — повторюємо без розмітки
      if (!res.ok && /parse entities/i.test(res.description || "")) {
        res = await tgCall(cfg.token, "sendMessage", {
          chat_id: cfg.channelId, text: body, disable_notification: silent,
        });
      }
    }

    if (!res.ok) return { ok: false, error: `${res.error_code}: ${res.description}` };
    const messageId = res.result.message_id;
    return { ok: true, messageId, link: postLink(cfg, messageId) };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}

/**
 * Перевіряє конфіг: чи робочий токен і чи є постинг-бот адміном каналу з правом публікації.
 */
export async function verifyChannel(cfg) {
  try {
    const me = await (await fetch(api(cfg.token, "getMe"))).json();
    if (!me.ok) return { ok: false, error: `токен не робочий: ${me.description}` };
    const botId = me.result.id;
    const mem = await (await fetch(api(cfg.token, `getChatMember?chat_id=${cfg.channelId}&user_id=${botId}`))).json();
    if (!mem.ok) return { ok: false, botUsername: me.result.username, error: `немає доступу до каналу: ${mem.description}` };
    const r = mem.result;
    const canPost = r.status === "creator" || (r.status === "administrator" && r.can_post_messages !== false);
    return {
      ok: canPost,
      botUsername: me.result.username,
      status: r.status,
      canPost,
      error: canPost ? undefined : "бот не адмін каналу або без права «Публікація повідомлень»",
    };
  } catch (e) {
    return { ok: false, error: e.message };
  }
}
