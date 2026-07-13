#!/usr/bin/env python3
"""Génère brief.html (FR) et brief-en.html (EN) — brief vidéo en ligne.
Champs blush au repos, bleus au survol/focus. Envoi Web3Forms + impression.
Usage: build_brief_web.py <out_dir>"""
import base64, sys, json, html as H

OUT = sys.argv[1] if len(sys.argv) > 1 else "/root/catalogue-models"
SKILL = "/root/.claude/skills/pdf-lou"
logo = "data:image/svg+xml;base64," + base64.b64encode(open(f"{SKILL}/assets/lou-denim-logo.svg","rb").read()).decode()
KEY = json.load(open(f"{SKILL}/prices.json"))["liens"]["web3forms_key"]

# (type, label_fr, hint_fr, label_en, hint_en) — type: line | area | checks:opt1|opt2
S = [
 ("1","Vos coordonnées","Your details",[
  ("line","Société / marque","","Company / brand",""),
  ("line","Personne à contacter","","Contact person",""),
  ("line","Fonction / rôle","","Role",""),
  ("line","Email","","Email",""),
  ("line","Téléphone","","Phone",""),
  ("line","Nom du projet","","Project name",""),
  ("line","Secteur d'activité","restauration, immobilier, mode, automobile…","Industry","food, real estate, fashion, automotive…"),
  ("line","Site web","site du produit ou de l'entreprise","Website","product or company site"),
 ]),
 ("2","Le projet","The project",[
  ("area","Objectif de la vidéo","lancement, notoriété, promo, événement, recrutement…","Goal of the video","launch, awareness, promo, event, recruitment…"),
  ("area","Message principal","si le spectateur ne retient qu'une seule chose, c'est quoi ?","Key message","if the viewer remembers one thing, what is it?"),
  ("line","Public cible","âge, profil, localisation, langue","Target audience","age, profile, location, language"),
  ("line","Action attendue","acheter, visiter, s'abonner, appeler…","Expected action","buy, visit, subscribe, call…"),
 ]),
 ("3","Le produit — si applicable","The product — if applicable",[
  ("line","Nom exact du produit","orthographe exacte + gamme","Exact product name","exact spelling + range"),
  ("area","Description du produit","ce que c'est, catégorie, à quoi ça sert","Product description","what it is, category, what it does"),
  ("area","Références visuelles du produit","photos HD, plusieurs angles — lien Drive / WeTransfer. Pas de référence = pas de garantie de fidélité.","Product visual references","HD photos, several angles — Drive / WeTransfer link. No reference = no fidelity guarantee."),
  ("line","Couleur(s) exacte(s)","Pantone / hex / RAL — produit ET packaging","Exact colour(s)","Pantone / hex / RAL — product AND packaging"),
  ("line","Format, dimensions, proportions","","Size, dimensions, proportions",""),
  ("line","Matière et finition","mat / brillant / métallisé / transparent…","Material & finish","matte / glossy / metallic / transparent…"),
  ("line","Variantes à montrer","parfums, coloris, tailles…","Variants to show","flavours, colours, sizes…"),
  ("line","Packaging / étiquette","textes exacts, placement du logo, mentions","Packaging / label","exact copy, logo placement, legal lines"),
  ("area","Éléments non-négociables","ce qui ne doit jamais changer : forme, proportions, logo, couleur","Non-negotiables","what must never change: shape, proportions, logo, colour"),
 ]),
 ("4","Usage & diffusion","Usage & distribution",[
  ("checks","Où sera diffusée la vidéo ?","Instagram|TikTok|YouTube|Facebook|LinkedIn|Site web|TV|Écran magasin / PLV|Cinéma|Autre",
            "Where will the video run?","Instagram|TikTok|YouTube|Facebook|LinkedIn|Website|TV|In-store screen|Cinema|Other"),
  ("line","Durée des droits d'utilisation","6 mois, 1 an, illimité…","Usage-rights duration","6 months, 1 year, unlimited…"),
  ("line","Territoire","Royaume-Uni, États-Unis, France, international…","Territory","UK, U.S., France, international…"),
 ]),
 ("5","Format & spécifications","Format & specs",[
  ("checks","Durée souhaitée","− de 15 s|20 s|30 s|40 s|+ de 40 s|À définir","Desired duration","under 15 s|20 s|30 s|40 s|over 40 s|TBD"),
  ("checks","Format / ratio","16:9 paysage|9:16 vertical|1:1 carré|4:5|À définir","Format / ratio","16:9 landscape|9:16 vertical|1:1 square|4:5|TBD"),
  ("checks","Résolution — influence le devis","720p|1080p (Full HD)|4K (UHD)|À définir","Resolution — affects the quote","720p|1080p (Full HD)|4K (UHD)|TBD"),
  ("checks","Langue(s)","Français|Anglais|Autre","Language(s)","French|English|Other"),
  ("checks","Sous-titres ?","Oui|Non|À définir","Subtitles?","Yes|No|TBD"),
  ("checks","Son","Voix-off|Musique|Dialogues|Sound design|Silencieux (sous-titré)","Sound","Voice-over|Music|Dialogue|Sound design|Silent (subtitled)"),
 ]),
 ("6","Contenu & script","Content & script",[
  ("checks","Avez-vous un script ?","Oui, fourni|Non|À développer ensemble","Do you have a script?","Yes, provided|No|To develop together"),
  ("checks","Souhaitez-vous un storyboard ?","Oui|Non","Do you want a storyboard?","Yes|No"),
  ("area","Textes, accroches, slogan imposés","tagline, mentions, hashtags…","Mandatory copy, taglines","tagline, required lines, hashtags…"),
  ("area","Éléments obligatoires à l'écran","produit, logo, prix, adresse, mentions légales…","Mandatory on-screen elements","product, logo, price, address, legal lines…"),
  ("line","Mentions légales / obligations","","Legal requirements",""),
 ]),
 ("7","Direction créative — l'ambiance","Creative direction — the mood",[
  ("area","L'ambiance générale recherchée","énergique, premium, chaleureuse, fun, cinématographique, épurée, luxe… avec vos mots","Overall mood","energetic, premium, warm, fun, cinematic, clean, luxury… in your own words"),
  ("area","Références que vous aimez","liens YouTube / Instagram, marques, moodboard","References you like","YouTube / Instagram links, brands, moodboard"),
  ("line","Style visuel souhaité","photoréaliste, animation 3D, dessin animé 2D, mix…","Visual style","photorealistic, 3D animation, 2D cartoon, mix…"),
  ("line","Combien de personnages ?","","How many characters?",""),
  ("line","Combien de produits ?","","How many products?",""),
  ("line","Combien d'environnements ?","","How many environments?",""),
  ("area","Description des personnages souhaités","genre, âge, look, énergie, tenue — ou choisissez dans le catalogue de modèles","Desired characters","gender, age, look, energy, outfit — or pick from the model catalogue"),
  ("line","Lieux / décors souhaités","","Desired locations / sets",""),
  ("line","Couleurs / charte à respecter","","Brand colours / guidelines",""),
 ]),
 ("8","Les négatifs — à éviter absolument","The negatives — to avoid at all costs",[
  ("area","Ce que vous ne voulez PAS voir","visuels, clichés, styles, éléments interdits","What you do NOT want to see","visuals, clichés, styles, forbidden elements"),
  ("area","Restrictions de marque / sensibilités","concurrents, symboles, sujets à éviter","Brand restrictions / sensitivities","competitors, symbols, topics to avoid"),
  ("line","Ton à éviter","trop corporate, trop humoristique…","Tone to avoid","too corporate, too jokey…"),
 ]),
 ("9","Vos éléments disponibles","Your available assets",[
  ("checks","Éléments que vous pouvez fournir","Logo vectoriel|Charte graphique|Photos produits|Packaging|Vidéos existantes|Polices de marque|Musique / licence|Aucun",
            "Assets you can provide","Vector logo|Brand guidelines|Product photos|Packaging|Existing videos|Brand fonts|Licensed music|None"),
  ("line","Lien vers vos fichiers","Google Drive, WeTransfer, Dropbox…","Link to your files","Google Drive, WeTransfer, Dropbox…"),
 ]),
 ("10","Délais","Timing",[
  ("line","Date de livraison souhaitée","","Desired delivery date",""),
  ("line","Dates clés / échéances","","Key dates / deadlines",""),
  ("checks","Rounds de révisions attendus","1|2|3|À définir","Expected revision rounds","1|2|3|TBD"),
  ("checks","Niveau d'urgence","Standard|Prioritaire (délai serré — supplément)|Flexible","Urgency","Standard|Priority (tight deadline — surcharge)|Flexible"),
 ]),
 ("11","Notes libres","Anything else",[
  ("area","Tout ce que je devrais savoir","et qui n'entre pas dans les cases ci-dessus","Anything I should know","that doesn't fit the boxes above"),
 ]),
]

