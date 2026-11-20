import os, re, shutil, zipfile

ROOT = "/tmp/claude-0/-home-claude/4160dc96-70e4-507e-bf5d-2fe78152fe1f/scratchpad"
HOME = ROOT + "/tilda-blocks"
OUT = ROOT + "/tilda-cases"
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT + "/logo")

src = open(ROOT + "/gen/build.py", encoding="utf-8").read()
BASE = re.search(r'BASE = """(.*?)"""', src, re.S).group(1)
CSS01 = re.search(r'css01 = """(.*?)"""', src, re.S).group(1)
FONTS = re.search(r"FONTS = '(.*?)'", src).group(1)
MARK = "https://static.tildacdn.com/REPLACE-ME/proxy-logo-mark.png"
WORD = "https://static.tildacdn.com/REPLACE-ME/proxy-logo-wordmark.png"

def wrap(num, name, css, html):
    return (f"<!-- Proxy Agency · страница «Кейсы» · блок {num} · {name} -->\n"
            "<!-- Вставка: Tilda → «Другое» → T123 «HTML-код». Вставлять целиком, вместе с <style>. -->\n"
            + FONTS + "\n<style>" + BASE + css + "</style>\n" + html + "\n")

# ---------- c01 header + intro ----------
css_c01 = CSS01 + """
.pxa-crumbs{margin:0 0 20px;font-size:14px;color:#5A5F7D}
.pxa-crumbs a{text-decoration:none;color:#5A5F7D}
.pxa-crumbs a:hover{color:var(--pxa-a)}
.pxa-crumbs span{margin:0 6px}
.pxa-chips{display:flex;flex-wrap:wrap;gap:10px;margin-top:32px;max-width:620px}
.pxa-chip{padding:8px 14px;border-radius:999px;background:#fff;border:1px solid var(--pxa-line);font-size:14px;font-weight:500;color:#3B3F63}
.pxa-intro-art img{max-width:400px}
.pxa-nav a[aria-current="page"]{color:var(--pxa-a);font-weight:600}
@media (max-width:860px){
.pxa-intro-art{display:none}
.pxa-chips{margin-top:24px}
.pxa-chip{font-size:13px;padding:6px 12px}
}
"""
chips = ["лидогенерация","контекстная реклама","таргетированная реклама","SEO","аналитика","SMM","брендинг","продвижение франшиз","репутационный маркетинг","запуск продукта","увеличение продаж","снижение CPL / CAC"]
chips_html = "\n".join(f'<span class="pxa-chip">{c}</span>' for c in chips)
html_c01 = f"""<section class="pxa pxa-hero" id="pxa-top">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{{"@type":"ListItem","position":1,"name":"Главная","item":"https://proxyagency.ru/"}},{{"@type":"ListItem","position":2,"name":"Кейсы","item":"https://proxyagency.ru/cases"}}]}}</script>
<div class="pxa-wrap">
<header class="pxa-head">
<a class="pxa-brand" href="/" aria-label="Proxy Creative Agency — на главную">
<img class="pxa-logo" src="{MARK}" alt="">
<img class="pxa-logo pxa-word" src="{WORD}" alt="Proxy creative agency">
</a>
<nav class="pxa-nav" aria-label="Основное меню">
<a href="/services">Услуги</a>
<a href="/cases" aria-current="page">Кейсы</a>
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

<div class="pxa-hero-row" style="padding-bottom:56px">
<div class="pxa-hero-text">
<nav class="pxa-crumbs" aria-label="Хлебные крошки"><a href="/">Главная</a><span>/</span>Кейсы</nav>
<h1 class="pxa-h1">Кейсы Proxy Agency: результаты в цифрах</h1>
<p class="pxa-lead">Увеличиваем продажи в интернете: делаем сайты, занимаемся SEO и запускаем эффективный трафик. Посмотрите, что получилось у наших клиентов.</p>
<div class="pxa-chips">
{chips_html}
</div>
</div>
<div class="pxa-hero-art pxa-intro-art">
<img class="pxa-logo" src="{MARK}" alt="" aria-hidden="true">
</div>
</div>
</div>
</section>"""

