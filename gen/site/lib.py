import re, os, io, base64, glob, html as _html
from PIL import Image

ROOT = "/tmp/claude-0/-home-claude/4160dc96-70e4-507e-bf5d-2fe78152fe1f/scratchpad"
SITE = "https://proxyagency.ru"
TODAY = "2026-11-20"

bsrc = open(ROOT + "/gen/build.py", encoding="utf-8").read()
BASE = re.search(r'BASE = """(.*?)"""', bsrc, re.S).group(1)
FONTS = re.search(r"FONTS = '(.*?)'", bsrc).group(1)

# ---------- logos ----------
def _webp(name, w, q):
    im = Image.open(f"{ROOT}/logo-work/proxy-logo-{name}.png").convert("RGBA")
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "WEBP", quality=q, method=6)
    return b.getvalue()
LOGOS = {
    "logo-mark-s.webp": _webp("mark", 100, 78),
    "logo-wordmark.webp": _webp("wordmark", 170, 78),
    "logo-mark-l.webp": _webp("mark", 440, 70),
    "logo-full.webp": _webp("full", 300, 72),
}
def _uri(d): return "data:image/webp;base64," + base64.b64encode(d).decode()
URI2PATH = {_uri(v): "/assets/img/" + k for k, v in LOGOS.items()}
def uris_to_paths(t):
    for u, p in URI2PATH.items(): t = t.replace(u, p)
    return t

# ---------- block helpers ----------
def block_css(f):
    t = re.sub(r"<!--.*?-->", "", open(f, encoding="utf-8").read(), flags=re.S)
    return t[t.index("<style>") + 7: t.index("</style>")]
def block_body(f):
    t = re.sub(r"<!--.*?-->", "", open(f, encoding="utf-8").read(), flags=re.S)
    b = t[t.index("</style>") + 8:]
    b = re.sub(r"<!--.*?-->\n?", "", b, flags=re.S)
    return uris_to_paths(b.strip())
def css_union(files, extra=""):
    out = BASE
    for f in files: out += block_css(f).replace(BASE, "", 1)
    return out + extra

def e(s): return _html.escape(s, quote=True)

CHECK = '<svg aria-hidden="true" width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M2.5 7.4l3 3 6-6.4"/></svg>'
FN = '<p class="pxa-fn">* Запрещённый на территории России сервис.</p>'

_k01 = block_body(ROOT + "/tilda-target/k01-header-hero.html")
HEADER = re.search(r'<header class="pxa-head">.*?</header>', _k01, re.S).group(0)
FOOTER = block_body(ROOT + "/tilda-target/k08-footer.html")
AUDIT_SRC = block_body(ROOT + "/tilda-target/k07-audit-form.html")

def header(active=None, audit=True):
    h = HEADER.replace(' aria-current="page"', "")
    if active:
        h = h.replace(f'<a href="/{active}">', f'<a href="/{active}" aria-current="page">', 1)
    if not audit:
        h = h.replace('href="#pxa-audit"', 'href="/contacts"')
    return h

def audit(h2="Хотите такой же результат?", lead="Расскажите о своей задаче. Начнём с бесплатного экспресс-аудита: покажем, где теряются заявки, за 3 рабочих дня."):
    t = AUDIT_SRC
    t = re.sub(r"<h2 class=\"pxa-h2\">.*?</h2>", f'<h2 class="pxa-h2">{h2}</h2>', t, count=1)
    t = re.sub(r'<p class="pxa-audit-lead">.*?</p>', f'<p class="pxa-audit-lead">{lead}</p>', t, count=1, flags=re.S)
    return t

def footer(audit_present=True):
    return FOOTER

# ---------- components ----------
def crumbs(items):
    parts = []
    for i, (label, href) in enumerate(items):
        if href: parts.append(f'<a href="{href}">{label}</a>')
        else: parts.append(label)
    return '<nav class="pxa-crumbs" aria-label="Хлебные крошки">' + "<span>/</span>".join(parts) + "</nav>"

