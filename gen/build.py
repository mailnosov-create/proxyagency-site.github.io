import os, shutil, zipfile

OUT = "/tmp/claude-0/-home-claude/4160dc96-70e4-507e-bf5d-2fe78152fe1f/scratchpad/tilda-blocks"
LOGOS = "/tmp/claude-0/-home-claude/4160dc96-70e4-507e-bf5d-2fe78152fe1f/scratchpad/logo-work"
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT + "/logo")

MARK = "https://static.tildacdn.com/REPLACE-ME/proxy-logo-mark.png"
WORD = "https://static.tildacdn.com/REPLACE-ME/proxy-logo-wordmark.png"
FULL = "https://static.tildacdn.com/REPLACE-ME/proxy-logo-full.png"

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600&family=Unbounded:wght@500;600&display=swap" rel="stylesheet">'

BASE = """
.pxa{--pxa-a:#5B3FE0;--pxa-b:#2F6BFF;--pxa-ink:#1B1646;--pxa-mute:#4B4F70;--pxa-tint:#F5F4FF;--pxa-line:#E3E1F5;
font-family:'Onest',system-ui,-apple-system,'Segoe UI',sans-serif;color:var(--pxa-ink);line-height:1.5;font-size:17px;-webkit-font-smoothing:antialiased;text-align:left}
.pxa *,.pxa *::before,.pxa *::after{box-sizing:border-box}
:where(.pxa) h1,:where(.pxa) h2,:where(.pxa) h3,:where(.pxa) h4,:where(.pxa) p,:where(.pxa) figure,:where(.pxa) blockquote{margin:0;padding:0}
:where(.pxa) a{color:inherit}
.pxa-wrap{max-width:1200px;margin:0 auto;padding:0 32px}
.pxa-sec{padding:96px 0}
.pxa-h1{font-family:'Unbounded',sans-serif;font-weight:600;font-size:50px;line-height:1.14;letter-spacing:-.02em}
.pxa-h2{font-family:'Unbounded',sans-serif;font-weight:600;font-size:34px;line-height:1.2;letter-spacing:-.02em}
.pxa-big{font-family:'Unbounded',sans-serif;font-weight:600;letter-spacing:-.02em}
.pxa-mute{color:var(--pxa-mute)}
.pxa-btn{display:inline-block;text-decoration:none;background:linear-gradient(135deg,var(--pxa-a),var(--pxa-b));color:#fff;font-weight:600;padding:16px 28px;border-radius:14px;border:0;font-family:inherit;font-size:17px;cursor:pointer}
.pxa-btn-ghost{display:inline-block;text-decoration:none;color:var(--pxa-ink);font-weight:600;padding:14px 26px;border-radius:14px;border:2px solid #CFCBEF;background:#fff}
.pxa-btn-dark{display:inline-block;text-decoration:none;background:var(--pxa-ink);color:#fff;font-weight:600;padding:14px 24px;border-radius:14px;border:0;font-family:inherit;font-size:17px;cursor:pointer}
.pxa-more{text-decoration:none;font-weight:600;color:var(--pxa-a)}
.pxa-more:hover{text-decoration:underline}
.pxa-logo{display:block}
.pxa{overflow-x:clip;-webkit-text-size-adjust:100%;text-size-adjust:100%}
.pxa img{max-width:100%}
:where(.pxa) ul,:where(.pxa) ol{list-style:none;margin:0;padding:0}
.pxa li::marker{content:none}
.pxa a:focus-visible,.pxa button:focus-visible,.pxa input:focus-visible,.pxa summary:focus-visible{outline:3px solid #2F6BFF;outline-offset:2px}
@media (max-width:860px){
.pxa-wrap{padding:0 20px}
.pxa-sec{padding:56px 0}
.pxa-h1{font-size:30px}
.pxa-h2{font-size:24px}
}
"""

def block(num, name, where, extra_css, html, fonts=True):
    head = f"<!-- Proxy Agency · блок {num} · {name} -->\n<!-- Вставка: Tilda → «Другое» → T123 «HTML-код». Вставлять целиком, вместе с <style>. -->\n"
    return (head + (FONTS + "\n" if fonts else "") + "<style>" + BASE + extra_css + "</style>\n" + html + "\n")

blocks = []

