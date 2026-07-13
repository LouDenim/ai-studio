#!/usr/bin/env python3
"""
LOU DENIM — Catalogue Modèles IA
Scans a MODEL CATALOG folder tree (section/Model/{*_CS, *_CU|*_ECU}) and
builds a self-contained static site: face grid by section -> click ->
character-sheet view. Studio Blush brand.

Usage: python3 build_catalog.py <source_dir> <out_dir>
Conventions:
  - subfolder of source        = section (femmes, hommes, ados, enfants, seniors)
  - subfolder of section       = model name (folder name displayed, capitalized)
  - file containing 'CS'       = character sheet (16:9)
  - file containing 'CU'/'ECU' = close-up portrait (grid thumbnail)
  - fallback: landscape image  = sheet, portrait image = close-up
"""
import base64, io, json, os, re, sys, unicodedata
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/uploads/MODEL CATALOG"
OUT = sys.argv[2] if len(sys.argv) > 2 else "/root/catalogue-models"
LOGO = "/root/.claude/skills/pdf-lou/assets/lou-denim-logo.svg"

SECTION_ORDER = ["femmes", "hommes", "ados", "enfants", "seniors"]
SECTION_LABEL = {"femmes": "Femmes", "hommes": "Hommes", "ados": "Ados",
                 "enfants": "Enfants", "seniors": "Seniors"}

THUMB_PX   = 560   # square face thumb
FACE_PX    = 1000  # face image in the sheet view
SHEET_W    = 1800  # character sheet width
JPG_Q      = 82

def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def classify(files):
    """return (sheet_path, face_path) from a model folder's image files"""
    sheet = face = None
    for f in files:
        base = os.path.splitext(os.path.basename(f))[0].upper().replace(" ", "_")
        if re.search(r"(^|_)CS($|_)", base):
            sheet = f
        elif re.search(r"(^|_)E?CU($|_)", base):
            face = f
    # fallback by orientation
    for f in files:
        if f in (sheet, face):
            continue
        with Image.open(f) as im:
            if im.width > im.height and sheet is None:
                sheet = f
            elif im.height >= im.width and face is None:
                face = f
    return sheet, face

def save_jpg(im, path, quality=JPG_Q):
    im.convert("RGB").save(path, "JPEG", quality=quality, optimize=True, progressive=True)

def detect_face_center(pil_im):
    """return (cx, cy) of the largest detected face, or None"""
    try:
        import cv2, numpy as np
        small = pil_im.convert("RGB").copy()
        scale = 800 / max(small.size)
        if scale < 1:
            small = small.resize((round(small.width*scale), round(small.height*scale)), Image.LANCZOS)
        else:
            scale = 1.0
        gray = cv2.cvtColor(np.array(small), cv2.COLOR_RGB2GRAY)
        cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = cascade.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))
        if len(faces) == 0:
            return None
        x, y, fw, fh = max(faces, key=lambda f: f[2]*f[3])
        return ((x + fw/2) / scale, (y + fh/2) / scale)
    except Exception:
        return None

