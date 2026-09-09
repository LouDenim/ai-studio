# -*- coding: utf-8 -*-
"""
Genere les deux grilles tarifaires (FR + EN) de Lou Denim, puis les PDF.

Le gabarit precedent avait ete supprime du depot le 1er septembre 2026 dans le
meme commit que la regeneration des PDF ; celui-ci est reconstruit a partir des
PDF en ligne (texte, geometrie, couleurs et polices releves au point pres) et
DOIT etre commite avec eux.

Usage :  python3 build_grille.py            -> ecrit les 2 HTML + les 2 PDF
"""
import os, html as H

OUT = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(OUT, 'fonts')
LOGO = os.path.join(OUT, 'assets', 'lou-denim-logo.svg')

# --------------------------------------------------------------------------
# DONNEES  (source unique des prix de la grille)
# --------------------------------------------------------------------------
def data(lang):
    fr = lang == 'fr'
    c = (lambda n: f"{n} €") if fr else (lambda n: f"£{n}")
    return dict(
      lang        = 'fr' if fr else 'en',
      kicker      = "Directeur artistique IA" if fr else "AI creative director",
      title       = "Grille tarifaire" if fr else "Rate card",
      subtitle    = "Services créatifs IA · 2026" if fr else "AI creative services · 2026",
      intro       = ("Les tarifs de cette grille correspondent exactement au simulateur de devis "
                     "en ligne. Le prix s’additionne : votre format, selon la durée, plus vos options.")
                    if fr else
                    ("The rates on this card match the online quote simulator exactly. Prices add up: "
                     "your format, by duration, plus your options."),
      footer      = "Lou Denim — ai.loudenim.com",
      sections = [
        dict(kind='ladder',
          title="Production vidéo par IA" if fr else "AI video production",
          tag="Produit / service" if fr else "Product / service",
          head=("Que montre votre vidéo ?" if fr else "What does your video show?"),
          cols=["15s","20s","30s","40s","50s"],
          rows=[
            ("Le produit seul" if fr else "The product on its own",
             "Votre produit mis en avant en studio ou sur fond neutre. Personne à l’écran."
             if fr else "Your product showcased in studio or on a neutral background. No one on screen.",
             [c("300"),c("400"),c("600"),c("800"),c("1 000" if fr else "1,000")]),
            ("Le produit + un personnage" if fr else "The product + one character",
             "Format publicitaire classique. Fond neutre par défaut."
             if fr else "The classic ad format. Neutral background by default.",
             [c("350"),c("450"),c("700"),c("900"),c("1 150" if fr else "1,150")]),
            ("UGC — face caméra" if fr else "UGC — to camera",
             "Un personnage parle au spectateur, teste ou présente le produit. Lieu réel inclus."
             if fr else "A character speaks to camera, tests or presents the product. One real location included.",
             [c("400"),c("500"),c("800"),c("1 000" if fr else "1,000"),c("1 300" if fr else "1,300")]),
            ("Film de marque" if fr else "Brand film",
             "Un film qui raconte une histoire, sans produit à vendre à l’écran. Un personnage inclus."
             if fr else "A film that tells a story, with no product to sell on screen. One character included.",
             [c("350"),c("450"),c("700"),c("900"),c("1 150" if fr else "1,150")]),
          ]),
        dict(kind='table',
          title="Rythme du film" if fr else "Pace of the film",
          tag="Par film" if fr else "Per film",
          w2=15.337 if fr else 14.370,
          head=("Option" if fr else "Option", "Supplément" if fr else "Surcharge"),
          rows=[
            ("Classique" if fr else "Standard",
             "Du plan qui dure au rythme d’une publicité ordinaire."
             if fr else "From long takes to the pace of an ordinary commercial.",
             "inclus" if fr else "included"),
            ("Rapide" if fr else "Fast",
             "Ça enchaîne, une image nouvelle toutes les deux secondes."
             if fr else "Cut to cut, a new image every couple of seconds.",
             "+ 20 %" if fr else "+ 20%"),
          ]),
        dict(kind='chips',
          title="Résolution" if fr else "Resolution",
          tag="Supplément" if fr else "Surcharge",
          chips=[("HD 720p","inclus" if fr else "included"),
                 ("Full HD 1080p","+ 25 %" if fr else "+ 25%"),
                 ("4K upscale","+ 50 %" if fr else "+ 50%")],
          note="Supplément de résolution appliqué au tarif vidéo uniquement."
               if fr else "Resolution surcharge applied to the video rate only."),
        dict(kind='centered',
          title="Style visuel — même tarif" if fr else "Visual style — same rate",
          tag="",
          text="Photoréaliste · Animation 3D · Dessin animé 2D"
               if fr else "Photorealistic · 3D animation · 2D cartoon"),
        dict(kind='table',
          title="Ajouts à la scène" if fr else "Added to the scene",
          tag="Tarif" if fr else "Rate",
          head=("Livrable" if fr else "Deliverable","Tarif" if fr else "Rate"),
          rows=[
            ("Environnement" if fr else "Environment",
             "chaque lieu supplémentaire" if fr else "each additional location", c("150")),
            ("Personnage supplémentaire" if fr else "Extra character",
             "casting, tenue et mise en scène inclus" if fr else "casting, wardrobe and staging included", c("150")),
            # ligne « Visage hors catalogue » (+50) retiree le 9 septembre 2026,
            # en meme temps que sa suppression du simulateur.
            ("Produit ou service en plus" if fr else "Extra product or service", "", c("75")),
          ]),
        dict(kind='table',
          title="Effets & transformations" if fr else "Effects & transformations",
          tag="Tarif" if fr else "Rate",
          head=("Livrable" if fr else "Deliverable","Tarif" if fr else "Rate"),
          rows=[
            ("Morphing / transformation","le produit se transforme, apparaît, se reconstruit"
             if fr else "the product transforms, appears, rebuilds itself", c("150")),
            ("Changement de décor ou de saison" if fr else "Set or season change",
             "même scène, autre lieu, autre ambiance" if fr else "same scene, another place, another mood", c("150")),
            ("Changement de lumière" if fr else "Relighting",
             "jour ou nuit, néon, golden hour" if fr else "day or night, neon, golden hour", c("150")),
            ("Remplacement d’objet ou de couleur produit" if fr else "Object or product-colour swap","", c("150")),
            ("Motion design","titres animés, typographie, habillage graphique"
             if fr else "animated titles, typography, graphics", c("150")),
            ("Motion transfer","à partir de votre vidéo source — prise de vue non incluse"
             if fr else "from your own source footage — filming not included", c("150")),
          ]),
        dict(kind='table',
          title="Son & finitions" if fr else "Sound & finishing",
          tag="Tarif" if fr else "Rate",
          head=("Livrable" if fr else "Deliverable","Tarif" if fr else "Rate"),
          rows=[
            ("Voix off IA" if fr else "AI voice-over",
             "français, anglais, espagnol" if fr else "French, English, Spanish", c("100")),
            ("Musique & sound design" if fr else "Music & sound design","", c("150")),
            ("Carte de fin" if fr else "End card",
             "logo animé + signature sonore" if fr else "animated logo + audio signature", c("150")),
            ("Sous-titres" if fr else "Captions / subtitles","", c("75")),
          ]),
        dict(kind='table',
          title="Personnages" if fr else "Characters",
          tag="Tarif" if fr else "Rate",
          head=("Livrable" if fr else "Deliverable","Tarif" if fr else "Rate"),
          rows=[
            ("Personnage qui parle" if fr else "Character speaking to camera",
             "voix + synchronisation labiale" if fr else "voice + lip-sync", c("100")),
            ("Dialogue entre deux personnages" if fr else "Two-character dialogue","", c("200")),
            # 9 septembre 2026 : 300 -> 500, renomme, duree precisee
            ("Exclusivité du mannequin" if fr else "Model exclusivity",
             "réservé à votre marque, 12 mois" if fr else "reserved to your brand, 12 months", c("500")),
          ]),
        dict(kind='table',
          title="Autres options" if fr else "Other options",
          tag="Tarif" if fr else "Rate",
          head=("Livrable" if fr else "Deliverable","Tarif" if fr else "Rate"),
          rows=[
            ("Storyboard","validation avant production" if fr else "sign-off before production", c("150")),
            ("Concept","l’idée du film, avant écriture — jusqu’à 50 s"
             if fr else "the idea for the film, before writing — up to 50s", c("200")),
            ("Script","le film écrit, plan par plan — jusqu’à 50 s"
             if fr else "the film written out, shot by shot — up to 50s", c("200")),
            ("Tour de révision supplémentaire" if fr else "Additional revision round",
             "au-delà des 2 inclus" if fr else "beyond the 2 included", c("150")),
            ("Supplément urgence" if fr else "Rush surcharge",
             "livraison sous 72 h" if fr else "delivery within 72 hours", "+ 40 %" if fr else "+ 40%"),
          ]),
        dict(kind='table', newpage=True,
          title="Images par IA" if fr else "AI images",
          tag="Lot de 5 images minimum" if fr else "Sets of 5 images minimum",
          head=("Livrable" if fr else "Deliverable","Tarif" if fr else "Rate"),
          rows=[
            ("Produit seul" if fr else "Product only","lot de 5" if fr else "set of 5", c("250")),
            ("1 personnage + produit" if fr else "1 character + product","lot de 5" if fr else "set of 5", c("380")),
            ("2 à 3 personnages + produit" if fr else "2 to 3 characters + product",
             "lot de 5" if fr else "set of 5", c("600")),
            ("Campagne complexe" if fr else "Complex campaign","lot de 10" if fr else "set of 10", c("900")),
            ("Environnement" if fr else "Environment",
             "par environnement, pour un lot" if fr else "per environment, for a set", c("50")),
          ],
          note="Vendues par lots. Tarif à l’unité sur demande." if fr else "Sold in sets. Unit rate on request."),
        dict(kind='table',
          title="Immobilier & lieux" if fr else "Property & places",
          w2=17.837 if fr else 17.308,
          tag="Tarif" if fr else "Rate",
          head=("Livrable" if fr else "Deliverable","Tarif" if fr else "Rate"),
          rows=[
            ("Visite animée du bien" if fr else "Animated property tour",
             "jusqu’à 15 s, maxi 5 images" if fr else "up to 15s, max 5 images", c("300")),
            ("Visite animée du bien" if fr else "Animated property tour",
             "jusqu’à 20 s, maxi 7 images" if fr else "up to 20s, max 7 images", c("400")),
            ("Visite animée du bien" if fr else "Animated property tour",
             "jusqu’à 30 s, maxi 10 images" if fr else "up to 30s, max 10 images", c("500")),
            ("Musique & ambiance sonore" if fr else "Music & ambience","", c("50")),
            ("Personnage ajouté" if fr else "Added character",
             "mise en vie du lieu" if fr else "bringing the place to life", c("150")),
            ("Embellissement photo" if fr else "Photo enhancement",
             "ciel, lumière, pelouse, désencombrement" if fr else "sky, light, lawn, decluttering",
             c("25")+(" / photo")),
            ("Home staging virtuel" if fr else "Virtual home staging",
             "meubler une pièce vide ou relooker la déco" if fr else "furnish an empty room or restyle the decor",
             c("75")+(" / photo")),
          ],
          note="À partir de vos photos. Mouvements de caméra, transitions, montage rythmé."
               if fr else "From your own photos. Camera moves, transitions, rhythmic editing."),
        dict(kind='note',
          title="Demande particulière" if fr else "Anything else",
          tag="Sur devis" if fr else "On request",
          note="Pour toute demande hors grille tarifaire, un devis est établi après échange avec le créatif."
               if fr else "For anything outside this rate card, a quote is issued after a conversation with the creative."),
        dict(kind='plain', newpage=True,
          title="Livraison" if fr else "Delivery", tag="",
          text="Chaque vidéo est livrée étalonnée, montée et exportée au format final de votre plateforme."
               if fr else "Every video is delivered colour-graded, edited and exported in your platform’s final format."),
        dict(kind='terms',
          title="Conditions" if fr else "Terms", tag="",
          items=[
            [("b","Tous les prix s’entendent hors taxes" if fr else "All prices exclude VAT"),
             ("l"," — la TVA applicable est ajoutée au devis." if fr else " — applicable VAT is added to the quote.")],
            [("b","2 révisions incluses" if fr else "2 revisions included"),
             ("l"," dans chaque prestation — au-delà, facturation selon le barème ci-dessus. · Délai de livraison standard : "
                  if fr else " in every project — beyond that, billed per the rates above. · Standard delivery: "),
             ("b","7 à 10 jours ouvrés" if fr else "7 to 10 business days"),
             ("l"," selon projet." if fr else " depending on the project.")],
            [("l","Le " if fr else "An "),("b","storyboard validé" if fr else "approved storyboard"),
             ("l"," fixe le point de départ de la production : toute modification d’un élément déjà validé "
                  "(storyboard, script, plan) constitue un tour de révision facturé."
                  if fr else " sets the production starting point: any change to an already-approved element "
                             "(storyboard, script, shot) counts as a billable revision round.")],
            [("l","Fichiers sources, prompts et workflows non livrés — " if fr else "Source files, prompts and workflows not delivered — "),
             ("b","propriété de Lou Denim" if fr else "property of Lou Denim"),("l",".")],
            [("b","Les tarifs de cette grille sont une base d’estimation. Le devis final est établi par Lou Denim."
                  if fr else "The rates in this card are a basis for estimation. The final quote is set by Lou Denim."),
             ("l"," Des frais de production peuvent s’ajouter selon la complexité du projet et le volume de générations nécessaires."
                  if fr else " Production costs may be added depending on the complexity of the project and the volume of generations required.")],
            [("b","Droits d’utilisation web & réseaux sociaux : inclus." if fr else "Web & social-media usage rights: included."),
             ("l"," Toute autre diffusion fait l’objet d’une cession : presse, édition (catalogue, brochure), campagne digitale, "
                  "TV, cinéma, affichage 4×3, écran PLV. "
                  if fr else " Any other distribution requires a separate licence: press, print (catalogue, brochure), digital campaign, "
                             "TV, cinema, 4×3 out-of-home, in-store screens. "),
             ("b","Territoire et durée à définir avec Lou Denim." if fr else "Territory and duration to be agreed with Lou Denim.")],
            [("b","Acompte de 50 % au-delà de 1 000 €" if fr else "50% deposit above £1,000"),
             ("l",", requis avant démarrage. · Aucun travail sans brief validé et accord signé."
                  if fr else ", required before starting. · No work begins without a validated brief and a signed agreement.")],
          ]),
      ])