def build(lang):
    fr = lang == 'fr'
    T = {
      'title': "LOU DENIM — Brief Vidéo IA" if fr else "LOU DENIM — AI Video Brief",
      'doc': "Brief Vidéo IA" if fr else "AI Video Brief",
      'sub2': "Vous souhaitez faire une vidéo en intelligence artificielle ?" if fr else "Planning an AI-made video?",
      'role': "Directeur artistique IA" if fr else "AI Creative Director",
      'intro': ("Ce formulaire me permet de comprendre précisément votre besoin avant de commencer. "
                "Remplissez-le autant que possible : chaque réponse évite un aller-retour, précise le devis et accélère la production. "
                "Un champ que vous ne connaissez pas encore ? Écrivez simplement « à définir ».") if fr else
               ("This form lets me understand your need precisely before we start. Fill it in as much as possible: "
                "every answer avoids a back-and-forth, sharpens the quote and speeds up production. Unsure about a field? Just write \"TBD\"."),
      'send': "Envoyer à Lou" if fr else "Send to Lou",
      'print': "Imprimer / Enregistrer en PDF" if fr else "Print / Save as PDF",
      'pdf': ("Préférez la version PDF à remplir hors ligne ? " if fr else "Prefer the fillable PDF? "),
      'pdffile': "Brief_Video_IA_LouDenim.pdf" if fr else "AI_Video_Brief_LouDenim.pdf",
      'pdflink': "Télécharger le brief PDF" if fr else "Download the PDF brief",
      'sending': "Envoi…" if fr else "Sending…",
      'thanks': ("Merci ! Votre brief a bien été envoyé à Lou Denim. Vous recevrez un devis et un planning rapidement." if fr else
                 "Thank you! Your brief has been sent to Lou Denim. You'll receive a quote and a schedule shortly."),
      'needid': ("Merci d'indiquer au minimum votre société et votre email (section 1) avant d'envoyer." if fr else
                 "Please fill in at least your company and email (section 1) before sending."),
      'neterr': ("Problème réseau — réessayez, ou utilisez « Imprimer / PDF » et envoyez-le à lou@loudenim.com." if fr else
                 "Network problem — try again, or use \"Print / PDF\" and email it to lou@loudenim.com."),
      'modal': ("La production démarre uniquement à réception de ce brief validé, du devis signé et de l'acompte. "
                "Un brief complet me permet de vous proposer un devis juste et un planning réaliste.") if fr else
               ("Production starts only once this brief is validated, the quote signed and the deposit received. "
                "A complete brief lets me give you a fair quote and a realistic schedule."),
      'back': "index.html",
      'subj': "Brief vidéo — " if fr else "Video brief (EN) — ",
    }
    body = []
    for num, tfr, ten, fields in S:
        title = tfr if fr else ten
        body.append(f'<h2 class="band"><span class="num">{num}</span>{H.escape(title)}</h2>')
        for f in fields:
            kind = f[0]
            label = f[1] if fr else f[3]
            hint  = f[2] if fr else f[4]
            hh = f' <span class="hint">{H.escape(hint)}</span>' if hint else ''
            name = f"{num}. {label}"
            if kind == 'line':
                body.append(f'<div class="field"><label>{H.escape(label)}{hh}</label><input type="text" data-n="{H.escape(name)}"></div>')
            elif kind == 'area':
                body.append(f'<div class="field"><label>{H.escape(label)}{hh}</label><textarea data-n="{H.escape(name)}"></textarea></div>')
            elif kind == 'checks':
                opts = (f[2] if fr else f[4]).split('|')
                cks = ''.join(f'<label class="ck"><input type="checkbox" value="{H.escape(o)}" data-g="{H.escape(name)}"> {H.escape(o)}</label>' for o in opts)
                body.append(f'<div class="field"><label>{H.escape(label)}</label><div class="checks">{cks}</div></div>')
    body_html = '\n'.join(body)

    page = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{T['title']}</title><meta name="robots" content="noindex">
