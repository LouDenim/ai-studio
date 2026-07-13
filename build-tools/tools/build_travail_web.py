#!/usr/bin/env python3
"""Génère travail.html (FR) + travail-en.html (EN) — « Le travail en images » / "The work".
16 vidéos YouTube en façade click-to-play (youtube-nocookie), zéro poids d'hébergement.
Usage: python3 build_travail_web.py <out_dir>
NOTE: template en chaîne SIMPLE (pas f-string) — tokens __XXX__ remplacés. Accolades normales."""
import base64, sys, os

SKILL = "/root/.claude/skills/pdf-lou"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/root/catalogue-models"

logo = "data:image/svg+xml;base64," + base64.b64encode(open(f"{SKILL}/assets/lou-denim-logo.svg","rb").read()).decode()

FILMS  = ["f8KkFZHk_38","BTXAdeSvGNo","3FaG_t7ooH4","na6QT4fhOOU","O5xgWge0gjA","NU2DFE3SXqc"]
SHORTS = ["UGYX9ExLo04","qnAD9OzUb6o","KxIryljbHVk","LG4u8d-GkKg","GGHXw06kIyQ","Zb2604Me_kI",
          "SOk8ZgUGfU8","8OITHSH83UA","fdYbw6vgS1Y","la-zG8RK4eU"]

SOCIALS = '<div class="socials"><a href="https://www.instagram.com/loudenim/" target="_blank" rel="noopener" aria-label="Instagram" title="Instagram"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.15 3.23-1.66 4.77-4.92 4.92-1.27.06-1.64.07-4.85.07s-3.58-.01-4.85-.07c-3.26-.15-4.77-1.7-4.92-4.92-.06-1.27-.07-1.64-.07-4.85s.01-3.58.07-4.85C2.38 3.92 3.9 2.38 7.15 2.23 8.42 2.17 8.8 2.16 12 2.16zM12 0C8.74 0 8.33.01 7.05.07 2.7.27.27 2.69.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.2 4.36 2.62 6.78 6.98 6.98 1.28.06 1.69.07 4.95.07s3.67-.01 4.95-.07c4.35-.2 6.78-2.62 6.98-6.98.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95C23.73 2.7 21.31.27 16.95.07 15.67.01 15.26 0 12 0zm0 5.84A6.16 6.16 0 1 0 18.16 12 6.16 6.16 0 0 0 12 5.84zm0 10.15A3.99 3.99 0 1 1 16 12a3.99 3.99 0 0 1-4 3.99zm6.41-11.85a1.44 1.44 0 1 0 1.43 1.44 1.44 1.44 0 0 0-1.43-1.44z"/></svg></a><a href="https://www.tiktok.com/@loudenim" target="_blank" rel="noopener" aria-label="TikTok" title="TikTok"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg></a><a href="https://www.youtube.com/@loudenim" target="_blank" rel="noopener" aria-label="YouTube" title="YouTube"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M23.5 6.19a3.02 3.02 0 0 0-2.12-2.14C19.5 3.55 12 3.55 12 3.55s-7.5 0-9.38.5A3.02 3.02 0 0 0 .5 6.19 31.6 31.6 0 0 0 0 12a31.6 31.6 0 0 0 .5 5.81 3.02 3.02 0 0 0 2.12 2.14c1.88.5 9.38.5 9.38.5s7.5 0 9.38-.5a3.02 3.02 0 0 0 2.12-2.14A31.6 31.6 0 0 0 24 12a31.6 31.6 0 0 0-.5-5.81zM9.55 15.57V8.43L15.82 12z"/></svg></a><a href="https://x.com/loudenim" target="_blank" rel="noopener" aria-label="X" title="X"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M18.9 1.2h3.7l-8.2 9.4L24 22.8h-7.6l-5.9-7.8-6.8 7.8H0l8.8-10L0 1.2h7.8l5.4 7.1zM17.6 20.6h2L6.5 3.3h-2.2z"/></svg></a><a href="https://www.linkedin.com/in/loudenim/" target="_blank" rel="noopener" aria-label="LinkedIn" title="LinkedIn"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.55C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.72C24 .77 23.2 0 22.22 0z"/></svg></a></div>'

PLAY = '<span class="play" aria-hidden="true"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M8 5.5v13l11-6.5z"/></svg></span>'
EXPAND = '<span class="expand" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3H3v6M15 21h6v-6M21 9V3h-6M3 15v6h6"/></svg></span>'

def tile(vid, vertical, label_play):
    if vertical:
        img = ('<img src="https://i.ytimg.com/vi/%s/oar2.jpg" alt="" loading="lazy" '
               'onerror="this.onerror=null;this.src=\'https://i.ytimg.com/vi/%s/hqdefault.jpg\'">' % (vid, vid))
        cls = "vid v916"
        extra = ""
    else:
        img = '<img src="https://i.ytimg.com/vi/%s/hqdefault.jpg" alt="" loading="lazy">' % vid
        cls = "vid v169"
        extra = ""
    return ('<div class="%s" data-id="%s" role="button" tabindex="0" aria-label="%s">%s%s%s</div>'
            % (cls, vid, label_play, img, PLAY, extra))

