# CLAUDE.md — AI Studio (loudenim)

**Read `PROJECT.md` first — it is the full master reference for this site.** This file is the quick brief.

## What this repo is
The bilingual (FR/EN) AI-studio website for Lou Denim. Live at **https://ai.loudenim.com**
(GitHub Pages, repo `LouDenim/ai-studio`, branch `main`; custom domain via `CNAME` = `ai.loudenim.com`,
DNS at 123 Reg). Push to `main` → live in ~1 min.

## Critical facts before editing
- **Pages are GENERATED, not hand-edited. Two toolchains — do not mix them up:**
  - `index.html`/`index-en.html`, `modeles.html`/`models-en.html`, `travail.html`/`travail-en.html`
    (dark design) ← `build-tools/dark-mode-tools/` (`build_d20.py`, `build_models_d2.py`,
    `build_travail_d2.py`, `deploy_production.py`).
  - `grille.html`/`-en`, `devis.html`/`-en`, `brief.html`/`-en`, and the 4 PDFs (white, unchanged
    design) ← the original toolchain in `/root/.claude/skills/pdf-lou/` (`tools/` + `templates/`),
    mirrored in this repo's `build-tools/tools/` + `build-tools/templates/`. `prices.json` there is
    the single source of all prices.
  - **Do NOT run the old `build_landing.py` / `build_catalog.py` / `make_models_en.py` /
    `build_travail_web.py`** — retired, would silently regenerate the old white homepage/catalogue/
    portfolio over the current dark one.
- Full rebuild commands for both toolchains are in `PROJECT.md §4`.
- **f-string trap:** `build_grille_web.py`, `build_brief_web.py`, and the dark-mode generators use
  Python f-strings — double every literal `{`/`}` in injected CSS/JS. Others use single braces.
- **Keep FR and EN in sync:** the `make_*_en.py` scripts hold FR→EN string maps; change a FR string
  and you must update its EN mapping or the translation silently won't apply.

## Locked design rules (do not break)
- **Homepage / Models / Portfolio:** near-black `#0a0a0c` background, pink `#E7549F`/`#ff7fc0` accents
  (permanent on title pills/section bands, hover-only elsewhere), typewriter bio (homepage only),
  fade-in intro (Models/Portfolio only), 5 footer social icons (no Facebook).
- **Rate card / Simulator / Video brief:** stay **white** — deliberate, these are printable forms.
  "Comet on dot-grid" canvas FX, blush palette, black doc-band pills unchanged.
- **Whole site:** logo 136px tall, no rule line under it, role text pink (`#ff7fc0`-family dark
  pages / `#D63E8D` white pages, not black). Logo click → studio home; studio home logo →
  `loudenim.com`. Font Jost. Lou dislikes the em dash "—" in prose (use commas/colons). Banned
  brand words are listed in `PROJECT.md §6`.

## Approval rule
Lou reviews before publishing. **Do not push without her go-ahead** unless she explicitly says to.
Forms submit to lou@loudenim.com (Web3Forms public key in the code).
