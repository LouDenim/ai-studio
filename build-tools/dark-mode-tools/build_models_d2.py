import re, json
A = json.load(open('/root/homepage-mockups/assets.json'))
M = json.load(open('/root/homepage-mockups/model_assets.json'))

# real catalogue data (FR) + EN labels — seeded ONCE from the original white catalogue
# (pre-dark-redesign snapshot), NOT from modeles.html/models-en.html directly: those now
# contain this script's own dark-design OUTPUT, which has no embedded `const DATA = [...]`
# block, so reading them here would fail (or silently go stale) on every later rebuild.
htmlfr = open('/root/backup_predeploy_snapshot/modeles.html').read()
DATA = json.loads(re.search(r'const DATA = (\[.*?\}\];)', htmlfr, re.S).group(1)[:-1])
htmlen = open('/root/backup_predeploy_snapshot/models-en.html').read()
DATA_EN = json.loads(re.search(r'const DATA = (\[.*?\}\];)', htmlen, re.S).group(1)[:-1])
EN_LABEL = {s['key']: s['label'] for s in DATA_EN}

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600;700;800&display=swap');
:root{--pink:#E7549F;--pink2:#ff7fc0}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Jost',sans-serif;background:#0a0a0c;color:#fff;-webkit-font-smoothing:antialiased;overflow-x:hidden}
a{color:inherit;text-decoration:none}
"""

css_d = """
header{position:sticky;top:0;z-index:30;background:#0a0a0c}
.hbar{max-width:1220px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;padding:22px 28px;gap:20px}
.brand{display:flex;align-items:center;gap:14px}
.brand span{font-size:15px;letter-spacing:.16em;font-weight:600;color:var(--pink2)}
nav{display:flex;gap:22px;align-items:center;flex-wrap:wrap}
nav a{font-size:14px;letter-spacing:.06em;color:#d8d8dc;white-space:nowrap}
nav a:hover,nav a.on{color:var(--pink2)}
.langs{display:flex;gap:6px}
.langs a{font-size:11px;letter-spacing:.1em;border:1px solid var(--pink2);color:var(--pink2);padding:5px 11px;border-radius:999px}
.langs a.on{background:var(--pink2);color:#0a0a0c;border-color:var(--pink2)}

.glowwrap{position:relative;padding:0 28px 12px;text-align:center;overflow:hidden}
#dotfx{position:absolute;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none}
@media (prefers-reduced-motion: reduce){#dotfx{display:none}}
.masthead{position:relative;z-index:2;display:flex;flex-direction:column;align-items:center;padding:26px 0 0}
.masthead .mlogo{height:136px;filter:brightness(0) invert(1);margin-bottom:2px}
.masthead .mrole{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--pink2);font-weight:500}
.pagehead{position:relative;z-index:2;max-width:760px;margin:0 auto}
.docband{position:relative;z-index:2;display:inline-block;background:var(--pink);color:#fff;padding:13px 42px;
  border-radius:999px;margin-top:26px;font-size:19px;letter-spacing:.28em;text-transform:uppercase;font-weight:600;
  box-shadow:0 8px 30px rgba(231,84,159,.28)}
.pagehead p{position:relative;max-width:640px;margin:20px auto 0;font-size:14.5px;color:#c7c7ce;font-weight:300;line-height:1.6;
  opacity:0;transform:translateY(10px);transition:opacity 1.1s ease,transform 1.1s ease}
.pagehead p.in{opacity:1;transform:translateY(0)}

.catnav{position:sticky;top:66px;z-index:20;background:rgba(10,10,12,.9);backdrop-filter:blur(8px)}
.catnav .inner{max-width:1180px;margin:0 auto;padding:22px 28px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.catnav a{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:#c7c7ce;padding:7px 16px;
  border:1px solid rgba(255,255,255,.14);border-radius:999px;transition:.15s}
.catnav a:hover{border-color:var(--pink2);color:var(--pink2)}

section{max-width:1180px;margin:0 auto;padding:0 28px;scroll-margin-top:120px}
.band{display:flex;justify-content:space-between;align-items:center;background:var(--pink);color:#fff;
  padding:12px 22px;border-radius:10px;margin-top:46px}
section:first-of-type .band{margin-top:18px}
.band h2{font-size:14px;letter-spacing:.3em;text-transform:uppercase;font-weight:600;color:#fff}
.band .count{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.85)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:16px;margin-top:20px}
.card{cursor:pointer;border-radius:14px;overflow:hidden;border:1px solid rgba(255,255,255,.12);
  background:#141418;transition:.15s;position:relative}
.card:hover{border-color:var(--pink2);transform:translateY(-2px)}
.card img{width:100%;aspect-ratio:3/4;object-fit:cover;display:block;opacity:.94}
.card:hover img{opacity:1}
.card .nm{position:absolute;left:0;right:0;bottom:0;padding:14px 12px 9px;font-size:12px;letter-spacing:.14em;
  text-transform:uppercase;text-align:center;background:linear-gradient(to top,rgba(0,0,0,.82),rgba(0,0,0,0))}

footer{position:relative;z-index:2;text-align:center;padding:44px 28px 30px;margin-top:56px;font-size:11px;color:#8a8a92;
  letter-spacing:.1em;text-transform:uppercase}
footer a{color:#c7c7ce}
footer a:hover{color:var(--pink2)}
.social{display:flex;justify-content:center;align-items:center;gap:20px;margin-top:16px}
.social a{color:#8a8a92;display:inline-flex;line-height:0}
.social a:hover{color:var(--pink2)}
.social svg{width:16px;height:16px;fill:currentColor}

/* lightbox */
#lb{position:fixed;inset:0;background:rgba(6,6,8,.97);z-index:60;display:none;overflow-y:auto}
#lb.open{display:block}
#lb .inner{max-width:1040px;margin:0 auto;padding:78px 28px 60px}
#lb .lbtop{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:22px}
#lb .lbtop h3{font-size:30px;font-weight:700}
#lb .lbtop .sec{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--pink2);margin-top:4px}
#lb .lbimgs img{width:100%;border-radius:14px;display:block;margin-bottom:16px;border:1px solid rgba(255,255,255,.1)}
#lb .duo{display:grid;grid-template-columns:minmax(0,360px) 1fr;gap:16px;align-items:start}
#lb .duo .side{font-size:13px;font-weight:300;color:#c7c7ce;line-height:1.6;padding:6px 4px}
#lb .lbclose{position:fixed;top:20px;right:24px;z-index:2;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.25);
  color:#fff;font-size:12px;letter-spacing:.12em;text-transform:uppercase;padding:9px 18px;border-radius:999px;cursor:pointer}
#lb .lbclose:hover{border-color:var(--pink2);color:var(--pink2)}
#lb .lbnav{position:fixed;top:20px;left:24px;z-index:2;display:flex;gap:8px}
#lb .lbnav button{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.25);color:#fff;font-size:12px;
  letter-spacing:.1em;text-transform:uppercase;padding:9px 16px;border-radius:999px;cursor:pointer}
#lb .lbnav button:hover{border-color:var(--pink2);color:var(--pink2)}
#lb .lbcta{margin-top:8px;display:inline-block;border:1px solid rgba(255,255,255,.25);padding:11px 22px;border-radius:999px;
  font-size:12px;letter-spacing:.12em;text-transform:uppercase}
#lb .lbcta:hover{border-color:var(--pink2);color:var(--pink2)}
"""

# --- Hero dot animation (same quiet calibration as the homepage) ----------
DOTFX_JS = r"""
(function(){
var wrap=document.querySelector('.glowwrap'); if(!wrap) return;
var cv=document.getElementById('dotfx'); if(!cv) return;
var ctx=cv.getContext('2d');
var W=0,H=0,BH=400,fadeStart=240,fadeEnd=420,zones=[];
function measure(){
  var r=wrap.getBoundingClientRect();
  W=Math.round(r.width); H=Math.round(r.height);
  cv.width=W; cv.height=H;
  var mh=wrap.querySelector('.masthead');
  var mb= mh ? (mh.getBoundingClientRect().bottom - r.top) : H*0.34;
  fadeStart=mb+14; fadeEnd=mb+150; BH=fadeEnd;
  zones=[];
  wrap.querySelectorAll('.docband,.pagehead p,.mrole').forEach(function(el){
    var b=el.getBoundingClientRect();
    zones.push({cx:b.left+b.width/2-r.left, cy:b.top+b.height/2-r.top, rx:b.width/2, ry:b.height/2});
  });
}
measure(); addEventListener('resize',measure);
setTimeout(measure,300); setTimeout(measure,1000);
function rnd(a,b){return a+Math.random()*(b-a);}
function env(x,y){
  var t=Math.min(1,Math.abs(x-W/2)/(W/2));
  var edge=Math.pow(t,1.6);
  var fe=fadeEnd+(H-fadeEnd)*edge;
  var fs=fadeStart+(H*0.55-fadeStart)*edge;
  if(y<=fs)return 1; if(y>=fe)return 0; return 1-(y-fs)/(fe-fs);
}
function protectGlow(x,y){
  var p=1;
  for(var k=0;k<zones.length;k++){
    var z=zones[k];
    var nx=(x-z.cx)/(z.rx+55), ny=(y-z.cy)/(z.ry+26);
    var d=Math.sqrt(nx*nx+ny*ny);
    var f=Math.min(1,Math.max(0,(d-1)/0.8));
    if(f<p)p=f;
  }
  return p;
}
var SP=32;
function makeSide(side){
  var spin=side==='L'?-1:1;
  var spd=spin*rnd(0.13,0.17);
  var cxF=side==='L'?rnd(0.24,0.31):rnd(0.69,0.76);
  return [0,1].map(function(i){return {
    cxF:cxF, cyF:rnd(0.24,0.36),
    rxF:rnd(0.34,0.44), ryF:rnd(0.34,0.52),
    ang0:i*Math.PI+rnd(-0.15,0.15), angSpd:spd,
    h2Amp:rnd(0.05,0.10), h2Mult:rnd(2.0,2.6)*Math.sign(spd), h2Ph:rnd(0,6.283),
    v2Amp:rnd(0.04,0.08), v2Mult:rnd(1.5,2.0)*Math.sign(spd), v2Ph:rnd(0,6.283),
    t0:performance.now()
  };});
}
var comets=makeSide('R').concat(makeSide('L'));
function pos(c,th){
  var x=W*c.cxF + W*c.rxF*Math.cos(th) + W*c.h2Amp*Math.cos(th*c.h2Mult+c.h2Ph);
  var y=BH*c.cyF + BH*c.ryF*Math.sin(th) + BH*c.v2Amp*Math.sin(th*c.v2Mult+c.v2Ph);
  return [x,y];
}
var TRAIL=30, DTH=0.05, HIT=150;
function draw(now){
  ctx.clearRect(0,0,W,H);
  var trail=[];
  for(var ci=0;ci<comets.length;ci++){
    var c=comets[ci];
    var th=c.ang0+(now-c.t0)/1000*c.angSpd;
    for(var k=0;k<TRAIL;k++){ trail.push({p:pos(c,th-k*DTH), decay:Math.max(0,1-k/TRAIL)}); }
  }
  for(var x=SP/2;x<W;x+=SP){
    for(var y=SP/2;y<H;y+=SP){
      var e=env(x,y); if(e<=0.01) continue;
      var lit=0;
      for(var t=0;t<trail.length;t++){
        var q=trail[t]; if(q.decay<=0) continue;
        var dx=x-q.p[0], dy=y-q.p[1];
        var d=Math.sqrt(dx*dx+dy*dy);
        if(d<HIT){ var v=(1-d/HIT)*q.decay; if(v>lit) lit=v; }
      }
      var glow=lit*protectGlow(x,y);
      var o=(0.12+glow*0.72)*e;
      if(o<=0.012) continue;
      var R=Math.round(140+(246-140)*glow);
      var G=Math.round(140+(122-140)*glow);
      var B=Math.round(150+(184-150)*glow);
      var rad=1.0+glow*2.2;
      ctx.beginPath(); ctx.arc(x,y,rad,0,6.283);
      ctx.fillStyle='rgba('+R+','+G+','+B+','+o.toFixed(3)+')'; ctx.fill();
    }
  }
  requestAnimationFrame(draw);
}
requestAnimationFrame(draw);
})();
"""

# --- Intro sentence: fade in and stay (deliberately NOT the homepage typewriter --
# Lou wants Models/Portfolio to read differently from the homepage: no typing effect here,
# just a soft fade+lift on scroll-into-view that settles and holds.
TYPE_JS = r"""
(function(){
var p=document.querySelector('.pagehead p'); if(!p) return;
if(matchMedia('(prefers-reduced-motion: reduce)').matches){ p.classList.add('in'); return; }
function run(){ p.classList.add('in'); }
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ io.disconnect(); run(); } }); },{threshold:0.6});
  io.observe(p);
}else{ run(); }
})();
"""

IG_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.9.2 2.3.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.3 1.1.4 2.3.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.2 1.9-.4 2.3-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1.1.3-2.3.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.9-.2-2.3-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.3-1.1-.4-2.3-.1-1.3-.1-1.7-.1-4.9s0-3.6.1-4.9c.1-1.2.2-1.9.4-2.3.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1.1-.3 2.3-.4 1.3-.1 1.7-.1 4.9-.1M12 0C8.7 0 8.3 0 7 .1c-1.3.1-2.2.3-3 .6-.8.3-1.5.7-2.2 1.4C1.1 2.8.7 3.5.4 4.3c-.3.8-.5 1.7-.6 3C-.1 8.3-.1 8.7-.1 12s0 3.7.1 5c.1 1.3.3 2.2.6 3 .3.8.7 1.5 1.4 2.2.7.7 1.4 1.1 2.2 1.4.8.3 1.7.5 3 .6 1.3.1 1.7.1 5 .1s3.7 0 5-.1c1.3-.1 2.2-.3 3-.6.8-.3 1.5-.7 2.2-1.4.7-.7 1.1-1.4 1.4-2.2.3-.8.5-1.7.6-3 .1-1.3.1-1.7.1-5s0-3.7-.1-5c-.1-1.3-.3-2.2-.6-3-.3-.8-.7-1.5-1.4-2.2C21.2 1.1 20.5.7 19.7.4c-.8-.3-1.7-.5-3-.6C15.7 0 15.3 0 12 0z"/><path d="M12 5.8A6.2 6.2 0 1 0 18.2 12 6.2 6.2 0 0 0 12 5.8zm0 10.2A4 4 0 1 1 16 12a4 4 0 0 1-4 4z"/><circle cx="18.4" cy="5.6" r="1.4"/></svg>'
LI_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.03-1.85-3.03-1.85 0-2.14 1.45-2.14 2.94v5.66H9.34V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.07 2.07 0 1 1 0-4.13 2.07 2.07 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45z"/></svg>'
X_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>'
YT_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.4 3.5 12 3.5 12 3.5s-7.4 0-9.4.6A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c2 .6 9.4.6 9.4.6s7.4 0 9.4-.6a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8zM9.6 15.5V8.5l6.3 3.5-6.3 3.5z"/></svg>'
FB_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M13.5 21v-8.1h2.7l.4-3.2h-3.1V7.7c0-.9.3-1.6 1.6-1.6h1.6V3.3C16.4 3.2 15.3 3 14 3c-2.6 0-4.4 1.6-4.4 4.5v2.2H6.9v3.2h2.7V21h3.9z"/></svg>'
TT_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M16.6 5.82c-.86-.9-1.34-2.07-1.34-3.32h-3.02v13.44c0 1.5-1.22 2.72-2.72 2.72-1.5 0-2.72-1.22-2.72-2.72 0-1.5 1.22-2.72 2.72-2.72.28 0 .55.04.8.12V10.3a5.7 5.7 0 0 0-.8-.06 5.74 5.74 0 1 0 5.74 5.74V8.86a8.3 8.3 0 0 0 4.86 1.56V7.4a5.34 5.34 0 0 1-3.52-1.58z"/></svg>'
SOCIAL_HTML = f"""<div class="social">
    <a href="https://www.instagram.com/loudenim" target="_blank" rel="noopener" aria-label="Instagram">{IG_SVG}</a>
    <a href="https://www.linkedin.com/in/loudenim" target="_blank" rel="noopener" aria-label="LinkedIn">{LI_SVG}</a>
    <a href="https://x.com/loudenim" target="_blank" rel="noopener" aria-label="X">{X_SVG}</a>
    <a href="https://www.youtube.com/@loudenim" target="_blank" rel="noopener" aria-label="YouTube">{YT_SVG}</a>
    <a href="https://www.tiktok.com/@loudenim" target="_blank" rel="noopener" aria-label="TikTok">{TT_SVG}</a>
  </div>"""

def build(lang):
    fr = (lang == 'fr')
    nav_home = "Accueil" if fr else "Home"
    nav_grille = "Grille tarifaire" if fr else "Rate card"
    nav_sim = "Simulateur" if fr else "Simulator"
    nav_brief = "Brief vidéo" if fr else "Video brief"
    nav_portfolio = "Portfolio"
    nav_models = "Mod&egrave;les" if fr else "Models"
    role = "Directeur artistique IA" if fr else "AI Creative Director"
    h1 = "Catalogue mod&egrave;les IA" if fr else "AI model catalogue"
    intro = ("Des mod&egrave;les g&eacute;n&eacute;r&eacute;s en IA, disponibles pour vos campagnes. "
             "Chaque mod&egrave;le garde une identit&eacute; coh&eacute;rente d&rsquo;une image &agrave; l&rsquo;autre "
             "et peut &ecirc;tre mis en sc&egrave;ne avec votre produit.") if fr else \
            ("AI generated models, available for your campaigns. Each model keeps a consistent identity from one image to the next "
             "and can be staged with your product.")
    home_href = "mockup-d20.html" if fr else "mockup-d20-en.html"
    portfolio_href = "mockup-travail-d2.html" if fr else "mockup-travail-d2-en.html"
    self_href = "mockup-models-d2.html" if fr else "mockup-models-d2-en.html"
    lang_href = "mockup-models-d2-en.html" if fr else "mockup-models-d2.html"
    grille_href = "mockup-grille-preview.html" if fr else "mockup-grille-en-preview.html"
    devis_href = "mockup-devis-preview.html" if fr else "mockup-devis-en-preview.html"
    brief_href = "mockup-brief-preview.html" if fr else "mockup-brief-en-preview.html"
    title = ("LOU DENIM — Catalogue Modèles IA" if fr else "LOU DENIM — AI Model Catalogue")
    lang_fr_on = "on" if fr else ""
    lang_en_on = "" if fr else "on"
    photo = "Photographie" if fr else "Photography"
    foot = (f'<div class="footline"><a href="mailto:lou@loudenim.com">lou@loudenim.com</a> &middot; '
            f'<a href="tel:+590690299544">+590&nbsp;(0)690&nbsp;299&nbsp;544</a> &middot; '
            f'<a href="https://www.loudenim.com" target="_blank" rel="noopener">{photo}&nbsp;: loudenim.com</a></div>{SOCIAL_HTML}')

    # category pills + sections
    cat_pills = ""
    sections = ""
    for sec in DATA:
        label = sec['label'] if fr else EN_LABEL[sec['key']]
        n = len(sec['models'])
        word = ("mod&egrave;le" + ("s" if n > 1 else "")) if fr else ("model" + ("s" if n > 1 else ""))
        cat_pills += f'<a href="#{sec["key"]}">{label}</a>'
        cards = ""
        for mo in sec['models']:
            thumb = M[mo['slug']+'-thumb']
            cards += (f'<div class="card" onclick="openLB(\'{mo["slug"]}\')">'
                      f'<img src="{thumb}" alt="{mo["name"]}">'
                      f'<div class="nm">{mo["name"]}</div></div>')
        sections += (f'<section id="{sec["key"]}"><div class="band"><h2>{label}</h2>'
                     f'<span class="count">{n} {word}</span></div><div class="grid">{cards}</div></section>')

    # flat model list for lightbox JS (slug, name, section label, sheet, face)
    flat = []
    for sec in DATA:
        seclabel = sec['label'] if fr else EN_LABEL[sec['key']]
        for mo in sec['models']:
            flat.append({"slug": mo['slug'], "name": mo['name'], "section": seclabel,
                         "sheet": M[mo['slug']+'-sheet'], "face": M[mo['slug']+'-face']})
    flat_json = json.dumps(flat)
    cta_txt = "Demander ce mod&egrave;le" if fr else "Request this model"
    subj = "Demande mod&egrave;le" if fr else "Model request"
    sheet_cap = "Fiche personnage : plans larges, tenues, expressions." if fr else "Character sheet: wide shots, outfits, expressions."
    close_txt = "Fermer ✕" if fr else "Close ✕"

    page = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{BASE_CSS}
{css_d}
</style>
</head>
<body>
<header><div class="hbar">
  <nav>
    <a href="{home_href}">{nav_home}</a>
    <a href="{portfolio_href}">{nav_portfolio}</a>
    <a class="on" href="{self_href}">{nav_models}</a>
    <a href="{grille_href}">{nav_grille}</a>
    <a href="{devis_href}">{nav_sim}</a>
    <a href="{brief_href}">{nav_brief}</a>
  </nav>
  <div class="brand"><span>AI STUDIO</span>
    <div class="langs"><a class="{lang_fr_on}" href="{self_href if fr else lang_href}">FR</a><a class="{lang_en_on}" href="{lang_href if fr else self_href}">EN</a></div>
  </div>
</div></header>

<div class="glowwrap">
  <canvas id="dotfx"></canvas>
  <a href="{home_href}" class="masthead">
    <img class="mlogo" src="{A['logo']}">
    <div class="mrole">{role}</div>
  </a>
  <div class="pagehead">
    <div class="docband">{h1}</div>
    <p>{intro}</p>
  </div>
</div>

<div class="catnav"><div class="inner">{cat_pills}</div></div>

{sections}

<footer>{foot}</footer>

<div id="lb">
  <div class="lbnav"><button onclick="stepLB(-1)">&larr;</button><button onclick="stepLB(1)">&rarr;</button></div>
  <button class="lbclose" onclick="closeLB()">{close_txt}</button>
  <div class="inner">
    <div class="lbtop"><div><h3 id="lb-name"></h3><div class="sec" id="lb-sec"></div></div></div>
    <div class="lbimgs" id="lb-imgs"></div>
    <a class="lbcta" id="lb-cta" href="#">{cta_txt}</a>
  </div>
</div>

<script>
const FLAT = {flat_json};
let cur = -1;
function openLB(slug){{
  cur = FLAT.findIndex(m => m.slug === slug);
  renderLB();
  document.getElementById('lb').classList.add('open');
  document.body.style.overflow = 'hidden';
  window.scrollTo(0,0);
}}
function renderLB(){{
  const m = FLAT[cur];
  document.getElementById('lb-name').textContent = m.name;
  document.getElementById('lb-sec').textContent = m.section;
  document.getElementById('lb-cta').href = 'mailto:lou@loudenim.com?subject=' + encodeURIComponent('{subj} — ' + m.name + ' (' + m.section + ')');
  let h = '';
  h += '<img src="' + m.sheet + '" alt="' + m.name + '">';
  h += '<div class="duo"><img src="' + m.face + '" alt="' + m.name + '"><div class="side">{sheet_cap}</div></div>';
  document.getElementById('lb-imgs').innerHTML = h;
  document.querySelector('#lb .inner').scrollTop = 0;
}}
function stepLB(d){{ cur = (cur + d + FLAT.length) % FLAT.length; renderLB(); window.scrollTo(0,0); }}
function closeLB(){{ document.getElementById('lb').classList.remove('open'); document.body.style.overflow=''; }}
document.addEventListener('keydown', e => {{
  if (!document.getElementById('lb').classList.contains('open')) return;
  if (e.key==='Escape') closeLB();
  if (e.key==='ArrowRight') stepLB(1);
  if (e.key==='ArrowLeft') stepLB(-1);
}});
</script>
<script>{TYPE_JS}</script>
<script>{DOTFX_JS}</script>
</body>
</html>"""
    fname = f'mockup-models-d2{"" if fr else "-en"}.html'
    open('/root/homepage-mockups/'+fname,'w').write(page)
    print("built", fname, f"{len(page)/1024/1024:.1f} MB")

build('fr'); build('en')
