import os, re, shutil

ROOT = "/tmp/claude-0/-home-claude/4160dc96-70e4-507e-bf5d-2fe78152fe1f/scratchpad"
HOME = ROOT + "/tilda-blocks"
CASES = ROOT + "/tilda-cases"
OUT = ROOT + "/tilda-opti"
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT + "/logo")

src = open(ROOT + "/gen/build.py", encoding="utf-8").read()
BASE = re.search(r'BASE = """(.*?)"""', src, re.S).group(1)
FONTS = re.search(r"FONTS = '(.*?)'", src).group(1)
MARK = "https://static.tildacdn.com/REPLACE-ME/proxy-logo-mark.png"

c01 = open(CASES + "/c01-header-intro.html", encoding="utf-8").read()
c01 = re.sub(r"<!--.*?-->", "", c01, flags=re.S)
c01_style = c01[c01.index("<style>") + 7: c01.index("</style>")]
c01_css = c01_style.replace(BASE, "", 1)          # CSS01 + crumbs, without BASE
header = re.search(r'<header class="pxa-head">.*?</header>', c01, re.S).group(0)

def wrap(num, name, css, html, with_base=True):
    return (f"<!-- Proxy Agency · кейс «ОПТИ» · блок {num} · {name} -->\n"
            "<!-- Вставка: Tilda → «Другое» → T123 «HTML-код». Вставлять целиком, вместе с <style>. -->\n"
            + FONTS + "\n<style>" + BASE + css + "</style>\n" + html + "\n")

CHECK = '<svg aria-hidden="true" width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 7.4l3 3 6-6.4"/></svg>'

# ---------------- k01 header + hero ----------------
css_k01 = c01_css + """
.pxa-k-h1{font-size:42px}
.pxa-meta{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px 32px;margin:36px 0 0;padding:24px 0 0;border-top:1px solid var(--pxa-line);max-width:640px}
.pxa-meta dt{font-size:13px;color:#5A5F7D;text-transform:uppercase;letter-spacing:.06em;font-weight:600}
.pxa-meta dd{margin:4px 0 0;font-weight:500}
.pxa-cta-row{display:flex;flex-wrap:wrap;gap:12px;margin-top:32px}
@media (max-width:860px){
.pxa-k-h1{font-size:26px}
.pxa-meta{grid-template-columns:1fr;gap:14px;margin-top:28px}
.pxa-cta-row{margin-top:24px}
.pxa-cta-row a{flex:1 1 100%;text-align:center}
}
"""
html_k01 = f"""<section class="pxa pxa-hero" id="pxa-top">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Главная","item":"https://proxyagency.ru/"}},{{"@type":"ListItem","position":2,"name":"Кейсы","item":"https://proxyagency.ru/cases"}},{{"@type":"ListItem","position":3,"name":"ОПТИ","item":"https://proxyagency.ru/cases/opti"}}]}}</script>
<div class="pxa-wrap">
{header}

<div class="pxa-hero-row" style="padding-bottom:64px">
<div class="pxa-hero-text">
<nav class="pxa-crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span><a href="/cases">Кейсы</a><span>/</span>ОПТИ</nav>
<p class="pxa-eyebrow">Кейс · АЗС и розница · B2C и B2B</p>
<h1 class="pxa-h1 pxa-k-h1">Сеть АЗС «ОПТИ»: федеральные акции в 35 регионах и рост скачиваний приложения в 2 раза</h1>
<p class="pxa-lead">Запускали акции с призовым фондом до 5 000 000 ₽, растили приложение и соцсети, создали Telegram-канал с нуля и привлекали новых франчайзи.</p>
<dl class="pxa-meta">
<div><dt>Клиент</dt><dd>Федеральная сеть АЗС «ОПТИ», партнёр «Газпром нефти»</dd></div>
<div><dt>Сегменты</dt><dd>B2C: аудитория сообществ АЗС. B2B: франчайзи</dd></div>
<div><dt>Каналы</dt><dd>Контекст, таргет, соцсети, Telegram, YouTube, TikTok, Яндекс.Навигатор, 2ГИС</dd></div>
<div><dt>Период</dt><dd>[добавить срок работы]</dd></div>
</dl>
<div class="pxa-cta-row">
<a class="pxa-btn" href="#pxa-audit">Хочу такой же результат</a>
<a class="pxa-btn-ghost" href="/cases">Все кейсы</a>
</div>
</div>
<div class="pxa-hero-art pxa-intro-art">
<img class="pxa-logo" src="{MARK}" alt="" aria-hidden="true">
</div>
</div>
</div>
</section>"""