def hero(crumb, eyebrow, h1, lead, meta=None, ctas=None, fn=False, active=None, audit_present=True, art=True, h1cls="pxa-k-h1"):
    m = ""
    if meta:
        m = '<dl class="pxa-meta">' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in meta) + "</dl>"
    ctas = ctas if ctas is not None else [("pxa-btn", "#pxa-audit" if audit_present else "/contacts", "Обсудить проект"), ("pxa-btn-ghost", "/cases", "Все кейсы")]
    c = '<div class="pxa-cta-row">' + "".join(f'<a class="{cl}" href="{hr}">{tx}</a>' for cl, hr, tx in ctas) + "</div>"
    a = '<div class="pxa-hero-art pxa-intro-art"><img class="pxa-logo" src="/assets/img/logo-mark-l.webp" alt="" aria-hidden="true"></div>' if art else ""
    f = FN.replace('<p class="pxa-fn">', '<p class="pxa-fn" style="margin-top:20px">') if fn else ""
    return f'''<section class="pxa pxa-hero" id="pxa-top">
<div class="pxa-wrap">
{header(active, audit_present)}
<div class="pxa-hero-row" style="padding-bottom:64px">
<div class="pxa-hero-text">
{crumbs(crumb)}
<p class="pxa-eyebrow">{eyebrow}</p>
<h1 class="pxa-h1 {h1cls}">{h1}</h1>
<p class="pxa-lead">{lead}</p>
{m}
{c}
{f}
</div>
{a}
</div>
</div>
</section>'''

def kpi(title, sub, hero_tile=None, tiles=(), scale=(), note="", fn=False):
    """hero_tile=(n,text,src); tiles=[(n,text,src)] with 'KPI выполнен'; scale=[(word,text)]"""
    done = f'<span class="pxa-badge">{CHECK}KPI выполнен</span>'
    task = f'<span class="pxa-badge">{CHECK}Задача выполнена</span>'
    sc = '<span class="pxa-badge pxa-scale">Масштаб проекта</span>'
    out = f'<section class="pxa pxa-sec pxa-dark pxa-kpis" id="pxa-kpi"><div class="pxa-wrap"><h2 class="pxa-h2">{title}</h2><p class="pxa-kpi-sub">{sub}</p>'
    if hero_tile:
        n, t, s = hero_tile
        out += f'<ul class="pxa-kpi-grid" style="list-style:none;margin:44px 0 0;padding:0"><li class="pxa-kpi pxa-done pxa-kpi-hero"><div class="pxa-kpi-n">{n}</div><div class="pxa-kpi-body">{done}<p class="pxa-kpi-t">{t}</p><p class="pxa-kpi-src">{s}</p></div></li></ul>'
    if tiles:
        cls = "pxa-g4" if len(tiles) >= 4 else ("pxa-g3" if len(tiles) == 3 else ("pxa-g2" if len(tiles) == 2 else "pxa-g1"))
        out += f'<ul class="pxa-kpi-grid {cls}" style="list-style:none;padding:0;margin-top:{20 if hero_tile else 44}px">'
        for kind, n, t, s in tiles:
            b = done if kind == "kpi" else task
            word = " pxa-word" if re.search(r"[А-Яа-я]{4,}", n) else ""
            out += f'<li class="pxa-kpi pxa-done">{b}<div class="pxa-kpi-n{word}">{n}</div><p class="pxa-kpi-t">{t}</p><p class="pxa-kpi-src">{s}</p></li>'
        out += "</ul>"
    if scale:
        cls = "pxa-g3" if len(scale) == 3 else ("pxa-g2" if len(scale) == 2 else "pxa-g1")
        out += f'<ul class="pxa-kpi-grid {cls}" style="list-style:none;padding:0;margin-top:20px">'
        for w, t in scale:
            out += f'<li class="pxa-kpi">{sc}<div class="pxa-kpi-n pxa-word">{w}</div><p class="pxa-kpi-t">{t}</p></li>'
        out += "</ul>"
    if note: out += f'<p class="pxa-kpi-note">{note}</p>'
    if fn: out += '<p class="pxa-fn-d">* Запрещённый на территории России сервис.</p>'
    return out + "</div></section>"

def li(items): return "\n".join(f"<li>{CHECK}<span>{t}</span></li>" for t in items)

def two_panel(h2, lt, lp, litems, rt, rp, ritems, fn=False):
    f = FN.replace('<p class="pxa-fn">', '<p class="pxa-fn" style="margin-top:20px">') if fn else ""
    return f'''<section class="pxa pxa-sec" id="pxa-task"><div class="pxa-wrap"><h2 class="pxa-h2">{h2}</h2>
<div class="pxa-two"><div class="pxa-panel"><h3>{lt}</h3><p>{lp}</p><ul class="pxa-list">{li(litems)}</ul></div>
<div class="pxa-panel"><h3>{rt}</h3><p>{rp}</p><ul class="pxa-list">{li(ritems)}</ul></div></div>{f}</div></section>'''