# ---------- c02 cases grid ----------
cases = [
 # name, label, industry key, figure, figure text, desc, slug
 ("Петров-Водкин","Ресторан русской кухни","rest","+77%","онлайн-бронирований за 3 месяца","Performance-реклама и локальные digital-каналы.","petrov-vodkin"),
 ("ОПТИ","Сеть АЗС, партнёр «Газпром нефти»","retail","+38%","регистраций в программе лояльности за 4 месяца","Performance-маркетинг и продвижение программы лояльности.","opti"),
  ("Le Grand", "Ресторан в Калифорнии", "rest", "В разы", "рост выручки год к году", "Реклама на нескольких языках, блогеры Лос-Анджелеса, овербукинг в акционные дни.", "legrand"),
 ("TARGET energy drink","Энергетический напиток","prod",None,None,"Запуск продукта. Репутационный маркетинг. SMM.","target"),
  ("La Perla", "Ресторан морской кухни", "rest", "500%+", "рост броней столиков в отдельных акциях", "Работа с рестораном и информационная поддержка новых открытий.", "la-perla"),
  ("Бочкари", "Пивоваренный завод", "prod", None, None, "Промо нового бренда безалкогольного пива Weissberg: узнаваемость, охваты, вовлечённость.", "bochkari"),
  ("Маzай", "Бренд пива", "prod", None, None, "Соцсети с нуля, персонаж-амбассадор и нативная реклама пива.", "mazay"),
  ("Алтайский замок", "Санаторий в Белокурихе", "hotel", None, None, "Контекст, карты, розыгрыши, таргет и SMM для санатория в Белокурихе.", "altay-zamok"),
  ("Санаторий Центросоюза РФ", "Лечебно-оздоровительный комплекс", "hotel", "+18%", "выручки от путёвок год к году", "Контекстная, таргетированная и CPA-реклама, 2016–2022.", "centrosouz"),
 ("Невский берег","Отели в центре Санкт-Петербурга","hotel",None,None,"Привлечение клиентов и снижение стоимости брони через performance-маркетинг, стратегию и digital.","nevsky-bereg"),
  ("Клиника им. Н. И. Пирогова", "Многопрофильное медицинское учреждение", "med", "+158%", "запросов от пациентов год к году", "Создание сайта, SEO и контекстная реклама. Пациенты со всей России.", "klinika-pirogova"),
  ("Alfa Feeds", "Производитель травяных кормов", "prod", "3 страны", "заказчики из ОАЭ, РФ и Казахстана", "Интернет-образ с нуля, контекст и SEO для B2B-аудитории агросектора.", "alfafeeds"),
]
inds = [("all","Все"),("rest","Рестораны"),("hotel","Отели и санатории"),("med","Медицина"),("prod","Производство и FMCG"),("retail","АЗС и розница")]
count = {k: sum(1 for c in cases if c[2]==k) for k,_ in inds}
count["all"] = len(cases)

covers = ["linear-gradient(135deg,#E4DCFF,#D2EEFF)","linear-gradient(135deg,#D2EEFF,#E4DCFF)","linear-gradient(135deg,#EFEBFF,#CFE9FF)"]
def card(i, c):
    name,label,ind,fig,figtxt,desc,slug = c
    colors = ["var(--pxa-a)","var(--pxa-b)"]
    res = ""
    if fig:
        res = f'<div class="pxa-big pxa-fig" style="color:{colors[i%2]}">{fig}</div><p class="pxa-strong">{figtxt}</p>'
    else:
        res = '<p class="pxa-strong">Плановые KPI выполнены</p>'
    d = f'<p class="pxa-desc">{desc}</p>' if desc else '<p class="pxa-desc pxa-ph">[Задача и что сделали — 1–2 предложения]</p>'
    return f'''<article class="pxa-case" data-ind="{ind}">
<div class="pxa-cover" style="background:{covers[i%3]}">{name}</div>
<div class="pxa-case-b">
<small>{label}</small>
<h3><a class="pxa-case-a" href="/cases/{slug}">{name}</a></h3>
{res}
{d}
<span class="pxa-go" aria-hidden="true">Смотреть кейс →</span>
</div>
</article>'''