# ---------------- 01 header + hero ----------------
css01 = """
.pxa.pxa-hero{position:relative;overflow:hidden;background:#fff}
.pxa-hero::before{content:"";position:absolute;top:0;right:0;bottom:0;left:0;background:radial-gradient(circle 420px at 88% 14%,rgba(122,63,242,.20),rgba(76,201,240,.16) 60%,rgba(255,255,255,0) 100%),radial-gradient(circle 360px at 2% 98%,rgba(76,201,240,.20),rgba(255,255,255,0) 100%);pointer-events:none}
.pxa-hero .pxa-wrap{position:relative}
.pxa-head{display:flex;align-items:center;justify-content:space-between;gap:24px;padding:16px 0}
.pxa-brand{display:flex;align-items:center;gap:8px;text-decoration:none}
.pxa-brand img{height:56px;width:auto;display:block}
.pxa-nav{display:flex;align-items:center;gap:28px}
.pxa-nav a{text-decoration:none;color:#3B3F63;font-size:15px}
.pxa-nav a:hover{color:var(--pxa-a)}
.pxa-head-r{display:flex;align-items:center;gap:20px}
.pxa-phone{text-decoration:none;font-weight:500;font-size:15px}
.pxa-head-btn{padding:12px 20px;font-size:15px}
.pxa-menu{display:none;position:relative}
.pxa-menu summary{list-style:none;width:44px;height:44px;border:1px solid #CFCBEF;border-radius:12px;background:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer}
.pxa-menu summary::-webkit-details-marker{display:none}
.pxa-menu-list{position:absolute;right:0;top:52px;z-index:20;background:#fff;border:1px solid var(--pxa-line);border-radius:16px;padding:12px;min-width:230px;box-shadow:0 12px 32px rgba(91,63,224,.15);display:flex;flex-direction:column}
.pxa-menu-list a{padding:12px;text-decoration:none;font-weight:500}
.pxa-hero-row{display:flex;flex-wrap:wrap;gap:32px 48px;align-items:center;padding:40px 0 72px}
.pxa-hero-text{flex:1 1 540px;min-width:0}
.pxa-eyebrow{margin:0 0 20px;font-size:13px;color:#4A3FB5;letter-spacing:.06em;text-transform:uppercase;font-weight:600}
.pxa-lead{margin:24px 0 0;font-size:19px;color:var(--pxa-mute);max-width:560px}
.pxa-cta{display:flex;flex-wrap:wrap;gap:16px;margin-top:36px}
.pxa-hero-stats{display:flex;flex-wrap:wrap;gap:16px;margin-top:44px}
.pxa-stat{flex:1 1 220px;background:#fff;border:1px solid var(--pxa-line);border-radius:20px;padding:22px;box-shadow:0 12px 32px rgba(91,63,224,.08)}
.pxa-stat .pxa-big{font-size:44px;line-height:1}
.pxa-stat p{margin:10px 0 0;font-weight:500}
.pxa-stat small{display:block;margin-top:4px;font-size:14px;color:#5A5F7D}
.pxa-hero-art{flex:1 1 360px;min-width:0;display:flex;align-items:center;justify-content:center}
.pxa-hero-art img{width:100%;max-width:480px;height:auto;display:block}
.pxa-trust{display:flex;flex-wrap:wrap;align-items:center;gap:12px 32px;padding:24px 0 36px;border-top:1px solid var(--pxa-line)}
.pxa-trust span{font-weight:600;color:#3B3F63}
.pxa-trust .pxa-trust-l{font-size:14px;font-weight:400;color:#5A5F7D}
@media (max-width:860px){
.pxa .pxa-nav,.pxa .pxa-phone,.pxa .pxa-head-btn{display:none}
.pxa .pxa-menu{display:block}
.pxa-brand img{height:44px}
.pxa-hero-row{padding:24px 0 40px}
.pxa-lead{font-size:17px}
.pxa-cta .pxa-btn,.pxa-cta .pxa-btn-ghost{display:block;text-align:center;flex:1 1 100%}
.pxa-stat .pxa-big{font-size:38px}
.pxa-hero-art{order:3}
.pxa-hero-art img{width:70%;max-width:280px}
}
"""
html01 = f"""<section class="pxa pxa-hero" id="pxa-top">
<div class="pxa-wrap">
<header class="pxa-head">
<a class="pxa-brand" href="/" aria-label="Proxy Creative Agency — на главную">
<img class="pxa-logo" src="{MARK}" alt="">
<img class="pxa-logo pxa-word" src="{WORD}" alt="Proxy creative agency">
</a>
<nav class="pxa-nav" aria-label="Основное меню">
<a href="/services">Услуги</a>
<a href="/cases">Кейсы</a>
<a href="/about">О нас</a>
<a href="/blog">Блог</a>
<a href="/contacts">Контакты</a>
</nav>
<div class="pxa-head-r">
<a class="pxa-phone" href="tel:+78129855830">+7 812 985 5830</a>
<a class="pxa-btn pxa-head-btn" href="#pxa-audit">Обсудить проект</a>
<details class="pxa-menu">
<summary aria-label="Открыть меню"><svg aria-hidden="true" width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h14M3 10h14M3 14h14"/></svg></summary>
<div class="pxa-menu-list">
<a href="/services">Услуги</a>
<a href="/cases">Кейсы</a>
<a href="/about">О нас</a>
<a href="/blog">Блог</a>
<a href="/contacts">Контакты</a>
<a href="tel:+78129855830">+7 812 985 5830</a>
</div>
</details>
</div>
</header>

<div class="pxa-hero-row">
<div class="pxa-hero-text">
<p class="pxa-eyebrow">Digital-агентство · Санкт-Петербург · с 2013 года</p>
<h1 class="pxa-h1">Маркетинг, который приводит гостей и заявки</h1>
<p class="pxa-lead">Для ресторанов, отелей и санаториев. Реклама, SEO и GEO, карты, Telegram и сайты в одной команде, с отчётом по каждой заявке.</p>
<div class="pxa-cta">
<a class="pxa-btn" href="#pxa-audit">Обсудить проект</a>
<a class="pxa-btn-ghost" href="/cases">Смотреть кейсы</a>
</div>
<div class="pxa-hero-stats">
<div class="pxa-stat">
<div class="pxa-big" style="color:var(--pxa-a)">+77%</div>
<p>онлайн-бронирований за 3 месяца</p>
<small>Петров-Водкин · ресторан русской кухни</small>
</div>
<div class="pxa-stat">
<div class="pxa-big" style="color:var(--pxa-b)">+38%</div>
<p>регистраций в программе лояльности за 4 месяца</p>
<small>ОПТИ · сеть АЗС, партнёр «Газпром нефти»</small>
</div>
</div>
</div>
<div class="pxa-hero-art">
<img class="pxa-logo" src="{MARK}" alt="" aria-hidden="true">
</div>
</div>

<div class="pxa-trust">
<span class="pxa-trust-l">Нам доверяют:</span>
<span>ОПТИ</span>
<span>Петров-Водкин</span>
<span>Невский берег</span>
<span>Алтайский замок</span>
<span>Клиника им. Пирогова</span>
</div>
</div>
</section>"""
blocks.append(("01-header-hero", "Шапка и первый экран", css01, html01))