# ---------------- k02 KPI ----------------
css_k02 = """
.pxa.pxa-dark{background:var(--pxa-ink);color:#fff}
.pxa-dark .pxa-h2{color:#fff}
.pxa-kpi-sub{margin-top:12px;color:#C9C6EE;max-width:620px}
.pxa-kpi-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:44px}
.pxa-kpi{position:relative;display:flex;flex-direction:column;gap:10px;padding:28px;border-radius:24px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14)}
.pxa-kpi.pxa-done{background:linear-gradient(160deg,rgba(91,63,224,.38),rgba(47,107,255,.16));border-color:rgba(122,200,255,.55);box-shadow:0 0 0 1px rgba(76,201,240,.15),0 20px 50px rgba(47,107,255,.18)}
.pxa-badge{align-self:flex-start;display:inline-flex;align-items:center;gap:6px;padding:5px 12px 5px 9px;border-radius:999px;font-size:13px;font-weight:600;line-height:1.2;background:rgba(76,201,240,.18);color:#8FE3FA}
.pxa-badge.pxa-scale{background:rgba(255,255,255,.1);color:#D6D3F5}
.pxa-kpi-n{font-family:'Unbounded',sans-serif;font-weight:600;letter-spacing:-.02em;font-size:60px;line-height:1.05;color:#BDB1FF;background:linear-gradient(135deg,#C9BFFF,#5FD4F7);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;margin-top:6px}
.pxa-kpi-t{font-size:17px;line-height:1.45;color:#EDEBFF}
.pxa-kpi-src{font-size:14px;color:#B9B5E6;margin-top:auto}
.pxa-kpi-note{margin-top:28px;font-size:14px;color:#B9B5E6}
@media (max-width:1000px){
.pxa-kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:860px){
.pxa-kpi-grid{grid-template-columns:1fr;gap:14px;margin-top:28px}
.pxa-kpi{padding:22px;border-radius:20px}
.pxa-kpi-n{font-size:46px}
.pxa-kpi-t{font-size:16px}
}
"""
kpis = [
 ("done", "×2", "рост скачиваний мобильного приложения АЗС «ОПТИ»", "Интеграция с онлайн-кинотеатром ОККО"),
 ("done", "×2", "рост вовлечённости аудитории в соцсетях", "Новое визуальное оформление, без рекламы"),
 ("done", "1 600", "подписчиков в Telegram-канале за 4 месяца", "Канал с нуля, без рекламного кабинета Telegram"),
 ("done", "+38%", "регистраций в программе лояльности за 4 месяца", "Performance-маркетинг и продвижение программы"),
 ("scale", "35", "регионов России в охвате рекламной поддержки акций", "Контекстная и таргетированная реклама"),
 ("scale", "5 млн ₽", "призовой фонд федеральных рекламных акций (до)", "Розыгрыши призов и подарков"),
]
def kpi(k):
    kind, n, t, s = k
    if kind == "done":
        b = f'<span class="pxa-badge">{CHECK}KPI выполнен</span>'
        cls = "pxa-kpi pxa-done"
    else:
        b = '<span class="pxa-badge pxa-scale">Масштаб проекта</span>'
        cls = "pxa-kpi"
    return f'<li class="{cls}">{b}<div class="pxa-kpi-n">{n}</div><p class="pxa-kpi-t">{t}</p><p class="pxa-kpi-src">{s}</p></li>'
html_k02 = f"""<section class="pxa pxa-sec pxa-dark pxa-kpis" id="pxa-kpi">
<div class="pxa-wrap">
<h2 class="pxa-h2">Результаты в цифрах</h2>
<p class="pxa-kpi-sub">Что мы получили по ключевым показателям проекта.</p>
<ul class="pxa-kpi-grid" style="list-style:none;margin:44px 0 0;padding:0">
{chr(10).join(kpi(k) for k in kpis)}
</ul>
<p class="pxa-kpi-note">Плановые значения KPI: [добавить, если можно раскрыть клиенту]</p>
</div>
</section>"""

