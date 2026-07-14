# build-tools — the machinery that generates the AI Studio site

This folder is the **complete toolkit** that builds the pages of ai.loudenim.com.
It's kept here so nothing is ever lost. The finished website (the `.html` and `.pdf` files
in the repo root) is generated *from* these files. See `/PROJECT.md` for the full project reference.

## What's inside
- `tools/` — the 8 Python generators (one per page-type). They read `prices.json` and
  `assets/`, and write the finished pages.
- `templates/` — source HTML for the PDFs and the quote simulator, plus `lou-denim.css` (PDF styles).
- `assets/` — the Lou Denim logo (svg used by the generators; png/pdf kept as backups).
- `prices.json` — **single source of truth for every price on the site.**
- `SETUP-DEVIS-IA.md` — the detailed maintenance log (design rules, locked decisions, history).
- `dark-mode-tools/` — the **separate toolchain** that builds the current dark "Direction D" design
  for `index.html`, `index-en.html`, `modeles.html`, `models-en.html`, `travail.html`, `travail-en.html`.
  See the warning below — this is important.

## ⚠️ TWO TOOLCHAINS NOW EXIST — READ BEFORE REBUILDING ANYTHING

As of 14 July 2026 the site runs two different generator systems for different pages:

1. **`dark-mode-tools/`** (`build_d20.py`, `build_models_d2.py`, `build_travail_d2.py`,
   `deploy_production.py`) builds the **dark homepage, Models catalogue, and Portfolio** pages
   (`index.html`, `index-en.html`, `modeles.html`, `models-en.html`, `travail.html`, `travail-en.html`).
   These generators need `assets.json` (site chrome/logos, base64) and `model_assets.json`
   (96 model photos, base64) — both included in this folder.
2. **`tools/` + `templates/`** (the original toolkit, unchanged in purpose) still builds the
   **white rate card, quote simulator, and video brief** (`grille.html`/`-en`, `devis.html`/`-en`,
   `brief.html`/`-en`) plus all 4 PDFs. These stayed white deliberately (Lou: form pages that get
   printed shouldn't burn ink on a black background).

**DO NOT run `build_landing.py`, `build_catalog.py`, `make_models_en.py`, or `build_travail_web.py`
from `tools/` anymore** — those built the *old white* homepage/catalogue/portfolio and would silently
overwrite the current dark design if run again. They're kept only for historical reference.

**Masthead consistency (locked, 14 July 2026):** logo 136px tall (was 86px), no black rule line under
the logo, role text (`Directeur artistique IA` / `AI Creative Director`) in `#D63E8D` (was black/ink).
This applies to every page, dark and white alike. The fix lives in `dark-mode-tools/build_d20.py`,
`build_models_d2.py`, `build_travail_d2.py` (dark pages) AND has been back-ported into
`tools/build_grille_web.py`, `tools/build_brief_web.py`, `templates/simulateur-devis.html` (white
pages) so a future price-driven rebuild of the rate card/brief/simulator won't regress it.

## How to restore / use it (for a future Claude session)
The generators expect to live at `/root/.claude/skills/pdf-lou/` (a Claude skill folder) and use
that absolute path internally (`SKILL = "/root/.claude/skills/pdf-lou"`). To rebuild the site,
copy this folder's contents back into that skill folder (or update the `SKILL` path at the top of
each script), then run the generators in the order below, pointing them at the repo checkout.

## Rebuild order (matters — build_landing.py runs LAST)
```
python3 tools/build_catalog.py "<MODEL CATALOG source folder>" <repo>   # writes index.html -> rename to modeles.html
python3 tools/make_models_en.py <repo>
python3 tools/build_grille_web.py <repo> "devis.html" "modeles.html"
python3 tools/make_grille_en.py <repo>
# devis.html: inject the logo (base64) into templates/simulateur-devis.html -> write devis.html
python3 tools/make_devis_en.py <repo>
python3 tools/build_brief_web.py <repo>
python3 tools/build_travail_web.py <repo>
python3 tools/build_landing.py <repo>          # LAST
# PDFs (WeasyPrint), run from templates/:
weasyprint templates/grille-tarifaire.html    <repo>/Grille_Tarifaire_LouDenim.pdf
weasyprint templates/grille-tarifaire-en.html <repo>/Rate_Card_LouDenim.pdf
weasyprint templates/brief-video.html         <repo>/Brief_Video_IA_LouDenim.pdf
weasyprint templates/brief-video-en.html      <repo>/AI_Video_Brief_LouDenim.pdf
```

## Notes / traps
- `build_landing.py`, `build_grille_web.py`, `build_brief_web.py` are Python **f-strings** —
  any literal `{`/`}` in injected CSS/JS must be doubled `{{ }}`. The others use single braces.
- Keep FR and EN in sync: `make_*_en.py` hold the FR→EN string maps. Change a FR string and you must
  update its EN mapping or the translation silently won't apply.
- To rebuild the **model catalogue**, the original `MODEL CATALOG` image folder is required
  (kept on Lou's computer) — `build_catalog.py` face-crops from those originals. The repo's
  `img/` folder holds only the finished web crops, not the sources.
- Dependencies: `weasyprint`, `opencv-python-headless`, `Pillow`, `numpy`.