def face_thumb(src, dst, px=THUMB_PX):
    with Image.open(src) as im:
        w, h = im.size
        side = min(w, h)
        c = detect_face_center(im)
        if c:
            # bias slightly below face centre: prioritise mouth/chin over forehead
            cx, cy = int(c[0]), int(c[1] + 0.05 * side)
        else:
            cx, cy = w // 2, int(h * 0.45)  # fallback
        left = max(0, min(w - side, cx - side // 2))
        top  = max(0, min(h - side, cy - side // 2))
        im = im.crop((left, top, left + side, top + side))
        # trim ~1% on every edge: kills 1-2px dark generation rims (e.g. Ella)
        t = max(2, side // 100)
        im = im.crop((t, t, side - t, side - t))
        im = im.resize((px, px), Image.LANCZOS)
        save_jpg(im, dst)

def resize_w(src, dst, target_w):
    with Image.open(src) as im:
        if im.width > target_w:
            im = im.resize((target_w, round(im.height * target_w / im.width)), Image.LANCZOS)
        save_jpg(im, dst)

def main():
    os.makedirs(os.path.join(OUT, "img"), exist_ok=True)
    logo_b64 = base64.b64encode(open(LOGO, "rb").read()).decode()
    logo_src = f"data:image/svg+xml;base64,{logo_b64}"

    sections = []
    found = sorted(d for d in os.listdir(SRC)
                   if os.path.isdir(os.path.join(SRC, d)) and not d.startswith("."))
    ordered = [s for s in SECTION_ORDER if s in found] + [s for s in found if s not in SECTION_ORDER]

    total = 0
    for sec in ordered:
        sec_dir = os.path.join(SRC, sec)
        models = []
        for mdl in sorted(os.listdir(sec_dir)):
            mdir = os.path.join(sec_dir, mdl)
            if not os.path.isdir(mdir) or mdl.startswith("."):
                continue
            files = [os.path.join(mdir, f) for f in os.listdir(mdir)
                     if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))]
            if not files:
                continue
            sheet, face = classify(files)
            if face is None and sheet is None:
                continue
            slug = f"{slugify(sec)}-{slugify(mdl)}"
            entry = {"name": mdl.capitalize(), "slug": slug, "section": SECTION_LABEL.get(sec, sec.capitalize())}
            # thumbnail (from face if present, else crop from sheet centre)
            thumb_rel = f"img/{slug}-thumb.jpg"
            face_src = face or sheet
            face_thumb(face_src, os.path.join(OUT, thumb_rel))
            entry["thumb"] = thumb_rel
            if face:
                face_rel = f"img/{slug}-face.jpg"
                resize_w(face, os.path.join(OUT, face_rel), FACE_PX)
                entry["face"] = face_rel
            if sheet:
                sheet_rel = f"img/{slug}-sheet.jpg"
                resize_w(sheet, os.path.join(OUT, sheet_rel), SHEET_W)
                entry["sheet"] = sheet_rel
            models.append(entry)
            total += 1
        if models:
            sections.append({"key": sec, "label": SECTION_LABEL.get(sec, sec.capitalize()), "models": models})

    data_json = json.dumps(sections, ensure_ascii=False)

    html = HTML_TEMPLATE.replace("__LOGO_SRC__", logo_src).replace("__DATA__", data_json)
    with open(os.path.join(OUT, "index.html"), "w") as f:
        f.write(html)
    print(f"built {total} models in {len(sections)} sections -> {OUT}")

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LOU DENIM — Catalogue Modèles IA</title>
<meta name="robots" content="noindex">
<style>
@import url('https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&display=swap');
:root{
  --blush:#FBF1EF; --blush2:#F5E3DF; --blush3:#EBC9C3;
  --ink:#000; --grey:#666;
}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Jost',sans-serif;background:#fff;color:var(--ink);position:relative}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}

header.wrap{padding:86px 20px 26px;text-align:center}
header img{height:86px;margin-bottom:8px}
.rule{width:330px;max-width:70%;height:1px;background:var(--ink);margin:0 auto 10px}
.doc-band{display:inline-block;background:var(--ink);color:#fff;padding:10px 34px;border-radius:999px;
  font-size:15px;letter-spacing:.32em;text-transform:uppercase;font-weight:500;margin-top:24px}
.sub{font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:var(--ink)}
.contact{margin-top:8px;font-size:11px;letter-spacing:.1em;color:var(--grey)}
.intro{max-width:640px;margin:20px auto 0;font-size:14px;font-weight:300;line-height:1.55;color:#333}

nav{position:sticky;top:0;background:#fff;border-top:1px solid #eee;border-bottom:1px solid #eee;
  z-index:5;margin-top:26px}
nav .wrap{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;padding:10px 20px}
nav a{font-size:12px;letter-spacing:.18em;text-transform:uppercase;text-decoration:none;
  color:var(--ink);padding:7px 16px;border-radius:999px;background:#fff;border:1px solid #000;transition:background .15s}
nav a:hover{border-color:#E7549F;color:#E7549F;background:#fff}

section{padding:34px 0 6px}
h2.band{background:var(--ink);color:#fff;font-size:14px;font-weight:500;letter-spacing:.3em;
  text-transform:uppercase;padding:9px 18px;border-radius:10px;display:flex;justify-content:space-between;align-items:center}
h2.band .count{font-size:11px;letter-spacing:.14em;color:var(--blush3)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(158px,1fr));gap:16px;margin-top:18px}
.card{cursor:pointer;background:#fff;border:1px solid #e8e0dd;padding:8px 8px 10px;border-radius:4px;
  transition:transform .12s, box-shadow .12s, border-color .12s}
.card:hover{border-color:#E7549F}
.card:hover{transform:translateY(-3px);box-shadow:0 8px 22px rgba(0,0,0,.10)}
.card img{width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:2px;display:block;background:var(--blush2)}
.card .nm{margin-top:8px;text-align:center;font-size:13px;letter-spacing:.16em;text-transform:uppercase;font-weight:500}

footer{margin-top:46px;padding:26px 0 34px;background:#F3F3F2;text-align:center}
footer p{font-size:11px;letter-spacing:.14em;color:#444;text-transform:uppercase}
footer p+p{margin-top:6px}
footer a{color:#000}

/* ---- sheet view (lightbox) ---- */
#lb{position:fixed;inset:0;background:#fff;z-index:50;display:none;overflow-y:auto}
#lb.open{display:block}
#lb .inner{max-width:1180px;margin:0 auto;padding:26px 20px 60px}
#lb .top{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}
#lb .nm-band{background:var(--ink);color:#fff;padding:8px 26px;border-radius:999px;font-size:15px;
  letter-spacing:.3em;text-transform:uppercase;font-weight:500}
#lb .sec-tag{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--grey);margin-left:14px}
#lb button{font-family:'Jost';background:var(--blush);border:0;cursor:pointer;font-size:12px;
  letter-spacing:.18em;text-transform:uppercase;padding:10px 18px;border-radius:999px}
#lb button:hover{background:#fff;box-shadow:inset 0 0 0 1px #E7549F;color:#E7549F}
#lb .imgs{display:flex;flex-direction:column;gap:18px}
#lb .imgs img{width:100%;border-radius:4px;display:block;background:var(--blush2)}
#lb .duo{display:grid;grid-template-columns:minmax(0,340px) 1fr;gap:18px;align-items:start}
#lb .duo .face{width:100%;border-radius:4px}
@media(max-width:700px){#lb .duo{grid-template-columns:1fr}}
#lb .navrow{display:flex;justify-content:space-between;margin-top:26px}
#lb .cta{margin-top:30px;background:var(--blush2);padding:18px 20px;border-radius:4px;
  display:flex;justify-content:space-between;align-items:center;gap:14px;flex-wrap:wrap}
#lb .cta span{font-size:13px;font-weight:300}
#lb .cta a{background:#000;color:#fff;text-decoration:none;font-size:12px;letter-spacing:.18em;
  text-transform:uppercase;padding:11px 20px;border-radius:999px}
#dotfx{position:absolute;top:0;left:0;width:100%;height:430px;z-index:-1;pointer-events:none}
@media (prefers-reduced-motion: reduce){#dotfx{display:none}}
.socials{display:flex;gap:20px;justify-content:center;margin-top:16px}.socials a{color:#8a8f93;transition:color .15s}.socials a:hover{color:#E7549F}.socials svg{height:18px;width:18px;fill:currentColor;display:block}
</style>
</head>
<body>

<canvas id="dotfx"></canvas>

<header class="wrap">
  <a href="index.html"><img src="__LOGO_SRC__" alt="Lou Denim"></a>
  <div class="rule"></div>
  <p class="sub">Directeur artistique IA</p>
  <div><span class="doc-band">Catalogue Modèles IA</span></div>
  <p class="intro">Des modèles générés en IA, disponibles pour vos campagnes.
  Chaque modèle a son identité préservée d'une image à l'autre et peut être mis en scène avec votre produit.
  Cliquez sur un visage pour voir sa fiche complète.</p>
</header>

<nav><div class="wrap" id="navlinks"></div></nav>

<main class="wrap" id="main"></main>

<footer>
  <p style="margin-bottom:6px"><a href="mailto:lou@loudenim.com">lou@loudenim.com</a> · <a href="tel:+590690299544">+590 (0)690 299 544</a></p>
  <p>Un modèle vous intéresse&nbsp;? <a href="mailto:lou@loudenim.com?subject=Demande%20mod%C3%A8le%20—%20Catalogue%20IA">lou@loudenim.com</a></p>
  <p>Estimez votre projet&nbsp;: <a href="devis.html" target="_blank" rel="noopener">simulateur de devis en ligne</a></p>
  <p style="margin-top:14px">© Lou Denim — modèles générés par IA, tous droits réservés</p>
<div class="socials"><a href="https://www.instagram.com/loudenim/" target="_blank" rel="noopener" aria-label="Instagram" title="Instagram"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.15 3.23-1.66 4.77-4.92 4.92-1.27.06-1.64.07-4.85.07s-3.58-.01-4.85-.07c-3.26-.15-4.77-1.7-4.92-4.92-.06-1.27-.07-1.64-.07-4.85s.01-3.58.07-4.85C2.38 3.92 3.9 2.38 7.15 2.23 8.42 2.17 8.8 2.16 12 2.16zM12 0C8.74 0 8.33.01 7.05.07 2.7.27.27 2.69.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.2 4.36 2.62 6.78 6.98 6.98 1.28.06 1.69.07 4.95.07s3.67-.01 4.95-.07c4.35-.2 6.78-2.62 6.98-6.98.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95C23.73 2.7 21.31.27 16.95.07 15.67.01 15.26 0 12 0zm0 5.84A6.16 6.16 0 1 0 18.16 12 6.16 6.16 0 0 0 12 5.84zm0 10.15A3.99 3.99 0 1 1 16 12a3.99 3.99 0 0 1-4 3.99zm6.41-11.85a1.44 1.44 0 1 0 1.43 1.44 1.44 1.44 0 0 0-1.43-1.44z"/></svg></a><a href="https://www.tiktok.com/@loudenim" target="_blank" rel="noopener" aria-label="TikTok" title="TikTok"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg></a><a href="https://www.youtube.com/@loudenim" target="_blank" rel="noopener" aria-label="YouTube" title="YouTube"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M23.5 6.19a3.02 3.02 0 0 0-2.12-2.14C19.5 3.55 12 3.55 12 3.55s-7.5 0-9.38.5A3.02 3.02 0 0 0 .5 6.19 31.6 31.6 0 0 0 0 12a31.6 31.6 0 0 0 .5 5.81 3.02 3.02 0 0 0 2.12 2.14c1.88.5 9.38.5 9.38.5s7.5 0 9.38-.5a3.02 3.02 0 0 0 2.12-2.14A31.6 31.6 0 0 0 24 12a31.6 31.6 0 0 0-.5-5.81zM9.55 15.57V8.43L15.82 12z"/></svg></a><a href="https://x.com/loudenim" target="_blank" rel="noopener" aria-label="X" title="X"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M18.9 1.2h3.7l-8.2 9.4L24 22.8h-7.6l-5.9-7.8-6.8 7.8H0l8.8-10L0 1.2h7.8l5.4 7.1zM17.6 20.6h2L6.5 3.3h-2.2z"/></svg></a><a href="https://www.linkedin.com/in/loudenim/" target="_blank" rel="noopener" aria-label="LinkedIn" title="LinkedIn"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.55C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.72C24 .77 23.2 0 22.22 0z"/></svg></a></div></footer>

<div id="lb">
  <div class="inner">
    <div class="top">
      <div><span class="nm-band" id="lb-name"></span><span class="sec-tag" id="lb-sec"></span></div>
      <button onclick="closeLB()">Fermer ✕</button>
    </div>
    <div class="imgs" id="lb-imgs"></div>
    <div class="cta">
      <span>Ce modèle vous plaît&nbsp;? Dites-moi pour quel projet — je vous réponds avec un devis.</span>
      <a id="lb-mail" href="#">Demander ce modèle</a>
    </div>
    <div class="navrow">
      <button onclick="stepLB(-1)">← Précédent</button>
      <button onclick="stepLB(1)">Suivant →</button>
    </div>
  </div>
</div>

<script>
const DATA = __DATA__;
const flat = [];
DATA.forEach(sec => sec.models.forEach(m => flat.push(m)));

const nav = document.getElementById('navlinks');
const main = document.getElementById('main');
DATA.forEach(sec => {
  nav.insertAdjacentHTML('beforeend',
    `<a href="#${sec.key}">${sec.label}</a>`);
  const cards = sec.models.map(m =>
    `<div class="card" onclick="openLB('${m.slug}')">
       <img loading="lazy" src="${m.thumb}" alt="${m.name}">
       <div class="nm">${m.name}</div>
     </div>`).join('');
  main.insertAdjacentHTML('beforeend',
    `<section id="${sec.key}">
       <h2 class="band">${sec.label}<span class="count">${sec.models.length} modèle${sec.models.length>1?'s':''}</span></h2>
       <div class="grid">${cards}</div>
     </section>`);
});

let cur = -1;
function openLB(slug){
  cur = flat.findIndex(m => m.slug === slug);
  renderLB();
  document.getElementById('lb').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function renderLB(){
  const m = flat[cur];
  document.getElementById('lb-name').textContent = m.name;
  document.getElementById('lb-sec').textContent = m.section;
  document.getElementById('lb-mail').href =
    'mailto:lou@loudenim.com?subject=' + encodeURIComponent('Demande modèle — ' + m.name + ' (' + m.section + ')');
  let h = '';
  if (m.sheet) h += `<img src="${m.sheet}" alt="${m.name} — fiche">`;
  if (m.face)  h += m.sheet
      ? `<div class="duo"><img class="face" src="${m.face}" alt="${m.name} — portrait"><div></div></div>`
      : `<div class="duo"><img class="face" src="${m.face}" alt="${m.name} — portrait"><div></div></div>`;
  document.getElementById('lb-imgs').innerHTML = h;
  document.querySelector('#lb .inner').scrollTop = 0;
  window.scrollTo(0,0);
}
function stepLB(d){
  cur = (cur + d + flat.length) % flat.length;
  renderLB();
}
function closeLB(){
  document.getElementById('lb').classList.remove('open');
  document.body.style.overflow = '';
}
document.addEventListener('keydown', e => {
  if (!document.getElementById('lb').classList.contains('open')) return;
  if (e.key === 'Escape') closeLB();
  if (e.key === 'ArrowRight') stepLB(1);
  if (e.key === 'ArrowLeft') stepLB(-1);
});
</script>
<script>(function(){
const cv=document.getElementById('dotfx');if(!cv)return;
const ctx=cv.getContext('2d');const HH=430;
function sz(){cv.width=document.documentElement.clientWidth;cv.height=HH;}
sz();addEventListener('resize',sz);
const SP=34;
function mask(x,y){const cx=cv.width/2;const dx=Math.max(0,Math.abs(x-cx)-150);const dy=Math.max(0,y-(HH-40));return Math.min(1,Math.hypot(dx,dy*2.2)/140);}
function rnd(a,b){return a+Math.random()*(b-a);}
function newPath(side){
  const w=cv.width;
  const x0=side==='L'?0.03:0.56, x1=side==='L'?0.44:0.97;
  const spots=[[w*x0,HH*0.9],[w*x1,HH*0.9],[w*x0,HH*0.1],[w*x1,HH*0.1],[w*(x0+x1)/2,HH*0.5]];
  const i=Math.floor(Math.random()*spots.length);
  let j;do{j=Math.floor(Math.random()*spots.length);}while(j===i);
  const P1=[rnd(w*x0,w*x1),rnd(HH*0.05,HH*0.95)];
  const P2=[rnd(w*x0,w*x1),rnd(HH*0.05,HH*0.95)];
  return {P:[spots[i],P1,P2,spots[j]],dur:rnd(5,7),start:performance.now()};
}
let comets=[newPath('L'),newPath('R')];
comets[1].start=performance.now()-comets[1].dur*500;
function bez(P,u){const a=1-u;return[a*a*a*P[0][0]+3*a*a*u*P[1][0]+3*a*u*u*P[2][0]+u*u*u*P[3][0],a*a*a*P[0][1]+3*a*a*u*P[1][1]+3*a*u*u*P[2][1]+u*u*u*P[3][1]];}
function draw(now){
  ctx.clearRect(0,0,cv.width,cv.height);
  const trail=[];
  comets.forEach((c,idx)=>{
    let tt=(now-c.start)/1000/c.dur;
    if(tt>1.08){comets[idx]=newPath(idx===0?'L':'R');c=comets[idx];tt=0;}
    for(let s=0;s<=Math.min(tt,1);s+=0.02){trail.push({p:bez(c.P,s),decay:Math.max(0,1-(tt-s)*2.2)});}
  });
  for(let x=SP/2;x<cv.width;x+=SP){
    for(let y=SP/2;y<HH-4;y+=SP){
      const m=mask(x,y);if(m<=0.02)continue;
      let lit=0;
      for(const q of trail){if(q.decay<=0)continue;const d=Math.hypot(x-q.p[0],y-q.p[1]);if(d<210){const v=(1-d/210)*q.decay;if(v>lit)lit=v;}}
      const o=(0.14+lit*0.86)*m;
      const sh=Math.round(133-133*lit);
      ctx.beginPath();ctx.arc(x,y,1.1+lit*1.7,0,6.283);
      ctx.fillStyle='rgba('+sh+','+sh+','+Math.round(sh*1.03)+','+o.toFixed(3)+')';
      ctx.fill();
    }
  }
  requestAnimationFrame(draw);
}
requestAnimationFrame(draw);
})();</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
