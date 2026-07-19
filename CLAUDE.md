# CLAUDE.md — AI Studio (loudenim)

**Read `PROJECT.md` first — it is the full master reference for this site.** This file is the quick brief.

## What this repo is
The bilingual (FR/EN) AI-studio website for Lou Denim. Live at **https://ai.loudenim.com**
(GitHub Pages, repo `LouDenim/ai-studio`, branch `main`; custom domain via `CNAME` = `ai.loudenim.com`,
DNS at 123 Reg). Push to `main` → live in ~1 min.


## ⚠️ 19 July 2026 redesign — generator drift
Nav is now 6 items everywhere (Home · Portfolio · Models · **Pricing** · **About** · **Contact**).
`pricing/contact/about(.html/-en.html)` are NEW hand-built static pages (no generator builds them).
Homepage lost its tool cards + inline About and gained the "How it works" section. Models tagline
changed. **The dark-mode generators have NOT been updated for any of this — running the dark rebuild
would silently revert the 19 July redesign.** See `PROJECT.md §0` and `§0bis` (20 July: pricing hub kept w/ PDF card, dark simulator, portfolio video carousel with local mp4s in /videos/, compact dark brief) before rebuilding anything. The white-page toolchain no longer matches the live simulator/brief either — full regeneration would revert them.
`add_topnav.py` IS updated (new nav + aligned geometry) — re-run it after regenerating white pages.

## Critical facts before editing
- **Pages are GENERATED, not hand-edited. Two toolchains — do not mix them up:**
  - `home.html`/`home-en.html`, `modeles.html`/`models-en.html`, `portfolio.html`/`portfolio-en.html`
    (dark design) ← `build-tools/dark-mode-tools/` (`build_d20.py`, `build_models_d2.py`,
    `build_travail_d2.py`, `deploy_production.py` — script names are historical, unchanged).
  - `rate.html`/`-en`, `simulator.html`/`-en`, `brief.html`/`-en`, and the 4 PDFs (white, unchanged
    design) ← the original toolchain in `/root/.claude/skills/pdf-lou/` (`tools/` + `templates/`),
    mirrored in this repo's `build-tools/tools/` + `build-tools/templates/`. `prices.json` there is
    the single source of all prices.
  - **Do NOT run the old `build_landing.py` / `build_catalog.py` / `make_models_en.py` /
    `build_travail_web.py`** — retired, would silently regenerate the old white homepage/catalogue/
    portfolio over the current dark one.
- **Filenames were renamed 14 July 2026** to drop leftover French from client-facing URLs:
  `index`→`home`, `grille`→`rate`, `devis`→`simulator`, `travail`→`portfolio`. `modeles`/`models-en`
  and `brief`/`brief-en` were already fine and untouched. If you see the old names anywhere they're
  stale — see `PROJECT.md §3` for the full history and reasoning.
- Full rebuild commands for both toolchains are in `PROJECT.md §4`.
- **f-string trap:** `build_grille_web.py`, `build_brief_web.py`, and the dark-mode generators use
  Python f-strings — double every literal `{`/`}` in injected CSS/JS. Others use single braces.
- **Keep FR and EN in sync:** the `make_*_en.py` scripts hold FR→EN string maps; change a FR string
  and you must update its EN mapping or the translation silently won't apply.
- **Never let a generator read its own deployed output as its data source.** `build_models_d2.py`
  and `build_travail_d2.py` both had this bug (see `PROJECT.md §4` for the full story): reading back
  already-deployed HTML to seed a data list, then appending more on every rebuild, snowballs
  duplicates or crashes outright. `build_models_d2.py` now depends on
  `/root/backup_predeploy_snapshot/` for its model data — **never delete that folder.**
- **White pages (grille/devis/brief) have a topnav added by a separate script**,
  `build-tools/dark-mode-tools/add_topnav.py`, run directly on the built HTML — it is NOT part of
  `build_grille_web.py`/`build_brief_web.py`/`simulateur-devis.html`. If those pages are ever
  regenerated from scratch, re-run `add_topnav.py` afterwards or the nav will be missing again.

- **Pricing model (July 2026):** video = 3 base formats under "Que montre votre vidéo ? / What does
  your video show?" — product only 300→1200, +1 character 350→1400, UGC (speech + 1 location
  included) 400→1600 across 15/20/30/40/50/60s (price doubles with length). Flat add-ons: extra
  character 150, environment 150, extra product 75. Online rate card shows 15/20/30s only; the
  simulator (slider + steppers + reset + sticky estimate + mobile total bar) covers all durations.
  `prices.json` holds the format ladders; the simulator constants live in
  `templates/simulateur-devis.html` (BASE_A/B/C) — change BOTH when prices move, and mirror any FR
  wording change into `make_devis_en.py`'s pair map.

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