css_c02 = """
.pxa.pxa-cases{background:var(--pxa-tint)}
.pxa-filters{display:flex;flex-wrap:wrap;gap:10px}
.pxa-filter{font-family:inherit;font-size:15px;font-weight:600;padding:10px 18px;border-radius:999px;border:1px solid #CFCBEF;background:#fff;color:var(--pxa-ink);cursor:pointer;line-height:1.2}
.pxa-filter span{font-weight:400;opacity:.75;margin-left:6px}
.pxa-filter[aria-pressed="true"]{background:linear-gradient(135deg,var(--pxa-a),var(--pxa-b));color:#fff;border-color:transparent}
.pxa-count{margin-top:20px;font-size:14px;color:#5A5F7D}
.pxa-case-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;margin-top:24px}
.pxa-case{position:relative;background:#fff;border-radius:24px;overflow:hidden;display:flex;flex-direction:column;border:1px solid transparent}
.pxa-case[hidden]{display:none}
.pxa-case:hover{border-color:#CFCBEF;box-shadow:0 16px 40px rgba(91,63,224,.12)}
.pxa-cover{height:190px;display:flex;align-items:center;justify-content:center;color:#3B3F63;font-size:14px}
.pxa-case-b{padding:28px;display:flex;flex-direction:column;gap:8px;flex:1}
.pxa-case-b small{font-size:14px;color:#5A5F7D}
.pxa-case-b h3{font-size:21px;line-height:1.25}
.pxa-case-a{text-decoration:none;color:inherit}
.pxa-case-a::after{content:"";position:absolute;top:0;right:0;bottom:0;left:0}
.pxa-case-a:focus-visible{outline:none}
.pxa-case:focus-within{outline:3px solid #2F6BFF;outline-offset:2px}
.pxa-fig{font-size:44px;line-height:1.1;margin-top:8px}
.pxa-strong{font-weight:500}
.pxa-desc{margin-top:4px;color:var(--pxa-mute);font-size:16px}
.pxa-ph{color:#5A5F7D;font-size:15px;margin-top:8px}
.pxa-go{margin-top:auto;padding-top:12px;font-weight:600;color:var(--pxa-a)}
@media (max-width:1100px){
.pxa-case-grid{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:860px){
.pxa-filters{flex-wrap:nowrap;overflow-x:auto;margin-right:-20px;padding:2px 20px 6px 0;-webkit-overflow-scrolling:touch}
.pxa-filter{flex:none;font-size:14px;padding:9px 16px}
.pxa-case-grid{grid-template-columns:1fr;gap:16px}
.pxa-cover{display:none}
.pxa-case{border-radius:20px}
.pxa-case-b{padding:24px}
.pxa-fig{font-size:36px}
.pxa-desc{font-size:15px}
}
"""
btns = "\n".join(f'<button class="pxa-filter" type="button" data-k="{k}" aria-pressed="{"true" if k=="all" else "false"}">{t}<span>{count[k]}</span></button>' for k,t in inds)
cards_html = "\n".join(card(i,c) for i,c in enumerate(cases))
html_c02 = f"""<section class="pxa pxa-sec pxa-cases" id="pxa-cases">
<div class="pxa-wrap">
<div class="pxa-filters" role="group" aria-label="Фильтр кейсов по отрасли">
{btns}
</div>
<p class="pxa-count" aria-live="polite">Показано кейсов: {len(cases)}</p>
<div class="pxa-case-grid">
{cards_html}
</div>
</div>
<script>
(function(){{
var root=document.getElementById('pxa-cases');if(!root)return;
var btns=root.querySelectorAll('.pxa-filter'),cards=root.querySelectorAll('.pxa-case'),cnt=root.querySelector('.pxa-count');
function apply(k){{
var n=0;
cards.forEach(function(c){{var show=(k==='all'||c.getAttribute('data-ind')===k);c.hidden=!show;if(show){{n++;}}}});
cnt.textContent='Показано кейсов: '+n;
btns.forEach(function(b){{b.setAttribute('aria-pressed',b.getAttribute('data-k')===k?'true':'false');}});
}}
btns.forEach(function(b){{b.addEventListener('click',function(){{apply(b.getAttribute('data-k'));}});}});
}})();
</script>
</section>"""

files = [("c01-header-intro","Шапка и вводный экран",css_c01,html_c01),
         ("c02-cases","Фильтры и кейсы",css_c02,html_c02)]
for i,(fn,name,css,html) in enumerate(files,1):
    open(f"{OUT}/{fn}.html","w",encoding="utf-8").write(wrap(f"c0{i}",name,css,html))

# reused blocks from the home page (same files, renamed)
for old,new,title in [("02-stats.html","c03-stats.html","Цифры"),("08-audit-form.html","c04-audit-form.html","Экспресс-аудит (форма)"),("10-footer.html","c05-footer.html","Подвал и контакты")]:
    t = open(f"{HOME}/{old}",encoding="utf-8").read()
    t = re.sub(r"<!-- Proxy Agency · блок \d+ · ", "<!-- Proxy Agency · страница «Кейсы» · блок "+new[:3]+" · ", t, count=1)
    if new.startswith("c04"):
        a = "Бесплатный экспресс-аудит рекламы и сайта"; b = "Покажем, где теряются заявки, за [2] рабочих дня. Срок подтвердим перед запуском сайта."
        assert a in t and b in t
        t = t.replace(a, "Хотите такой же результат?").replace(b, "Расскажите о своей задаче. Начнём с бесплатного экспресс-аудита: покажем, где теряются заявки, за [2] рабочих дня.")
    open(f"{OUT}/{new}","w",encoding="utf-8").write(t)

for f in ["proxy-logo-mark.png","proxy-logo-wordmark.png","proxy-logo-full.png"]:
    shutil.copy(f"{ROOT}/logo-work/{f}", f"{OUT}/logo/{f}")

# preview
import glob
parts=[open(f,encoding="utf-8").read().replace("https://static.tildacdn.com/REPLACE-ME/","logo/") for f in sorted(glob.glob(OUT+"/c0*.html"))]
open(OUT+"/preview.html","w",encoding="utf-8").write('<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Превью страницы «Кейсы»</title><style>body{margin:0;background:#fff}</style></head><body>'+"\n".join(parts)+"</body></html>")
print("ok", os.listdir(OUT))