# ---------------- 02 stats ----------------
css02 = """
.pxa.pxa-stats{background:var(--pxa-tint)}
.pxa-stats-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:32px;padding:56px 0}
.pxa-stats-grid .pxa-big{font-size:44px;line-height:1.1;color:var(--pxa-a)}
.pxa-stats-grid p{margin:8px 0 0;color:var(--pxa-mute);font-size:16px}
@media (max-width:860px){
.pxa-stats-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:24px 16px;padding:32px 0}
.pxa-stats-grid .pxa-big{font-size:30px}
.pxa-stats-grid p{font-size:14px}
}
"""
html02 = """<section class="pxa pxa-stats" aria-label="Агентство в цифрах">
<div class="pxa-wrap">
<div class="pxa-stats-grid">
<div><div class="pxa-big">2013</div><p>год, с которого работаем в digital-маркетинге</p></div>
<div><div class="pxa-big">200+</div><p>реализованных проектов</p></div>
<div><div class="pxa-big">8+</div><p>регионов, где работают наши клиенты</p></div>
<div><div class="pxa-big">4+</div><p>страны, где работают наши клиенты</p></div>
</div>
</div>
</section>"""
blocks.append(("02-stats", "Цифры", css02, html02))

# ---------------- 03 services ----------------
css03 = """
.pxa-lede{margin:16px 0 0;max-width:620px;color:var(--pxa-mute)}
.pxa-cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;margin-top:48px}
.pxa-card{border:1px solid var(--pxa-line);border-radius:24px;padding:28px;display:flex;flex-direction:column;gap:12px;background:#fff}
.pxa-card-n{width:44px;height:44px;border-radius:14px;background:#EFEBFF;color:#4A3FB5;display:flex;align-items:center;justify-content:center;font-size:14px}
.pxa-card-n.pxa-blue{background:#E3F1FF;color:#1F4FC4}
.pxa-card h3{margin:8px 0 0;font-size:22px;line-height:1.25}
.pxa-card p{color:var(--pxa-mute)}
.pxa-card .pxa-more{margin-top:auto;padding-top:8px}
.pxa-cta-band{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:20px;margin-top:32px;padding:24px 28px;background:var(--pxa-tint);border-radius:24px}
.pxa-cta-band p{font-weight:600;font-size:19px}
@media (max-width:860px){
.pxa-cards{grid-template-columns:1fr;gap:12px;margin-top:24px}
.pxa-card{padding:20px;border-radius:20px;gap:4px}
.pxa-card-n{display:none}
.pxa-card h3{margin:0;font-size:18px}
.pxa-card p{font-size:15px}
.pxa-card .pxa-more{padding-top:4px;font-size:15px}
.pxa-cta-band{padding:0;background:none;margin-top:20px}
.pxa-cta-band p{display:none}
.pxa-cta-band .pxa-btn-dark{display:block;text-align:center;width:100%}
}
"""
def card(n, title, text, href, blue=False):
    cls = "pxa-card-n pxa-blue" if blue else "pxa-card-n"
    return f'<div class="pxa-card"><span class="{cls} pxa-big">{n}</span><h3>{title}</h3><p>{text}</p><a class="pxa-more" href="{href}">Подробнее →</a></div>'