# ---------------- k03 task + scope ----------------
css_k03 = """
.pxa-two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin-top:40px}
.pxa-panel{padding:36px;border-radius:24px;background:var(--pxa-tint)}
.pxa-panel h3{font-size:22px;line-height:1.3;font-family:'Unbounded',sans-serif;font-weight:600;letter-spacing:-.01em}
.pxa-panel p{margin-top:12px;color:var(--pxa-mute)}
.pxa-list{list-style:none;margin:20px 0 0;padding:0;display:flex;flex-direction:column;gap:12px}
.pxa-list li{display:flex;gap:12px;align-items:flex-start}
.pxa-list li::before{content:"";flex:none;width:22px;height:22px;margin-top:2px;border-radius:50%;background:linear-gradient(135deg,var(--pxa-a),var(--pxa-b))}
.pxa-list li{position:relative}
.pxa-list li svg{position:absolute;left:4px;top:7px;color:#fff}
@media (max-width:860px){
.pxa-two{grid-template-columns:1fr;gap:16px;margin-top:28px}
.pxa-panel{padding:24px;border-radius:20px}
.pxa-panel h3{font-size:19px}
}
"""
tasks = [
 "Поддержать федеральные рекламные акции в регионах присутствия сети",
 "Стимулировать бонусную программу лояльности и рост установок приложения",
 "Вырастить вовлечённость аудитории сообществ АЗС",
 "Привлечь новых франчайзи в B2B-сегменте",
]
scope = [
 "Ведение соцсетей",
 "Настройка и ведение таргетированной рекламы",
 "Контекстная реклама для B2B и B2C",
 "Визуалы для digital-каналов",
 "Федеральные акции: розыгрыши призов и подарков",
 "Управление репутацией: комьюнити-менеджмент, работа с негативом",
 "Influence-маркетинг",
 "Фото- и видеосъёмка АЗС, рекламные ролики",
]
li = lambda items: "\n".join(f"<li>{CHECK}<span>{t}</span></li>" for t in items)
html_k03 = f"""<section class="pxa pxa-sec" id="pxa-task">
<div class="pxa-wrap">
<h2 class="pxa-h2">Задача и что вошло в работу</h2>
<div class="pxa-two">
<div class="pxa-panel">
<h3>Клиент и задачи</h3>
<p>«ОПТИ» — федеральная сеть автозаправочных станций, партнёр «Газпром нефти». Работаем с двумя аудиториями: клиенты сети и будущие франчайзи.</p>
<ul class="pxa-list">
{li(tasks)}
</ul>
</div>
<div class="pxa-panel">
<h3>Что сделали</h3>
<p>Единая digital-стратегия для B2C и B2B: от акций до контента и съёмки.</p>
<ul class="pxa-list">
{li(scope)}
</ul>
</div>
</div>
</div>
</section>"""

# ---------------- k04 steps ----------------
css_k04 = """
.pxa.pxa-tint{background:var(--pxa-tint)}
.pxa-steps{list-style:none;margin:40px 0 0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
.pxa-step{display:flex;flex-direction:column;gap:10px;padding:32px;border-radius:24px;background:#fff;border:1px solid transparent}
.pxa-step:hover{border-color:#CFCBEF;box-shadow:0 16px 40px rgba(91,63,224,.12)}
.pxa-step-n{font-family:'Unbounded',sans-serif;font-weight:600;font-size:15px;color:var(--pxa-a)}
.pxa-step h3{font-size:21px;line-height:1.25}
.pxa-step p{color:var(--pxa-mute);font-size:16px}
.pxa-res{margin-top:auto;padding-top:10px}
.pxa-res span{display:inline-flex;align-items:center;gap:8px;padding:8px 14px;border-radius:12px;background:linear-gradient(135deg,rgba(91,63,224,.12),rgba(47,107,255,.12));color:#3A25B8;font-weight:600;font-size:15px;line-height:1.3}
.pxa-res span.pxa-open{background:#fff;border:1px dashed #B9B5E6;color:#5A5F7D;font-weight:500}
.pxa-gallery{margin-top:24px;padding:40px;border:2px dashed #CFCBEF;border-radius:24px;text-align:center;color:#5A5F7D}
@media (max-width:1000px){
.pxa-steps{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:860px){
.pxa-steps{grid-template-columns:1fr;gap:14px;margin-top:28px}
.pxa-step{padding:24px;border-radius:20px}
.pxa-step h3{font-size:19px}
.pxa-gallery{padding:24px}
}
"""
steps = [
 ("Федеральные рекламные акции", "Запустили акции с призовым фондом до 5 000 000 ₽. Для их поддержки вели контекстную и таргетированную рекламу на 35 регионов, использовали Яндекс.Навигатор и 2ГИС. Для каждой акции разработали и адаптировали визуалы.", "35 регионов в охвате", False),
 ("Influence-маркетинг", "Для акции «Выгода набирает повороты» сделали интеграцию с блогерами в YouTube и TikTok. Вместе с онлайн-кинотеатром ОККО провели интерактивный квиз с еженедельными розыгрышами и подпиской «Премиум» в конце месяца.", "Скачивания приложения ×2", False),
 ("Визуалы для соцсетей", "Проверили гипотезу: можно повысить вовлечённость без таргетированной рекламы. Обновили визуальное оформление соцсетей.", "Вовлечённость ×2", False),
 ("Telegram-канал с нуля", "После ухода Meta* создали и раскрутили канал без рекламного кабинета Telegram и без переманивания аудитории из других соцсетей.", "1 600 подписчиков за 4 месяца", False),
 ("B2B: новые франчайзи", "Привлекали франчайзи через контекстную рекламу на площадках.", "[добавить число заявок или франчайзи]", True),
 ("Фото- и видеосъёмка", "Организовали съёмку АЗС и произвели рекламные ролики для digital-каналов и акций.", "[добавить число материалов]", True),
]
def step(i, s):
    t, d, r, op = s
    return f'<li class="pxa-step"><span class="pxa-step-n">{i:02d}</span><h3>{t}</h3><p>{d}</p><div class="pxa-res"><span class="{"pxa-open" if op else ""}">{r if op else CHECK + r}</span></div></li>'
