import sys
from playwright.sync_api import sync_playwright
R="/tmp/claude-0/-home-claude/4160dc96-70e4-507e-bf5d-2fe78152fe1f/scratchpad"
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,w in [("d",1440),("m",390)]:
        pg=b.new_page(viewport={"width":w,"height":900})
        errs=[]
        pg.on("pageerror",lambda e:errs.append(str(e)))
        pg.goto(f"file://{R}/tilda-nevsky/preview.html"); pg.wait_for_timeout(800)
        sw=pg.evaluate("document.documentElement.scrollWidth"); h=pg.evaluate("document.documentElement.scrollHeight")
        print(name,"scrollW",sw,"h",h,"errs",errs)
        pg.screenshot(path=f"{R}/gen/nev_{name}.png",full_page=True)
    b.close()