<style>
@import url('https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&display=swap');
:root{{--blush:#FBF1EF;--blush2:#F5E3DF;--blue:#E7EDF9;--blue2:#D9E3F5;--ink:#000;--grey:#666}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:'Jost',sans-serif;background:#fff;color:var(--ink);position:relative;line-height:1.55}}
#dotfx{{position:absolute;top:0;left:0;width:100%;height:440px;z-index:-1;pointer-events:none}}
@media (prefers-reduced-motion: reduce){{#dotfx{{display:none}}}}
.wrap{{max-width:860px;margin:0 auto;padding:0 20px 90px}}
header{{padding:86px 0 8px;text-align:center}}
header img{{height:86px;margin-bottom:8px}}
.rule{{width:300px;max-width:70%;height:1px;background:#000;margin:0 auto 10px}}
.sub{{font-size:12px;letter-spacing:.24em;text-transform:uppercase}}
.contact{{margin-top:8px;font-size:11px;letter-spacing:.1em;color:var(--grey)}}
.doc-band{{display:inline-block;background:#000;color:#fff;padding:11px 36px;border-radius:999px;margin-top:22px;
  font-size:15px;letter-spacing:.3em;text-transform:uppercase;font-weight:500}}
.doc-band small{{display:block;font-size:9.5px;letter-spacing:.2em;color:#e8cfca;font-weight:400;text-transform:none}}
.intro{{max-width:640px;margin:18px auto 0;font-size:13px;color:#444;text-align:center}}
h2.band{{background:#000;color:#fff;font-size:12.5px;font-weight:500;letter-spacing:.22em;text-transform:uppercase;
  padding:8px 15px;border-radius:10px;margin:32px 0 12px;display:flex;align-items:center;gap:10px}}
h2.band .num{{background:#fff;color:#000;font-size:11px;padding:1px 7px;border-radius:6px}}
.field{{margin:0 0 14px}}
.field label{{display:block;font-size:12.5px;font-weight:500;letter-spacing:.06em;margin-bottom:5px}}
.field .hint{{font-weight:300;color:var(--grey);font-style:italic;letter-spacing:0}}
input[type=text],textarea{{width:100%;padding:9px 12px;border:1px solid transparent;border-bottom:1px solid #000;
  border-radius:8px 8px 0 0;background:var(--blush);font-family:inherit;font-size:13px;transition:background .15s,border-color .15s}}
textarea{{min-height:64px;resize:vertical}}
input[type=text]:hover,textarea:hover{{background:var(--blue)}}
input[type=text]:focus,textarea:focus{{background:var(--blue2);outline:none;border-color:#000}}
.checks{{display:flex;flex-wrap:wrap;gap:8px}}
.ck{{display:inline-flex;align-items:center;gap:7px;background:var(--blush);border:1px solid transparent;
  padding:7px 13px;border-radius:999px;font-size:12.5px;cursor:pointer;user-select:none;transition:.12s}}
.ck:hover{{background:var(--blue)}}
.ck input{{accent-color:#000;margin:0}}
.ck:has(input:checked){{background:var(--blue2);border-color:#000}}
.modal{{margin:32px 0 0;background:#F3F3F2;border-radius:12px;padding:15px 18px;font-size:12px;color:#333}}
.actions{{position:sticky;bottom:14px;margin-top:26px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap}}
.actions button{{font-family:'Jost';font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;cursor:pointer;
  padding:13px 30px;border-radius:999px;border:1px solid #000}}
.actions .primary{{background:#000;color:#fff}}
.actions .ghost{{background:#fff;color:#000}}
.actions button:hover{{border-color:#E7549F}}
.actions .primary:hover{{background:#E7549F}}
.pdfline{{text-align:center;margin-top:16px;font-size:12px;color:var(--grey)}}
.pdfline a{{color:#000}}
footer{{margin-top:44px;text-align:center;font-size:11px;color:var(--grey);letter-spacing:.12em;text-transform:uppercase}}
@media print{{#dotfx,.actions,.pdfline{{display:none}} h2.band{{-webkit-print-color-adjust:exact}}}}
.socials{{display:flex;gap:20px;justify-content:center;margin-top:16px}}.socials a{{color:#8a8f93;transition:color .15s}}.socials a:hover{{color:#E7549F}}.socials svg{{height:18px;width:18px;fill:currentColor;display:block}}
</style>
</head>
<body>
<canvas id="dotfx"></canvas>
<div class="wrap">
<header>
  <a href="{T['back']}"><img src="{logo}" alt="Lou Denim"></a>
  <div class="rule"></div>
  <p class="sub">{T['role']}</p>
  <div><span class="doc-band">{T['doc']}<small>{T['sub2']}</small></span></div>
  <p class="intro">{T['intro']}</p>
</header>

<form id="brief" onsubmit="return false">
{body_html}
</form>

<div class="modal">{T['modal']}</div>

<div class="actions">
  <button class="primary" id="sendBtn" onclick="sendBrief()">{T['send']}</button>
  <button class="ghost" onclick="window.print()">{T['print']}</button>
</div>
<p class="pdfline">{T['pdf']}<a href="{T['pdffile']}" download>{T['pdflink']}</a></p>

<footer>Lou Denim — loudenim.com · <a href="mailto:lou@loudenim.com" style="color:#000">lou@loudenim.com</a> · <a href="tel:+590690299544" style="color:#000">+590 (0)690 299 544</a><div class="socials"><a href="https://www.instagram.com/loudenim/" target="_blank" rel="noopener" aria-label="Instagram" title="Instagram"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.15 3.23-1.66 4.77-4.92 4.92-1.27.06-1.64.07-4.85.07s-3.58-.01-4.85-.07c-3.26-.15-4.77-1.7-4.92-4.92-.06-1.27-.07-1.64-.07-4.85s.01-3.58.07-4.85C2.38 3.92 3.9 2.38 7.15 2.23 8.42 2.17 8.8 2.16 12 2.16zM12 0C8.74 0 8.33.01 7.05.07 2.7.27.27 2.69.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.2 4.36 2.62 6.78 6.98 6.98 1.28.06 1.69.07 4.95.07s3.67-.01 4.95-.07c4.35-.2 6.78-2.62 6.98-6.98.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95C23.73 2.7 21.31.27 16.95.07 15.67.01 15.26 0 12 0zm0 5.84A6.16 6.16 0 1 0 18.16 12 6.16 6.16 0 0 0 12 5.84zm0 10.15A3.99 3.99 0 1 1 16 12a3.99 3.99 0 0 1-4 3.99zm6.41-11.85a1.44 1.44 0 1 0 1.43 1.44 1.44 1.44 0 0 0-1.43-1.44z"/></svg></a><a href="https://www.tiktok.com/@loudenim" target="_blank" rel="noopener" aria-label="TikTok" title="TikTok"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M12.53.02C13.84 0 15.14.01 16.44 0c.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg></a><a href="https://www.youtube.com/@loudenim" target="_blank" rel="noopener" aria-label="YouTube" title="YouTube"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M23.5 6.19a3.02 3.02 0 0 0-2.12-2.14C19.5 3.55 12 3.55 12 3.55s-7.5 0-9.38.5A3.02 3.02 0 0 0 .5 6.19 31.6 31.6 0 0 0 0 12a31.6 31.6 0 0 0 .5 5.81 3.02 3.02 0 0 0 2.12 2.14c1.88.5 9.38.5 9.38.5s7.5 0 9.38-.5a3.02 3.02 0 0 0 2.12-2.14A31.6 31.6 0 0 0 24 12a31.6 31.6 0 0 0-.5-5.81zM9.55 15.57V8.43L15.82 12z"/></svg></a><a href="https://x.com/loudenim" target="_blank" rel="noopener" aria-label="X" title="X"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M18.9 1.2h3.7l-8.2 9.4L24 22.8h-7.6l-5.9-7.8-6.8 7.8H0l8.8-10L0 1.2h7.8l5.4 7.1zM17.6 20.6h2L6.5 3.3h-2.2z"/></svg></a><a href="https://www.linkedin.com/in/loudenim/" target="_blank" rel="noopener" aria-label="LinkedIn" title="LinkedIn"><svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.36V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.55C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.73V1.72C24 .77 23.2 0 22.22 0z"/></svg></a></div></footer>
</div>
<script>
const KEY='{KEY}';
function collect(){{
  const out=[];let pending=null;
  function item(line){{if(pending){{out.push('');out.push(pending);pending=null;}}out.push(line);}}
  document.querySelectorAll('#brief h2.band, #brief input[type=text], #brief textarea, #brief .field .checks').forEach(el=>{{
    if(el.tagName==='H2'){{
      const num=el.querySelector('.num')?el.querySelector('.num').textContent.trim():'';
      const t=el.textContent.replace(num,'').trim();
      pending='=== '+(num?num+'. ':'')+t+' ===';
    }}
    else if(el.classList&&el.classList.contains('checks')){{
      const label=el.closest('.field').querySelector('label').childNodes[0].textContent.trim();
      const vals=[...el.querySelectorAll('input:checked')].map(i=>i.value);
      if(vals.length)item('• '+label+' : '+vals.join(', '));
    }}
    else{{
      const v=el.value.trim();
      if(v)item('• '+el.dataset.n.replace(/^\d+\. /,'')+' : '+v);
    }}
  }});
  return out.join('\\n');
}}
async function sendBrief(){{
  const f=document.getElementById('brief');
  const soc=f.querySelector('input')?f.querySelector('input').value.trim():'';
  const mailInput=[...f.querySelectorAll('input')].find(i=>(i.dataset.n||'').toLowerCase().includes('email'));
  const mail=mailInput?mailInput.value.trim():'';
  if(!soc||!mail){{alert({json.dumps(T['needid'])});return;}}
  const btn=document.getElementById('sendBtn');const old=btn.textContent;btn.textContent='{T['sending']}';btn.disabled=true;
  try{{
    const res=await fetch('https://api.web3forms.com/submit',{{
      method:'POST',headers:{{'Content-Type':'application/json','Accept':'application/json'}},
      body:JSON.stringify({{access_key:KEY,subject:'{T['subj']}'+soc,from_name:'Brief en ligne Lou Denim',
        name:soc,email:mail,replyto:mail,message:collect()}})
    }});
    const d=await res.json();
    if(d.success){{document.querySelector('.actions').innerHTML='<p style="font-size:14px;max-width:480px;text-align:center">'+{json.dumps(T['thanks'])}+'</p>';}}
    else{{alert(d.message||'Erreur');btn.textContent=old;btn.disabled=false;}}
  }}catch(e){{alert({json.dumps(T['neterr'])});btn.textContent=old;btn.disabled=false;}}
}}
__FX__
</script>
</body>
</html>"""
    return page

FXsrc = open('/root/build_catalog.py').read()
import re as R
m = R.search(r'\(function\(\)\{\nconst cv=document\.getElementById.*?\}\)\(\);', FXsrc, R.S)
fx = m.group(0).replace('const HH=430;','const HH=440;')

for lang, fname in [('fr','brief.html'), ('en','brief-en.html')]:
    page = build(lang).replace('__FX__', fx)
    open(f"{OUT}/{fname}",'w').write(page)
    print(fname, 'ok')