html_k04 = f"""<section class="pxa pxa-sec pxa-tint" id="pxa-work">
<div class="pxa-wrap">
<h2 class="pxa-h2">Как мы это сделали</h2>
<ol class="pxa-steps">
{chr(10).join(step(i, s) for i, s in enumerate(steps, 1))}
</ol>
<div class="pxa-gallery">[Галерея: визуалы акций, фото АЗС, скриншоты Telegram-канала и квиза ОККО]</div>
<p style="margin-top:20px;font-size:14px;color:#5A5F7D">* Запрещённый на территории России сервис.</p>
</div>
</section>"""

# ---------------- k05 conclusions ----------------
css_k05 = """
.pxa-concl{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:64px;align-items:start}
.pxa-concl-l{position:sticky;top:32px}
.pxa-concl-l p{margin-top:16px;color:var(--pxa-mute)}
.pxa-concl-l .pxa-btn{margin-top:28px}
.pxa-ol{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:0}
.pxa-ol li{display:grid;grid-template-columns:56px minmax(0,1fr);gap:20px;padding:28px 0;border-top:1px solid var(--pxa-line)}
.pxa-ol li:last-child{border-bottom:1px solid var(--pxa-line)}
.pxa-ol-n{font-family:'Unbounded',sans-serif;font-weight:600;font-size:28px;line-height:1;background:linear-gradient(135deg,var(--pxa-a),var(--pxa-b));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:var(--pxa-a)}
.pxa-ol h3{font-size:20px;line-height:1.3}
.pxa-ol p{margin-top:8px;color:var(--pxa-mute);font-size:16px}
@media (max-width:1000px){
.pxa-concl{grid-template-columns:1fr;gap:32px}
.pxa-concl-l{position:static}
}
@media (max-width:860px){
.pxa-ol li{grid-template-columns:40px minmax(0,1fr);gap:14px;padding:22px 0}
.pxa-ol-n{font-size:22px}
.pxa-ol h3{font-size:18px}
}
"""
concl = [
 ("Партнёрская механика даёт установки", "Квиз с ОККО с понятным призом удвоил скачивания приложения. Интеграции с сервисами, которыми аудитория уже пользуется, быстрее всего приводят в приложение."),
 ("Визуал вовлекает без рекламы", "Обновление оформления соцсетей дало рост вовлечённости в 2 раза без таргетированной рекламы. Сначала проверяем гипотезы на контенте, затем вкладываем бюджет."),
 ("Органика работает, если есть система", "Telegram-канал с нуля набрал 1 600 подписчиков за 4 месяца без рекламного кабинета. Свой канал с живой аудиторией остаётся у бренда и после смены правил на других площадках."),
 ("Акции масштабируются через гео-каналы", "Контекст и таргет на 35 регионов вместе с Яндекс.Навигатором и 2ГИС приводят аудиторию туда, где она выбирает АЗС."),
 ("B2C и B2B в одной стратегии", "Один подрядчик ведёт и аудиторию сети, и привлечение франчайзи. Это единый стиль коммуникации и меньше разрозненных команд."),
]
html_k05 = f"""<section class="pxa pxa-sec" id="pxa-takeaways">
<div class="pxa-wrap">
<div class="pxa-concl">
<div class="pxa-concl-l">
<h2 class="pxa-h2">Выводы по проекту</h2>
<p>Что сработало в «ОПТИ» и что мы переносим в проекты клиентов из ритейла, FMCG и сервиса.</p>
<a class="pxa-btn" href="#pxa-audit">Обсудить ваш проект</a>
</div>
<ol class="pxa-ol">
{chr(10).join(f'<li><span class="pxa-ol-n">{i:02d}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (t, d) in enumerate(concl, 1))}
</ol>
</div>
</div>
</section>"""

