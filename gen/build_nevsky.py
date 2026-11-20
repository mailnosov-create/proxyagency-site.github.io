import os, re, shutil, glob

ROOT = "/tmp/claude-0/-home-claude/4160dc96-70e4-507e-bf5d-2fe78152fe1f/scratchpad"
OUT = ROOT + "/tilda-nevsky"
osrc = open(ROOT + "/gen/build_opti.py", encoding="utf-8").read()

# reuse setup (BASE, FONTS, header, wrap, CHECK) and CSS from the OPTI build
pre = osrc[:osrc.index("# ---------------- k01")].replace('OUT = ROOT + "/tilda-opti"', 'OUT = ROOT + "/tilda-nevsky"').replace("кейс «ОПТИ»", "кейс «Невский берег»")
exec(pre)
css = {k: re.search(k + r' = (?:c01_css \+ )?"""(.*?)"""', osrc, re.S).group(1) for k in ["css_k01", "css_k02", "css_k03", "css_k04", "css_k05", "css_k06"]}
css["css_k01"] = c01_css + css["css_k01"]
wrap_src = None

MARK = "https://static.tildacdn.com/REPLACE-ME/proxy-logo-mark.png"

# ---------------- k01 ----------------
html_k01 = f"""<section class="pxa pxa-hero" id="pxa-top">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Главная","item":"https://proxyagency.ru/"}},{{"@type":"ListItem","position":2,"name":"Кейсы","item":"https://proxyagency.ru/cases"}},{{"@type":"ListItem","position":3,"name":"Невский берег","item":"https://proxyagency.ru/cases/nevsky-bereg"}}]}}</script>
<div class="pxa-wrap">
{header}

<div class="pxa-hero-row" style="padding-bottom:64px">
<div class="pxa-hero-text">
<nav class="pxa-crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span><a href="/cases">Кейсы</a><span>/</span>Невский берег</nav>
<p class="pxa-eyebrow">Кейс · Отели · Санкт-Петербург</p>
<h1 class="pxa-h1 pxa-k-h1">Отель «Невский берег»: рост доходности на 12,3% после редизайна сайта и запуска рекламы</h1>
<p class="pxa-lead">Обновили сайт без потери трафика и позиций в поиске, продвинули его в Яндексе и Google и запустили контекстную рекламу со сквозной аналитикой.</p>
<dl class="pxa-meta">
<div><dt>Клиент</dt><dd>Мини-отель «Невский берег» в двух исторических зданиях на Невском проспекте</dd></div>
<div><dt>Услуги</dt><dd>Редизайн сайта, SEO, контекстная реклама</dd></div>
<div><dt>Каналы</dt><dd>Яндекс и Google: поиск и контекст</dd></div>
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
css_k02 = css["css_k02"] + """
.pxa-kpi-hero{grid-column:1 / -1;flex-direction:row;align-items:center;gap:40px;padding:36px 40px}
.pxa-kpi-hero .pxa-kpi-n{font-size:96px;margin:0;flex:none}
.pxa-kpi-hero .pxa-kpi-body{display:flex;flex-direction:column;gap:10px}
.pxa-kpi-hero .pxa-kpi-t{font-size:22px;line-height:1.35}
.pxa-kpi-n.pxa-word{font-size:30px;line-height:1.2;margin-top:6px}
.pxa-kpi-open{border-style:dashed;background:transparent}
.pxa-kpi-open .pxa-kpi-t{color:#B9B5E6}
@media (max-width:860px){
.pxa-kpi-hero{flex-direction:column;align-items:flex-start;gap:10px;padding:22px}
.pxa-kpi-hero .pxa-kpi-n{font-size:56px}
.pxa-kpi-hero .pxa-kpi-t{font-size:17px}
.pxa-kpi-n.pxa-word{font-size:24px}
}
"""
done_badge = f'<span class="pxa-badge">{CHECK}KPI выполнен</span>'
task_badge = f'<span class="pxa-badge">{CHECK}Задача выполнена</span>'
html_k02 = f"""<section class="pxa pxa-sec pxa-dark pxa-kpis" id="pxa-kpi">
<div class="pxa-wrap">
<h2 class="pxa-h2">Результаты проекта</h2>
<p class="pxa-kpi-sub">Что получил отель по ключевым показателям.</p>
<ul class="pxa-kpi-grid" style="list-style:none;margin:44px 0 0;padding:0">
<li class="pxa-kpi pxa-done pxa-kpi-hero"><div class="pxa-kpi-n">+12,3%</div><div class="pxa-kpi-body">{done_badge}<p class="pxa-kpi-t">рост доходности отеля</p><p class="pxa-kpi-src">Итог работы по сайту, SEO и контекстной рекламе</p></div></li>
<li class="pxa-kpi pxa-done">{task_badge}<div class="pxa-kpi-n pxa-word">Трафик сохранён</div><p class="pxa-kpi-t">объёмы трафика и позиции в поиске после полного редизайна сайта</p><p class="pxa-kpi-src">Разработка и редизайн сайта</p></li>
<li class="pxa-kpi pxa-done">{task_badge}<div class="pxa-kpi-n pxa-word">Рост из поиска</div><p class="pxa-kpi-t">больше трафика из Яндекса и Google, лучше юзабилити сайта</p><p class="pxa-kpi-src">SEO-продвижение</p></li>
<li class="pxa-kpi pxa-done">{task_badge}<div class="pxa-kpi-n pxa-word">Заявки под контролем</div><p class="pxa-kpi-t">сквозная аналитика, конверсионные формы, лидогенерация</p><p class="pxa-kpi-src">Контекстная реклама</p></li>
</ul>
<p class="pxa-kpi-note">Цифры по трафику, броням и стоимости заявки, плановые значения KPI: [добавить, если можно раскрыть клиенту]</p>
</div>
</section>"""

# ---------------- k03 ----------------
tasks = [
 "Привлекать новых клиентов отеля через интернет",
 "Сохранить объёмы трафика и позиции в поиске при полном редизайне сайта",
 "Вырастить трафик из Яндекса и Google",
 "Наладить лидогенерацию и сквозную аналитику",
]
scope = [
 "Разработка и редизайн сайта",
 "SEO-продвижение и улучшение юзабилити",
 "Запуск и ведение контекстной рекламы",
 "Построение сквозной аналитики",
 "Конверсионные формы и лидогенерация",
]
li = lambda items: "\n".join(f"<li>{CHECK}<span>{t}</span></li>" for t in items)
html_k03 = f"""<section class="pxa pxa-sec" id="pxa-task">
<div class="pxa-wrap">
<h2 class="pxa-h2">Задача и что вошло в работу</h2>
<div class="pxa-two">
<div class="pxa-panel">
<h3>Клиент и задачи</h3>
<p>«Невский берег» — мини-отель в двух исторических зданиях на Невском проспекте в Санкт-Петербурге.</p>
<ul class="pxa-list">
{li(tasks)}
</ul>
</div>
<div class="pxa-panel">
<h3>Что сделали</h3>
<p>Сайт, поисковое продвижение и реклама в одной связке: от редизайна до заявок.</p>
<ul class="pxa-list">
{li(scope)}
</ul>
</div>
</div>
</div>
</section>"""

# ---------------- k04 ----------------
steps = [
 ("Разработка и редизайн сайта", "Полностью обновили сайт отеля и сохранили объёмы трафика и позиции в поисковых системах после редизайна.", "Трафик и позиции сохранены", False),
 ("SEO-продвижение", "Улучшили юзабилити сайта и вырастили трафик из поисковых систем Яндекс и Google.", "Рост трафика из поиска", False),
 ("Контекстная реклама", "Запустили и вели контекстную рекламу: построили сквозную аналитику, создали конверсионные формы, настроили лидогенерацию.", "[добавить: брони, стоимость заявки]", True),
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
<div class="pxa-gallery">[Галерея: скриншоты нового сайта, до и после, дашборд сквозной аналитики, фото отеля]</div>
</div>
</section>"""

# ---------------- k05 ----------------
concl = [
 ("Редизайн без потери трафика — задача SEO с первого дня", "Требования поиска учитывали при разработке нового сайта, поэтому после полного редизайна объёмы трафика и позиции в поиске сохранились."),
 ("Сайт, SEO и реклама работают как одна система", "Новый сайт, продвижение в поиске и контекст опираются на общие формы и аналитику, а не на разрозненные решения разных подрядчиков."),
 ("Сквозная аналитика делает результат управляемым", "Видно, какие каналы приводят заявки и доходность, и бюджет можно перераспределять под результат: +12,3% к доходности."),
 ("Юзабилити — часть продвижения", "Улучшения сайта работают на рост трафика из Яндекса и Google: удобный сайт лучше принимает и удерживает поисковую аудиторию."),
]
html_k05 = f"""<section class="pxa pxa-sec" id="pxa-takeaways">
<div class="pxa-wrap">
<div class="pxa-concl">
<div class="pxa-concl-l">
<h2 class="pxa-h2">Выводы по проекту</h2>
<p>Что сработало в «Невском береге» и что мы переносим в проекты отелей, санаториев и сервисных компаний.</p>
<a class="pxa-btn" href="#pxa-audit">Обсудить ваш проект</a>
</div>
<ol class="pxa-ol">
{chr(10).join(f'<li><span class="pxa-ol-n">{i:02d}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (t, d) in enumerate(concl, 1))}
</ol>
</div>
</div>
</section>"""

# ---------------- k06 ----------------
more = [
 ("Ресторан русской кухни", "Петров-Водкин", "+77%", "онлайн-бронирований за 3 месяца", "petrov-vodkin"),
 ("Санаторий в Белокурихе", "Алтайский замок", "", "", "altay-zamok"),
 ("Лечебно-оздоровительный комплекс", "Санаторий Центросоюза РФ", "", "", "centrosouz"),
]
def mc(m):
    l, n, f, d, s = m
    fig = f'<div class="pxa-big pxa-mc-fig">{f}</div>' if f else ""
    p = f"<p>{d}</p>" if d else ""
    return f'<article class="pxa-mc"><small>{l}</small><h3><a href="/cases/{s}">{n}</a></h3>{fig}{p}<span class="pxa-go" aria-hidden="true">Смотреть кейс →</span></article>'
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
 ("k01-header-hero", "Шапка и первый экран", css["css_k01"], html_k01),
 ("k02-kpi", "Результаты и KPI", css_k02, html_k02),
 ("k03-task-scope", "Задача и состав работ", css["css_k03"], html_k03),
 ("k04-work", "Как мы это сделали", css["css_k04"], html_k04),
 ("k05-conclusions", "Выводы", css["css_k05"], html_k05),
 ("k06-more-cases", "Другие кейсы", css["css_k06"], html_k06),
]
for fn, name, c, h in blocks:
    open(f"{OUT}/{fn}.html", "w", encoding="utf-8").write(wrap(fn[:3], name, c, h))

for old, new in [("c04-audit-form.html", "k07-audit-form.html"), ("c05-footer.html", "k08-footer.html")]:
    t = open(f"{CASES}/{old}", encoding="utf-8").read()
    t = re.sub(r"<!-- Proxy Agency · страница «Кейсы» · блок c0\d · ", f"<!-- Proxy Agency · кейс «Невский берег» · блок {new[:3]} · ", t, count=1)
    open(f"{OUT}/{new}", "w", encoding="utf-8").write(t)
for f in ["proxy-logo-mark.png", "proxy-logo-wordmark.png", "proxy-logo-full.png"]:
    shutil.copy(f"{ROOT}/logo-work/{f}", f"{OUT}/logo/{f}")
parts = [open(f, encoding="utf-8").read().replace("https://static.tildacdn.com/REPLACE-ME/", "logo/") for f in sorted(glob.glob(OUT + "/k0*.html"))]
open(OUT + "/preview.html", "w", encoding="utf-8").write('<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Превью: кейс Невский берег</title><style>body{margin:0;background:#fff}</style></head><body>' + "\n".join(parts) + "</body></html>")
print(sorted(os.listdir(OUT)))