# --------------------------------------------------------------------------
# GABARIT
# --------------------------------------------------------------------------
CSS = """
@font-face{font-family:'Jost';src:url('fonts/jost-latin-300-normal.woff2')format('woff2');font-weight:300}
@font-face{font-family:'Jost';src:url('fonts/jost-latin-400-normal.woff2')format('woff2');font-weight:400}
@font-face{font-family:'Jost';src:url('fonts/jost-latin-500-normal.woff2')format('woff2');font-weight:500}
@font-face{font-family:'JBMono';src:url('fonts/JetBrainsMono-Regular.ttf')format('truetype');font-weight:400}
@font-face{font-family:'JBMono';src:url('fonts/JetBrainsMono-Medium.ttf')format('truetype');font-weight:500}

@page{
  size:A4; margin:15mm 16mm 13mm 16mm;
  @bottom-left{ content:"LOU DENIM — AI.LOUDENIM.COM"; font-family:'JBMono'; font-size:6pt;
    letter-spacing:.14em; color:#0B0B0D; vertical-align:top; padding-top:11pt; }
  @bottom-right{ content:counter(page)" / "counter(pages); font-family:'JBMono'; font-size:6pt;
    letter-spacing:.10em; color:#0B0B0D; vertical-align:top; padding-top:11pt; }
}
*{box-sizing:border-box}
body{margin:0;font-family:'Jost';color:#0B0B0D;-weasy-hyphens:none}
h2,h3,p,table{margin:0}
.brand{text-align:center;margin:0 0 0 0}
.brand img{width:58mm;display:block;margin:2mm auto 0}
.brand .rule{width:32mm;height:1pt;background:#E7549F;margin:4.79mm auto 4.8mm}
.brand .kick{font-family:'JBMono';font-size:6.6pt;letter-spacing:.34em;text-indent:.34em;color:#E7549F;
  text-transform:uppercase;margin-bottom:7.2mm}
.tband{background:#0B0B0D;color:#fff;text-align:center;height:76.5pt;padding:19.5pt 6mm 0}
.tband h1{margin:0;font-weight:300;font-size:18.5pt;letter-spacing:.30em;text-indent:.30em;text-transform:uppercase;line-height:1}
.tband .sub{font-family:'JBMono';font-size:6.5pt;letter-spacing:.28em;text-indent:.28em;color:#E7549F;
  text-transform:uppercase;margin-top:9.5pt}
.intro{font-weight:300;font-size:9.3pt;line-height:1.5;color:#3A3A42;margin:7.58mm 0 7.13mm;max-width:440pt}
section{break-inside:avoid;margin-bottom:6.4mm}
.band{background:#0B0B0D;color:#fff;height:31.5pt;display:flex;align-items:center;
  justify-content:space-between;padding:0 5mm}
.band h2{font-weight:400;font-size:10pt;letter-spacing:.20em;text-transform:uppercase}
.band .tag{font-family:'JBMono';font-size:6pt;letter-spacing:.20em;color:#E7549F;text-transform:uppercase}
table{width:100%;border-collapse:collapse;table-layout:fixed;
  border:.5pt solid #E4E4E8;border-top:none}
thead th{background:#FBEAF2;color:#8B3F66;font-family:'JBMono';font-weight:500;font-size:6.1pt;
  letter-spacing:.16em;text-transform:uppercase;text-align:right;padding:6.2pt 4.988mm;height:22.7pt}
thead th:first-child{text-align:left}
tbody td{border-bottom:.5pt solid #E4E4E8;padding:8.4pt 4.988mm 7.47pt;vertical-align:top;text-align:right}
tbody tr:last-child td{border-bottom:none}
tbody td.l{text-align:left}
.nm{font-weight:400;font-size:9.5pt;line-height:1.15}
.ds{font-weight:300;font-size:7.6pt;line-height:1.4145;color:#77777F;margin-top:1.55pt}
.pr{display:block;font-weight:400;font-size:9.5pt;line-height:1.15;white-space:nowrap}
.wrap{border:.5pt solid #E4E4E8;border-top:none}
.chips{display:flex;border:.5pt solid #E4E4E8;border-top:none}
.chip{flex:1;text-align:center;padding:4.89mm 2mm 5.48mm;border-left:.5pt solid #E4E4E8}
.chip:first-child{border-left:none}
.chip.c2{background:#FBEAF2}
.chip.c3{background:#F6DBE8}
.chip b{display:block;font-weight:400;font-size:9.6pt;text-transform:uppercase;letter-spacing:.142em}
.chip span{display:block;font-family:'JBMono';font-size:8.2pt;color:#E7549F;margin-top:2.6mm;
  letter-spacing:.162em;text-transform:uppercase}
.mid{border:.5pt solid #E4E4E8;border-top:none;text-align:center;padding:4.87mm 4mm}
.mid p{font-size:10.4pt;font-weight:400;letter-spacing:.06em}
.plain{border:.5pt solid #E4E4E8;border-top:none;padding:3.91mm 5.2mm}
.plain p{font-weight:300;font-size:9.2pt;line-height:1.5;color:#3A3A42}
.note{font-weight:300;font-size:7.8pt;line-height:1.4;color:#77777F;padding:2.6mm 0 0 .49mm}
.terms{border:.5pt solid #E4E4E8;border-top:none;padding:3.69mm 4.988mm 4.8mm}
.terms p{font-size:8.1pt;line-height:1.48;margin:0 0 4.94mm}
.terms p:last-child{margin-bottom:0}
.terms b{font-weight:500;color:#0B0B0D}
.terms span{font-weight:300;color:#3A3A42}
.pagebreak{break-before:page}
"""

