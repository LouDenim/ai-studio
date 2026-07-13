# Lou Denim — Système Grille + Devis IA (setup & maintenance)

Fiche de référence. Tout est verrouillé ici pour ne rien reperdre.

## ⚠️ SOURCE UNIQUE DES PRIX : `prices.json`
Tous les tarifs (vidéo, images, effets, son, personnages, immobilier, socle) vivent dans
`prices.json` à la racine du skill. Pour changer un prix : modifier prices.json, puis
régénérer (1) grille.html via `tools/build_grille_web.py`, (2) les PDF FR/EN (templates
mis à jour à la main pour refléter prices.json, puis weasyprint), (3) le simulateur
(constantes JS dans `templates/simulateur-devis.html` — SCENES/FX/SON/PERSO/IMMO).
Validé par Lou le 12/07/2026 : effets 150 · voix 100 · musique 100 · carte de fin 150 ·
sous-titres 75 · dialogue 200 · immobilier 300/400/500, +150 perso, 25/photo, 75/photo staging.

## Taglines officielles du site (12/07/2026, validées mot à mot par Lou)
- FR (rév. 13/07/2026) : « Création générative au service des marques : images et campagnes vidéo IA sur mesure. »
- EN (rév. 13/07/2026) : « Gen AI for brands: images and video campaigns ready to run. »
Interdits par Lou : « publicitaire » en tête, « personnages cohérents / consistent characters »,
« produits mis en scène / staged products », « campagnes livrées finies », toute mention photographe,
« prêtes à diffuser » (implique du pré-fabriqué). Vocabulaire voulu : Gen AI / génératif, sur mesure.

## Accent ROSE (12/07/2026, soir) — décision Lou
Rose accent #E7549F (pipette sur le survol du menu de loudenim.com/Portfoliobox — à affiner si
Lou fournit le hex exact). Règle : le rose n'apparaît QU'AU SURVOL (cartes, boutons, icônes
sociales, pastilles FR/EN) — jamais en décor permanent, sauf les pastilles langue FR/EN
(liseré rose, active remplie). Champs de formulaire : hover BLEU conservé (saisie ≠ navigation).
Bandeau clients : logos EN COULEUR (img/logos-color/), gris monochrome dispo dans img/logos/.
Boucle marquee : 2 séquences x3 logos, translateX(-50%), 60 s.

## 🔒 Packs dégressifs — UPSELL SIMULATEUR (verrouillé 13/07/2026)
Sous le total du simulateur (devis.html + devis-en.html), deux boîtes d'upsell qui se
recalculent EN DIRECT à partir du sous-total vidéo :
- **Pack de 3 vidéos : −20 %** → prix/vidéo = round(videoTotal × 0,80), + total « 3 vidéos ».
- **Pack de 10 vidéos : −40 %** → prix/vidéo = round(videoTotal × 0,60), + total « 10 vidéos ».
Règles verrouillées :
- La remise s'applique au **sous-total VIDÉO uniquement** (`window._videoTotal` dans calc()) :
  scène + résolution + urgence + fx + son + personnages + options + révisions. **Exclut** les
  images (lots, déjà dégressifs) et l'immobilier. Les boîtes n'apparaissent que si videoTotal>0,
  sinon un indice gris « Configurez une vidéo pour voir les tarifs de pack ».
- Boîtes = fonds blush2 (pack 3) et blush3 (pack 10, plus profond = plus grosse remise).
  **Économies en NOIR** (jamais rose permanent — règle rose = survol only) ; liseré rose au survol.
- Légende obligatoire : « Tarifs indicatifs pour des vidéos similaires, ajustés selon vos besoins »
  / « Indicative rates for similar videos, adjusted to your needs ».
- Boîte estimation **alignée en haut** avec la boîte « Vos coordonnées » (.summary margin-top:26px ;
  colonne droite 320px). Le paragraphe « retainer » a été RETIRÉ du simulateur (le retainer mensuel
  reste sur la grille en ligne + PDF — offre distincte).