html03 = f"""<section class="pxa pxa-sec" id="pxa-services">
<div class="pxa-wrap">
<h2 class="pxa-h2">Услуги</h2>
<p class="pxa-lede">Шесть направлений, которые работают как одна система: трафик, сайт, контент и аналитика.</p>
<div class="pxa-cards">
{card("01","Реклама в интернете","Яндекс Директ и таргет в соцсетях. Считаем стоимость заявки и снижаем её.","/services/ads")}
{card("02","SEO и GEO","Чтобы вас находили в поиске и рекомендовали нейросети.","/services/seo-geo")}
{card("03","Карты и 2ГИС","Яндекс Карты, Навигатор и 2ГИС: клиенты, которые ищут «рядом».","/services/maps")}
{card("04","SMM и Telegram","Каналы и соцсети, которые приводят клиентов, а не только подписчиков.","/services/smm-telegram",True)}
{card("05","Сайты и разработка","Сайты и приложения с настроенной аналитикой, быстрые и удобные с телефона.","/services/web",True)}
{card("06","Продакшн","Фото- и видеосъёмки для рекламы и соцсетей: контент, который продаёт.","/services/production",True)}
</div>
<div class="pxa-cta-band">
<p>Не знаете, что нужно? Начнём с бесплатного аудита.</p>
<a class="pxa-btn-dark" href="#pxa-audit">Получить экспресс-аудит</a>
</div>
</div>
</section>"""
blocks.append(("03-services", "Услуги", css03, html03))

