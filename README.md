# Proxy Agency — статический сайт (29 страниц)

Обычный HTML/CSS без сборщиков. Адреса чистые: `/services/ads/` → `services/ads/index.html`.

## Публикация
Репозиторий подключён к Netlify: каждый коммит в ветку `main` публикуется автоматически. Редиректы со старых адресов `/keys_*` лежат в `_redirects` (для Apache и Nginx есть `.htaccess` и `nginx-redirects.conf`).

## Форма заявок
Все формы работают через Netlify Forms (две формы: `contact` и `audit`), после отправки открывается страница `/thanks/`.
1. Email: в Netlify → Forms → Form notifications → Add notification → Email, адрес info@proxyagency.ru.
2. Telegram (по желанию): создайте бота у @BotFather, в Netlify → Site configuration → Environment variables добавьте `TELEGRAM_BOT_TOKEN` (токен бота) и `TELEGRAM_CHAT_ID` (ваш chat id, его покажет бот @userinfobot). Функция `netlify/functions/submission-created.js` отправит каждую заявку в Telegram. Токен никому не отправляйте и в код не вставляйте.

## Что ещё нужно заполнить
- Legrand: год начала работы.
- Страница `/cases/` и главная: обложки карточек (сейчас градиент с названием клиента).
- Юридические тексты `/privacy/` и `/consent/`: типовой шаблон, нужна проверка юристом.
- Страницы `thanks`, `blog`, `privacy`, `consent`, `404` закрыты от индексации (`noindex`). Для privacy и consent уберите `noindex`, когда юрист проверит текст.

## Правила
- Instagram и Facebook всегда со звёздочкой и сноской «* Запрещённый на территории России сервис.»
- На сайте нет имён сотрудников и банковских реквизитов.
