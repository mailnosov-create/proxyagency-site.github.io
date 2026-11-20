import base64, io, re, glob, os, shutil
from PIL import Image
R="/tmp/claude-0/-home-claude/4160dc96-70e4-507e-bf5d-2fe78152fe1f/scratchpad"
def webp(name, w, q=82):
    im=Image.open(f"{R}/logo-work/proxy-logo-{name}.png").convert("RGBA")
    h=round(im.height*w/im.width); im=im.resize((w,h),Image.LANCZOS)
    b=io.BytesIO(); im.save(b,"WEBP",quality=q,method=6); d=b.getvalue()
    print(name,w,len(d)); return "data:image/webp;base64,"+base64.b64encode(d).decode()
MARK_S=webp("mark",100,78); WORD=webp("wordmark",170,78); MARK_L=webp("mark",440,70); FULL=webp("full",300,72)
P="https://static.tildacdn.com/REPLACE-ME/"
def conv(t):
    t=t.replace(P+"proxy-logo-wordmark.png",WORD).replace(P+"proxy-logo-full.png",FULL)
    # first mark = header (small), second = hero art (large)
    parts=t.split(P+"proxy-logo-mark.png")
    if len(parts)==3: t=parts[0]+MARK_S+parts[1]+MARK_L+parts[2]
    elif len(parts)==2: t=parts[0]+MARK_L+parts[1]
    assert "REPLACE-ME" not in t.replace("REPLACE_FORM_ENDPOINT","")
    return t
for d in ["tilda-blocks","tilda-cases","tilda-opti","tilda-nevsky","tilda-target"]:
    for f in glob.glob(f"{R}/{d}/*.html"):
        if f.endswith("preview.html"): continue
        t=open(f,encoding="utf-8").read()
        if "REPLACE-ME" in t: open(f,"w",encoding="utf-8").write(conv(t))
    shutil.rmtree(f"{R}/{d}/logo",ignore_errors=True)
    # preview from converted blocks
    fs=sorted(x for x in glob.glob(f"{R}/{d}/*.html") if not x.endswith("preview.html"))
    head='<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Превью</title><style>body{margin:0;background:#fff}</style></head><body>' 
    open(f"{R}/{d}/preview.html","w",encoding="utf-8").write(head+"\n".join(open(x,encoding="utf-8").read() for x in fs)+"</body></html>")
    print(d,"ok",[os.path.getsize(x)//1024 for x in fs])
