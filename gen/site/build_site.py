import re
import sys, os, re, shutil, glob
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
from content_cases import CASES, case_page, MAZAY
from content_services import SERVICES, ORDER, service_page, hub_page
import media as M
from content_misc import about_page, contacts_page, audit_page, blog_page, thanks_page, legal_page, notfound_page

OUTS = {"prod": ROOT + "/site", "preview": ROOT + "/site-preview"}

# ---------- CSS bundles ----------
site_css = css_union(CSS_FILES_SITE, EXTRA) + M.CSS
home_files = sorted(glob.glob(ROOT + "/tilda-blocks/[0-9]*.html"))
home_css = css_union(home_files) + M.CSS
cases_files = sorted(glob.glob(ROOT + "/tilda-cases/c0*.html"))
cases_css = css_union(cases_files) + M.CSS

def from_blocks(files):
    return "\n".join(block_body(f) for f in files)

PAGES = {}   # path -> html

# ---------- existing pages (from earlier blocks) ----------
PAGES[""] = page("", "Proxy Agency — digital-агентство в Санкт-Петербурге: реклама, SEO, сайты, соцсети",
                 "Digital-агентство Proxy Agency в Санкт-Петербурге с 2013 года. Контекстная реклама и таргет, SEO и GEO, карты, SMM, сайты и продакшн. Кейсы с результатами в цифрах.",
                 "home.css", from_blocks(home_files),
                 jsonld({"@context": "https://schema.org", "@type": "Organization", "name": "Proxy Agency", "url": SITE + "/", "foundingDate": "2013", "telephone": "+78129855830", "email": "hello@proxyagency.ru",
                         "address": {"@type": "PostalAddress", "addressLocality": "Санкт-Петербург", "streetAddress": "ул. Марата, д. 86", "addressCountry": "RU"}, "sameAs": ["https://t.me/proxyagency_SPB"]}))
hub = from_blocks(cases_files).replace("Mazай", MAZAY)
PAGES["cases"] = page("cases", "Кейсы digital-агентства: результаты в цифрах — Proxy Agency",
                      "Кейсы Proxy Agency: реклама, SEO, сайты и продвижение ресторанов, отелей, санаториев и производителей. Результаты в цифрах.", "cases.css", hub)
for slug, title, desc in [
    ("opti", "Кейс сети АЗС «ОПТИ»: рост скачиваний приложения в 2 раза — Proxy Agency",
     "Как Proxy Agency вела digital-продвижение сети АЗС «ОПТИ»: федеральные акции в 35 регионах, приложение ×2, Telegram-канал с нуля на 1 600 подписчиков за 4 месяца."),
    ("nevsky-bereg", "Кейс отеля «Невский берег»: рост доходности на 12,3% — Proxy Agency",
     "Как Proxy Agency сохранила трафик и позиции отеля «Невский берег» после редизайна сайта, настроила SEO и контекстную рекламу со сквозной аналитикой: доходность выросла на 12,3%."),
    ("target", "Кейс TARGET energy drink: соцсети с нуля и 26 000+ подписчиков — Proxy Agency",
     "Как Proxy Agency с нуля создала соцсети энергетика TARGET: ВКонтакте 13 000+, Instagram* 10 000+, MAX 1 700+, Telegram 1 400+ подписчиков. Конкурсы, розыгрыши, комьюнити-менеджмент."),
]:
    d = {"opti": "tilda-opti", "nevsky-bereg": "tilda-nevsky", "target": "tilda-target"}[slug]
    files = sorted(glob.glob(f"{ROOT}/{d}/k0*.html"))
    PAGES["cases/" + slug] = page("cases/" + slug, title, desc, "site.css", from_blocks(files))

# ---------- new pages ----------
for slug, c in CASES.items():
    PAGES["cases/" + slug] = case_page(c)
PAGES["services"] = hub_page()
for k in ORDER:
    PAGES["services/" + k] = service_page(SERVICES[k])
PAGES["about"] = about_page()
PAGES["contacts"] = contacts_page()
PAGES["audit"] = audit_page()
PAGES["blog"] = blog_page()
PAGES["thanks"] = thanks_page()
PAGES["privacy"] = legal_page("privacy", "Политика конфиденциальности", "Политика конфиденциальности — Proxy Agency")
PAGES["consent"] = legal_page("consent", "Согласие на обработку персональных данных", "Согласие на обработку персональных данных — Proxy Agency")
PAGES["404"] = notfound_page()

