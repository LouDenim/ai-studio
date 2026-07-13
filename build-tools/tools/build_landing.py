#!/usr/bin/env python3
"""Génère l'accueil AI Studio (index.html) — bilingue FR/EN, cartes blanches, logo home.
Usage: build_landing.py <out_dir>"""
import base64, sys, os
OUT = sys.argv[1] if len(sys.argv) > 1 else "/root/catalogue-models"
logo_dir = os.path.join(OUT, "img", "logos-color")
logo_files = sorted(f for f in os.listdir(logo_dir) if f.endswith(".png")) if os.path.isdir(logo_dir) else []
_imgs = "".join(f'<img src="img/logos-color/{f}" alt="{f.rsplit(chr(46),1)[0]}" loading="lazy">' for f in logo_files)
_seq = '<div class="seq">' + _imgs*3 + '</div>'
trust_html = ""
if logo_files:
    trust_html = ('<div class="trust"><p class="cap" data-l="fr">Ils m\'ont fait confiance</p>'
                  '<p class="cap" data-l="en">Trusted by</p>'
                  '<div class="marq"><div class="track">' + _seq + _seq + '</div></div></div>')
logo = "data:image/svg+xml;base64," + base64.b64encode(open('/root/.claude/skills/pdf-lou/assets/lou-denim-logo.svg','rb').read()).decode()