def steps(h2, items, fn=False, tint=True, cols=3):
    """items: (title, text, result|None, open?)"""
    lis = ""
    for i, it in enumerate(items, 1):
        t, d, r, op = (list(it) + [None, False])[:4]
        res = ""
        if r: res = f'<div class="pxa-res"><span class="{"pxa-open" if op else ""}">{r if op else CHECK + r}</span></div>'
        p = f"<p>{d}</p>" if d else ""
        lis += f'<li class="pxa-step"><span class="pxa-step-n">{i:02d}</span><h3>{t}</h3>{p}{res}</li>'
    f = FN.replace('<p class="pxa-fn">', '<p class="pxa-fn" style="margin-top:20px">') if fn else ""
    cl = "pxa-steps" + (" pxa-s2" if cols == 2 else "")
    return f'<section class="pxa pxa-sec{" pxa-tint" if tint else ""}" id="pxa-work"><div class="pxa-wrap"><h2 class="pxa-h2">{h2}</h2><ol class="{cl}">{lis}</ol>{f}</div></section>'

def cards(h2, items, cols=3, tint=False, sub="", idn="pxa-for"):
    """plain cards (title, text)"""
    g = {2: " pxa-g2", 3: "", 4: " pxa-g4c"}[cols]
    cs = "".join(f'<article class="pxa-mc"><h3>{t}</h3><p>{d}</p></article>' for t, d in items)
    s = f'<p class="pxa-lead2">{sub}</p>' if sub else ""
    return f'<section class="pxa pxa-sec{" pxa-tint" if tint else ""}" id="{idn}"><div class="pxa-wrap"><h2 class="pxa-h2">{h2}</h2>{s}<div class="pxa-more-grid{g}">{cs}</div></div></section>'

def link_cards(h2, items, tint=True, more=True, idn="pxa-more"):
    """items: (label, title, fig, desc, href)"""
    cs = ""
    for l, n, f, d, h in items:
        fig = f'<div class="pxa-big pxa-mc-fig">{f}</div>' if f else ""
        p = f"<p>{d}</p>" if d else ""
        cs += f'<article class="pxa-mc"><small>{l}</small><h3><a href="{h}">{n}</a></h3>{fig}{p}<span class="pxa-go" aria-hidden="true">Смотреть →</span></article>'
    m = '<p style="margin-top:28px"><a class="pxa-more" href="/cases">Все кейсы →</a></p>' if more else ""
    return f'<section class="pxa pxa-sec{" pxa-tint" if tint else ""}" id="{idn}"><div class="pxa-wrap"><h2 class="pxa-h2">{h2}</h2><div class="pxa-more-grid">{cs}</div>{m}</div></section>'

def quote(text, author, role, placeholder=False):
    ph = " pxa-ph" if placeholder else ""
    return f'''<section class="pxa pxa-sec" id="pxa-review"><div class="pxa-wrap"><h2 class="pxa-h2">Отзыв клиента</h2>
<figure class="pxa-quote"><blockquote class="{ph.strip()}">{text}</blockquote><figcaption><b>{author}</b><span>{role}</span></figcaption></figure></div></section>'''

def concl(h2, lead, items, fn=False):
    f = FN.replace('<p class="pxa-fn">', '<p class="pxa-fn" style="margin-top:28px">') if fn else ""
    ol = "".join(f'<li><span class="pxa-ol-n">{i:02d}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (t, d) in enumerate(items, 1))
    return f'''<section class="pxa pxa-sec" id="pxa-takeaways"><div class="pxa-wrap"><div class="pxa-concl"><div class="pxa-concl-l"><h2 class="pxa-h2">{h2}</h2><p>{lead}</p><a class="pxa-btn" href="#pxa-audit">Обсудить ваш проект</a></div><ol class="pxa-ol">{ol}</ol></div>{f}</div></section>'''

def faq(items, h2="Частые вопросы"):
    half = (len(items) + 1) // 2
    col = lambda its: '<div class="pxa-faq-col">' + "".join(f"<div><h3>{q}</h3><p>{a}</p></div>" for q, a in its) + "</div>"
    return f'<section class="pxa pxa-sec" id="pxa-faq"><div class="pxa-wrap"><h2 class="pxa-h2">{h2}</h2><div class="pxa-faq">{col(items[:half])}{col(items[half:])}</div></div></section>'

def text_section(h2, paras, idn="pxa-text", tint=False):
    ps = "".join(f"<p>{p}</p>" for p in paras)
    return f'<section class="pxa pxa-sec{" pxa-tint" if tint else ""}" id="{idn}"><div class="pxa-wrap"><div class="pxa-prose"><h2 class="pxa-h2">{h2}</h2>{ps}</div></div></section>'

def jsonld(*objs):
    import json
    return "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False, separators=(",", ":"))}</script>\n' for o in objs)

def breadcrumb_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items, 1)]}