def esc(s): return H.escape(s, quote=False)

def build(d):
    P=[]
    P.append(f'<!DOCTYPE html><html lang="{d["lang"]}"><head><meta charset="utf-8">'
             f'<title>{esc(d["title"])}</title><style>{CSS}</style></head><body>')
    P.append('<div class="brand">'
             f'<img src="assets/lou-denim-logo.svg" alt="Lou Denim">'
             '<div class="rule"></div>'
             f'<div class="kick">{esc(d["kicker"])}</div></div>')
    P.append(f'<div class="tband"><h1>{esc(d["title"])}</h1>'
             f'<div class="sub">{esc(d["subtitle"])}</div></div>')
    P.append(f'<p class="intro">{esc(d["intro"])}</p>')

    for s in d['sections']:
        cls = 'pagebreak' if s.get('newpage') else ''
        P.append(f'<section class="{cls}">')
        tag = f'<span class="tag">{esc(s["tag"])}</span>' if s.get('tag') else ''
        P.append(f'<div class="band"><h2>{esc(s["title"])}</h2>{tag}</div>')
        k = s['kind']

        if k == 'ladder':
            w = f'{100/6:.4f}%'
            P.append('<table><colgroup><col style="width:35.292%">'
                     + f'<col style="width:12.921%">'*5 + '</colgroup><thead><tr>'
                     f'<th>{esc(s["head"])}</th>'
                     + ''.join(f'<th>{esc(c)}</th>' for c in s['cols']) + '</tr></thead><tbody>')
            for nm, ds, prices in s['rows']:
                P.append('<tr><td class="l"><div class="nm">'+esc(nm)+'</div>'
                         + (f'<div class="ds">{esc(ds)}</div>' if ds else '') + '</td>'
                         + ''.join(f'<td><span class="pr">{esc(p)}</span></td>' for p in prices)
                         + '</tr>')
            P.append('</tbody></table>')

        elif k == 'table':
            P.append(f'<table><colgroup><col><col style="width:{s.get("w2",12.921)}%"></colgroup><thead><tr>'
                     f'<th>{esc(s["head"][0])}</th><th>{esc(s["head"][1])}</th></tr></thead><tbody>')
            for nm, ds, pr in s['rows']:
                P.append('<tr><td class="l"><div class="nm">'+esc(nm)+'</div>'
                         + (f'<div class="ds">{esc(ds)}</div>' if ds else '')
                         + f'</td><td><span class="pr">{esc(pr)}</span></td></tr>')
            P.append('</tbody></table>')
            if s.get('note'): P.append(f'<p class="note">{esc(s["note"])}</p>')

        elif k == 'chips':
            P.append('<div class="chips">' + ''.join(
                f'<div class="chip c{i+1}"><b>{esc(n)}</b><span>{esc(v)}</span></div>'
                for i,(n,v) in enumerate(s['chips'])) + '</div>')
            P.append(f'<p class="note">{esc(s["note"])}</p>')

        elif k == 'centered':
            P.append(f'<div class="mid"><p>{esc(s["text"])}</p></div>')

        elif k == 'plain':
            P.append(f'<div class="plain"><p>{esc(s["text"])}</p></div>')

        elif k == 'note':
            P.append(f'<div class="plain"><p>{esc(s["note"])}</p></div>')

        elif k == 'terms':
            P.append('<div class="terms">')
            for item in s['items']:
                P.append('<p>' + ''.join(
                    (f'<b>{esc(t)}</b>' if w=='b' else f'<span>{esc(t)}</span>') for w,t in item) + '</p>')
            P.append('</div>')

        P.append('</section>')
    P.append('</body></html>')
    return '\n'.join(P)

if __name__ == '__main__':
    from weasyprint import HTML
    for lang, htmlname, pdfname in [('fr','grille-tarifaire.html','Grille_Tarifaire_LouDenim.pdf'),
                                    ('en','grille-tarifaire-en.html','Rate_Card_LouDenim.pdf')]:
        d = data(lang)
        doc = build(d)
        hp = os.path.join(OUT, htmlname)
        open(hp,'w',encoding='utf-8').write(doc)
        HTML(filename=hp, base_url=OUT).write_pdf(os.path.join(OUT,'rebuilt-'+pdfname))
        print('ecrit :', htmlname, '->', 'rebuilt-'+pdfname)
