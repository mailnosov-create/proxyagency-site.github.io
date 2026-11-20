"""Медиа кейсов. Кладёте файлы в media/<slug>/ — сборка сама сжимает и вставляет.
  cover.jpg|png     — обложка (карточка на «Кейсах», верх страницы кейса)
  01-*.jpg … 09-*   — галерея (по алфавиту)
  captions.txt      — подписи: «имя_файла | текст» построчно (необязательно)
  video.txt         — 1-я строка ссылка (YouTube/RuTube/VK), 2-я — заголовок (необязательно)
  video-poster.jpg  — превью видео (необязательно)
media/_logos/*.png  — логотипы клиентов для главной (имя файла = название клиента)
"""
import os, io, glob, re, html as _html
from PIL import Image
ROOT = "/tmp/claude-0/-home-claude/4160dc96-70e4-507e-bf5d-2fe78152fe1f/scratchpad"
MEDIA = ROOT + "/media"
EXT = (".jpg", ".jpeg", ".png", ".webp")
OUT = {}   # путь в сайте -> байты (то, что надо записать на диск)

def _conv(src, dest, maxw=1400, limit=250_000):
    im = Image.open(src)
    if im.mode in ("RGBA", "LA", "P") and not dest.startswith("/assets/img/clients"):
        im = im.convert("RGBA"); bg = Image.new("RGB", im.size, "white"); bg.paste(im, mask=im.split()[3]); im = bg
    elif im.mode not in ("RGB", "RGBA"): im = im.convert("RGB")
    if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    for q in (82, 76, 70, 62, 55, 48):
        b = io.BytesIO(); im.save(b, "WEBP", quality=q, method=6)
        if b.tell() <= limit: break
    OUT[dest] = b.getvalue()
    return im.width, im.height

def _files(slug):
    return sorted(f for f in glob.glob(f"{MEDIA}/{slug}/*") if f.lower().endswith(EXT))

def cover(slug):
    """путь обложки или None"""
    for f in _files(slug):
        if os.path.basename(f).lower().startswith("cover."):
            d = f"/assets/img/cases/{slug}/cover.webp"
            _conv(f, d, 900, 120_000)
            return d
    return None

def _video_embed(url):
    m = re.search(r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|shorts/))([\w-]{6,})", url)
    if m: return f"https://www.youtube-nocookie.com/embed/{m.group(1)}?autoplay=1"
    m = re.search(r"rutube\.ru/(?:video|play/embed)/([0-9a-f]{32})", url)
    if m: return f"https://rutube.ru/play/embed/{m.group(1)}?autoStart=true"
    m = re.search(r"vk(?:video)?\.(?:com|ru)/video(-?\d+)_(\d+)", url)
    if m: return f"https://vk.com/video_ext.php?oid={m.group(1)}&id={m.group(2)}&autoplay=1"
    return None

def gallery(slug, title):
    fs = [f for f in _files(slug) if not os.path.basename(f).lower().startswith(("cover.", "video-poster."))]
    caps = {}
    cf = f"{MEDIA}/{slug}/captions.txt"
    if os.path.exists(cf):
        for ln in open(cf, encoding="utf-8"):
            if "|" in ln:
                a, b = ln.split("|", 1); caps[a.strip()] = b.strip()
    figs = ""
    for i, f in enumerate(fs, 1):
        name = os.path.basename(f)
        d = f"/assets/img/cases/{slug}/{i:02d}.webp"
        w, h = _conv(f, d)
        cap = _html.escape(caps.get(name, ""))
        alt = _html.escape(caps.get(name) or f"{title}: материал проекта {i}")
        fc = f"<figcaption>{cap}</figcaption>" if cap else ""
        figs += f'<figure class="pxa-shot"><img src="{d}" width="{w}" height="{h}" loading="lazy" decoding="async" alt="{alt}">{fc}</figure>'
    vid = ""
    vf = f"{MEDIA}/{slug}/video.txt"
    if os.path.exists(vf):
        lines = [l.strip() for l in open(vf, encoding="utf-8") if l.strip()]
        emb = _video_embed(lines[0]) if lines else None
        if emb:
            vt = _html.escape(lines[1]) if len(lines) > 1 else "Смотреть видео"
            poster = ""
            for p in _files(slug):
                if os.path.basename(p).lower().startswith("video-poster."):
                    d = f"/assets/img/cases/{slug}/video-poster.webp"; _conv(p, d)
                    poster = f' style="background-image:url({d})"'
            vid = f'<div class="pxa-video"{poster} data-embed="{emb}"><button type="button" class="pxa-play" aria-label="Запустить видео"><svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg><span>{vt}</span></button></div>'
    if not figs and not vid: return ""
    return f'<section class="pxa pxa-sec pxa-tint" id="pxa-media"><div class="pxa-wrap"><h2 class="pxa-h2">Материалы проекта</h2>{vid}<div class="pxa-shots">{figs}</div></div></section>'

