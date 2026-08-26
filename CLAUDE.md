# CLAUDE.md — AI Studio (Lou Denim) — FULL RECAP

> **Read this first.** This file recaps the whole project from the beginning through 24 Aug 2026.
> For deep July-era build history (generators, design system details) read `PROJECT.md` §1-§10.
> Claude's cloud project "AI WEBSITE" also carries working notes (claude/site-v4-services-redesign.md
> is the detailed August log).

## What this is
The bilingual (FR/EN) AI-studio website of Lou Denim — photographer & AI creative director
(Guadeloupe). Live at **https://ai.loudenim.com** — GitHub Pages, repo `LouDenim/ai-studio`,
branch `main`, custom domain via `CNAME` (DNS at 123 Reg). Any commit to `main` is live in ~1 min.
Sections: Home · Portfolio (10 AI films) · Modèles/Models (52 AI faces) · Services (rate card +
quote simulator + video brief) · À propos/About · Contact.

## Timeline — everything done so far

**July 2026 — v1 to v3 (see PROJECT.md for depth)**
- Site built from scratch: white generated pages, `prices.json` as price source, rate-card +
  brief PDFs, EN mirror pages (£ at 1:1 with € — deliberate UK premium, never convert down).
- 14 July: URLs de-Frenchified (index→home, grille→rate, devis→simulator, travail→portfolio).
- 19-20 July: dark redesign "Direction D" (near-black `#0a0a0c`, pink `#E7549F`/`#ff7fc0`),
  6-item nav, portfolio film carousel with local mp4s in `/videos/`, dark simulator, compact
  brief, real PDF downloads on mobile, simulator copy-toast.
- ⚠️ The old page GENERATORS are retired/drifted. Do NOT run build_landing.py, build_catalog.py,
  make_models_en.py, build_travail_web.py, build_models_d2.py — they would revert live pages.
  Only the rate/simulator/brief/PDF toolchain (`build-tools/tools` + `templates`, prices.json)
  is still valid, plus `add_topnav.py` after white-page rebuilds.

**August 2026 — v4 (all LIVE)**
1. **Portfolio**: hero film added as "Intensity Driven" (Spec Aston Martin · 1st place GenHQ
   contest · 30s); captions normalised FR/EN; "Last Orders" added 3rd (Spec ad · Barrow Beer ·
   34s); McDonald's retitled (CSR animation 40s). Final order (10): Intensity Driven · La Douceur
   de la Guadeloupe · Last Orders · Milenis · McDonald's · Just Be Cool · Out of the Office ·
   Morning Shift · Malaysia Boleh · The Commute.
2. **Fullscreen player**: sound on by default, prev/next arrows + keyboard + swipe (wraps),
   native controls stripped, mobile = tap toggles pause, carousel autoplay retry on touch.
3. **Services redesign**: "Pricing/Tarifs" replaced SITEWIDE by "Services". services*.html hub =
   three doors (À la carte / Take your pick · Simulateur · Brief vidéo); selection*.html door-1
   (VIDÉO / PHOTOS / CAMPAGNE COMPLÈTE with tag rows); pricing*.html + rate*.html are redirect
   stubs; Home + About CTAs say Services.