# ---------- output ----------
def out_file(path):
    if path == "": return "index.html"
    if path == "404": return "404.html"
    return path + "/index.html"

def to_preview(html, path):
    depth = 0 if path in ("", "404") else path.count("/") + 1
    pre = "../" * depth
    def rel(m):
        attr, v = m.group(1), m.group(2)
        if v.startswith("//") or not v.startswith("/"): return m.group(0)
        v2 = v[1:]
        frag = ""
        if "#" in v2: v2, frag = v2.split("#", 1); frag = "#" + frag
        last = v2.rstrip("/").split("/")[-1]
        if v2 == "": v2 = "index.html"
        elif "." in last: pass
        else: v2 = v2.rstrip("/") + "/index.html"
        return f'{attr}="{pre}{v2}{frag}"'
    return re.sub(r'(href|src)="(/[^"]*)"', rel, html)

REDIRECTS = [("/uslugi", "/services/"), ("/vsekeysi", "/cases/"), ("/digital", "/services/"), ("/digitalservices", "/services/ads/"), ("/contextual", "/services/ads/"),
             ("/seo", "/services/seo-geo/"), ("/map", "/services/maps/"), ("/telegram", "/services/smm-telegram/"), ("/socialmedia", "/services/smm-telegram/"),
             ("/productionservices", "/services/production/"), ("/developmentservices", "/services/web/"),
             ("/keys_legrand", "/cases/legrand/"), ("/keys_petrovvodkin", "/cases/petrov-vodkin/"), ("/keys_target", "/cases/target/"), ("/keys_la_perla", "/cases/la-perla/"),
             ("/keys_opti", "/cases/opti/"), ("/keys_bochkari", "/cases/bochkari/"), ("/keys_mazay", "/cases/mazay/"), ("/keys_altay_zamok", "/cases/altay-zamok/"),
             ("/keys_centrosouz", "/cases/centrosouz/"), ("/keys_nevsky", "/cases/nevsky-bereg/"), ("/keys_clinic", "/cases/klinika-pirogova/"), ("/keys_alfafeeds", "/cases/alfafeeds/")]

SUBMISSION_JS = """// Netlify запускает эту функцию после каждой заявки из формы на сайте.
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
    body: JSON.stringify({ chat_id: chat, text: lines.join("\\n").slice(0, 3500) }),
  });
  return { statusCode: res.ok ? 200 : 502, body: res.ok ? "ok" : "telegram error" };
};
"""

METRIKA = """<!-- Yandex.Metrika counter -->
<script type="text/javascript">
(function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
m[i].l=1*new Date();
for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
ym(33925959, "init", {clickmap:true, trackLinks:true, accurateTrackBounce:true});
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/33925959" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->
"""
PERIOD = {"cases/opti": "с 2021", "cases/nevsky-bereg": "с 2019", "cases/target": "с 2019"}
FORM_HIDDEN = '<input type="hidden" name="form-name" value="%s"><p hidden><label>Не заполняйте: <input name="bot-field"></label></p>'
def media_inject(path, h):
    used = False
    if path.startswith("cases/") and path.count("/") == 1:
        slug = path.split("/")[1]
        c = CASES.get(slug)
        if not c:
            t = re.search(r"<h1[^>]*>(.*?)</h1>", h, re.S)
            c = {"crumb": re.sub(r"<[^>]+>", "", t.group(1)).strip() if t else slug}
        if c:
            g = M.gallery(slug, c["crumb"])
            if g:
                key = '<section class="pxa pxa-sec" id="pxa-review"' if 'id="pxa-review"' in h else '<section class="pxa pxa-sec" id="pxa-takeaways"'
                h = h.replace(key, g + key, 1); used = True

    if path == "cases":
        def rep(m):
            sl = re.search(r'href="/cases/([a-z0-9-]+)', m.group(0)).group(1)
            cv = M.cover(sl)
            if not cv: return m.group(0)
            return re.sub(r'<div class="pxa-cover"[^>]*>[^<]*</div>', f'<img class="pxa-cover-img" src="{cv}" loading="lazy" alt="" style="{M.COVER_STYLE.get(sl, "")}">', m.group(0), count=1)
        h = re.sub(r'<article class="pxa-case".*?</article>', rep, h, flags=re.S)
    if path == "":
        HOME = {"Петров-Водкин": "petrov-vodkin", "ОПТИ": "opti", "Невский берег": "nevsky-bereg", "Le Grand": "legrand", "La Perla": "la-perla"}
        def hrep(m):
            t = re.search(r"<h3>([^<]*)</h3>", m.group(0))
            sl = HOME.get(t.group(1).strip()) if t else None
            cv = M.cover(sl) if sl else None
            if not cv: return m.group(0)
            return re.sub(r'<div class="pxa-cover"[^>]*>[^<]*</div>', f'<img class="pxa-cover-img" src="{cv}" loading="lazy" alt="" style="{M.COVER_STYLE.get(sl, "")}">', m.group(0), count=1)
        h = re.sub(r'<article class="pxa-case">.*?</article>', hrep, h, flags=re.S)
        lg = M.logos()
        if lg: h = h.replace('<section class="pxa pxa-sec" id="pxa-services"', lg + '<section class="pxa pxa-sec" id="pxa-services"', 1); used = True
    if used or 'pxa-play' in h:
        h = h.replace("</body>", M.JS + "</body>", 1)
    return h

