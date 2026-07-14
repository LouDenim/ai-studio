import re, json
A = json.load(open('/root/homepage-mockups/assets.json'))

# real video IDs from the production travail.html
htmlfr = open('/root/catalogue-models/travail.html').read()
IDS_169 = re.findall(r'v169" data-id="([^"]+)"', htmlfr)
IDS_916 = re.findall(r'v916" data-id="([^"]+)"', htmlfr)
if not IDS_169:
    IDS_169 = ["f8KkFZHk_38","BTXAdeSvGNo","3FaG_t7ooH4","na6QT4fhOOU","O5xgWge0gjA","NU2DFE3SXqc"]
if not IDS_916:
    IDS_916 = ["UGYX9ExLo04","qnAD9OzUb6o","KxIryljbHVk","LG4u8d-GkKg","GGHXw06kIyQ","Zb2604Me_kI","SOk8ZgUGfU8","8OITHSH83UA"]

# --- Landscape order by Lou (14 Jul): 1-2-4-6-3-8-9-5-7 (read the dup "6" as "5"). All 9 kept. ---
#  1 f8KkFZHk_38  INTENSITY DRIVEN
#  2 BTXAdeSvGNo  MORNING AFTER
#  4 6zJx8hfEUlw  LA DOUCEUR DE LA GUADELOUPE
#  6 3FaG_t7ooH4  JUST BE COOL
#  3 55nJLwmTokc  WATCHED - In cinemas April 26
#  8 O5xgWge0gjA  OUT OF THE OFFICE
#  9 NU2DFE3SXqc  THE UGLY SIDE OF FASHION
#  5 Muy9NOETw5k  THE SNEEZE
#  7 na6QT4fhOOU  THE COMMUTE
IDS_169 = ["f8KkFZHk_38", "BTXAdeSvGNo", "6zJx8hfEUlw", "3FaG_t7ooH4", "55nJLwmTokc",
           "O5xgWge0gjA", "NU2DFE3SXqc", "Muy9NOETw5k", "na6QT4fhOOU"]
# 2 new shorts (9:16, unique — fj9ihwxF0Co was sent twice): appended, cartoon-last still to confirm.
NEW_916 = ["fj9ihwxF0Co", "4RWnzGciM0I"]
IDS_916 = IDS_916 + NEW_916

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

section{max-width:1180px;margin:0 auto;padding:0 28px;}
.band{display:flex;justify-content:space-between;align-items:center;background:var(--pink);color:#fff;
  padding:12px 22px;border-radius:10px;margin-top:46px}
