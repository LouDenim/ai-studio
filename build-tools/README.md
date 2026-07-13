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
