# build-tools — source des grilles tarifaires PDF

Ce dossier contient **la source** des deux PDF publiés à la racine du dépôt :

| PDF (racine du dépôt)          | Langue | Généré depuis      |
|--------------------------------|--------|--------------------|
| `Grille_Tarifaire_LouDenim.pdf`| FR     | `build_grille.py`  |
| `Rate_Card_LouDenim.pdf`       | EN     | `build_grille.py`  |

## Pourquoi ce dossier existe

Le 1er septembre 2026, le commit `e1c377d` a régénéré les deux PDF **et** supprimé
`build-tools/` dans le même commit. Les gabarits modifiés n'ont donc jamais été
enregistrés : les PDF étaient en ligne sans leur source, impossible à mettre à jour.

Le 9 septembre 2026, la source a été reconstruite à partir des PDF en ligne
(texte, géométrie, couleurs et polices relevés au point près) puis vérifiée
page par page contre les originaux. **Ne pas supprimer ce dossier.**

## Régénérer les PDF

```bash
cd build-tools
pip install weasyprint
python3 build_grille.py
```

Le script écrit :

- `grille-tarifaire.html` et `grille-tarifaire-en.html` (gabarits intermédiaires, à commiter aussi)
- `rebuilt-Grille_Tarifaire_LouDenim.pdf` et `rebuilt-Rate_Card_LouDenim.pdf`

Renommer les deux PDF sans le préfixe `rebuilt-` et les copier à la racine du dépôt.

## Où sont les prix

**Tous** les prix des deux langues sont dans la fonction `data()` en haut de
`build_grille.py`, une seule fois — FR et EN sortent de la même structure, donc
les deux grilles ne peuvent pas diverger.

⚠️ Les prix EN sont en **£ aux mêmes chiffres** que les € (premium UK volontaire).
Ne jamais convertir.

### Les prix apparaissent à 4 endroits — les changer ensemble

1. `simulator.html` (FR)
2. `simulator-en.html` (EN)
3. `build-tools/build_grille.py` → puis régénérer les 2 PDF
4. `modeles.html` / `models-en.html` pour l'exclusivité et le sur-mesure

## Polices

`fonts/` contient les polices réellement embarquées dans les PDF :

- **Jost** Light 300 / Regular 400 / Medium 500 (woff2, SIL OFL)
- **JetBrains Mono** Regular 400 / Medium 500 (ttf, SIL OFL)

Elles sont dans le dépôt volontairement : sans elles le rendu change
(interlettrage, largeurs de colonnes, sauts de page).

## Historique des modifications de contenu

- **9 sept. 2026** — « Visage sur mesure » → **« Visage hors catalogue »**
  (EN : « Custom face » → « Face outside the catalogue »), 50 € inchangé.
- **9 sept. 2026** — « Exclusivité personnage — réservé à votre marque » **300 €**
  → **« Exclusivité du mannequin — réservé à votre marque, 12 mois » 500 €**
  (EN : « Model exclusivity — reserved to your brand, 12 months » £500).
