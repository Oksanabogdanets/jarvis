# Instagram DM через Meta API — план підключення

> Мета: Агент на сервері сам читає директ (переписки з лідами) і готує чернетки відповідей. Без паролів і ризику бану — через офіційний API Meta.
> Статус: план створено 2026-09-04. Виконання не почато.

## Що отримаємо в результаті

1. Агент бачить усі діалоги директа: хто написав, що написав, хто мовчить
2. Команда в Telegram типу «покажи нові заявки» → список лідів зі статусами
3. Агент готує чернетку відповіді в стилі продажника → Оксана копіює/редагує і відправляє
4. (Пізніше) Webhook: нова заявка в директ → Агент одразу пише Оксані в Telegram

## Передумови (перевірити перед стартом)

- [ ] Instagram `ksysha.bogdanets` — професійний акаунт (Business або Creator). Перевірка: Налаштування → Тип акаунта
- [ ] Є акаунт на developers.facebook.com (є — там уже живе застосунок для реклами)
- [ ] Доступ до сервера з Агентом (VPS), щоб покласти токен в `.env`

## Етапи

### Етап 1 — кабінет Meta (разом з Оксаною, ~30–40 хв)

1. developers.facebook.com → My Apps → відкрити наявний застосунок (або створити новий, тип Business)
2. Add Product → **Instagram** → обрати **Instagram API with Instagram Login** (новий шлях: Facebook-сторінка не обов'язкова)
3. У розділі API setup with Instagram login: додати акаунт `ksysha.bogdanets` як Instagram Tester і підтвердити запрошення в Instagram (Налаштування → Website permissions → Apps and websites → Tester invites)
4. Згенерувати **User Access Token** з дозволами: `instagram_business_basic`, `instagram_business_manage_messages`
5. Обміняти на **long-lived token** (живе 60 днів, оновлюється автоматично) — це зробить скрипт
6. Токен записати ТІЛЬКИ в `.env` на сервері (`IG_ACCESS_TOKEN=...`), не в чат і не в git

Примітка: поки застосунок у Dev mode, API працює лише з акаунтами, доданими в застосунок (нам цього досить — акаунт один). App Review не потрібен.

### Етап 2 — скрипт на сервері (Агент, ~1–2 год)

1. `~/projects/ig-dm/` — Node.js скрипт:
   - `GET /me/conversations?platform=instagram` — список діалогів
   - `GET /{conversation-id}?fields=messages{created_time,from,message}` — повідомлення діалогу
   - автооновлення long-lived токена (раз на ~50 днів)
2. Команди для Агента: «покажи директ», «покажи діалог з X», «хто не відповів за 24 год»
3. Тест: звірити вивід зі скріншотами реального директа

### Етап 3 — опційно, після обкатки

- Webhook на нові повідомлення (потрібен HTTPS-ендпоінт на VPS + Verify Token)
- Авточернетки: нове повідомлення від ліда → Агент формує відповідь за скриптами продажів → шле Оксані в Telegram на затвердження
- Відправка відповідей через API (в межах 24-годинного вікна після повідомлення клієнта)

## Обмеження, про які треба знати

- Відповідати через API можна протягом 24 год після останнього повідомлення клієнта (далі — тільки вручну)
- Історія: API віддає діалоги і повідомлення, але дуже старі переписки можуть підтягуватись не повністю
- Токен — секрет рівня пароля: тільки `.env` на сервері

## Джерела

- [Meta: Instagram Messaging API (Instagram Login)](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/messaging-api/)
- [Гайд по webhooks для Instagram Messaging](https://innocentanyaele.medium.com/setup-meta-webhooks-for-instagram-messaging-and-respond-to-message-4575bc95c7a2)