def postprocess(path, h):
    h = re.sub(r'\s*<a href="https://vk\.com/proxy_agency">VK</a>', "", h)
    if path in PERIOD:
        h = h.replace("[добавить срок работы]", PERIOD[path])
    h = re.sub(r'<div class="pxa-gallery">\[Галерея[^<]*</div>\n?', "", h)
    h = re.sub(r'<div class="pxa-res"><span class="pxa-open">\[добавить[^<]*</span></div>', "", h)
    h = re.sub(r'<p class="pxa-kpi-note">[^<]*\[добавить[^<]*</p>\n?', "", h)
    # форма заявок: Netlify Forms
    h = h.replace('<form class="pxa-contact-form" action="REPLACE_FORM_ENDPOINT" method="post">', '<form class="pxa-contact-form" name="contact" action="/thanks/" method="post" data-netlify="true" netlify-honeypot="bot-field">' + FORM_HIDDEN % "contact")
    h = h.replace('<form class="pxa-form" action="REPLACE_FORM_ENDPOINT" method="post">', '<form class="pxa-form" name="audit" action="/thanks/" method="post" data-netlify="true" netlify-honeypot="bot-field">' + FORM_HIDDEN % "audit")
    if path == "":
        h = h.replace('<div class="pxa-big" style="color:#5A5F7D">[ЦИФРА]</div>', '<div class="pxa-big" style="color:var(--pxa-b)">+12,3%</div>')
        h = h.replace("[показатель и срок: например, стоимость брони]", "рост доходности отеля")
        h = h.replace("«[Текст отзыва клиента: какая была задача, что сделали, какой получили результат]»", "«Агентство PROXY создало и провело промо-кампанию безалкогольного пива Weissberg: CPA-рекламу в соцсетях и на видеохостингах. Также они ведут таргетированную рекламу и SMM наших брендов. Работой довольны, рекомендуем.»")
        h = h.replace("«[Текст отзыва клиента или видеоотзыв: вставить ссылку на ролик]»", "«Это уже наш четвёртый совместный проект с агентством PROXY. Продолжаем плодотворно сотрудничать с ними по всем новым проектам La Perla Group.»")
        h = h.replace("[Имя Фамилия], [должность], [компания]", "Татьяна Быковская, Департамент маркетинга и рекламы, пивоваренная компания «Бочкари»", 1)
        h = h.replace("[Имя Фамилия], [должность], [компания]", "Игорь Мельцер, ресторатор, La Perla Restaurant Group", 1)
        h = h.replace("[диапазон — заполнить]", "контекстная реклама от 24 000 ₽ в месяц, SEO от 40 000 ₽ в месяц, SMM и Telegram от 48 000 ₽ в месяц, корпоративный сайт от 120 000 ₽, карты от 36 000 ₽ в год, продакшн от 220 000 ₽")
        h = h.replace("[Описать формат и периодичность отчёта: заявки, стоимость заявки, динамика по каналам.]", "Показываем заявки, стоимость заявки и динамику по каналам. Отчёт — ежемесячно или по запросу.")
        h = h.replace("[Обложка кейса]", "Proxy Agency")
        h = h.replace("[указать ориентиры по каждой услуге]", "первые результаты обычно видны уже через 3 месяца")
        h = re.sub(r'<p class="pxa-note">Периодичность: \[указать\]</p>', '<p class="pxa-note">Периодичность: ежемесячно или по запросу.</p>', h)
        h = re.sub(r'<p class="pxa-note">Срок: \[указать\]</p>', "", h)
    return media_inject(path, h)

