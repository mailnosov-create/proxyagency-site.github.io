import json
from playwright.sync_api import sync_playwright
R="/tmp/claude-0/-home-claude/4160dc96-70e4-507e-bf5d-2fe78152fe1f/scratchpad"
o={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for k,w in [("d",1440),("m",390)]:
        pg=b.new_page(viewport={"width":w,"height":900}); pg.goto(f"file://{R}/tilda-target/preview.html"); pg.wait_for_timeout(500)
        o[k]=pg.evaluate("document.documentElement.scrollHeight")
json.dump(o,open(R+"/gen/tgt_h.json","w")); print(o)