# ---------------- k06 more cases ----------------
css_k06 = """
.pxa-more-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;margin-top:36px}
.pxa-mc{position:relative;background:#fff;border-radius:24px;padding:32px;display:flex;flex-direction:column;gap:8px;border:1px solid transparent}
.pxa-mc:hover{border-color:#CFCBEF;box-shadow:0 16px 40px rgba(91,63,224,.12)}
.pxa-mc small{font-size:14px;color:#5A5F7D}
.pxa-mc h3{font-size:21px;line-height:1.25}
.pxa-mc a{text-decoration:none;color:inherit}
.pxa-mc a::after{content:"";position:absolute;top:0;right:0;bottom:0;left:0}
.pxa-mc:focus-within{outline:3px solid #2F6BFF;outline-offset:2px}
.pxa-mc a:focus-visible{outline:none}
.pxa-mc-fig{font-size:40px;line-height:1.1;margin-top:6px;color:var(--pxa-a)}
.pxa-mc p{color:var(--pxa-mute);font-size:16px}
.pxa-mc .pxa-go{margin-top:auto;padding-top:12px;font-weight:600;color:var(--pxa-a)}
@media (max-width:1000px){
.pxa-more-grid{grid-template-columns:1fr;gap:14px}
}
@media (max-width:860px){
.pxa-mc{padding:24px;border-radius:20px}
.pxa-mc-fig{font-size:34px}
}
"""
more = [
 ("Ресторан русской кухни", "Петров-Водкин", "+77%", "онлайн-бронирований за 3 месяца", "petrov-vodkin"),
 ("Отели в центре Санкт-Петербурга", "Невский берег", "", "Привлечение клиентов и снижение стоимости брони через performance-маркетинг, стратегию и digital.", "nevsky-bereg"),
 ("Энергетический напиток", "TARGET energy drink", "", "Запуск продукта. Репутационный маркетинг. SMM.", "target"),
]
def mc(m):
    l, n, f, d, s = m
    fig = f'<div class="pxa-big pxa-mc-fig">{f}</div>' if f else ""
    return f'<article class="pxa-mc"><small>{l}</small><h3><a href="/cases/{s}">{n}</a></h3>{fig}<p>{d}</p><span class="pxa-go" aria-hidden="true">Смотреть кейс →</span></article>'
html_k06 = f"""<section class="pxa pxa-sec pxa-tint" id="pxa-more">
<div class="pxa-wrap">
<h2 class="pxa-h2">Другие кейсы</h2>
<div class="pxa-more-grid">
{chr(10).join(mc(m) for m in more)}
</div>
<p style="margin-top:28px"><a class="pxa-more" href="/cases">Все кейсы →</a></p>
</div>
</section>"""

blocks = [
 ("k01-header-hero", "Шапка и первый экран", css_k01, html_k01),
 ("k02-kpi", "Выполненные KPI", css_k02, html_k02),
 ("k03-task-scope", "Задача и состав работ", css_k03, html_k03),
 ("k04-work", "Как мы это сделали", css_k04, html_k04),
 ("k05-conclusions", "Выводы", css_k05, html_k05),
 ("k06-more-cases", "Другие кейсы", css_k06, html_k06),
]
for fn, name, css, html in blocks:
    open(f"{OUT}/{fn}.html", "w", encoding="utf-8").write(wrap(fn[:3], name, css, html))

# reused blocks
for old, new in [("c04-audit-form.html", "k07-audit-form.html"), ("c05-footer.html", "k08-footer.html")]:
    t = open(f"{CASES}/{old}", encoding="utf-8").read()
    t = re.sub(r"<!-- Proxy Agency · страница «Кейсы» · блок c0\d · ", f"<!-- Proxy Agency · кейс «ОПТИ» · блок {new[:3]} · ", t, count=1)
    open(f"{OUT}/{new}", "w", encoding="utf-8").write(t)

for f in ["proxy-logo-mark.png", "proxy-logo-wordmark.png", "proxy-logo-full.png"]:
    shutil.copy(f"{ROOT}/logo-work/{f}", f"{OUT}/logo/{f}")

import glob
parts = [open(f, encoding="utf-8").read().replace("https://static.tildacdn.com/REPLACE-ME/", "logo/") for f in sorted(glob.glob(OUT + "/k0*.html"))]
open(OUT + "/preview.html", "w", encoding="utf-8").write('<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Превью: кейс ОПТИ</title><style>body{margin:0;background:#fff}</style></head><body>' + "\n".join(parts) + "</body></html>")
print(sorted(os.listdir(OUT)))
