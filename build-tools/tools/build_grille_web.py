#!/usr/bin/env python3
"""Génère grille.html (grille tarifaire en ligne) depuis prices.json — peau Studio Blush web.
Usage: python3 build_grille_web.py <out_dir> [lien_simulateur] [lien_catalogue]"""
import json, base64, sys, os

SKILL = "/root/.claude/skills/pdf-lou"
P = json.load(open(f"{SKILL}/prices.json"))
OUT = sys.argv[1] if len(sys.argv) > 1 else "/root/catalogue-models"
LINK_SIM = sys.argv[2] if len(sys.argv) > 2 else P["liens"]["simulateur"]
LINK_CAT = sys.argv[3] if len(sys.argv) > 3 else "index.html"

logo = "data:image/svg+xml;base64," + base64.b64encode(open(f"{SKILL}/assets/lou-denim-logo.svg","rb").read()).decode()

def eur(n): return f"{n:,}".replace(",", " ") + " €"

def row(label, price, des=False):
    p = f"dès {eur(price)}" if des else (eur(price) if isinstance(price,int) else price)
    return f"<tr><td>{label}</td><td class='num'>{p}</td></tr>"

NCARD = P["video"].get("durees_carte", 3)   # the online card shows 15/20/30s; longer -> simulator
video_rows = "".join(
    f"<tr><td>{v['label']}</td>" + "".join(f"<td class='num'>{eur(p)}</td>" for p in v["prix"][:NCARD]) + "</tr>"
    for v in P["video"]["formats"].values())
video_supp_rows = "".join(
    f"<tr><td>{v['label']}</td><td class='num'>+&nbsp;{eur(v['prix'])}</td></tr>"
    for v in P["video"]["supplements"].values())

effets_rows = "".join(row(v["label"], v["prix"], True) for v in P["effets"].values())
son_rows    = "".join(row(v["label"], v["prix"], v.get("des",False)) for v in P["son_finitions"].values())
perso_rows  = (row(P["personnages"]["parlant"]["label"], P["personnages"]["parlant"]["prix"], True)
             + row(P["personnages"]["dialogue"]["label"], P["personnages"]["dialogue"]["prix"], True)
             + row(P["personnages"]["exclusivite"]["label"], P["personnages"]["exclusivite"]["prix"]))
autres_rows = (row(P["autres_options"]["storyboard"]["label"], P["autres_options"]["storyboard"]["prix"], True)
             + row(P["autres_options"]["script"]["label"], P["autres_options"]["script"]["prix"], True)
             + row(P["autres_options"]["revision"]["label"], P["autres_options"]["revision"]["prix"] + " €")
             + row(P["autres_options"]["urgence"]["label"], P["autres_options"]["urgence"]["prix"]))
im = P["immobilier"]
immo_rows = (f"<tr><td>{im['visite']['label']}</td><td class='num'>{im['visite'].get('affichage_grille','dès 300 €')}</td></tr>"
             + row(im["personnage"]["label"], im["personnage"]["prix"])
             + row(im["embellissement"]["label"] + " — par photo", im["embellissement"]["prix"], True)
             + row(im["staging"]["label"] + " — par photo", im["staging"]["prix"], True))
img_rows = (row("Produit seul — sans personnage", P["images"]["produit_seul"])
          + row("1 personnage + produit", P["images"]["perso1_produit"])
          + row("2–3 personnages + produit", P["images"]["perso23_produit"])
          + row("Lot de 10 images — campagne complexe", P["images"]["lot10"]))

