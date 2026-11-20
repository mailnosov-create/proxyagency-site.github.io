import os, re, shutil, glob

ROOT = "/tmp/claude-0/-home-claude/4160dc96-70e4-507e-bf5d-2fe78152fe1f/scratchpad"
osrc = open(ROOT + "/gen/build_opti.py", encoding="utf-8").read()
pre = (osrc[:osrc.index("# ---------------- k01")]
       .replace('OUT = ROOT + "/tilda-opti"', 'OUT = ROOT + "/tilda-target"')
       .replace("кейс «ОПТИ»", "кейс TARGET"))
exec(pre)
css = {k: re.search(k + r' = (?:c01_css \+ )?"""(.*?)"""', osrc, re.S).group(1) for k in ["css_k01", "css_k02", "css_k03", "css_k04", "css_k05", "css_k06"]}
css["css_k01"] = c01_css + css["css_k01"]
MARK = "https://static.tildacdn.com/REPLACE-ME/proxy-logo-mark.png"
FN = '<p class="pxa-fn">* Запрещённый на территории России сервис.</p>'

# ---------------- k01 ----------------
html_k01 = f"""<section class="pxa pxa-hero" id="pxa-top">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Главная","item":"https://proxyagency.ru/"}},{{"@type":"ListItem","position":2,"name":"Кейсы","item":"https://proxyagency.ru/cases"}},{{"@type":"ListItem","position":3,"name":"TARGET energy drink","item":"https://proxyagency.ru/cases/target"}}]}}</script>
<div class="pxa-wrap">
{header}

<div class="pxa-hero-row" style="padding-bottom:64px">
<div class="pxa-hero-text">
<nav class="pxa-crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span><a href="/cases">Кейсы</a><span>/</span>TARGET energy drink</nav>
<p class="pxa-eyebrow">Кейс · Производство и FMCG · SMM</p>
<h1 class="pxa-h1 pxa-k-h1">TARGET energy drink: соцсети с нуля и 26 000+ подписчиков</h1>
<p class="pxa-lead">Создали все соцсети бренда энергетика, вели общение с аудиторией, проводили конкурсы и розыгрыши и нарастили сообщество во ВКонтакте, Instagram*, Telegram и MAX.</p>
<dl class="pxa-meta">
<div><dt>Клиент</dt><dd>TARGET — энергетический напиток от завода «Бочкари»</dd></div>
<div><dt>Услуги</dt><dd>SMM-стратегия, контент, таргет, комьюнити-менеджмент</dd></div>
<div><dt>Каналы</dt><dd>ВКонтакте, Instagram*, Telegram, MAX</dd></div>
<div><dt>Период</dt><dd>[добавить срок работы]</dd></div>
</dl>
<div class="pxa-cta-row">
<a class="pxa-btn" href="#pxa-audit">Хочу такой же результат</a>
<a class="pxa-btn-ghost" href="/cases">Все кейсы</a>
</div>
<p class="pxa-fn" style="margin-top:20px">* Запрещённый на территории России сервис.</p>
</div>
<div class="pxa-hero-art pxa-intro-art">
<img class="pxa-logo" src="{MARK}" alt="" aria-hidden="true">
</div>
</div>
</div>
</section>"""
css_k01 = css["css_k01"] + """
.pxa-fn{font-size:13px;color:#5A5F7D}
"""

