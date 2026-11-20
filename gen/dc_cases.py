import re, ast, json, os, glob

ROOT = "/tmp/claude-0/-home-claude/4160dc96-70e4-507e-bf5d-2fe78152fe1f/scratchpad"
SRC = ROOT + "/tilda-cases"
PUB = ROOT + "/proxy-cases-pub/project"
os.makedirs(PUB, exist_ok=True)

MARK_NEW = "/_blob/14d987b680d53fde2ef3b53675aaad06"
WORD_NEW = "/_blob/aaefb421f4dccf9d5548c8bca2e7f1ba"
FULL_NEW = "/_blob/f4eef8cb2c85e54e8ec1eb97567edb50"

build_src = open(ROOT + "/gen/build.py", encoding="utf-8").read()
BASE = re.search(r'BASE = """(.*?)"""', build_src, re.S).group(1)
FONTS = re.search(r"FONTS = '(.*?)'", build_src).group(1)
cs = open(ROOT + "/gen/build_cases.py", encoding="utf-8").read()
cases = ast.literal_eval(re.search(r"cases = (\[.*?\n\])", cs, re.S).group(1))
inds = ast.literal_eval(re.search(r"inds = (\[.*?\])\n", cs, re.S).group(1))

def split(fn):
    t = re.sub(r"<!--.*?-->", "", open(f"{SRC}/{fn}", encoding="utf-8").read(), flags=re.S)
    css = t[t.index("<style>") + 7: t.index("</style>")]
    html = t[t.index("</style>") + 8:].strip()
    return css, html

def fix_urls(h):
    return (h.replace("https://static.tildacdn.com/REPLACE-ME/proxy-logo-mark.png", MARK_NEW)
             .replace("https://static.tildacdn.com/REPLACE-ME/proxy-logo-wordmark.png", WORD_NEW)
             .replace("https://static.tildacdn.com/REPLACE-ME/proxy-logo-full.png", FULL_NEW)
             .replace('action="REPLACE_FORM_ENDPOINT"', 'action="#"'))

css_all = BASE
html_parts = []
for fn in ["c01-header-intro.html", "c02-cases.html", "c03-stats.html", "c04-audit-form.html", "c05-footer.html"]:
    css, html = split(fn)
    css_all += css.replace(BASE, "")
    if fn.startswith("c01"):
        html = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", html, flags=re.S)
    if fn.startswith("c02"):
        # replace static filters + grid with dynamic markup
        html = '''<section class="pxa pxa-sec pxa-cases" id="pxa-cases">
<div class="pxa-wrap">
<div class="pxa-filters" role="group" aria-label="Фильтр кейсов по отрасли">
<sc-for list="{{chips}}" as="chip" hint-placeholder-count="6">
<button class="pxa-filter" type="button" aria-pressed="{{chip.pressed}}" onClick="{{chip.pick}}">{{chip.label}}<span>{{chip.count}}</span></button>
</sc-for>
</div>
<p class="pxa-count" aria-live="polite">Показано кейсов: {{shown}}</p>
<div class="pxa-case-grid">
<sc-for list="{{cards}}" as="c" hint-placeholder-count="12">
<article class="pxa-case">
<div class="pxa-cover" style="background: {{c.cover}}">[Обложка кейса]</div>
<div class="pxa-case-b">
<small>{{c.label}}</small>
<h3><a class="pxa-case-a" href="{{c.href}}">{{c.name}}</a></h3>
<sc-if value="{{c.hasFig}}" hint-placeholder-val="{{ false }}">
<div class="pxa-big pxa-fig" style="color: {{c.color}}">{{c.fig}}</div>
<p class="pxa-strong">{{c.figtxt}}</p>
</sc-if>
<sc-if value="{{c.noFig}}" hint-placeholder-val="{{ true }}">
<p class="pxa-ph">Результат: [добавить цифру и срок]</p>
</sc-if>
<p class="pxa-desc {{c.descCls}}">{{c.desc}}</p>
<span class="pxa-go" aria-hidden="true">Смотреть кейс →</span>
</div>
</article>
</sc-for>
</div>
</div>
</section>'''
    html = re.sub(r"<!--.*?-->\n?", "", html, flags=re.S)
    html_parts.append(fix_urls(html))

css_all = css_all.replace("}}", "} }").replace("{{", "{ {")
body = "\n".join(html_parts)
assert "{{" in body and "REPLACE" not in body, "check"

data = json.dumps(cases, ensure_ascii=False)
inds_js = json.dumps(inds, ensure_ascii=False)

def dc(title, w, h):
    return f'''<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONTS}
<style>
body{{margin:0}}
{css_all}
</style>
</helmet>
<div>
{body}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
renderVals() {{
const all = {data};
const inds = {inds_js};
const covers = ["linear-gradient(135deg,#E4DCFF,#D2EEFF)", "linear-gradient(135deg,#D2EEFF,#E4DCFF)", "linear-gradient(135deg,#EFEBFF,#CFE9FF)"];
const f = (this.state && this.state.f) || "all";
const shown = all.filter((c) => f === "all" || c[2] === f);
const chips = inds.map((i) => ({{
label: i[1],
count: i[0] === "all" ? all.length : all.filter((c) => c[2] === i[0]).length,
pressed: i[0] === f ? "true" : "false",
pick: () => this.setState({{ f: i[0] }}),
}}));
const cards = shown.map((c, n) => ({{
name: c[0],
label: c[1],
href: "/cases/" + c[6],
cover: covers[n % 3],
hasFig: !!c[3],
noFig: !c[3],
fig: c[3] || "",
figtxt: c[4] || "",
color: n % 2 ? "#2F6BFF" : "#5B3FE0",
desc: c[5] || "[Задача и что сделали — 1–2 предложения]",
descCls: c[5] ? "" : "pxa-ph",
}}));
return {{ chips, cards, shown: shown.length }};
}}
}}
</script>
</body>
</html>
'''

open(PUB + "/Cases.dc.html", "w", encoding="utf-8").write(dc("Proxy Agency — страница «Кейсы»", 1440, 4205))
open(PUB + "/CasesMobile.dc.html", "w", encoding="utf-8").write(dc("Proxy Agency — страница «Кейсы», телефон", 390, 5842))

cv = {
 "v": 3,
 "attachments": {},
 "boards": {
  "Main.dc.html": {"expand": "fill", "h": 5200, "title": "Главная — десктоп 1440", "w": 1440, "x": 0, "y": 0},
  "Mobile.dc.html": {"expand": "fill", "h": 8000, "title": "Главная — мобильная 390", "w": 390, "x": 1520, "y": 0},
  "Cases.dc.html": {"expand": "fill", "h": 4205, "title": "Кейсы — десктоп 1440", "w": 1440, "x": 0, "y": 5320},
  "CasesMobile.dc.html": {"expand": "fill", "h": 5842, "title": "Кейсы — мобильная 390", "w": 390, "x": 1520, "y": 8120},
 },
 "createdOnFiles": {"at": "2026-11-13T07:40:00Z", "v": 1},
 "designSystems": [],
 "launch": {"view": "canvas"},
 "notes": {},
 "order": ["Main.dc.html", "Mobile.dc.html", "Cases.dc.html", "CasesMobile.dc.html"],
 "pages": [],
 "title": "Proxy Agency — прототип сайта",
}
open(PUB + "/canvas.json", "w", encoding="utf-8").write(json.dumps(cv, ensure_ascii=False, indent=2))
print("ok", os.listdir(PUB), len(css_all), len(body))