# ---------------- 04 cases ----------------
css04 = """
.pxa.pxa-cases{background:var(--pxa-tint)}
.pxa-row-h{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:16px}
.pxa-case-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;margin-top:40px}
.pxa-case{background:#fff;border-radius:24px;overflow:hidden;display:flex;flex-direction:column}
.pxa-cover{height:200px;background:linear-gradient(135deg,#E4DCFF,#D2EEFF);display:flex;align-items:center;justify-content:center;color:#3B3F63;font-size:14px}
.pxa-case-b{padding:28px;display:flex;flex-direction:column;gap:8px}
.pxa-case-b small{font-size:14px;color:#5A5F7D}
.pxa-case-b h3{font-size:22px}
.pxa-case-b .pxa-big{font-size:44px;line-height:1.1;margin-top:8px}
.pxa-case-b .pxa-strong{font-weight:500}
.pxa-case-b .pxa-desc{margin-top:8px;color:var(--pxa-mute);font-size:16px}
@media (max-width:860px){
.pxa-case-grid{grid-template-columns:1fr;gap:16px;margin-top:24px}
.pxa-cover{display:none}
.pxa-case{border-radius:20px}
.pxa-case-b{padding:24px}
.pxa-case-b .pxa-big{font-size:36px}
.pxa-case-b .pxa-desc{display:none}
}
"""
html04 = """<section class="pxa pxa-sec pxa-cases" id="pxa-cases">
<div class="pxa-wrap">
<div class="pxa-row-h">
<h2 class="pxa-h2">Кейсы</h2>
<a class="pxa-more" href="/cases">Все кейсы →</a>
</div>
<div class="pxa-case-grid">

<article class="pxa-case">
<div class="pxa-cover">[Обложка кейса]</div>
<div class="pxa-case-b">
<small>Ресторан русской кухни</small>
<h3>Петров-Водкин</h3>
<div class="pxa-big" style="color:var(--pxa-a)">+77%</div>
<p class="pxa-strong">онлайн-бронирований за 3 месяца</p>
<p class="pxa-desc">Performance-реклама и локальные digital-каналы.</p>
</div>
</article>

<article class="pxa-case">
<div class="pxa-cover" style="background:linear-gradient(135deg,#D2EEFF,#E4DCFF)">[Обложка кейса]</div>
<div class="pxa-case-b">
<small>Сеть АЗС, партнёр «Газпром нефти»</small>
<h3>ОПТИ</h3>
<div class="pxa-big" style="color:var(--pxa-b)">+38%</div>
<p class="pxa-strong">регистраций в программе лояльности за 4 месяца</p>
<p class="pxa-desc">Performance-маркетинг и продвижение программы лояльности.</p>
</div>
</article>

<article class="pxa-case">
<div class="pxa-cover">[Обложка кейса]</div>
<div class="pxa-case-b">
<small>Отели в центре Санкт-Петербурга</small>
<h3>Невский берег</h3>
<div class="pxa-big" style="color:#5A5F7D">[ЦИФРА]</div>
<p class="pxa-strong">[показатель и срок: например, стоимость брони]</p>
<p class="pxa-desc">Привлекаем клиентов, снижаем стоимость брони и масштабируем продажи через performance-маркетинг, стратегию и digital.</p>
</div>
</article>

</div>
</div>
</section>"""
blocks.append(("04-cases", "Кейсы", css04, html04))

# ---------------- 05 process ----------------
css05 = """
.pxa-steps{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:24px;margin-top:48px}
.pxa-num{width:44px;height:44px;flex:none;border-radius:50%;background:linear-gradient(135deg,var(--pxa-a),var(--pxa-b));color:#fff;display:flex;align-items:center;justify-content:center;font-weight:600;margin-bottom:16px}
.pxa-num.pxa-last{background:#4CC9F0;color:var(--pxa-ink)}
.pxa-step h3{font-size:19px;margin:0 0 8px}
.pxa-step p{color:var(--pxa-mute);font-size:16px}
.pxa-step .pxa-note{margin-top:12px;font-size:14px;color:#5A5F7D}
@media (max-width:860px){
.pxa-steps{grid-template-columns:1fr;gap:20px;margin-top:24px}
.pxa-step{display:flex;gap:16px}
.pxa-num{width:40px;height:40px;margin-bottom:0}
.pxa-step h3{font-size:18px;margin:0}
.pxa-step p{font-size:15px;margin-top:4px}
.pxa-step .pxa-note{display:none}
}
"""
def step(n, t, d, note, last=False):
    cls = "pxa-num pxa-last" if last else "pxa-num"
    return f'<div class="pxa-step"><div class="{cls}">{n}</div><div><h3>{t}</h3><p>{d}</p><p class="pxa-note">{note}</p></div></div>'
html05 = f"""<section class="pxa pxa-sec" id="pxa-process">
<div class="pxa-wrap">
<h2 class="pxa-h2">Как мы работаем</h2>
<p class="pxa-lede pxa-mute" style="margin:16px 0 0;max-width:620px">Пять шагов от первого разговора до роста заявок. Сроки каждого шага согласуем в брифе.</p>
<div class="pxa-steps">
{step(1,"Бриф и аудит","Разбираем задачу, сайт и текущую рекламу.","Срок: [указать]")}
{step(2,"Стратегия","Выбираем каналы, считаем бюджет и цели.","Срок: [указать]")}
{step(3,"Запуск","Настраиваем рекламу, аналитику и страницы.","Срок: [указать]")}
{step(4,"Отчётность","Показываем заявки и стоимость заявки по каждому каналу.","Периодичность: [указать]")}
{step(5,"Масштабирование","Усиливаем то, что работает, и убираем то, что нет.","Срок: [указать]",True)}
</div>
</div>
</section>"""
blocks.append(("05-process", "Как мы работаем", css05, html05))