T = {
 "fr": dict(
    lang="fr", other="travail-en.html", self_="travail.html",
    title="LOU DENIM — Le travail en images",
    sub="Directeur artistique IA",
    band="Le travail en images", band_small="Vidéos IA",
    intro="Une sélection de vidéos 16:9 et de formats verticaux, créés par le studio.",
    s1="Vidéos 16:9", s1tag="Format paysage",
    s2="Formats verticaux", s2tag="Reels · Stories · Shorts",
    play="Lire la vidéo",
    cta="Un projet ? <a href=\"devis.html\">Estimez-le en ligne</a> ou écrivez à <a href=\"mailto:lou@loudenim.com\">lou@loudenim.com</a>",
    foot="© Lou Denim — Guadeloupe · <a href=\"https://www.loudenim.com\" target=\"_blank\" rel=\"noopener\">Photographie&nbsp;: loudenim.com</a>",
    yt="Voir la chaîne YouTube",
 ),
 "en": dict(
    lang="en", other="travail.html", self_="travail-en.html",
    title="LOU DENIM — The work",
    sub="AI Creative Director",
    band="The work", band_small="AI videos",
    intro="A selection of 16:9 videos and vertical formats, created by the studio.",
    s1="16:9 videos", s1tag="Landscape",
    s2="Vertical formats", s2tag="Reels · Stories · Shorts",
    play="Play video",
    cta="A project? <a href=\"devis-en.html\">Estimate it online</a> or write to <a href=\"mailto:lou@loudenim.com\">lou@loudenim.com</a>",
    foot="© Lou Denim — Guadeloupe · <a href=\"https://www.loudenim.com\" target=\"_blank\" rel=\"noopener\">Photography&nbsp;: loudenim.com</a>",
    yt="See the YouTube channel",
 ),
}

