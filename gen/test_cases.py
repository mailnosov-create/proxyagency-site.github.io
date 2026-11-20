from playwright.sync_api import sync_playwright
d="/tmp/claude-0/-home-claude/4160dc96-70e4-507e-bf5d-2fe78152fe1f/scratchpad/"
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,w in [("desktop",1440),("mobile",390)]:
        pg=b.new_page(viewport={"width":w,"height":900})
        errs=[]; pg.on("pageerror",lambda e:errs.append(str(e)))
        pg.goto("file://"+d+"tilda-cases/preview.html"); pg.wait_for_timeout(1200)
        print(name,"scrollWidth",pg.evaluate("document.documentElement.scrollWidth"),"errors",errs)
        pg.click('button[data-k="rest"]')
        vis=pg.evaluate("[...document.querySelectorAll('.pxa-case')].filter(e=>!e.hidden).map(e=>e.querySelector('h3').textContent)")
        print(" rest:",vis, pg.inner_text('.pxa-count'))
        pg.click('button[data-k="prod"]')
        print(" prod:",pg.inner_text('.pxa-count'))
        pg.click('button[data-k="all"]')
        print(" all:",pg.inner_text('.pxa-count'))
        pg.screenshot(path=d+f"gen/cases2_{name}.png",full_page=True)
    b.close()
