import re, os, json, glob
ROOT="/tmp/claude-0/-home-claude/4160dc96-70e4-507e-bf5d-2fe78152fe1f/scratchpad"
SRC=ROOT+"/tilda-nevsky"; PUB=ROOT+"/proxy-nev-pub/project"; os.makedirs(PUB,exist_ok=True)
MARK="/_blob/14d987b680d53fde2ef3b53675aaad06"; WORD="/_blob/aaefb421f4dccf9d5548c8bca2e7f1ba"; FULL="/_blob/f4eef8cb2c85e54e8ec1eb97567edb50"
bs=open(ROOT+"/gen/build.py",encoding="utf-8").read()
BASE=re.search(r'BASE = """(.*?)"""',bs,re.S).group(1)
FONTS=re.search(r"FONTS = '(.*?)'",bs).group(1)
css_all=BASE; parts=[]
for f in sorted(glob.glob(SRC+"/k0*.html")):
    t=re.sub(r"<!--.*?-->","",open(f,encoding="utf-8").read(),flags=re.S)
    css=t[t.index("<style>")+7:t.index("</style>")]
    html=t[t.index("</style>")+8:].strip()
    css_all+=css.replace(BASE,"",1)
    html=re.sub(r'<script type="application/ld\+json">.*?</script>\n?',"",html,flags=re.S)
    html=re.sub(r"<!--.*?-->\n?","",html,flags=re.S)
    html=(html.replace("https://static.tildacdn.com/REPLACE-ME/proxy-logo-mark.png",MARK)
        .replace("https://static.tildacdn.com/REPLACE-ME/proxy-logo-wordmark.png",WORD)
        .replace("https://static.tildacdn.com/REPLACE-ME/proxy-logo-full.png",FULL)
        .replace('action="REPLACE_FORM_ENDPOINT"','action="#"'))
    parts.append(html)
body="\n".join(parts)
assert "{{" not in body and "{{" not in css_all and "REPLACE" not in body
def dc(title,w,h):
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
return {{}};
}}
}}
</script>
</body>
</html>
'''
H=json.load(open(ROOT+"/gen/nev_h.json"))
open(PUB+"/Nevsky.dc.html","w",encoding="utf-8").write(dc("Proxy Agency — кейс Невский берег",1440,H["d"]))
open(PUB+"/NevskyMobile.dc.html","w",encoding="utf-8").write(dc("Proxy Agency — кейс Невский берег, телефон",390,H["m"]))
print("ok",H)