- Générateur EN : `tools/make_devis_en.py` (libellés packs traduits, £ via eur()).
- ⚠️ Ne pas confondre avec le « Pack campagne complète » de la grille (1 500–2 000 € = 3 formats
  d'UN concept Reel/Story/Feed) : produit différent des 3 vidéos similaires du simulateur.

## Divers verrouillés 13/07/2026
- Sous-titres : FR « Sous-titres » · EN « Captions / subtitles » (plus « incrustés / burned-in »).
  Source prices.json (soustitres.label/.en) → grille web + PDF + simulateurs.
- Licence : ligne bold « **Droit à l'image et licence : à définir selon vos besoins.** » /
  « Image rights and licence: to be defined to suit your needs. » — grille en ligne + PDF FR/EN (Conditions).
- PDF rate card FR/EN : ordre ORIGINAL rétabli (13/07 soir, décision Lou « trop de texte ») —
  tableau vidéo → notes Studio/Environnement/Style → chips résolution (720/1080/4K). NE PAS remonter les chips.
- **Rate card EN en ligne : grille-en.html** — généré par `tools/make_grille_en.py` (transpose grille.html
  FR→EN + convertit € → £ mêmes chiffres, séparateurs U+00A0/U+202F gérés). La carte accueil EN « Rate card »
  ouvre grille-en.html (page avec bouton téléchargement) au lieu de télécharger le PDF direct — parité avec le FR.
- Brief (en ligne + PDF FR/EN) : champ « Site web / Website » ajouté (section 1) ; « Territoire de diffusion /
  Distribution territory » → « Territoire / Territory » (ex. Royaume-Uni, États-Unis, France / UK, U.S., France) ;
  intro « autant que possible / as much as possible » ; mantra PDF sans tiret (« … aucun projet ne démarre, c'est ce qui… »).
- Page « Le travail en images » (travail.html / travail-en.html) : bandeau « Vidéos IA » (sans
  « studio Lou Denim ») ; intro « Une sélection de films 16:9 et de formats verticaux, créés par le
  studio. » ; 5e carte accueil, liseré NOIR comme les autres (pas de rose permanent) ;
  desc EN « AI videos built for both cinematic widescreen and vertical mobile screens ».
- Intro simulateur (sans tiret) : « … Ceci est une estimation, votre devis final est établi par Lou Denim. … »

## Peau graphique verrouillée (12/07/2026, révisée le soir)
**FOND WEB DÉFINITIF : « comète sur grille de points »** — canvas JS (généré par les
tools/build_*), grille de points gris 34px, une comète lumineuse suit une courbe de Bézier
ALÉATOIRE à chaque cycle (départ/arrivée/contrôles tirés au sort, durée 6,5–9 s), traîne
qui s'éteint, fondu doux (mask) sous le bloc central et en bas. Zéro vidéo, ~2 Ko de JS.
Pages : accueil, modèles FR/EN, grille web, simulateur. Les PDF gardent le blush.

## (Historique) Peau gradient (12/07/2026)
- Dégradé blush ANIMÉ en fond d'en-tête : vidéos `img/gradient-loop.webm` (97 Ko) +
  `gradient-loop.mp4` (850 Ko), boucle parfaite 20 s, poster `img/hero-still.jpg`,
  fallback image fixe si prefers-reduced-motion. Généré par frames numpy
  (champ de sinus, cycles entiers → boucle sans couture) + ffmpeg.
- Titres de document en PASTILLE arrondie (border-radius 999px web / 4mm PDF).
- Bandes de section : radius 10px web / 2.5mm PDF (lou-denim.css mis à jour).
- Pas de grain. Palette FBF1EF / F5E3DF / EBC9C3, jamais de dérive grise/verte.

## ✅ EN LIGNE depuis le 12/07/2026
- **Site AI Studio : https://loudenim.github.io/ai-studio/** — TOUT-EN-UN depuis le 12/07 au soir :
  le simulateur vit sur le site (devis.html), plus besoin de tiiny.host. L'ancienne adresse
  tiiny (loudenim-devis-ia.tiiny.site) reste en ligne comme legacy — Lou peut la supprimer
  ou y laisser l'ancien fichier.
- Site : (dépôt github.com/LouDenim/ai-studio, branche main, Pages actif)
- Pages : index.html (accueil FR/EN) · modeles.html (FR) · models-en.html (EN) · grille.html · 4 PDF · img/
- Mises à jour : modifier localement → git push (token 'claude-ai-studio', expire ~11/08/2026) → en ligne en ~1 min.
- ⚠️ Le proxy GitHub du sandbox ne peut PAS créer de dépôts ni activer Pages (Lou le fait via l'UI web) — le push fonctionne.
- **Brief en ligne : brief.html (FR) + brief-en.html (EN)** — générés par tools/build_brief_web.py
  (97 champs, 11 sections = miroir du PDF ; blush au repos, bleu au survol/focus ;
  « Envoyer à Lou » via Web3Forms ; bouton Imprimer/PDF ; lien de secours vers le PDF).
- Fond web v3 : DOUBLE comète (une à gauche, une à droite, cycles décalés) — points noirs
  au passage, gris en retombée, rayon 210, durée 5-7 s, quasi aucun temps mort.
- **Simulateur EN : devis-en.html** (£, mêmes chiffres, généré par tools/make_devis_en.py depuis le template FR).
- Reste : liens YouTube galerie · DNS ai.loudenim.com · menu « AI » Portfoliobox (en dernier).

## Architecture en ligne (cible GitHub Pages)
- Site (dépôt GitHub → Pages) : `index.html` (catalogue) + `grille.html` (grille en ligne,
  boutons PDF/simulateur) + `Grille_Tarifaire_LouDenim.pdf` + `Rate_Card_LouDenim.pdf`
  + `img/`. Dossier local : `/root/catalogue-models`.
- Simulateur : reste sur https://loudenim-devis-ia.tiiny.site (fichier autonome,
  vidéos embarquées en base64, ~1,1 Mo). Tokens `#CATALOGUE#`/`#GRILLE#` à patcher
  avec les URL Pages avant livraison.
- tiiny.host gratuit = 3 Mo → le catalogue (16 Mo) vit sur GitHub Pages (gratuit).
- Sous-domaine prévu : studio.loudenim.com (CNAME vers GitHub Pages) — vérifier où
  est géré le DNS de loudenim.com (Portfoliobox ou registrar).
- Page « Le travail en images » : à créer quand Lou fournit ses liens YouTube (embeds).

## Le simulateur en ligne (client-facing)
- **Lien public (à envoyer aux clients) :** https://loudenim-devis-ia.tiiny.site
- **Hébergé sur** tiiny.host (compte lou@loudenim.com).
- **Clé Web3Forms (publique, OK dans le code) :** `fbddfe3a-fa8b-49d4-bbe3-5b329a81dd67`
- Les demandes arrivent par **email à lou@loudenim.com** (le mail du client est en reply-to → réponse directe avec le devis).
- Le tout premier email peut partir en spam → marquer « pas spam » une fois.

## Fichiers (dans ce skill)
- `templates/grille-tarifaire.html` — Grille tarifaire **FR** (source, verrouillée)
- `templates/grille-tarifaire-en.html` — Rate Card **EN**
- `templates/brief-video.html` — Brief vidéo **FR**
- `templates/brief-video-en.html` — AI Video Brief **EN**
- `templates/simulateur-devis.html` — Simulateur (template, logo = `__LOGO_SRC__`, clé Web3Forms incluse)
- `Simulateur_Devis_LouDenim.html` — **Simulateur FINAL** (logo + clé intégrés) = **c'est CE fichier qui est hébergé sur tiiny.host**

## Prix (grille ET simulateur — TOUJOURS synchro)
Vidéo (15s / 20s / 30–40s) :
- Produit seul — studio : 350 / 450 / 550
- Produit en environnement : 400 / 500 / 650
- Produit + 1 personnage : 550 / 750 / 1000
- Produit + 2 personnages : 750 / 950 / 1200
Résolution : 720p inclus · 1080p +20% · 4K +50%
Options : VFX dès 150 · Storyboard dès 150 · Script dès 200 · Personnage parlant dès 100 · Dialogue 2 personnages / texte complexe dès 200 · Exclusivité personnage sur mesure 300 · Révision 75–150 · Urgence +30–50%
Images (lot de 5 min) : Produit seul 250 · 1 perso+produit 380 · 2–3 perso+produit 600 · Lot de 10 900

## Pour MODIFIER quelque chose (workflow)
1. Dire à Claude quoi changer.
2. Claude met à jour la **grille (PDF)** ET le **simulateur** en gardant les prix synchro.
3. Claude renvoie le **nouveau fichier HTML**.
4. **Reglisser ce fichier sur tiiny.host** → il remplace l'ancien, le lien ne change pas. (C'est cette étape qui rend le changement visible aux clients.)
5. Claude rafraîchit aussi l'artifact dans la galerie (copie perso).

Rappel : l'**artifact** (galerie Cowork) et le **lien tiiny.host** sont deux copies séparées — seul le lien tiiny.host compte pour les clients.

## Rebuild technique du simulateur (pour Claude)
Lire `assets/lou-denim-logo.svg` → base64 → remplacer `__LOGO_SRC__` dans `templates/simulateur-devis.html` → écrire le HTML final `Simulateur_Devis_LouDenim.html`.

## Le catalogue modèles IA (client-facing)
- **Source (Mac de Lou) :** `/Users/loudenim2020/Documents/MODEL CATALOG` — 1 dossier par section (femmes/hommes/ados/enfants/seniors), 1 sous-dossier par modèle, fichiers `*_CS` (fiche 16:9) + `*_CU`/`*_ECU` (portrait).
- **Générateur :** `tools/build_catalog.py` — scanne le dossier, crop les visages par **détection de visage OpenCV** (carré centré sur le visage, biais +5% vers le bas pour privilégier bouche/menton ; fallback 45% si aucun visage détecté), rognage 1% des bords (anti-liseré sombre), compresse (thumb 560px / fiche 1800px / portrait 1000px, JPEG q82), génère `index.html` (marque Studio Blush, logo intégré, lightbox fiche, mailto + lien simulateur).
- **Dépendance :** `pip install opencv-python-headless --break-system-packages` (+ Pillow).
- **Rebuild :** `python3 build_catalog.py "<dossier source>" <dossier sortie>` puis zipper le dossier sortie → glisser le zip sur tiiny.host.
- Limite connue : si un close-up est cadré très serré (visage plus haut que la largeur, ex. Joy/Bernard), le carré ne peut pas contenir front + menton → le bas du visage est priorisé. Solution durable : régénérer le close-up cadré épaules.
- **Ajouter un modèle :** Lou ajoute un dossier dans MODEL CATALOG → reconnecter le dossier → re-stager → rebuild → re-glisser le zip. Le lien ne change pas.
- Poids du site ≈ 13 Mo → dépasse le plan gratuit tiiny.host (≈3 Mo) ; prévoir plan payant tiiny ou autre hébergeur statique.

## À faire quand voulu
- Version **anglaise** du simulateur (même méthode, sous-domaine ex. `loudenim-devis-ia-en`, nouvelle clé Web3Forms ou la même).
- Détail : passer les durées « 15s / 20s / 40s » sans espace dans le simulateur (déjà fait sur la grille).