# ---------------- 06 reviews ----------------
css06 = """
.pxa.pxa-dark{background:var(--pxa-ink);color:#fff}
.pxa-rev{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin-top:40px}
.pxa-rev figure{background:#262060;border:1px solid #3A3380;border-radius:24px;padding:32px}
.pxa-rev blockquote{font-size:20px;line-height:1.45}
.pxa-rev figcaption{margin-top:24px;color:#C9C5EE;font-size:15px}
.pxa-names{display:flex;flex-wrap:wrap;gap:12px 32px;margin-top:48px;color:#E4E1FA;font-weight:600}
@media (max-width:860px){
.pxa-rev{grid-template-columns:1fr;gap:16px;margin-top:24px}
.pxa-rev figure{padding:24px;border-radius:20px}
.pxa-rev blockquote{font-size:17px}
.pxa-rev figcaption{margin-top:16px;font-size:14px}
.pxa-names{margin-top:32px;font-size:15px}
}
"""
html06 = """<section class="pxa pxa-sec pxa-dark" id="pxa-reviews">
<div class="pxa-wrap">
<h2 class="pxa-h2">Отзывы клиентов</h2>
<div class="pxa-rev">
<figure>
<blockquote>«[Текст отзыва клиента: какая была задача, что сделали, какой получили результат]»</blockquote>
<figcaption>[Имя Фамилия], [должность], [компания]</figcaption>
</figure>
<figure>
<blockquote>«[Текст отзыва клиента или видеоотзыв: вставить ссылку на ролик]»</blockquote>
<figcaption>[Имя Фамилия], [должность], [компания]</figcaption>
</figure>
</div>
<div class="pxa-names">
<span>ОПТИ</span><span>Петров-Водкин</span><span>La Perla</span><span>Бочкари</span><span>Маzай</span><span>TARGET</span><span>Алтайский замок</span><span>Невский берег</span>
</div>
</div>
</section>"""
blocks.append(("06-reviews", "Отзывы и клиенты", css06, html06))

# ---------------- 07 team ----------------
css07 = """
.pxa-team{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:24px;margin-top:40px}
.pxa-photo{width:100%;aspect-ratio:1/1;border-radius:24px;background:linear-gradient(135deg,#EFEBFF,#E3F1FF);display:flex;align-items:center;justify-content:center;color:#3B3F63;font-size:14px;overflow:hidden}
.pxa-photo img{width:100%;height:100%;object-fit:cover;display:block}
.pxa-person h3{margin:16px 0 4px;font-size:19px}
.pxa-person p{color:var(--pxa-mute);font-size:16px}
@media (max-width:860px){
.pxa-team{grid-template-columns:repeat(2,minmax(0,1fr));gap:20px 16px;margin-top:24px}
.pxa-photo{border-radius:20px}
.pxa-person h3{font-size:17px}
.pxa-person p{font-size:14px}
}
"""
def person(role):
    return f'<div class="pxa-person"><div class="pxa-photo">[Фото]</div><h3>[Имя Фамилия]</h3><p>{role}</p></div>'
html07 = f"""<section class="pxa pxa-sec" id="pxa-team">
<div class="pxa-wrap">
<div class="pxa-row-h" style="display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:16px">
<h2 class="pxa-h2">Команда</h2>
<a class="pxa-more" href="/about">О нас →</a>
</div>
<div class="pxa-team">
{person("[Руководитель агентства]")}
{person("[Руководитель направления рекламы]")}
{person("[Специалист по SEO и GEO]")}
{person("[Менеджер по работе с клиентами]")}
</div>
</div>
</section>"""
blocks.append(("07-team", "Команда", css07, html07))