html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>LOU DENIM — AI Studio</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&display=swap');
:root{{--blush:#FBF1EF;--blush2:#F5E3DF;--blush3:#EBC9C3;--ink:#000;--grey:#666}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Jost',sans-serif;background:#fff;color:var(--ink);position:relative;min-height:100vh}}
.wrap{{max-width:980px;margin:0 auto;padding:0 20px 90px;text-align:center}}
header{{padding:86px 0 10px}}
header img{{height:86px;margin-bottom:10px}}
.rule{{width:300px;max-width:70%;height:1px;background:#000;margin:8px auto 10px}}
.sub{{font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:var(--ink)}}
.contact{{margin-top:8px;font-size:11px;letter-spacing:.1em;color:var(--grey)}}
.doc-band{{display:inline-block;background:#000;color:#fff;padding:12px 40px;border-radius:999px;margin-top:26px;
  font-size:17px;letter-spacing:.34em;text-transform:uppercase;font-weight:500}}
.langs{{display:flex;gap:10px;justify-content:center;margin-top:26px}}
.langs button{{font-family:'Jost';font-size:11px;letter-spacing:.18em;text-transform:uppercase;cursor:pointer;
  padding:6px 16px;border-radius:999px;border:1px solid #E7549F;background:#fff;color:#E7549F;transition:.15s}}
.langs button:hover{{background:#E7549F;color:#fff}}
.langs button.on{{background:#E7549F;color:#fff}}
.tagline{{max-width:560px;margin:26px auto 0;font-size:14.5px;font-weight:300;line-height:1.6;color:#333}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin-top:38px}}
.card{{display:flex;flex-direction:column;text-decoration:none;color:var(--ink);background:#fff;
  border:1px solid #000;border-radius:14px;padding:26px 18px;transition:transform .12s, box-shadow .12s}}
.card:hover{{transform:translateY(-3px);border-color:#E7549F;box-shadow:0 10px 26px rgba(231,84,159,.14)}}
.card b{{display:block;font-size:14px;letter-spacing:.16em;text-transform:uppercase;font-weight:500;line-height:1.3;min-height:2.6em}}
.card span{{display:block;margin-top:7px;font-size:12px;font-weight:300;color:#555;line-height:1.5;flex:1}}
.card em{{display:inline-block;margin-top:18px;align-self:center;font-style:normal;font-size:10px;letter-spacing:.14em;
  text-transform:uppercase;color:#000;border-bottom:1px solid #000;padding-bottom:2px;transition:.15s}}
.card:hover em{{color:#E7549F;border-bottom-color:#E7549F}}
.soon{{opacity:.55;pointer-events:none}}

.trust{{margin-top:60px}}
.trust .cap{{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--grey)}}
.marq{{overflow:hidden;position:relative;margin-top:20px;
  -webkit-mask-image:linear-gradient(to right,transparent,#000 8%,#000 92%,transparent);
  mask-image:linear-gradient(to right,transparent,#000 8%,#000 92%,transparent)}}
.track{{display:flex;width:max-content;animation:logoscroll 60s linear infinite}}
.seq{{display:flex;gap:74px;align-items:center;padding-right:74px}}
.marq:hover .track{{animation-play-state:paused}}
.track img{{height:44px;width:auto;opacity:.9}}
@keyframes logoscroll{{from{{transform:translateX(0)}}to{{transform:translateX(-50%)}}}}
@media (prefers-reduced-motion: reduce){{.track{{animation:none}}}}
footer{{margin-top:70px;font-size:11px;color:var(--grey);letter-spacing:.12em;text-transform:uppercase}}
footer a{{color:#000}}
[data-l]{{display:none}}
#dotfx{{position:absolute;top:0;left:0;width:100%;height:640px;z-index:-1;pointer-events:none}}
@media (prefers-reduced-motion: reduce){{#dotfx{{display:none}}}}
.socials{{display:flex;gap:20px;justify-content:center;margin-top:16px}}.socials a{{color:#8a8f93;transition:color .15s}}.socials a:hover{{color:#E7549F}}.socials svg{{height:18px;width:18px;fill:currentColor;display:block}}
</style>
</head>
<body>
<canvas id="dotfx"></canvas>
<div class="wrap">
<header>
  <a href="https://www.loudenim.com"><img src="{logo}" alt="Lou Denim"></a>
  <div class="rule"></div>
  <p class="sub" data-l="fr">Directeur artistique IA</p>
  <p class="sub" data-l="en">AI Creative Director</p>
  <div><span class="doc-band" data-l="fr">Studio IA</span><span class="doc-band" data-l="en">AI Studio</span></div>
</header>

<div class="langs">
  <button id="bfr" onclick="setLang('fr')">FR</button>
  <button id="ben" onclick="setLang('en')">EN</button>
</div>

<p class="tagline" data-l="fr">Création générative au service des marques : images et campagnes vidéo IA sur mesure.</p>
<p class="tagline" data-l="en">Gen AI for brands: images and video campaigns ready to run.</p>

<div class="cards" data-l="fr">
  <a class="card" href="modeles.html"><b>Les modèles</b><span>32 modèles virtuels conçus pour garantir une parfaite continuité visuelle.</span><em>Voir le catalogue</em></a>
  <a class="card" href="grille.html"><b>Grille tarifaire</b><span>Tous les prix, clairs et sans surprise.</span><em>Voir les tarifs</em></a>
  <a class="card" href="devis.html"><b>Simulateur de devis</b><span>Composez votre projet, le montant se calcule en direct, envoyez la demande.</span><em>Estimer mon projet</em></a>
  <a class="card" href="brief.html"><b>Brief vidéo</b><span>Le formulaire à remplir pour lancer votre projet vidéo dans de bonnes conditions.</span><em>Remplir le brief</em></a>
  <a class="card" href="travail.html"><b>Le travail en images</b><span>Vidéos IA pensées pour le grand écran cinéma comme pour le format vertical mobile.</span><em>Voir les vidéos</em></a>
</div>

<div class="cards" data-l="en">
  <a class="card" href="models-en.html"><b>The models</b><span>32 AI-generated faces, consistent frame after frame, ready for your campaigns.</span><em>View the catalogue</em></a>
  <a class="card" href="grille-en.html"><b>Rate card</b><span>All prices, clear and upfront.</span><em>View the rates</em></a>
  <a class="card" href="devis-en.html"><b>Quote simulator</b><span>Build your project in pounds, get a live estimate, send the request.</span><em>Estimate my project</em></a>
  <a class="card" href="brief-en.html"><b>Video brief</b><span>The form to fill in so your video project starts on solid ground.</span><em>Fill in the brief</em></a>
  <a class="card" href="travail-en.html"><b>The work</b><span>AI videos built for both cinematic widescreen and vertical mobile screens.</span><em>Watch the videos</em></a>
</div>

{trust_html}

<footer>
  <p style="margin-bottom:8px"><a href="mailto:lou@loudenim.com">lou@loudenim.com</a> · <a href="tel:+590690299544">+590 (0)690 299 544</a></p>
  <p data-l="fr">© Lou Denim — Guadeloupe · <a href="https://www.loudenim.com" target="_blank" rel="noopener">Photographie&nbsp;: loudenim.com</a></p>
  <p data-l="en">© Lou Denim — Guadeloupe · <a href="https://www.loudenim.com" target="_blank" rel="noopener">Photography&nbsp;: loudenim.com</a></p>
<div class="socials"><a href="https://www.instagram.com/loudenim/" target="_blank" rel="noopener" aria-label="Instagram" title="Instagram"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.15 3.23-1.66 4.77-4.92 4.92-1.27.06-1.64.07-4.85.07s-3.58-.01-4.85-.07c-3.26-.15-4.77-1.7-4.92-4.92-.06-1.27-.07-1.64-.07-4.85s.01-3.58.07-4.85C2.38 3.92 3.9 2.38 7.15 2.23 8.42 2.17 8.8 2.16 12 2.16zM12 0C8.74 0 8.33.01 7.05.07 2.7.27.27 2.69.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.2 4.36 2.62 6.78 6.98 6.98 1.28.06 1.69.07 4.95.07s3.67-.01 4.95-.07c4.35-.2 6.78-2.62 6.98-6.98.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95C23.73 2.7 21.31.27 16.95.07 15.67.01 15.26 0 12 0zm0 5.84A6.16 6.16 0 1 0 18.16 12 6.16 6.16 0 0 0 12 5.84zm0 10.15A3.99 3.99 0 1 1 16 12a3.99 3.99 0 0 1-4 3.99zm6.41-11.85a1.44 1.44 0 1 0 1.43 1.44 1.44 1.44 0 0 0-1.43-1.44z"/></svg></a><a href="https://www.tiktok.com/@loudenim" target="_blank" rel="noopener" aria-label="TikTok" title="TikTok"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg></a><a href="https://www.youtube.com/@loudenim" target="_blank" rel="noopener" aria-label="YouTube" title="YouTube"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M23.5 6.19a3.02 3.02 0 0 0-2.12-2.14C19.5 3.55 12 3.55 12 3.55s-7.5 0-9.38.5A3.02 3.02 0 0 0 .5 6.19 31.6 31.6 0 0 0 0 12a31.6 31.6 0 0 0 .5 5.81 3.02 3.02 0 0 0 2.12 2.14c1.88.5 9.38.5 9.38.5s7.5 0 9.38-.5a3.02 3.02 0 0 0 2.12-2.14A31.6 31.6 0 0 0 24 12a31.6 31.6 0 0 0-.5-5.81zM9.55 15.57V8.43L15.82 12z"/></svg></a><a href="https://x.com/loudenim" target="_blank" rel="noopener" aria-label="X" title="X"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M18.9 1.2h3.7l-8.2 9.4L24 22.8h-7.6l-5.9-7.8-6.8 7.8H0l8.8-10L0 1.2h7.8l5.4 7.1zM17.6 20.6h2L6.5 3.3h-2.2z"/></svg></a><a href="https://www.linkedin.com/in/loudenim/" target="_blank" rel="noopener" aria-label="LinkedIn" title="LinkedIn"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.55C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.72C24 .77 23.2 0 22.22 0z"/></svg></a></div></footer>
</div>
<script>
function setLang(l){{
  document.querySelectorAll('[data-l]').forEach(e=>e.style.display=e.dataset.l===l?(e.tagName==='DIV'?'grid':(e.tagName==='SPAN'?'inline-block':'block')):'none');
  document.getElementById('bfr').classList.toggle('on',l==='fr');
  document.getElementById('ben').classList.toggle('on',l==='en');
  try{{localStorage.setItem('lang',l)}}catch(e){{}}
}}
let saved='fr';
try{{saved=localStorage.getItem('lang')||((navigator.language||'fr').startsWith('en')?'en':'fr')}}catch(e){{}}
setLang(saved);
</script>
<script>(function(){{
const cv=document.getElementById('dotfx');if(!cv)return;
const ctx=cv.getContext('2d');const HH=640;
function sz(){{cv.width=document.documentElement.clientWidth;cv.height=HH;}}
sz();addEventListener('resize',sz);
const SP=34;
function mask(x,y){{const cx=cv.width/2;const dx=Math.max(0,Math.abs(x-cx)-150);const dy=Math.max(0,y-(HH-40));return Math.min(1,Math.hypot(dx,dy*2.2)/140);}}
function rnd(a,b){{return a+Math.random()*(b-a);}}
function newPath(side){{
  const w=cv.width;
  const x0=side==='L'?0.03:0.56, x1=side==='L'?0.44:0.97;
  const spots=[[w*x0,HH*0.9],[w*x1,HH*0.9],[w*x0,HH*0.1],[w*x1,HH*0.1],[w*(x0+x1)/2,HH*0.5]];
  const i=Math.floor(Math.random()*spots.length);
  let j;do{{j=Math.floor(Math.random()*spots.length);}}while(j===i);
  const P1=[rnd(w*x0,w*x1),rnd(HH*0.05,HH*0.95)];
  const P2=[rnd(w*x0,w*x1),rnd(HH*0.05,HH*0.95)];
  return {{P:[spots[i],P1,P2,spots[j]],dur:rnd(5,7),start:performance.now()}};
}}
let comets=[newPath('L'),newPath('R')];
comets[1].start=performance.now()-comets[1].dur*500;
function bez(P,u){{const a=1-u;return[a*a*a*P[0][0]+3*a*a*u*P[1][0]+3*a*u*u*P[2][0]+u*u*u*P[3][0],a*a*a*P[0][1]+3*a*a*u*P[1][1]+3*a*u*u*P[2][1]+u*u*u*P[3][1]];}}
function draw(now){{
  ctx.clearRect(0,0,cv.width,cv.height);
  const trail=[];
  comets.forEach((c,idx)=>{{
    let tt=(now-c.start)/1000/c.dur;
    if(tt>1.08){{comets[idx]=newPath(idx===0?'L':'R');c=comets[idx];tt=0;}}
    for(let s=0;s<=Math.min(tt,1);s+=0.02){{trail.push({{p:bez(c.P,s),decay:Math.max(0,1-(tt-s)*2.2)}});}}
  }});
  for(let x=SP/2;x<cv.width;x+=SP){{
    for(let y=SP/2;y<HH-4;y+=SP){{
      const m=mask(x,y);if(m<=0.02)continue;
      let lit=0;
      for(const q of trail){{if(q.decay<=0)continue;const d=Math.hypot(x-q.p[0],y-q.p[1]);if(d<210){{const v=(1-d/210)*q.decay;if(v>lit)lit=v;}}}}
      const o=(0.14+lit*0.86)*m;
      const sh=Math.round(133-133*lit);
      ctx.beginPath();ctx.arc(x,y,1.1+lit*1.7,0,6.283);
      ctx.fillStyle='rgba('+sh+','+sh+','+Math.round(sh*1.03)+','+o.toFixed(3)+')';
      ctx.fill();
    }}
  }}
  requestAnimationFrame(draw);
}}
requestAnimationFrame(draw);
}})();</script>
</body>
</html>"""
import os
open(os.path.join(OUT,'index.html'),'w').write(html)
print('index.html (accueil) ->', OUT)
