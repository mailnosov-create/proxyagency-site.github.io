from playwright.sync_api import sync_playwright
d="/tmp/claude-0/-home-claude/4160dc96-70e4-507e-bf5d-2fe78152fe1f/scratchpad/"
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,w in [("desktop",1440),("mobile",390)]:
        pg=b.new_page(viewport={"width":w,"height":900})
        errs=[]; pg.on("pageerror",lambda e: errs.append(str(e)))
        pg.goto("file://"+d+"tilda-cases/preview.html"); pg.wait_for_timeout(1500)
        print(name,"height",pg.evaluate("document.documentElement.scrollHeight"),"scrollWidth",pg.evaluate("document.documentElement.scrollWidth"),"errors",errs)
        pg.screenshot(path=d+f"gen/cases_{name}.png",full_page=True)
        if name=="desktop":
            pg.click("button[data-k=rest]"); pg.wait_for_timeout(200)
            print("rest count:",pg.inner_text(".pxa-count"),"visible cards:",pg.evaluate("[...document.querySelectorAll('.pxa-case')].filter(c=>!c.hidden).length"),"pressed:",pg.evaluate("document.querySelector('button[data-k=rest]').getAttribute('aria-pressed')"))
            pg.click("button[data-k=all]"); pg.wait_for_timeout(200)
            print("all:",pg.inner_text(".pxa-count"))
    b.close()