def faq_ld(items):
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}

EXTRA = """
.pxa-lead2{margin-top:12px;color:var(--pxa-mute);max-width:640px}
.pxa-more-grid.pxa-g2{grid-template-columns:repeat(2,minmax(0,1fr))}
.pxa-more-grid.pxa-g4c{grid-template-columns:repeat(4,minmax(0,1fr))}
.pxa-more-grid .pxa-mc{background:var(--pxa-tint)}
.pxa-tint .pxa-more-grid .pxa-mc{background:#fff}
.pxa-kpi-grid.pxa-g1{grid-template-columns:1fr;margin-top:20px}
.pxa-kpi-grid.pxa-g3{grid-template-columns:repeat(3,minmax(0,1fr));margin-top:20px}
.pxa-kpi-grid.pxa-g4{grid-template-columns:repeat(4,minmax(0,1fr));margin-top:20px}
.pxa-kpi-grid.pxa-g2{grid-template-columns:repeat(2,minmax(0,1fr));margin-top:20px}
.pxa-kpi-hero{grid-column:1 / -1;flex-direction:row;align-items:center;gap:40px;padding:36px 40px}
.pxa-kpi-hero .pxa-kpi-n{font-size:96px;margin:0;flex:none}
.pxa-kpi-hero .pxa-kpi-body{display:flex;flex-direction:column;gap:10px}
.pxa-kpi-hero .pxa-kpi-t{font-size:22px;line-height:1.35}
.pxa-kpi-n.pxa-word{font-size:30px;line-height:1.2;margin-top:6px}
.pxa-g4 .pxa-kpi-n{font-size:42px}
.pxa-g4 .pxa-kpi-n.pxa-word{font-size:26px}
.pxa-fn-d{margin-top:12px;font-size:14px;color:#B9B5E6}
.pxa-fn{font-size:13px;color:#5A5F7D}
.pxa-steps.pxa-s2{grid-template-columns:repeat(2,minmax(0,1fr))}
.pxa-quote{margin:32px 0 0;padding:40px;border-radius:24px;background:var(--pxa-tint)}
.pxa-quote blockquote{margin:0;font-size:22px;line-height:1.5;font-weight:500}
.pxa-quote blockquote.pxa-ph{color:#5A5F7D;font-weight:400;border:1px dashed #B9B5E6;padding:16px;border-radius:12px}
.pxa-quote figcaption{margin-top:20px;display:flex;flex-direction:column;gap:2px;color:var(--pxa-mute)}
.pxa-quote figcaption b{color:var(--pxa-ink)}
.pxa-prose{max-width:760px}
.pxa-prose p{margin-top:16px;color:var(--pxa-mute)}
.pxa-prose h3{margin-top:32px;font-size:21px}
.pxa-prose ul{margin:12px 0 0 20px;list-style:disc;padding:0;color:var(--pxa-mute)}
.pxa-prose li{margin-top:6px}
.pxa-ph{color:#5A5F7D}
.pxa-price{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px;margin-top:32px}
.pxa-price .pxa-panel .pxa-big{font-size:34px;color:var(--pxa-a);margin-top:14px}
.pxa-contact-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin-top:36px}
.pxa-contact-list{list-style:none;margin:18px 0 0;padding:0;display:flex;flex-direction:column;gap:14px}
.pxa-contact-list dt{font-size:13px;color:#5A5F7D;text-transform:uppercase;letter-spacing:.06em;font-weight:600}
.pxa-contact-list dd{margin:2px 0 0;font-size:19px;font-weight:500}
.pxa-contact-list a{text-decoration:none;color:var(--pxa-a)}
.pxa-contact-list a:hover{text-decoration:underline}
.pxa-contact-form{display:flex;flex-direction:column;gap:14px;margin-top:18px}
.pxa-contact-form .pxa-field{display:flex;flex-direction:column;gap:6px}
.pxa-contact-form label{font-size:14px;color:var(--pxa-mute)}
.pxa-contact-form input,.pxa-contact-form textarea{width:100%;font:inherit;padding:14px 16px;border-radius:12px;border:1px solid #CFCBEF;background:#fff;color:var(--pxa-ink)}
.pxa-contact-form .pxa-consent{display:flex;gap:10px;align-items:flex-start;font-size:14px;color:var(--pxa-mute)}
.pxa-contact-form .pxa-consent input{width:auto;margin-top:4px}
.pxa-timeline{list-style:none;margin:32px 0 0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.pxa-timeline li{padding:20px;border-radius:20px;background:var(--pxa-tint)}
.pxa-timeline b{display:block;font-family:'Unbounded',sans-serif;font-size:22px;color:var(--pxa-a);margin-bottom:6px}
.pxa-team{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:20px;margin-top:32px}
.pxa-team article{padding:20px;border-radius:20px;background:#fff}
.pxa-team .pxa-ava{aspect-ratio:1;border-radius:16px;background:linear-gradient(135deg,#E4DCFF,#D2EEFF);display:flex;align-items:center;justify-content:center;color:#5A5F7D;font-size:14px;text-align:center;padding:8px}
.pxa-team h3{margin-top:14px;font-size:18px}
.pxa-team p{margin-top:4px;font-size:15px;color:var(--pxa-mute)}
.pxa-404{min-height:60vh;display:flex;align-items:center}
@media (max-width:1000px){
.pxa-more-grid.pxa-g4c{grid-template-columns:repeat(2,minmax(0,1fr))}
.pxa-kpi-grid.pxa-g3,.pxa-kpi-grid.pxa-g4{grid-template-columns:repeat(2,minmax(0,1fr))}
.pxa-team,.pxa-timeline{grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:860px){
.pxa-more-grid.pxa-g2,.pxa-more-grid.pxa-g4c{grid-template-columns:1fr}
.pxa-kpi-hero{flex-direction:column;align-items:flex-start;gap:10px;padding:22px}
.pxa-kpi-hero .pxa-kpi-n{font-size:56px}
.pxa-kpi-hero .pxa-kpi-t{font-size:17px}
.pxa-kpi-grid.pxa-g1,.pxa-kpi-grid.pxa-g2,.pxa-kpi-grid.pxa-g3,.pxa-kpi-grid.pxa-g4{grid-template-columns:1fr;gap:14px;margin-top:14px}
.pxa-g4 .pxa-kpi-n{font-size:40px}
.pxa-kpi-n.pxa-word,.pxa-g4 .pxa-kpi-n.pxa-word{font-size:26px}
.pxa-steps.pxa-s2{grid-template-columns:1fr}
.pxa-quote{padding:24px;border-radius:20px}
.pxa-quote blockquote{font-size:18px}
.pxa-price,.pxa-contact-grid{grid-template-columns:1fr}
.pxa-team,.pxa-timeline{grid-template-columns:1fr}
.pxa-contact-list dd{font-size:17px}
}
"""

CSS_FILES_SITE = [ROOT + "/tilda-target/" + f for f in ["k01-header-hero.html", "k02-kpi.html", "k03-task-scope.html", "k04-work.html", "k05-conclusions.html", "k06-more-cases.html", "k07-audit-form.html", "k08-footer.html"]] + [ROOT + "/tilda-blocks/09-faq.html"]

def page(path, title, desc, css, body, ld="", noindex=False, og_image=None):
    url = SITE + ("/" if path == "" else "/" + path + "/")
    canon = url
    robots = '<meta name="robots" content="noindex,follow">\n' if noindex else ""
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ru_RU">
<meta property="og:site_name" content="Proxy Agency">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<link rel="icon" href="/assets/img/logo-mark-s.webp" type="image/webp">
{FONTS}
<link rel="stylesheet" href="/assets/css/{css}">
{ld}</head>
<body>
{body}
</body>
</html>
'''