html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>LOU DENIM — Grille Tarifaire IA</title><meta name="robots" content="noindex">
<style>
@import url('https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&display=swap');
:root{{--blush:#FBF1EF;--blush2:#F5E3DF;--blush3:#EBC9C3;--ink:#000;--grey:#666}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Jost',sans-serif;background:#fff;color:var(--ink);position:relative;line-height:1.55}}
.wrap{{max-width:900px;margin:0 auto;padding:0 20px 80px}}
header{{padding:20px 0 26px;text-align:center}}
header img{{height:136px;margin-bottom:2px}}
.sub{{font-size:12px;letter-spacing:.24em;text-transform:uppercase;color:#D63E8D}}
.contact{{margin-top:8px;font-size:11px;letter-spacing:.1em;color:var(--grey)}}
.doc-band{{display:inline-block;background:#000;color:#fff;padding:13px 40px;border-radius:999px;margin-top:12px;
  font-size:18px;letter-spacing:.28em;text-transform:uppercase;font-weight:600;text-align:center}}
.doc-band small{{display:block;font-size:10px;letter-spacing:.2em;color:#e8cfca;font-weight:400;text-transform:none;margin-top:3px}}
.actions{{display:flex;gap:10px;justify-content:center;margin-top:20px;flex-wrap:wrap}}
.actions a{{display:inline-block;padding:11px 24px;border-radius:999px;font-size:13.5px;letter-spacing:.16em;
  text-transform:uppercase;text-decoration:none}}
.actions a.primary{{background:#000;color:#fff}}
.actions a.ghost{{background:#fff;color:#000;border:1px solid #000;transition:.15s}}
.actions a:hover{{border-color:#E7549F;color:#E7549F}}
.actions a.primary:hover{{background:#E7549F;color:#fff;border-color:#E7549F}}
h2.band{{background:#000;color:#fff;font-size:14.5px;font-weight:500;letter-spacing:.28em;text-transform:uppercase;
  padding:9px 18px;border-radius:10px;margin:34px 0 12px;display:flex;justify-content:space-between;align-items:center}}
h2.band .tag{{font-size:11px;letter-spacing:.14em;color:var(--blush3)}}
table{{width:100%;border-collapse:collapse;font-size:15px}}
td,th{{padding:9px 11px;border-bottom:1px solid #eee;text-align:left;vertical-align:top}}
th{{font-size:12px;letter-spacing:.18em;text-transform:uppercase;font-weight:700}}
th .lc{{text-transform:none}}
td.num,th.num{{text-align:right;white-space:nowrap;font-weight:500}}
tr:nth-child(even) td{{background:var(--blush)}}
.note{{font-size:13px;color:var(--grey);margin:8px 2px 0}}
.chips{{display:flex;gap:10px;margin:16px 0 6px;flex-wrap:wrap}}
.chip{{flex:1;min-width:140px;text-align:center;padding:10px;border-radius:12px;background:var(--blush)}}
.chip.c2{{background:var(--blush2)}}.chip.c3{{background:var(--blush3)}}
.chip b{{display:block;font-size:14.5px}}.chip span{{font-size:12px;color:#444}}
.pack{{display:flex;justify-content:space-between;align-items:center;gap:14px;background:var(--blush2);
  border-radius:12px;padding:14px 18px;margin:14px 0;flex-wrap:wrap}}
.pack b{{font-size:15.5px}}.pack .desc{{font-size:13.5px;color:#444;flex:1}}.pack .price{{font-weight:600;white-space:nowrap}}
.socle{{margin:30px 0 0;background:var(--blush);border-radius:12px;padding:16px 20px;font-size:14.5px;text-align:center;color:#333}}
.conditions{{margin-top:30px;font-size:13px;color:#444;border-top:2px solid #000;padding-top:14px}}
.conditions p{{margin:6px 0}}
footer{{margin-top:44px;text-align:center;font-size:12px;color:var(--grey);letter-spacing:.12em;text-transform:uppercase}}
footer a{{color:#000}}
#dotfx{{position:absolute;top:0;left:0;width:100%;height:440px;z-index:-1;pointer-events:none}}
@media (prefers-reduced-motion: reduce){{#dotfx{{display:none}}}}
.socials{{display:flex;gap:20px;justify-content:center;margin-top:16px}}.socials a{{color:#8a8f93;transition:color .15s}}.socials a:hover{{color:#E7549F}}.socials svg{{height:18px;width:18px;fill:currentColor;display:block}}
</style>
</head>
<body>
<canvas id="dotfx"></canvas>
<div class="wrap">
<header>
  <a href="home.html"><img src="{logo}" alt="Lou Denim"></a>
  <p class="sub">Directeur artistique IA</p>
  <div><span class="doc-band">Grille Tarifaire<small>Services créatifs IA</small></span></div>
  <div class="actions">
    <a class="primary" href="{LINK_SIM}" target="_blank" rel="noopener">Estimer votre projet — simulateur</a>
    <a class="ghost" href="Grille_Tarifaire_LouDenim.pdf" download>Télécharger le PDF</a>
    <a class="ghost" href="{LINK_CAT}">Catalogue de modèles</a>
  </div>
</header>

<h2 class="band">Création d'images par IA <span class="tag">Lot de 5 minimum</span></h2>
<table><thead><tr><th>Livrable</th><th class="num">Tarif</th></tr></thead><tbody>{img_rows}</tbody></table>
<p class="note">Images vendues par lots de 5 minimum. Tarif à l'unité disponible sur demande.</p>

<h2 class="band">Production vidéo par IA <span class="tag">Produit / service</span></h2>
<table><thead><tr><th>Que montre votre vidéo ?</th><th class="num">15<span class="lc">s</span></th><th class="num">20<span class="lc">s</span></th><th class="num">30<span class="lc">s</span></th></tr></thead>
<tbody>{video_rows}</tbody></table>
<table><tbody>{video_supp_rows}</tbody></table>
<p class="note">Le prix s'additionne : votre format (selon la durée) + vos environnements + vos personnages et produits supplémentaires. Les deux premiers formats sont sur fond neutre ; le format UGC inclut la parole (voix + synchro labiale) et 1 lieu réel. Pour votre combinaison exacte — et les formats plus longs (40 à 60 s) — utilisez le <a href="simulator.html">simulateur</a>.</p>
<p class="note"><strong>Personnage :</strong> choisi dans le <a href="modeles.html">catalogue de modèles</a> ou créé pour vous, même tarif. Pour le réserver à votre marque (non réutilisé ailleurs), voir <strong>Exclusivité</strong> dans la section Personnages.</p>
<p class="note"><strong>Un service ?</strong> Son lieu, son enseigne ou sa façade fait office de produit (ex : la façade de la banque, la salle d'un restaurant).</p>
<p class="note"><strong>Style visuel — même tarif :</strong> Photoréaliste · Animation 3D · Dessin animé 2D.</p>

<div class="chips">
  <div class="chip"><b>HD 720p</b><span>inclus</span></div>
  <div class="chip c2"><b>Full HD 1080p</b><span>+&nbsp;20&nbsp;%</span></div>
  <div class="chip c3"><b>4K Upscale</b><span>+&nbsp;50&nbsp;%</span></div>
</div>

<div class="pack"><b>Pack campagne complète</b><span class="desc">3 vidéos sur le même concept (Reel / Story / Feed)</span><span class="price">1&nbsp;500&nbsp;€&nbsp;–&nbsp;2&nbsp;000&nbsp;€</span></div>

<h2 class="band">Effets &amp; transformations</h2>
<table><tbody>{effets_rows}</tbody></table>

<h2 class="band">Son &amp; finitions</h2>
<table><tbody>{son_rows}</tbody></table>

<h2 class="band">Personnages</h2>
<table><tbody>{perso_rows}</tbody></table>

<h2 class="band">Autres options</h2>
<table><tbody>{autres_rows}</tbody></table>

<h2 class="band">Immobilier &amp; lieux <span class="tag">À partir de vos photos</span></h2>
<table><tbody>{immo_rows}</tbody></table>
<p class="note">{im["note_shoot"]}</p>

<div class="pack"><b>Demande particulière</b><span class="desc">Toute demande hors grille&nbsp;: sur devis, après échange avec le créatif.</span><span class="price" style="font-size:15.5px;font-weight:bold">Sur devis</span></div>
<p class="note"><strong>Commandes régulières&nbsp;?</strong> Un forfait mensuel (retainer) peut être mis en place pour plusieurs vidéos par mois&nbsp;: tarif dégressif, priorité de production, à discuter avec le créatif.</p>

<div class="socle">{P["socle"]}</div>

<div class="conditions">
  <p><strong>Tous les prix s'entendent hors taxes</strong> — la TVA applicable est ajoutée au devis.</p>
  <p><strong>2 révisions incluses</strong> dans chaque prestation — au-delà, facturation selon le barème. · Délai standard : <strong>7 à 10 jours ouvrés</strong>.</p>
  <p>Le <strong>storyboard validé</strong> fixe le point de départ de la production : toute modification d'un élément déjà validé constitue un tour de révision facturé.</p>
  <p>Tarifs valables pour une diffusion <strong>réseaux sociaux</strong> — TV, affichage ou écran point de vente : sur devis.</p>
  <p>Fichiers sources, prompts et workflows non livrés — <strong>propriété de Lou Denim</strong>. · Devis final selon brief.</p>
  <p><strong>Droit à l'image et licence&nbsp;: à définir selon vos besoins.</strong></p>
  <p><strong>Acompte de 50&nbsp;%</strong> avant démarrage. · Aucun travail sans brief validé et accord signé.</p>
</div>

<footer>
  <p style="margin-bottom:6px"><a href="mailto:lou@loudenim.com">lou@loudenim.com</a> · <a href="tel:+590690299544">+590 (0)690 299 544</a> · loudenim.com</p>
  <p style="margin-bottom:6px">Envie de voir&nbsp;? <a href="portfolio.html">Le travail en images</a></p>
  <p>Un projet ? <a href="{LINK_SIM}" target="_blank" rel="noopener">Estimez-le en ligne</a> ou écrivez à <a href="mailto:lou@loudenim.com">lou@loudenim.com</a></p>
<div class="socials"><a href="https://www.instagram.com/loudenim/" target="_blank" rel="noopener" aria-label="Instagram" title="Instagram"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.15 3.23-1.66 4.77-4.92 4.92-1.27.06-1.64.07-4.85.07s-3.58-.01-4.85-.07c-3.26-.15-4.77-1.7-4.92-4.92-.06-1.27-.07-1.64-.07-4.85s.01-3.58.07-4.85C2.38 3.92 3.9 2.38 7.15 2.23 8.42 2.17 8.8 2.16 12 2.16zM12 0C8.74 0 8.33.01 7.05.07 2.7.27.27 2.69.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.2 4.36 2.62 6.78 6.98 6.98 1.28.06 1.69.07 4.95.07s3.67-.01 4.95-.07c4.35-.2 6.78-2.62 6.98-6.98.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95C23.73 2.7 21.31.27 16.95.07 15.67.01 15.26 0 12 0zm0 5.84A6.16 6.16 0 1 0 18.16 12 6.16 6.16 0 0 0 12 5.84zm0 10.15A3.99 3.99 0 1 1 16 12a3.99 3.99 0 0 1-4 3.99zm6.41-11.85a1.44 1.44 0 1 0 1.43 1.44 1.44 1.44 0 0 0-1.43-1.44z"/></svg></a><a href="https://www.tiktok.com/@loudenim" target="_blank" rel="noopener" aria-label="TikTok" title="TikTok"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg></a><a href="https://www.youtube.com/@loudenim" target="_blank" rel="noopener" aria-label="YouTube" title="YouTube"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M23.5 6.19a3.02 3.02 0 0 0-2.12-2.14C19.5 3.55 12 3.55 12 3.55s-7.5 0-9.38.5A3.02 3.02 0 0 0 .5 6.19 31.6 31.6 0 0 0 0 12a31.6 31.6 0 0 0 .5 5.81 3.02 3.02 0 0 0 2.12 2.14c1.88.5 9.38.5 9.38.5s7.5 0 9.38-.5a3.02 3.02 0 0 0 2.12-2.14A31.6 31.6 0 0 0 24 12a31.6 31.6 0 0 0-.5-5.81zM9.55 15.57V8.43L15.82 12z"/></svg></a><a href="https://x.com/loudenim" target="_blank" rel="noopener" aria-label="X" title="X"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M18.9 1.2h3.7l-8.2 9.4L24 22.8h-7.6l-5.9-7.8-6.8 7.8H0l8.8-10L0 1.2h7.8l5.4 7.1zM17.6 20.6h2L6.5 3.3h-2.2z"/></svg></a><a href="https://www.linkedin.com/in/loudenim/" target="_blank" rel="noopener" aria-label="LinkedIn" title="LinkedIn"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.55C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.72C24 .77 23.2 0 22.22 0z"/></svg></a></div></footer>
</div>
<script>(function(){{
const cv=document.getElementById('dotfx');if(!cv)return;
const ctx=cv.getContext('2d');const HH=440;
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

open(os.path.join(OUT, "grille.html"), "w").write(html)
print("grille.html ->", OUT)