# ---------------- k02 KPI ----------------
css_k02 = css["css_k02"] + """
.pxa-kpi-hero{grid-column:1 / -1;flex-direction:row;align-items:center;gap:40px;padding:36px 40px}
.pxa-kpi-hero .pxa-kpi-n{font-size:96px;margin:0;flex:none}
.pxa-kpi-hero .pxa-kpi-body{display:flex;flex-direction:column;gap:10px}
.pxa-kpi-hero .pxa-kpi-t{font-size:22px;line-height:1.35}
.pxa-kpi-n.pxa-word{font-size:30px;line-height:1.2;margin-top:6px}
.pxa-kpi-grid.pxa-g4{grid-template-columns:repeat(4,minmax(0,1fr));margin-top:20px}
.pxa-g4 .pxa-kpi-n{font-size:42px}
.pxa-kpi-grid.pxa-g2{grid-template-columns:repeat(2,minmax(0,1fr));margin-top:20px}
.pxa-fn-d{margin-top:12px;font-size:14px;color:#B9B5E6}
@media (max-width:1000px){
.pxa-kpi-grid.pxa-g4{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:860px){
.pxa-kpi-hero{flex-direction:column;align-items:flex-start;gap:10px;padding:22px}
.pxa-kpi-hero .pxa-kpi-n{font-size:56px}
.pxa-kpi-hero .pxa-kpi-t{font-size:17px}
.pxa-kpi-grid.pxa-g4,.pxa-kpi-grid.pxa-g2{grid-template-columns:1fr;gap:14px;margin-top:14px}
.pxa-g4 .pxa-kpi-n{font-size:40px}
.pxa-kpi-n.pxa-word{font-size:28px}
}
"""
done_badge = f'<span class="pxa-badge">{CHECK}KPI выполнен</span>'
scale_badge = '<span class="pxa-badge pxa-scale">Масштаб проекта</span>'
ch = [
 ("13 000+", "подписчиков ВКонтакте", "Сообщество с нуля"),
 ("10 000+", "подписчиков в Instagram*", "Аккаунт с нуля"),
 ("1 700+", "подписчиков в MAX", "Канал с августа 2026 года"),
 ("1 400+", "подписчиков в Telegram", "Канал с нуля"),
]
tile = lambda n, t, s: f'<li class="pxa-kpi pxa-done">{done_badge}<div class="pxa-kpi-n">{n}</div><p class="pxa-kpi-t">{t}</p><p class="pxa-kpi-src">{s}</p></li>'
html_k02 = f"""<section class="pxa pxa-sec pxa-dark pxa-kpis" id="pxa-kpi">
<div class="pxa-wrap">
<h2 class="pxa-h2">Результаты в цифрах</h2>
<p class="pxa-kpi-sub">Аудитория бренда, которую мы построили с нуля.</p>
<ul class="pxa-kpi-grid" style="list-style:none;margin:44px 0 0;padding:0">
<li class="pxa-kpi pxa-done pxa-kpi-hero"><div class="pxa-kpi-n">26 000+</div><div class="pxa-kpi-body">{done_badge}<p class="pxa-kpi-t">подписчиков в четырёх соцсетях бренда</p><p class="pxa-kpi-src">ВКонтакте, Instagram*, Telegram и MAX: все площадки созданы с нуля</p></div></li>
</ul>
<ul class="pxa-kpi-grid pxa-g4" style="list-style:none;padding:0">
{chr(10).join(tile(*c) for c in ch)}
</ul>
<ul class="pxa-kpi-grid pxa-g2" style="list-style:none;padding:0">
<li class="pxa-kpi">{scale_badge}<div class="pxa-kpi-n pxa-word">Вся Россия</div><p class="pxa-kpi-t">компания клиента расширила присутствие продукта по всей стране</p></li>
<li class="pxa-kpi">{scale_badge}<div class="pxa-kpi-n pxa-word">Рынок СНГ</div><p class="pxa-kpi-t">продукт выведен на рынок стран СНГ</p></li>
</ul>
<p class="pxa-kpi-note">Охваты, вовлечённость, число участников конкурсов, плановые значения KPI: [добавить, если можно раскрыть клиенту]</p>
<p class="pxa-fn-d">* Запрещённый на территории России сервис.</p>
</div>
</section>"""

# ---------------- k03 ----------------
tasks = [
 "Расширить географию присутствия бренда",
 "Стимулировать спрос на продукт",
 "Сделать бренд узнаваемым",
 "Построить с нуля сообщество в соцсетях",
]
scope = [
 "Стратегия продвижения в соцсетях",
 "Создание аккаунтов и уникального контента",
 "Таргетированная реклама в Instagram* и ВКонтакте",
 "Telegram-канал и канал в MAX",
 "Конкурсы и розыгрыши",
 "Повышение активности аудитории",
 "Комьюнити-менеджмент, работа с негативом",
]
li = lambda items: "\n".join(f"<li>{CHECK}<span>{t}</span></li>" for t in items)
html_k03 = f"""<section class="pxa pxa-sec" id="pxa-task">
<div class="pxa-wrap">
<h2 class="pxa-h2">Задача и что вошло в работу</h2>
<div class="pxa-two">
<div class="pxa-panel">
<h3>Клиент и задачи</h3>
<p>TARGET — бренд энергетического напитка от завода «Бочкари» для тех, кто хочет успевать больше и достигать большего.</p>
<ul class="pxa-list">
{li(tasks)}
</ul>
</div>
<div class="pxa-panel">
<h3>Что сделали</h3>
<p>Выстроили присутствие бренда в соцсетях: от стратегии до ежедневного общения с аудиторией.</p>
<ul class="pxa-list">
{li(scope)}
</ul>
</div>
</div>
<p class="pxa-fn" style="margin-top:20px">* Запрещённый на территории России сервис.</p>
</div>
</section>"""

