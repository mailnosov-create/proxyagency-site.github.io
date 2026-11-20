from playwright.sync_api import sync_playwright
d="/tmp/claude-0/-home-claude/4160dc96-70e4-507e-bf5d-2fe78152fe1f/scratchpad/"
with sync_playwright() as p:
    b=p.chromium.launch()
    for name,w in [("desktop",1440),("mobile",390)]:
        pg=b.new_page(viewport={"width":w,"height":900})
        pg.goto("file://"+d+"tilda-blocks/preview.html"); pg.wait_for_timeout(1500)
        h=pg.evaluate("document.documentElement.scrollHeight"); sw=pg.evaluate("document.documentElement.scrollWidth")
        print(name,"height",h,"scrollWidth",sw)
        pg.screenshot(path=d+f"gen/{name}.png",full_page=True)
    b.close()