# ---------------- 08 audit ----------------
css08 = """
.pxa.pxa-audit{background:linear-gradient(135deg,var(--pxa-a),var(--pxa-b));color:#fff}
.pxa-audit-row{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}
.pxa-audit-lead{margin-top:20px;font-size:19px;max-width:520px}
.pxa-form{background:#fff;color:var(--pxa-ink);border-radius:24px;padding:32px;display:flex;flex-direction:column;gap:16px}
.pxa-field{display:flex;flex-direction:column;gap:6px}
.pxa-field label{font-size:14px;font-weight:600}
.pxa-field input{font-family:inherit;font-size:17px;padding:14px 16px;border:1px solid #B9B6DD;border-radius:12px;background:#fff;color:var(--pxa-ink);width:100%}
.pxa-consent{display:flex;align-items:flex-start;gap:10px}
.pxa-consent input{margin-top:5px;width:18px;height:18px;flex:none}
.pxa-consent label{font-size:14px;color:var(--pxa-mute)}
.pxa-consent a{color:var(--pxa-ink)}
@media (max-width:860px){
.pxa-audit-row{grid-template-columns:1fr;gap:24px}
.pxa-audit-lead{font-size:17px;margin-top:14px}
.pxa-form{padding:20px;border-radius:20px}
.pxa-form .pxa-btn-dark{width:100%}
}
"""
html08 = """<section class="pxa pxa-sec pxa-audit" id="pxa-audit">
<div class="pxa-wrap">
<div class="pxa-audit-row">
<div>
<h2 class="pxa-h2">Бесплатный экспресс-аудит рекламы и сайта</h2>
<p class="pxa-audit-lead">Покажем, где теряются заявки, за [2] рабочих дня. Срок подтвердим перед запуском сайта.</p>
</div>
<!-- ВНИМАНИЕ: эта форма — только оформление. Чтобы заявки приходили, замените её штатным блоком формы Tilda
     (он умеет слать заявки на почту, в Telegram и CRM), либо укажите свой обработчик в action. -->
<form class="pxa-form" action="REPLACE_FORM_ENDPOINT" method="post">
<div class="pxa-field"><label for="pxa-site">Сайт или аккаунт</label><input id="pxa-site" name="site" type="text" placeholder="proxyagency.ru"></div>
<div class="pxa-field"><label for="pxa-contact">Телефон или Telegram</label><input id="pxa-contact" name="contact" type="text" placeholder="+7 ___ ___ __ __" required></div>
<div class="pxa-consent"><input id="pxa-consent" name="consent" type="checkbox" required><label for="pxa-consent">Согласен на обработку персональных данных. <a href="/privacy">Политика конфиденциальности</a></label></div>
<button class="pxa-btn-dark" type="submit">Получить аудит</button>
</form>
</div>
</div>
</section>"""
blocks.append(("08-audit-form", "Экспресс-аудит (форма)", css08, html08))

# ---------------- 09 faq ----------------
css09 = """
.pxa-faq{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:40px 48px;margin-top:48px}
.pxa-faq-col{display:flex;flex-direction:column;gap:32px}
.pxa-faq h3{font-size:20px;margin:0 0 8px}
.pxa-faq p{color:var(--pxa-mute)}
@media (max-width:860px){
.pxa-faq{grid-template-columns:1fr;gap:24px;margin-top:24px}
.pxa-faq-col{gap:24px}
.pxa-faq h3{font-size:18px;margin-bottom:6px}
.pxa-faq p{font-size:15px}
}
"""
html09 = """<section class="pxa pxa-sec" id="pxa-faq">
<div class="pxa-wrap">
<h2 class="pxa-h2">Частые вопросы</h2>
<div class="pxa-faq">
<div class="pxa-faq-col">
<div><h3>Сколько стоит работа агентства?</h3><p>Стоимость зависит от задачи, каналов и бюджета на рекламу. После экспресс-аудита называем ориентир: [диапазон — заполнить].</p></div>
<div><h3>Как быстро будет результат?</h3><p>Сроки зависят от канала и ниши: [указать ориентиры по каждой услуге].</p></div>
<div><h3>С какими отраслями вы работаете?</h3><p>Рестораны, гостиницы, санатории, клиники, производители и розничные сети. Наши клиенты работают в 8+ регионах и 4+ странах.</p></div>
</div>
<div class="pxa-faq-col">
<div><h3>Как строится отчётность?</h3><p>[Описать формат и периодичность отчёта: заявки, стоимость заявки, динамика по каналам.]</p></div>
<div><h3>Нужен ли новый сайт, чтобы запустить рекламу?</h3><p>Не обязательно. Сначала разберём ваш сайт в аудите: если он мешает заявкам, подскажем, что исправить, или сделаем новый.</p></div>
<div><h3>Что такое GEO и зачем оно мне?</h3><p>GEO — оптимизация под ответы нейросетей и ИИ-поиска. Она помогает, чтобы ваш бренд упоминали в ответах Яндекс Нейро, Алисы и других ассистентов.</p></div>
</div>
</div>
</div>
</section>"""
blocks.append(("09-faq", "Частые вопросы", css09, html09))