.band h2{font-size:14px;letter-spacing:.3em;text-transform:uppercase;font-weight:600;color:#fff}
.band .stag{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:rgba(255,255,255,.85)}

.vgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:16px;margin-top:20px}
.vgrid.vert{grid-template-columns:repeat(auto-fill,minmax(168px,1fr))}
.vid{position:relative;border-radius:14px;overflow:hidden;aspect-ratio:16/9;display:block;cursor:pointer;
  border:1px solid rgba(255,255,255,.12);transition:.15s;
  background:radial-gradient(130% 150% at 32% 22%, #2a2a30 0%, #131317 55%, #0c0c0f 100%)}
.vid.v916{aspect-ratio:9/16;background:radial-gradient(120% 130% at 50% 28%, #2a2a30 0%, #131317 58%, #0c0c0f 100%)}
.vid:hover{border-color:var(--pink2);transform:translateY(-2px)}
.vid iframe{position:absolute;inset:0;width:100%;height:100%;border:0;z-index:6}
/* --- video lightbox (shorts open big), same system as production travail.html --- */
.lb{position:fixed;inset:0;background:rgba(0,0,0,.92);display:none;align-items:center;justify-content:center;z-index:999}
.lb.on{display:flex}
.lb-inner{position:relative;height:88vh;aspect-ratio:9/16;max-width:94vw;border-radius:14px;overflow:hidden;background:#000}
.lb-inner iframe{width:100%;height:100%;border:0}
.lb-x{position:absolute;top:16px;right:20px;width:46px;height:46px;border-radius:999px;border:0;cursor:pointer;
  background:rgba(255,255,255,.16);color:#fff;font-size:26px;line-height:1;transition:.15s;z-index:1000}
.lb-x:hover{background:var(--pink)}
.vid .play{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:56px;height:56px;border-radius:50%;
  background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.4);display:flex;align-items:center;justify-content:center;
  backdrop-filter:blur(3px);transition:.15s}
.vid:hover .play{background:rgba(231,84,159,.22);border-color:var(--pink2)}
.vid .play svg{width:20px;height:20px;fill:#fff;margin-left:3px}
.vid .fmt{position:absolute;left:14px;top:12px;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;
  color:#c7c7ce;background:rgba(0,0,0,.4);border:1px solid rgba(255,255,255,.18);padding:4px 10px;border-radius:999px}

.note{max-width:1180px;margin:22px auto 0;padding:0 28px;font-size:12px;color:#7a7a82;font-weight:300;text-align:center;font-style:italic}

footer{position:relative;z-index:2;text-align:center;padding:44px 28px 30px;margin-top:56px;font-size:11px;color:#8a8a92;
  letter-spacing:.1em;text-transform:uppercase}
footer a{color:#c7c7ce}
footer a:hover{color:var(--pink2)}
.social{display:flex;justify-content:center;align-items:center;gap:20px;margin-top:16px}
.social a{color:#8a8a92;display:inline-flex;line-height:0}
.social a:hover{color:var(--pink2)}
.social svg{width:16px;height:16px;fill:currentColor}
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

PLAY_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M8 5.5v13l11-6.5z"/></svg>'
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

def vid(vid_id, vertical, fmt):
    cls = "vid v916" if vertical else "vid"
    return (f'<div class="{cls}" data-id="{vid_id}" role="button" tabindex="0" aria-label="Play">'
            f'<span class="fmt">{fmt}</span><span class="play">{PLAY_SVG}</span></div>')

def build(lang):
    fr = (lang == 'fr')
    nav_home = "Accueil" if fr else "Home"
    nav_grille = "Grille tarifaire" if fr else "Rate card"
    nav_sim = "Simulateur" if fr else "Simulator"
    nav_brief = "Brief vidéo" if fr else "Video brief"
    nav_portfolio = "Portfolio"
    nav_models = "Mod&egrave;les" if fr else "Models"
    role = "Directeur artistique IA" if fr else "AI Creative Director"
    h1 = "Portfolio"
    intro = ("Une s&eacute;lection de vid&eacute;os 16:9 et de formats verticaux, cr&eacute;&eacute;s par le studio.") if fr else \
            ("A selection of 16:9 videos and vertical formats, created by the studio.")
    band169 = "Vid&eacute;os 16:9" if fr else "16:9 videos"
    tag169 = "Format paysage" if fr else "Landscape"
    band916 = "Formats verticaux" if fr else "Vertical formats"
    tag916 = "Reels &middot; Stories &middot; Shorts"
    fmt169 = "16:9"
    fmt916 = "9:16"
    note = ("Aper&ccedil;u&nbsp;: les vignettes vid&eacute;o s&rsquo;affichent en direct sur le site publi&eacute; "
            "(chaque case ouvre d&eacute;j&agrave; la vraie vid&eacute;o YouTube).") if fr else \
           ("Preview note: video thumbnails load live on the published site (each tile already opens the real YouTube video).")
    home_href = "mockup-d20.html" if fr else "mockup-d20-en.html"
    models_href = "mockup-models-d2.html" if fr else "mockup-models-d2-en.html"
    self_href = "mockup-travail-d2.html" if fr else "mockup-travail-d2-en.html"
    lang_href = "mockup-travail-d2-en.html" if fr else "mockup-travail-d2.html"
    grille_href = "mockup-grille-preview.html" if fr else "mockup-grille-en-preview.html"
    devis_href = "mockup-devis-preview.html" if fr else "mockup-devis-en-preview.html"
    brief_href = "mockup-brief-preview.html" if fr else "mockup-brief-en-preview.html"
    title = ("LOU DENIM — Le travail en images" if fr else "LOU DENIM — The work")
    lang_fr_on = "on" if fr else ""
    lang_en_on = "" if fr else "on"
    photo = "Photographie" if fr else "Photography"
    foot = (f'<div class="footline"><a href="mailto:lou@loudenim.com">lou@loudenim.com</a> &middot; '
            f'<a href="tel:+590690299544">+590&nbsp;(0)690&nbsp;299&nbsp;544</a> &middot; '
            f'<a href="https://www.loudenim.com" target="_blank" rel="noopener">{photo}&nbsp;: loudenim.com</a></div>{SOCIAL_HTML}')

    grid169 = "".join(vid(v, False, fmt169) for v in IDS_169)
    grid916 = "".join(vid(v, True, fmt916) for v in IDS_916)

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
    <a class="on" href="{self_href}">{nav_portfolio}</a>
    <a href="{models_href}">{nav_models}</a>
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

<section>
  <div class="band"><h2>{band169}</h2><span class="stag">{tag169}</span></div>
  <div class="vgrid">{grid169}</div>
</section>

<section>
  <div class="band"><h2>{band916}</h2><span class="stag">{tag916}</span></div>
  <div class="vgrid vert">{grid916}</div>
</section>

<div class="note">{note}</div>

<footer>{foot}</footer>

<div id="lb" class="lb" aria-hidden="true"><button class="lb-x" id="lbx" aria-label="Fermer">&times;</button><div class="lb-inner" id="lbInner"></div></div>
<script>
function ytIframe(id){{return '<iframe src="https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0&playsinline=1" title="Lou Denim" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';}}
var lb=document.getElementById('lb'), lbInner=document.getElementById('lbInner');
function openLB(id){{lbInner.innerHTML=ytIframe(id);lb.classList.add('on');lb.setAttribute('aria-hidden','false');document.body.style.overflow='hidden';}}
function closeLB(){{lb.classList.remove('on');lb.setAttribute('aria-hidden','true');lbInner.innerHTML='';document.body.style.overflow='';}}
document.getElementById('lbx').addEventListener('click',closeLB);
lb.addEventListener('click',function(e){{if(e.target===lb)closeLB();}});
document.addEventListener('keydown',function(e){{if(e.key==='Escape')closeLB();}});
document.querySelectorAll('.vid').forEach(function(v){{
  function go(){{
    var id=v.dataset.id;
    if(v.classList.contains('v916')){{openLB(id);return;}}      /* shorts -> big lightbox */
    if(v.querySelector('iframe'))return;
    v.innerHTML=ytIframe(id);                                    /* landscape -> plays inline in the tile */
  }}
  v.addEventListener('click',go);
  v.addEventListener('keydown',function(e){{if(e.key==='Enter'||e.key===' '){{e.preventDefault();go();}}}});
}});
</script>
<script>{TYPE_JS}</script>
<script>{DOTFX_JS}</script>
</body>
</html>"""
    fname = f'mockup-travail-d2{"" if fr else "-en"}.html'
    open('/root/homepage-mockups/'+fname,'w').write(page)
    print("built", fname, f"({len(IDS_169)} x 16:9, {len(IDS_916)} x 9:16)")

build('fr'); build('en')