TPL = """<!DOCTYPE html>
<html lang="__LANG__">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title><meta name="robots" content="noindex">
<style>
@import url('https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&display=swap');
:root{--blush:#FBF1EF;--blush2:#F5E3DF;--blush3:#EBC9C3;--ink:#000;--grey:#666}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Jost',sans-serif;background:#fff;color:var(--ink);position:relative;line-height:1.55}
.wrap{max-width:900px;margin:0 auto;padding:0 20px 80px}
header{padding:86px 0 26px;text-align:center}
header img{height:86px;margin-bottom:8px}
.rule{width:300px;max-width:70%;height:1px;background:#000;margin:0 auto 10px}
.sub{font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:var(--ink)}
.doc-band{display:inline-block;background:#000;color:#fff;padding:10px 34px;border-radius:999px;margin-top:24px;
  font-size:15px;letter-spacing:.32em;text-transform:uppercase;font-weight:500}
.doc-band small{display:block;font-size:10px;letter-spacing:.22em;color:#e8cfca;font-weight:400}
.langs{display:flex;gap:10px;justify-content:center;margin-top:20px}
.langs a{font-size:11px;letter-spacing:.18em;text-transform:uppercase;text-decoration:none;
  padding:6px 16px;border-radius:999px;border:1px solid #E7549F;background:#fff;color:#E7549F;transition:.15s}
.langs a:hover{background:#E7549F;color:#fff}
.langs a.on{background:#E7549F;color:#fff}
.intro{max-width:560px;margin:18px auto 0;text-align:center;font-size:13.5px;font-weight:300;color:#333}
h2.band{background:#000;color:#fff;font-size:13px;font-weight:500;letter-spacing:.28em;text-transform:uppercase;
  padding:9px 18px;border-radius:10px;margin:34px 0 16px;display:flex;justify-content:space-between;align-items:center}
h2.band .tag{font-size:10px;letter-spacing:.14em;color:var(--blush3)}
.grid169{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}
.grid916{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px}
.vid{position:relative;overflow:hidden;border-radius:14px;background:#0b0b0c;border:1px solid #000;cursor:pointer;
  transition:transform .12s, box-shadow .12s, border-color .12s}
.vid:hover{transform:translateY(-3px);border-color:#E7549F;box-shadow:0 10px 26px rgba(231,84,159,.14)}
.v169{aspect-ratio:16/9}
.v916{aspect-ratio:9/16}
.vid img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;opacity:.93}
.vid iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.play{position:absolute;inset:0;margin:auto;width:52px;height:52px;border-radius:999px;background:rgba(255,255,255,.92);
  display:flex;align-items:center;justify-content:center;transition:.15s;pointer-events:none}
.play svg{width:22px;height:22px;fill:#000;margin-left:3px;transition:.15s}
.vid:hover .play{background:#E7549F}
.vid:hover .play svg{fill:#fff}
.lb{position:fixed;inset:0;background:rgba(0,0,0,.9);display:none;align-items:center;justify-content:center;z-index:999}
.lb.on{display:flex}
.lb-inner{position:relative;height:88vh;aspect-ratio:9/16;max-width:94vw;border-radius:14px;overflow:hidden;background:#000}
.lb-inner iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.lb-x{position:absolute;top:16px;right:20px;width:46px;height:46px;border-radius:999px;border:0;cursor:pointer;
  background:rgba(255,255,255,.16);color:#fff;font-size:26px;line-height:1;transition:.15s;z-index:1000}
.lb-x:hover{background:#E7549F}
.ytline{margin-top:26px;text-align:center;font-size:11px;letter-spacing:.14em;text-transform:uppercase}
.ytline a{color:#000;border-bottom:1px solid #000;padding-bottom:2px;text-decoration:none;transition:.15s}
.ytline a:hover{color:#E7549F;border-bottom-color:#E7549F}
footer{margin-top:44px;text-align:center;font-size:11px;color:var(--grey);letter-spacing:.12em;text-transform:uppercase}
footer a{color:#000}
#dotfx{position:absolute;top:0;left:0;width:100%;height:440px;z-index:-1;pointer-events:none}
@media (prefers-reduced-motion: reduce){#dotfx{display:none}}
.socials{display:flex;gap:20px;justify-content:center;margin-top:16px}.socials a{color:#8a8f93;transition:color .15s}.socials a:hover{color:#E7549F}.socials svg{height:18px;width:18px;fill:currentColor;display:block}
</style>
</head>
<body>
<canvas id="dotfx"></canvas>
<div class="wrap">
<header>
  <a href="index.html"><img src="__LOGO__" alt="Lou Denim"></a>
  <div class="rule"></div>
  <p class="sub">__SUB__</p>
  <div><span class="doc-band">__BAND__<small>__BAND_SMALL__</small></span></div>
  <div class="langs">__LANGBTNS__</div>
  <p class="intro">__INTRO__</p>
</header>

<h2 class="band">__S1__ <span class="tag">__S1TAG__</span></h2>
<div class="grid169">__FILMS__</div>

<h2 class="band">__S2__ <span class="tag">__S2TAG__</span></h2>
<div class="grid916">__SHORTS__</div>

<p class="ytline"><a href="https://www.youtube.com/@loudenim" target="_blank" rel="noopener">__YT__ →</a></p>

<footer>
  <p style="margin-bottom:6px"><a href="mailto:lou@loudenim.com">lou@loudenim.com</a> · <a href="tel:+590690299544">+590 (0)690 299 544</a> · loudenim.com</p>
  <p>__CTA__</p>
  <p style="margin-top:6px">__FOOT__</p>
__SOCIALS__</footer>
</div>
<div id="lb" class="lb" aria-hidden="true"><button class="lb-x" id="lbx" aria-label="Fermer">&times;</button><div class="lb-inner" id="lbInner"></div></div>
<script>
function ytIframe(id){return '<iframe src="https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0&playsinline=1" title="Lou Denim" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';}
var lb=document.getElementById('lb'), lbInner=document.getElementById('lbInner');
function openLB(id){lbInner.innerHTML=ytIframe(id);lb.classList.add('on');lb.setAttribute('aria-hidden','false');document.body.style.overflow='hidden';}
function closeLB(){lb.classList.remove('on');lb.setAttribute('aria-hidden','true');lbInner.innerHTML='';document.body.style.overflow='';}
document.getElementById('lbx').addEventListener('click',closeLB);
lb.addEventListener('click',function(e){if(e.target===lb)closeLB();});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeLB();});
document.querySelectorAll('.vid').forEach(function(v){
  function go(){
    var id=v.dataset.id;
    if(v.classList.contains('v916')){openLB(id);return;}
    if(v.querySelector('iframe'))return;
    v.innerHTML=ytIframe(id);
  }
  v.addEventListener('click',go);
  v.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();go();}});
});
</script>
<script>(function(){
const cv=document.getElementById('dotfx');if(!cv)return;
const ctx=cv.getContext('2d');const HH=440;
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
</html>"""

for k, t in T.items():
    films  = "".join(tile(v, False, t["play"]) for v in FILMS)
    shorts = "".join(tile(v, True,  t["play"]) for v in SHORTS)
    if k == "fr":
        langbtns = '<a class="on" href="travail.html">FR</a><a href="travail-en.html">EN</a>'
    else:
        langbtns = '<a href="travail.html">FR</a><a class="on" href="travail-en.html">EN</a>'
    html = (TPL
        .replace("__LANG__", t["lang"]).replace("__TITLE__", t["title"])
        .replace("__LOGO__", logo).replace("__SUB__", t["sub"])
        .replace("__BAND_SMALL__", t["band_small"]).replace("__BAND__", t["band"])
        .replace("__LANGBTNS__", langbtns).replace("__INTRO__", t["intro"])
        .replace("__S1TAG__", t["s1tag"]).replace("__S1__", t["s1"])
        .replace("__S2TAG__", t["s2tag"]).replace("__S2__", t["s2"])
        .replace("__FILMS__", films).replace("__SHORTS__", shorts)
        .replace("__YT__", t["yt"]).replace("__CTA__", t["cta"])
        .replace("__FOOT__", t["foot"]).replace("__SOCIALS__", SOCIALS))
    out = os.path.join(OUT, t["self_"])
    open(out, "w").write(html)
    print(out, len(html), "octets")