# ---------------- 10 footer ----------------
css10 = """
.pxa.pxa-foot{background:var(--pxa-tint);color:var(--pxa-ink)}
.pxa-foot .pxa-wrap{padding-top:72px;padding-bottom:32px}
.pxa-foot-grid{display:grid;grid-template-columns:1.4fr 1fr .8fr 1.4fr;gap:40px 48px}
.pxa-foot-logo{width:180px;height:auto;display:block}
.pxa-foot-about{margin-top:16px;color:var(--pxa-mute);font-size:16px;max-width:320px}
.pxa-foot h4{margin:0 0 16px;font-weight:600;font-size:17px}
.pxa-foot-list{display:flex;flex-direction:column;gap:10px;font-size:16px;color:#3B3F63}
.pxa-foot-list a{text-decoration:none;color:#3B3F63}
.pxa-foot-list a:hover{color:var(--pxa-a)}
.pxa-soc{display:flex;flex-wrap:wrap;gap:8px 20px;margin-top:4px}
.pxa-legal{display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px 24px;margin-top:56px;padding-top:24px;border-top:1px solid #DAD6F3;font-size:14px;color:#5A5F7D}
.pxa-legal span{display:flex;flex-wrap:wrap;gap:8px 24px}
.pxa-legal a{text-decoration:none;color:#3B3F63}
@media (max-width:860px){
.pxa-foot .pxa-wrap{padding-top:40px;padding-bottom:28px}
.pxa-foot-grid{grid-template-columns:1fr;gap:28px}
.pxa-foot-logo{width:150px}
.pxa-foot-hide{display:none}
.pxa-foot-list{font-size:15px}
.pxa-legal{margin-top:28px;padding-top:20px;font-size:13px}
}
"""
html10 = f"""<footer class="pxa pxa-foot" id="pxa-contacts">
<div class="pxa-wrap">
<div class="pxa-foot-grid">
<div>
<img class="pxa-logo pxa-foot-logo" src="{FULL}" alt="Proxy creative agency">
<p class="pxa-foot-about">Digital-агентство в Санкт-Петербурге. Работаем с 2013 года.</p>
</div>
<div class="pxa-foot-hide">
<h4>Услуги</h4>
<div class="pxa-foot-list">
<a href="/services/ads">Реклама в интернете</a>
<a href="/services/seo-geo">SEO и GEO</a>
<a href="/services/maps">Карты и 2ГИС</a>
<a href="/services/smm-telegram">SMM и Telegram</a>
<a href="/services/web">Сайты и разработка</a>
<a href="/services/production">Продакшн</a>
</div>
</div>
<div class="pxa-foot-hide">
<h4>Компания</h4>
<div class="pxa-foot-list">
<a href="/about">О нас</a>
<a href="/cases">Кейсы</a>
<a href="/blog">Блог</a>
</div>
</div>
<div>
<h4>Контакты</h4>
<div class="pxa-foot-list">
<a href="tel:+78129855830">+7 812 985 5830</a>
<a href="mailto:hello@proxyagency.ru">hello@proxyagency.ru</a>
<span>Санкт-Петербург, ул. Марата, д. 86, ТРК «Нептун», 3 этаж (лофт)</span>
<div class="pxa-soc">
<a href="#">Telegram</a>
<a href="#">WhatsApp</a>
<a href="https://vk.com/proxy_agency">VK</a>
</div>
</div>
</div>
</div>
<div class="pxa-legal">
<div>© Proxy Agency · [Реквизиты: название юрлица, ИНН, ОГРН]</div>
<span>
<a href="/privacy">Политика конфиденциальности</a>
<a href="/consent">Согласие на обработку данных</a>
</span>
</div>
</div>
</footer>"""
blocks.append(("10-footer", "Подвал и контакты", css10, html10))

names = []
for i, (fname, title, css, html) in enumerate(blocks, 1):
    num = fname.split("-")[0]
    content = block(num, title, "", css, html)
    path = f"{OUT}/{fname}.html"
    open(path, "w", encoding="utf-8").write(content)
    names.append((fname, title, len(content.encode("utf-8"))))

for f in ["proxy-logo-mark.png", "proxy-logo-wordmark.png", "proxy-logo-full.png"]:
    shutil.copy(f"{LOGOS}/{f}", f"{OUT}/logo/{f}")

for n in names:
    print(n)