# ---------------- k04 ----------------
steps = [
 ("Стратегия и запуск соцсетей", "Разработали стратегию продвижения, создали аккаунты бренда с нуля и подготовили уникальный контент.", "Все соцсети созданы с нуля", False),
 ("ВКонтакте", "Развивали сообщество: контент, таргетированная реклама, общение с подписчиками и работа с негативом.", "13 000+ подписчиков", False),
 ("Instagram*", "Запустили аккаунт, вели контент и таргетированную рекламу, привлекали аудиторию конкурсами и розыгрышами.", "10 000+ подписчиков", False),
 ("Telegram-канал", "Создали канал бренда и нарастили аудиторию.", "1 400+ подписчиков", False),
 ("Канал в MAX", "Запустили канал бренда в мессенджере MAX.", "1 700+ подписчиков с августа 2026", False),
 ("Конкурсы и общение", "Проводили конкурсы и розыгрыши, вели коммуникацию с подписчиками, повышали активность аудитории.", "[добавить: число участников, охваты]", True),
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
<div class="pxa-gallery">[Галерея: банки TARGET, посты и креативы, механики конкурсов, скриншоты сообществ]</div>
<p class="pxa-fn" style="margin-top:20px">* Запрещённый на территории России сервис.</p>
</div>
</section>"""

# ---------------- k05 ----------------
concl = [
 ("Бренд с нуля строим сразу во всех каналах аудитории", "ВКонтакте, Instagram*, Telegram и MAX вместе дали 26 000+ подписчиков. Каждая площадка собирает свою часть аудитории и усиливает остальные."),
 ("Новые площадки — новые точки роста", "Канал в MAX с августа 2026 года уже собрал 1 700+ подписчиков. Выходить на новые платформы лучше раньше конкурентов."),
 ("Конкурсы привлекают, общение удерживает", "Розыгрыши дают приток аудитории, а комьюнити-менеджмент и работа с негативом превращают подписчиков в сообщество бренда."),
 ("Соцсети работают на узнаваемость и спрос", "Стратегия, контент и таргет в связке поддерживали рост бренда: за время сотрудничества компания расширила присутствие по России и вышла на рынок СНГ."),
]
html_k05 = f"""<section class="pxa pxa-sec" id="pxa-takeaways">
<div class="pxa-wrap">
<div class="pxa-concl">
<div class="pxa-concl-l">
<h2 class="pxa-h2">Выводы по проекту</h2>
<p>Что сработало в TARGET и что мы переносим в проекты производителей, FMCG-брендов и розничных сетей.</p>
<a class="pxa-btn" href="#pxa-audit">Обсудить ваш проект</a>
</div>
<ol class="pxa-ol">
{chr(10).join(f'<li><span class="pxa-ol-n">{i:02d}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (t, d) in enumerate(concl, 1))}
</ol>
</div>
<p class="pxa-fn" style="margin-top:28px">* Запрещённый на территории России сервис.</p>
</div>
</section>"""

# ---------------- k06 ----------------
more = [
 ("Пивоваренный завод", "Бочкари", "", "", "bochkari"),
 ("Сеть АЗС, партнёр «Газпром нефти»", "ОПТИ", "", "", "opti"),
 ("Производитель травяных кормов", "Alfa Feeds", "", "", "alfafeeds"),
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
 ("k01-header-hero", "Шапка и первый экран", css_k01, html_k01),
 ("k02-kpi", "Результаты и KPI", css_k02, html_k02),
 ("k03-task-scope", "Задача и состав работ", css["css_k03"], html_k03),
 ("k04-work", "Как мы это сделали", css["css_k04"], html_k04),
 ("k05-conclusions", "Выводы", css["css_k05"], html_k05),
 ("k06-more-cases", "Другие кейсы", css["css_k06"], html_k06),
]
OUT = ROOT + "/tilda-target"
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT + "/logo")
for fn, name, c, h in blocks:
    open(f"{OUT}/{fn}.html", "w", encoding="utf-8").write(wrap(fn[:3], name, c, h))
for old, new in [("c04-audit-form.html", "k07-audit-form.html"), ("c05-footer.html", "k08-footer.html")]:
    t = open(f"{CASES}/{old}", encoding="utf-8").read()
    t = re.sub(r"<!-- Proxy Agency · страница «Кейсы» · блок c0\d · ", f"<!-- Proxy Agency · кейс TARGET · блок {new[:3]} · ", t, count=1)
    open(f"{OUT}/{new}", "w", encoding="utf-8").write(t)
for f in ["proxy-logo-mark.png", "proxy-logo-wordmark.png", "proxy-logo-full.png"]:
    shutil.copy(f"{ROOT}/logo-work/{f}", f"{OUT}/logo/{f}")
parts = [open(f, encoding="utf-8").read().replace("https://static.tildacdn.com/REPLACE-ME/", "logo/") for f in sorted(glob.glob(OUT + "/k0*.html"))]
open(OUT + "/preview.html", "w", encoding="utf-8").write('<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Превью: кейс TARGET</title><style>body{margin:0;background:#fff}</style></head><body>' + "\n".join(parts) + "</body></html>")
print(sorted(os.listdir(OUT)))
