// Netlify запускает эту функцию после каждой заявки из формы на сайте.
// Если в настройках сайта заданы TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID, заявка приходит в Telegram.
const LABELS = { name: "Имя", contact: "Телефон или Telegram", message: "Задача", site: "Сайт или аккаунт" };
const SKIP = ["form-name", "bot-field", "consent", "ip", "user_agent", "referrer"];

exports.handler = async (event) => {
  const token = process.env.TELEGRAM_BOT_TOKEN;
  const chat = process.env.TELEGRAM_CHAT_ID;
  if (!token || !chat) return { statusCode: 200, body: "Telegram не настроен" };
  const { payload } = JSON.parse(event.body);
  const data = payload.data || {};
  const lines = ["Новая заявка с proxyagency.ru", "Форма: " + (payload.form_name || "")];
  for (const [k, v] of Object.entries(data)) {
    if (SKIP.includes(k) || !v) continue;
    lines.push((LABELS[k] || k) + ": " + v);
  }
  const res = await fetch("https://api.telegram.org/bot" + token + "/sendMessage", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ chat_id: chat, text: lines.join("\n").slice(0, 3500) }),
  });
  return { statusCode: res.ok ? 200 : 502, body: res.ok ? "ok" : "telegram error" };
};