def logos():
    fs = sorted(f for f in glob.glob(f"{MEDIA}/_logos/*") if f.lower().endswith(EXT))
    if not fs: return ""
    items = ""
    for f in fs:
        n = os.path.splitext(os.path.basename(f))[0]
        d = f"/assets/img/clients/{re.sub(r'[^a-z0-9-]', '-', n.lower())}.webp"
        im = Image.open(f).convert("RGBA"); im.thumbnail((320, 120))
        b = io.BytesIO(); im.save(b, "WEBP", quality=85, method=6); OUT[d] = b.getvalue()
        items += f'<li><img src="{d}" width="{im.width}" height="{im.height}" loading="lazy" alt="{_html.escape(n)}"></li>'
    return f'<section class="pxa pxa-sec" id="pxa-clients"><div class="pxa-wrap"><p class="pxa-clients-t">Нам доверяют</p><ul class="pxa-clients">{items}</ul></div></section>'

CSS = """
.pxa-shots{display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin-top:8px;align-items:start}
.pxa-shots:has(.pxa-shot:only-child){grid-template-columns:1fr;max-width:900px}
.pxa-shot{margin:0;background:#fff;border:1px solid var(--pxa-line,#E3E5F1);border-radius:20px;overflow:hidden}
.pxa-shot img{display:block;width:100%;height:auto}
.pxa-shot figcaption{padding:14px 18px;font-size:14px;color:#5A5F7D}
.pxa-video{position:relative;aspect-ratio:16/9;border-radius:20px;overflow:hidden;background:#1d2040 center/cover;margin:24px 0 20px}
.pxa-video iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.pxa-play{position:absolute;inset:0;width:100%;border:0;background:rgba(20,22,50,.35);color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;cursor:pointer;font:600 16px/1.3 inherit}
.pxa-play svg{width:68px;height:68px;padding:18px;border-radius:50%;background:rgba(255,255,255,.18)}
.pxa-clients-t{margin:0 0 18px;font-size:14px;color:#5A5F7D;text-align:center}
.pxa-clients{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:20px 44px}
.pxa-clients img{display:block;height:40px;width:auto;max-width:150px;object-fit:contain;filter:grayscale(1);opacity:.75}
.pxa-cover-img{height:190px;width:100%;object-fit:cover;display:block}
.pxa-hero-img{display:block;width:100%;height:auto;border-radius:20px;margin-top:28px}
@media (max-width:760px){.pxa-shots{grid-template-columns:1fr}.pxa-clients{gap:16px 28px}.pxa-clients img{height:32px}}
"""
JS = """<script>document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.pxa-play');if(!b)return;var v=b.parentNode,f=document.createElement('iframe');f.src=v.getAttribute('data-embed');f.allow='autoplay; fullscreen; picture-in-picture';f.allowFullscreen=true;v.appendChild(f);b.remove();});</script>"""
