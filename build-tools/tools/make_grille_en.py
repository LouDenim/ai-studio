#!/usr/bin/env python3
"""Génère grille-en.html (Rate Card en ligne, £ mêmes chiffres) depuis grille.html (FR).
Transposition FR→EN + conversion € → £. Usage: make_grille_en.py <out_dir>"""
import re, sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "/root/catalogue-models"
h = open(f"{OUT}/grille.html").read()

REP = [
 ('<html lang="fr">', '<html lang="en">'),
 ('<title>LOU DENIM — Grille Tarifaire IA</title>', '<title>LOU DENIM — Rate Card</title>'),
 ('<p class="sub">Directeur artistique IA</p>', '<p class="sub">AI Creative Director</p>'),
 ('Grille Tarifaire<small>Services créatifs IA</small>', 'Rate Card<small>AI creative services</small>'),
 # header actions
 ('href="simulator.html" target="_blank" rel="noopener">Estimer votre projet — simulateur</a>',
  'href="simulator-en.html" target="_blank" rel="noopener">Estimate your project — simulator</a>'),
 ('href="Grille_Tarifaire_LouDenim.pdf" download>Télécharger le PDF</a>',
  'href="Rate_Card_LouDenim.pdf" download>Download the PDF</a>'),
 ('href="modeles.html">Catalogue de modèles</a>', 'href="models-en.html">Model catalogue</a>'),
 # images section
 ("Création d'images par IA", 'AI image creation'),
 ('<span class="tag">Lot de 5 minimum</span>', '<span class="tag">Sets of 5 minimum</span>'),
 ('<th>Livrable</th><th class="num">Tarif</th>', '<th>Deliverable</th><th class="num">Rate</th>'),
 ('Produit seul — sans personnage', 'Product only — no character'),
 ('1 personnage + produit', '1 character + product'),
 ('2–3 personnages + produit', '2–3 characters + product'),
 ('Lot de 10 images — campagne complexe', 'Set of 10 images — complex campaign'),
 ("Images vendues par lots de 5 minimum. Tarif à l'unité disponible sur demande.",
  'Images sold in sets of 5 minimum. Per-unit rate available on request.'),
 # video section
 ('Production vidéo par IA', 'AI video production'),
 ('<span class="tag">Produit / service</span>', '<span class="tag">Product / service</span>'),
 ('<th>Que montre votre vidéo ?</th>', '<th>What does your video show?</th>'),
 ('Le produit seul</td>', 'The product on its own</td>'),
 ('Le produit + 1 personnage</td>', 'The product + 1 character</td>'),
 ('UGC : personnage qui parle face caméra, lieu réel inclus', 'UGC: character talking to camera, real location included'),
 ('+ chaque personnage supplémentaire : casting, tenue & mise en scène inclus', '+ each extra character: casting, wardrobe & staging included'),
 ('+ chaque environnement (lieu réel)', '+ each environment (real location)'),
 ('+ chaque produit ou service supplémentaire', '+ each extra product or service'),
 ("Le prix s'additionne : votre format (selon la durée) + vos environnements + vos personnages et produits supplémentaires. Les deux premiers formats sont sur fond neutre ; le format UGC inclut la parole (voix + synchro labiale) et 1 lieu réel. Pour votre combinaison exacte — et les formats plus longs (40 à 60 s) — utilisez le <a href=\"simulator.html\">simulateur</a>.",
  'Prices add up: your format (by duration) + your environments + your extra characters and products. The first two formats are on a plain background; the UGC format includes speech (voice + lip-sync) and 1 real location. For your exact combination — and longer formats (40–60s) — use the <a href="simulator-en.html">simulator</a>.'),
 ('<strong>Personnage :</strong> choisi dans le <a href=\"modeles.html\">catalogue de modèles</a> ou créé pour vous, même tarif. Pour le réserver à votre marque (non réutilisé ailleurs), voir <strong>Exclusivité</strong> dans la section Personnages.',
  '<strong>Character:</strong> picked from the <a href="models-en.html">model catalogue</a> or created for you, same rate. To reserve it for your brand (never reused elsewhere), see <strong>Exclusivity</strong> in the Characters section.'),
 ('<strong>Studio</strong> = fond neutre · <strong>Environnement</strong> = lieu réel · <strong>Personnages</strong> = présents dans la scène — casting, habillement, accessoires et mise en scène <strong>inclus</strong>.',
  '<strong>Studio</strong> = plain background · <strong>Environment</strong> = real location · <strong>Characters</strong> = present in the scene — casting, wardrobe, props and staging <strong>included</strong>.'),
 ("<strong>Un service ?</strong> Son lieu, son enseigne ou sa façade fait office de produit (ex : la façade de la banque, la salle d'un restaurant).",
  "<strong>A service?</strong> Its location, sign or storefront acts as the product (e.g. the bank's facade, a restaurant's dining room)."),
 ('<strong>Style visuel — même tarif :</strong> Photoréaliste · Animation 3D · Dessin animé 2D.',
  '<strong>Visual style — same rate:</strong> Photorealistic · 3D animation · 2D cartoon.'),
 ('<b>HD 720p</b><span>inclus</span>', '<b>HD 720p</b><span>included</span>'),
 # campaign pack
 ('<b>Pack campagne complète</b>', '<b>Full campaign pack</b>'),
 ('3 vidéos sur le même concept (Reel / Story / Feed)', '3 videos on the same concept (Reel / Story / Feed)'),
 ('<span class="price">1&nbsp;500&nbsp;€&nbsp;–&nbsp;2&nbsp;000&nbsp;€</span>',
  '<span class="price">£1,500 – £2,000</span>'),
 # effets
 ('Effets &amp; transformations', 'Effects &amp; transformations'),
 ('Morphing / transformation — le produit se transforme, apparaît, se reconstruit',
  'Morphing / transformation: the product transforms, appears, rebuilds itself'),
 ('Changement de décor ou de saison — même scène, autre lieu, autre ambiance',
  'Set or season change: same scene, different place, different mood'),
 ('Changement de lumière — jour ↔ nuit, néon, golden hour',
  'Relighting — day ↔ night, neon, golden hour'),
 ("Remplacement d'objet ou de couleur produit", 'Object or product-colour swap'),
 ('Motion design — titres animés, typographie, habillage graphique',
  'Motion design: animated titles, typography, graphic package'),
 # son
 ('Son &amp; finitions', 'Sound &amp; finishing'),
 ('Voix off IA (FR / EN / ES)', 'AI voice-over (FR / EN / ES)'),
 ('Musique originale & sound design sur mesure', 'Custom music & sound design'),
 ('Carte de fin — logo animé + signature sonore', 'End card: animated logo + audio signature'),
 ('<td>Sous-titres</td>', '<td>Captions / subtitles</td>'),
 # personnages
 ('<h2 class="band">Personnages</h2>', '<h2 class="band">Characters</h2>'),
 ('Personnage qui parle face caméra — voix + synchro labiale',
  'Character speaking to camera: voice + lip-sync'),
 ('Dialogue entre 2 personnages', '2-character dialogue'),
 ("Droit d'exclusivité sur un personnage sur mesure — réservé à votre marque",
  'Exclusivity rights on a custom character — reserved to your brand'),
 # autres
 ('<h2 class="band">Autres options</h2>', '<h2 class="band">Other options</h2>'),
 ('Storyboard — validation avant production', 'Storyboard — sign-off before production'),
 ('Script / concept', 'Script / concept'),
 ('Tour de révision supplémentaire (au-delà des 2 inclus)', 'Additional revision round (beyond the 2 included)'),
 ('Supplément urgence (livraison sous 48 h)', 'Rush surcharge (delivery within 48 h)'),
 # immobilier
 ('Immobilier &amp; lieux', 'Real estate &amp; places'),
 ('<span class="tag">À partir de vos photos</span>', '<span class="tag">From your photos</span>'),
 ('Visite animée du bien, à partir de vos photos',
  'Animated property tour, from your photos'),
 ('Personnage ajouté pour donner vie à l\'espace', 'Character added to bring the space to life'),
 ('Embellissement photo : ciel, lumière, pelouse, désencombrement — par photo',
  'Photo enhancement: sky, light, lawn, decluttering — per photo'),
 ('Home staging virtuel : meubler une pièce vide ou relooker la déco — par photo',
  'Virtual home staging: furnish an empty room or restyle the décor — per photo'),
 ('Photos du bien à réaliser ? Prise de vue sur place possible.',
  'Need photos of the property? On-location shoot available.'),
 # demande particulière + retainer
 ('<b>Demande particulière</b>', '<b>Special request</b>'),
 ('Toute demande hors grille&nbsp;: sur devis, après échange avec le créatif.',
  'Anything outside this list&nbsp;: on quote, after a chat with the creative.'),
 ('>Sur devis</span>', '>On quote</span>'),
 ('<strong>Commandes régulières&nbsp;?</strong> Un forfait mensuel (retainer) peut être mis en place pour plusieurs vidéos par mois&nbsp;: tarif dégressif, priorité de production, à discuter avec le créatif.',
  '<strong>Regular orders&nbsp;?</strong> A monthly retainer can be arranged for several videos a month&nbsp;: volume rate, production priority, discussed with the creative.'),
 # socle
 ("Chaque vidéo est livrée finie : étalonnée, montée, sonorisée (musique d'illustration et effets sonores inclus) et exportée au format final de votre plateforme.",
  "Every video is delivered finished: colour-graded, edited, sound-designed (library music and sound effects included) and exported in your platform's final format."),
 # conditions
 ("<strong>Tous les prix s'entendent hors taxes</strong> — la TVA applicable est ajoutée au devis.",
  '<strong>All prices exclude VAT</strong> — applicable VAT is added to the quote.'),
 ('<strong>2 révisions incluses</strong> dans chaque prestation — au-delà, facturation selon le barème. · Délai standard : <strong>7 à 10 jours ouvrés</strong>.',
  '<strong>2 revisions included</strong> in every project — beyond that, billed per the rates. · Standard delivery: <strong>7 to 10 business days</strong>.'),
 ("Le <strong>storyboard validé</strong> fixe le point de départ de la production : toute modification d'un élément déjà validé constitue un tour de révision facturé.",
  'An <strong>approved storyboard</strong> sets the production starting point: any change to an already-approved element counts as a billable revision round.'),
 ('Tarifs valables pour une diffusion <strong>réseaux sociaux</strong> — TV, affichage ou écran point de vente : sur devis.',
  'Rates valid for <strong>social-media distribution</strong> — TV, out-of-home or in-store screens: on quote.'),
 ('Fichiers sources, prompts et workflows non livrés — <strong>propriété de Lou Denim</strong>. · Devis final selon brief.',
  'Source files, prompts and workflows not delivered — <strong>property of Lou Denim</strong>. · Final quote depends on the brief.'),
 ("<strong>Droit à l'image et licence&nbsp;: à définir selon vos besoins.</strong>",
  '<strong>Image rights and licence: to be defined to suit your needs.</strong>'),
 ('<strong>Acompte de 50&nbsp;%</strong> avant démarrage. · Aucun travail sans brief validé et accord signé.',
  '<strong>50% deposit</strong> before starting. · No work begins without a validated brief and signed agreement.'),
 # footer
 ('Envie de voir&nbsp;? <a href="portfolio.html">Le travail en images</a>',
  'Want to see? <a href="portfolio-en.html">The work</a>'),
 ('Un projet ? <a href="simulator.html" target="_blank" rel="noopener">Estimez-le en ligne</a> ou écrivez à',
  'A project? <a href="simulator-en.html" target="_blank" rel="noopener">Estimate it online</a> or write to'),
]
miss = 0
for a, b in REP:
    if a in h: h = h.replace(a, b)
    elif a != b: miss += 1; print('  (absent):', a[:75])

# des -> from
h = h.replace('d\u00e8s ', 'from ')
# ranges '75-150 EUR' -> 'GBP75-150' (any dash + nbsp/space tolerant)
h = re.sub('(\\d+)([\u2012\u2013\u2014-])(\\d+)[\u00a0\u202f ]?\u20ac',
           lambda m: '\u00a3'+m.group(1)+m.group(2)+m.group(3), h)
# generic currency 'N EUR' -> 'GBP N,NNN'
def gbp(m):
    n = int(re.sub(r'[^\d]', '', m.group(1)))
    return '\u00a3' + format(n, ',')
h = re.sub('(\\d[\\d\u00a0\u202f ]*)\u20ac', gbp, h)

open(f"{OUT}/grille-en.html", "w").write(h)
print('grille-en.html ok - non traduits:', miss)