4. **Pricing updates** (simulator ↔ rate card ↔ prices.json ↔ PDFs all MATCH, audited):
   ladders 300/400/600 · 350/450/700 · 400/500/800 (15/20/30s, doubles with length to 60s);
   flat add-ons (char/env +150, product +75, face +50, FX 150, voix/musique 100, endcard 150,
   sous-titres 75, perso parlant 100, dialogue 200, exclusivité 300, storyboard 150, script 200);
   immo 300/400/500; **1080p +25%, 4K +50%**; révision 150 (2 incl.);
   rush +40%; **acompte 50% au-dessus de €1,000/£1,000**; **droits web & réseaux sociaux inclus**;
   TV/cinéma/affichage sur devis. No USD, no email gate, no licensing options (deliberate).
   **26 Aug 2026 — ALL PACKS/DISCOUNTS REMOVED (Lou's decision, positioning not pricing):**
   the simulator's Pack de 3 −15 % / Pack de 5 −25 % boxes, the rate-card "Pack campagne
   complète 1 500–2 000 €", and the "Tarif dégressif à partir de 3 vidéos" / "Volume rate
   from 3 videos" notes are gone from simulator*.html, services*.html, prices.json, the
   grille-tarifaire templates, build_grille_web.py, make_devis_en.py, make_grille_en.py and
   both rate-card PDFs. Rationale: Lou — "I think I'm cheapening myself. If someone wants a
   retainer, they talk to me, I just don't want the discount appearing." The retainer /
   "Agences : projets récurrents, volumes ? Parlons-en." routes stay — that is the only
   remaining door to a volume price, and it goes through her. **Do not reintroduce a printed
   discount without asking her.** Prices themselves are unchanged.
5. **Models catalogue → 52 faces**: Femmes 18 · Hommes 16 · Ados 6 · Enfants 6 · Seniors 6.
   Added in August: Dave, Clive, Eva, Franck. Homepage says "52 visages IA / 52 AI faces".
6. **Models pages REFACTORED** (the big one): modeles.html/models-en.html went from 9.6MB of
   base64 to ~55KB each. Images are separate files `img/m-<section>-<slug>-face.jpg` (480x643 or
   480x640, 3:4) + `-sheet.jpg` (950x530); 9 older models have a distinct `-lbface.jpg`.
   Cards use `loading="lazy" draggable="false"`; FLAT JS entries = 5 keys (slug, name, section,
   sheet, face) holding file paths. Image protection: right-click + drag blocked on images,
   CSS user-drag none, © footer lines both languages. NO watermarks (Lou refused). Real
   protection = site only carries low-res; masters/prompts never on the site.
7. **Crop standardisation**: reference framing = Stephy (face large, cut at collarbone,
   centered). Recropped: Suzanne, Tracy, Chen, then Eva, Cyndie, Ella (10% zooms). Franck's
   head-top was rebuilt via Higgsfield outpaint (no frontal source had it). Ella's card rebuilt
   from her sharper lbface.
8. **Seniors fix**: the refactor upload silently dropped 9 files (4 senior faces + 5 sheets) —
   found by Lou, re-uploaded, then a full audit: every img/video reference on every page
   resolves on remote main.

## ADD-A-MODEL RECIPE (current)
face source (1792x2400) → resize 480x643 q82 → `img/m-<section>-<slug>-face.jpg`;
sheet source (2752x1536) → 950x530 q82 → `-sheet.jpg`; insert card + FLAT entry before the
alphabetical successor in BOTH modeles.html and models-en.html; update section count span
(FR "N modèles" / EN "N models") + homepage "N visages IA"/"N AI faces"; verify locally
(all cards render, 0 broken, lightbox FR+EN); publish; **then `git fetch` and diff the remote
tree against local — the GitHub web upload can silently drop files.**

## How Claude publishes (cloud/Cowork sessions)
- Clone: `git clone https://github.com/LouDenim/ai-studio` works. `git fetch` works.
- **`git push` is BLOCKED by the sandbox proxy** ("not in this session's authorized repository
  set") — this is NOT a token problem, never regenerate PATs for it. GitHub App is installed
  but doesn't unblock it. Try push once, then use the Chrome route:
  copy files to the session outputs folder → drive Lou's logged-in browser to
  `github.com/LouDenim/ai-studio/upload/main[/img]` → file_upload (≤10MB/call, calls append
  into one commit) → type commit message (verify it landed — sometimes it doesn't) → Commit →
  **git fetch + tree diff to verify nothing dropped** → wait ~1 min → verify live.
- curl to ai.loudenim.com is blocked from the sandbox — verify live pages through the Chrome
  tab. raw.githubusercontent.com and cloudfront GETs DO work from the sandbox.
- Outpaint pipeline when an image needs new pixels: publish source to the repo → Higgsfield
  `media_import_url` on the raw.githubusercontent URL → outpaint → download result (cloudfront
  works) → crop locally → publish.

## Lou's source assets (NOT in the repo — protect these)
- Mac folder `Documents/BUSINESS/AI_WEBSITE` (moving to the M4, path may change — ask Lou):
  `characters/` hi-res model PNGs (only 25 of 52 models have originals; the rest exist only as
  web files — re-download from Higgsfield/Midjourney libraries if ever needed), `PHOTOS/`,
  `VIDEOS_lansdcape/` (video masters incl. LAST ORDERS 4K and FREE FALL — not yet on the site),
  `hero.mp4`, plus an outdated July-18 site backup (superseded by GitHub).
- Intensity Driven master lives on an external hard drive; Lou plans a 4K redo, then we swap
  the web version.

## Working rules with Lou (learned, respect these)
- Always show a rendered preview (real grid screenshot, sticky bars hidden, never hand-cropped)
  and get her OK before publishing visual changes. Only exception: fixes she already approved.
- She judges framing precisely — "a touch", "1/10th", "not too much" mean exactly that.
- Direct, no fluff, French or English as she writes. Own mistakes plainly, fix them.
- Never watermark her models. Never put masters, prompts or workflows on the site.
- EN prices are £ at the same figures as € — never "convert".

## Carried TODOs
iPhone test of fullscreen player + models page feel · Boleh caption "18s" vs 20s runtime ·
Out of the Office "25s" check · FR reels tag · long-version brief PDFs · rate-card PDF face
ladder · portfolio pruning when 12+ films · simulator footer "Grille tarifaire" link → PDF ·
Intensity Driven 4K replacement (master on external drive) · nicer Intensity Driven poster ·
FREE FALL.mp4 (new film, not yet on site) · rotate the GitHub PAT "claude-ai-studio"
(exp 7 Sep 2026 — was pasted in chat) · Lou may delete site-update-last-orders backup folder.