for mode, root in OUTS.items():
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root + "/assets/css"); os.makedirs(root + "/assets/img")
    for n, d in LOGOS.items(): open(f"{root}/assets/img/{n}", "wb").write(d)
    for n, c in [("site.css", site_css), ("home.css", home_css), ("cases.css", cases_css)]:
        open(f"{root}/assets/css/{n}", "w", encoding="utf-8").write(c)
    for path, html in PAGES.items():
        html = postprocess(path, html)
        html = re.sub(r'<section class="pxa pxa-sec" id="pxa-team">.*?</section>\n?', "", html, flags=re.S)
        html = html.replace('[Реквизиты: название юрлица, ИНН, ОГРН]', 'ООО «Респект», ИНН 7838493558')
        html = html.replace('<a href="#">Telegram</a>\n<a href="#">WhatsApp</a>', '<a href="https://t.me/proxyagency_SPB" rel="noopener">Telegram</a>\n<a href="mailto:info@proxyagency.ru">Email</a>')
        h = to_preview(html, path) if mode == "preview" else html
        if mode == "prod": h = h.replace("</head>", METRIKA + "</head>", 1)
        f = f"{root}/{out_file(path)}"
        os.makedirs(os.path.dirname(f), exist_ok=True)
        open(f, "w", encoding="utf-8").write(h)
    for d, b in M.OUT.items():
        os.makedirs(os.path.dirname(root + d), exist_ok=True); open(root + d, "wb").write(b)
    if mode == "prod":
        open(root + "/yandex_1e48adc4b47dc923.html", "w", encoding="utf-8").write('<html>\n    <head>\n        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">\n    </head>\n    <body>Verification: 1e48adc4b47dc923</body>\n</html>\n')
        os.makedirs(root + "/netlify/functions", exist_ok=True)
        open(root + "/netlify/functions/submission-created.js", "w", encoding="utf-8").write(SUBMISSION_JS)
        open(root + "/netlify.toml", "w", encoding="utf-8").write('[build]\n  publish = "."\n\n[functions]\n  directory = "netlify/functions"\n')
        urls = [p for p in PAGES if p not in ("404", "thanks", "privacy", "consent", "blog") and "noindex" not in PAGES[p].split("</head>")[0]]
        sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
            f'<url><loc>{SITE}{"/" if p == "" else "/" + p + "/"}</loc><lastmod>{TODAY}</lastmod></url>\n' for p in sorted(urls)) + "</urlset>\n"
        open(root + "/sitemap.xml", "w", encoding="utf-8").write(sm)
        open(root + "/robots.txt", "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nDisallow: /thanks/\n\nSitemap: {SITE}/sitemap.xml\n")
        open(root + "/_redirects", "w", encoding="utf-8").write("".join(f"{a}  {b}  301\n" for a, b in REDIRECTS) + "/*  /404.html  404\n")
        ht = "ErrorDocument 404 /404.html\nDirectoryIndex index.html\n\n" + "".join(f"Redirect 301 {a} {b}\n" for a, b in REDIRECTS)
        open(root + "/.htaccess", "w", encoding="utf-8").write(ht)
        nginx = "".join(f"rewrite ^{a}/?$ {b} permanent;\n" for a, b in REDIRECTS)
        open(root + "/nginx-redirects.conf", "w", encoding="utf-8").write(nginx)
print(len(PAGES), "pages")
print(sorted(PAGES))

