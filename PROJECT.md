# LOU DENIM — AI STUDIO — Project Reference

> **This is the master document for the AI Studio website.**
> If you're coming back to this after months away, read this file first — it tells you
> what the site is, where it lives, how it's built, every locked decision, and how to change it.
> You are **not** starting from scratch.

Last updated: 14 July 2026.

---

## 1. WHAT THIS IS

A bilingual (French / English) client-facing website for Lou Denim's AI creative studio.
It replaces nothing on the main photography site — it is the **AI home**.

- **Live address:** https://ai.loudenim.com
- **Also reachable at:** https://loudenim.github.io/ai-studio/
- **Purpose:** show the AI video/image work, present the model catalogue, give clients
  prices, let them build a quote, and let them fill a project brief — all online, no download needed.

---

## 2. WHERE IT LIVES (hosting, domain, accounts)

- **Code repository (GitHub):** `github.com/LouDenim/ai-studio`, branch `main`.
- **Hosting:** GitHub Pages (free). Every push to `main` goes live in ~1 minute.
- **Language gateway:** the site root `index.html` is NOT a page — it's a tiny browser-language
  detector. It reads `navigator.languages` and `location.replace()`s to `home.html` (FR) only if
  the visitor prefers French, otherwise to `home-en.html` (EN default, since loudenim.com is English).
  Inline head script + black background = no flash, no back-button entry. No-JS falls back to English
  via meta-refresh. Do NOT turn `index.html` back into a plain redirect.
- **Custom domain:** `ai.loudenim.com`
  - The repo contains a file named `CNAME` holding the text `ai.loudenim.com`.
  - **DNS is at 123 Reg** (GoDaddy-group infrastructure). There is a CNAME record:
    `ai` → `loudenim.github.io`.
  - HTTPS is enforced in the repo's **Settings → Pages → Enforce HTTPS** (already ticked).
- **Forms go to email:** all "Send to Lou" buttons deliver to **lou@loudenim.com** via Web3Forms.
  - Public form key (safe to be in code): `fbddfe3a-fa8b-49d4-bbe3-5b329a81dd67`
  - The very first form email may land in spam once — mark "not spam" and it's fine after.
- **Push token:** a GitHub token named `claude-ai-studio` was used to push. Tokens expire
  (this one ~11 Aug 2026). If pushing fails in future with an auth error, a new token is needed.

**Two steps only Lou (a human) can do**, because the sandbox can't: (1) create the GitHub repo,
(2) enable GitHub Pages. Both are already done. Everything else (edits + push) is automatable.

---

## 3. THE PAGES (what each one is)

All pages are bilingual via an FR/EN toggle **except** the ones marked FR-only / EN-only,
which are language-specific files linked from the toggle.

| File | What it is | Language |
|---|---|---|
| `home.html` | Home / landing — dark "Direction D" design (hero, typewriter bio, trusted-by logos, Portfolio/Models boxes, 3 tool cards) | FR |
| `home-en.html` | Home / landing, same design | EN |
| `modeles.html` | Model catalogue — dark design (face grid, category filter pills → click → character sheet) | FR |
| `models-en.html` | Model catalogue | EN |
| `rate.html` | Rate card, online (interactive page + buttons) | FR |
| `rate-en.html` | Rate card, online (£ prices, same numbers) | EN |
| `simulator.html` | Quote simulator (build project, live total, send) | FR (€) |
| `simulator-en.html` | Quote simulator | EN (£, same numbers) |
| `brief.html` | Video brief, fill online + send + print/PDF | FR |
| `brief-en.html` | Video brief | EN |
| `portfolio.html` | "Le travail en images" — video showcase (16:9 + verticals), dark design | FR |
| `portfolio-en.html` | "The work" | EN |
| `Grille_Tarifaire_LouDenim.pdf` | Printable rate card | FR |
| `Rate_Card_LouDenim.pdf` | Printable rate card | EN |
| `Brief_Video_IA_LouDenim.pdf` | Printable/fillable brief | FR |
| `AI_Video_Brief_LouDenim.pdf` | Printable/fillable brief | EN |
| `img/` | 96 model images + `img/logos-color/` (colour client logos) + `img/logos/` (grey versions) | — |

The home page links to: models, portfolio, rate card, simulator, video brief.
The rate card and video brief cards open the **online pages** (not auto-downloads) — each online
page has its own "download PDF" option inside it.

**Filename history:** the homepage was originally one bilingual file with a client-side FR/EN
toggle, then split into `index.html`(FR)/`index-en.html`(EN) for consistency with the two-file
convention, then renamed again the same day (14 July 2026) — along with the rate card, simulator,
and portfolio pages — to plain English words with no leftover French in the URL: `index`→`home`,
`grille`→`rate`, `devis`→`simulator`, `travail`→`portfolio`. Lou wanted every client-facing URL to
read cleanly regardless of language (e.g. `simulator-en.html`, not `devis-en.html`). `modeles.html`/
`models-en.html` and `brief.html`/`brief-en.html` were already fine as-is and were left untouched.
**If you ever see the old names (`index`, `grille`, `devis`, `travail`) referenced anywhere — a
stray script, an old email, a bookmark — they no longer exist; the current names above are current
as of 14 July 2026.**

---

## 4. HOW IT'S BUILT (the generators)

**⚠️ Two toolchains exist — see `build-tools/README.md` for the full warning before rebuilding
anything.** Short version: `home.html`, `home-en.html`, `modeles.html`, `models-en.html`,
`portfolio.html`, `portfolio-en.html` are now built by the **dark-mode generators**
(`build-tools/dark-mode-tools/build_d20.py`, `build_models_d2.py`, `build_travail_d2.py` +
`deploy_production.py` — note the scripts themselves still have their old `_d20`/`d2`/`travail`
internal names; only the *deployed* filenames changed). `rate.html`/`-en`, `simulator.html`/`-en`,
`brief.html`/`-en`, and the 4 PDFs are still built by the **original toolchain** below. Do NOT run
the old `build_landing.py` / `build_catalog.py` / `make_models_en.py` / `build_travail_web.py` —
they'd regenerate the old white design and silently wipe out the dark redesign.

The original toolchain's scripts live **outside the repo**, in the Claude skill folder:
`/root/.claude/skills/pdf-lou/`. `prices.json` in that folder is the **single source of truth for
every price** on the site. A full mirror of both toolchains (including the dark-mode one) is kept
inside this repo at `build-tools/` so nothing is ever lost even if the skill folder disappears.

Generators (`tools/`) still in active use for the white pages (script names are historical, unchanged):
- `build_grille_web.py` — FR online rate card (`rate.html`), reads `prices.json`
- `make_grille_en.py` — FR→EN + € → £ for the rate card (`rate-en.html`)
- `build_brief_web.py` — the online brief, both languages (`brief.html`, `brief-en.html`)
- `make_devis_en.py` — EN simulator (`simulator-en.html`) from the FR template

Retired (historical reference only — do NOT run, see warning above):
`build_landing.py`, `build_catalog.py`, `make_models_en.py`, `build_travail_web.py`.

Templates (`templates/`): `simulateur-devis.html` (FR quote simulator source),
`grille-tarifaire.html` / `-en.html` (rate card PDFs), `brief-video.html` / `-en.html` (brief PDFs),
`lou-denim.css` (PDF stylesheet).

**PDFs** are built with WeasyPrint from the template HTML. The simulator (`simulator.html`) is built
by injecting the logo into `templates/simulateur-devis.html`.

### Rebuild order for the white pages only (rate card / simulator / brief / PDFs)
```
python3 tools/build_grille_web.py <out> "simulator.html" "modeles.html"
python3 tools/make_grille_en.py <out>
# simulator.html: inject logo into templates/simulateur-devis.html
python3 tools/make_devis_en.py <out>
python3 tools/build_brief_web.py <out>
# PDFs:
weasyprint templates/grille-tarifaire.html    <out>/Grille_Tarifaire_LouDenim.pdf
weasyprint templates/grille-tarifaire-en.html <out>/Rate_Card_LouDenim.pdf
weasyprint templates/brief-video.html         <out>/Brief_Video_IA_LouDenim.pdf
weasyprint templates/brief-video-en.html      <out>/AI_Video_Brief_LouDenim.pdf
# then: git add -A && git commit && git push  (goes live in ~1 min)
```

### Rebuild order for the dark pages (homepage / Models / Portfolio)
```
cd build-tools/dark-mode-tools
python3 build_d20.py && python3 build_models_d2.py && python3 build_travail_d2.py
python3 deploy_production.py     # remaps mockup filenames -> home.html/modeles.html/etc. and writes into the repo
# then: git add -A && git commit && git push
```
To add a model: edit `model_assets.json` (or the DATA list in `build_models_d2.py`), rerun the 3
builds + deploy above. To add a video: edit the `IDS_169`/`IDS_916` lists in `build_travail_d2.py`.

**⚠️ f-string trap:** `build_grille_web.py`, `build_brief_web.py`, and the dark-mode generators are
Python f-strings — any literal `{` or `}` in injected CSS/JS must be **doubled** (`{{` `}}`).
`make_*` and the templates are plain strings (single braces).

**⚠️ Self-referential data trap — read this before touching `build_models_d2.py` or
`build_travail_d2.py`:** both scripts originally seeded their own input data by reading the
**already-deployed production HTML** (`modeles.html`/`models-en.html`, `portfolio.html`) instead of
a stable independent source. That is backwards — a generator must never read its own prior output
as if it were raw data, because every rebuild bakes that run's output back into the file the next
run will read.
- `build_models_d2.py` now reads the model `const DATA = [...]` blob from
  `/root/backup_predeploy_snapshot/modeles.html` / `models-en.html` — a frozen pre-redesign
  snapshot — **not** from the live dark-design files, which no longer contain that JS blob at all
  (reading them crashes with `AttributeError: 'NoneType' object has no attribute 'group'`).
  **`/root/backup_predeploy_snapshot/` must never be deleted** — `build_models_d2.py` depends on
  it to run at all. If it's ever lost, the model data will need to be re-sourced from
  `model_assets.json` / the original catalogue export instead.
- `build_travail_d2.py` had the same shape of bug but a different symptom: it read the `data-id`
  list back out of the deployed `portfolio.html` to seed `IDS_916`, then unconditionally appended a
  `NEW_916` list on top. Every rebuild+redeploy cycle re-read IDs it had already written, so the
  same "new" IDs kept getting appended again — 2 videos ended up tripled. Fixed with an
  order-preserving dedupe right after the append: `IDS_916 = list(dict.fromkeys(IDS_916))`. If you
  add more videos to `IDS_169`/`IDS_916` by hand in future, that dedupe line stays as a safety net,
  but the real fix is: **never treat a generator's own deployed output as its data source.**

---

## 5. DESIGN SYSTEM (locked, current as of 14 July 2026 — "Direction D")

**Homepage, Models catalogue, Portfolio — dark:**
- **Background: near-black `#0a0a0c`.** Pink accent `#E7549F` / bright `#ff7fc0`.
- **Pink is not hover-only on these 3 pages.** The page-title pill (`.docband`) and section headers
  (`.band`) are **solid, permanent pink** — explicit request from Lou ("it needs to be the same box,
  bright pink, written in white"). Hover-only pink still applies to nav links, cards, and other
  secondary elements.
- **Hero:** faint static dot texture behind the masthead, no moving comet animation, no glow —
  several animated versions (moving comets, glow halos) were tried and rejected as looking like "a
  nightclub"; plain black + static dots is the locked final call.
- **Intro-line animation differs BY PAGE, deliberately:**
  - **Homepage only:** typewriter — the bio line types itself out on scroll-into-view (steady
    ~30ms/char, no stutter), then "super-pouvoirs IA." flashes brighter pink with light radiating
    out for under a second and settles back to normal. Plays once per page load.
  - **Models & Portfolio:** plain fade-in-and-hold (no typing) — deliberately different from the
    homepage. Soft opacity+lift on scroll-into-view, settles, stays. No glow/flash.
  - **Models page filter pills:** the first category band (Femmes/Women) sits close under the
    filter pills (`section:first-of-type .band{margin-top:18px}`) — tighter than the 46px gap
    between subsequent category bands, which stays wide.
- **Footer icons: 5** — Instagram, LinkedIn, X, YouTube, TikTok (TikTok last). Facebook was tried
  and explicitly dropped by Lou ("not very trendy these days") — do not reintroduce without asking.

**Rate card, Simulator, Video brief — stay white (deliberate):**
- **Background: white**, unchanged — these are printable forms; Lou does not want them on a black
  background ("that's a lot of ink").
- Original comet-on-dot-grid canvas animation, blush palette (`#FBF1EF`/`#F5E3DF`/`#EBC9C3`), and
  black doc-band pills all unchanged from before.

**Whole-site masthead consistency (applies to all 8 pages, dark and white alike):**
- **Logo: 136px tall** (was 86px on the white form pages before 14 July — now matches).
- **No rule line** under the logo on any page (the white form pages had a black `.rule` divider —
  removed for consistency with the dark pages, which never had one).
- **Role text** ("Directeur artistique IA" / "AI Creative Director"): pink `#ff7fc0`-family on dark
  pages, **`#D63E8D`** (a slightly darker pink, chosen so it reads clearly on white) on the white
  form pages — was plain black before.
- **Logo click:** every inner page → the AI Studio home (`home.html` FR / `home-en.html` EN);
  the AI Studio home logo → the main photography site `loudenim.com`.
- **Font:** Jost (Google Fonts), weights 300–600.
- **Client logos (homepage):** right-to-left seamless marquee, colour logos, pauses on hover.
  Track is centred and capped at **`max-width:820px`** (not full page width) — a wide/edge-to-edge
  loop looked off-centre and read as sloppy; narrower reads as a deliberate, contained strip roughly
  the width of the "générative" line above it. Built as a doubled `.seq` list scrolling via
  `@keyframes logoscroll` (translateX 0 → -50%), with an edge mask-image fade.
- **Document title bands:** rounded pill (border-radius 999px web / 4mm PDF).
- **Top nav on the white pages (grille/devis/brief, FR+EN):** these 6 pages never had a nav bar in
  the original design (they were meant to be reached only via a link from the dark pages). Lou asked
  for a full site nav + AI STUDIO brand + FR/EN toggle on all 6, matching the dark pages'. This was
  added by a **separate, standalone script**, `build-tools/dark-mode-tools/add_topnav.py`, which
  patches the already-built HTML directly (checks for `class="topnav"` to avoid double-inserting,
  so re-running it after the nav is present is a safe no-op). **Known gap:** the original white-page
  generators (`build_grille_web.py`, `build_brief_web.py`, `simulateur-devis.html`) do **not**
  include the topnav themselves — if any of the 6 white pages is ever fully regenerated from those
  scripts (e.g. for a price change), the topnav will be missing again until `add_topnav.py` is
  re-run afterwards. Don't forget that step.
- **Nav link underlines:** the dark pages have a global `a{text-decoration:none}` reset; the white
  pages never did, so the newly-added topnav links inherited the browser default underline until
  `.topnav a{text-decoration:none}` was added to `add_topnav.py`'s injected CSS.
- **Simulator masthead alignment:** `simulator.html`/`simulator-en.html`'s `.wrap` had an extra 28px
  of top padding that `rate.html`/`brief.html` didn't, which pushed the logo visibly lower than
  the other two pages. Fixed in `simulator.html`, `simulator-en.html`, and the source template
  `templates/simulateur-devis.html` (`.wrap{padding:28px ...}` → `.wrap{padding:0 ...}`) so a future
  rebuild from the template won't reintroduce the misalignment.

---

## 6. BRAND VOICE — taglines & banned words (locked)

**Home page taglines (current):**
- FR: « Création générative au service des marques : images et campagnes vidéo IA sur mesure. »
- EN: "Gen AI for brands: images and video campaigns ready to run."

**Words Lou does NOT want** anywhere on the site:
- « publicitaire » leading a sentence
- « personnages cohérents » / "consistent characters"
- « produits mis en scène » / "staged products"
- « campagnes livrées finies »
- any mention of "photographer" (this is the AI studio, not the photo site)
- « prêtes à diffuser » (implies pre-made stock)

Preferred vocabulary: Gen AI / génératif, sur mesure. Lou dislikes the em dash "—" in prose —
use commas or colons instead (labels can keep it).

---

## 7. PRICES (source of truth = `prices.json`; € on FR, £ same numbers on EN)

**AI video** (15s / 20s / 30–40s):
- Product only — studio: 350 / 450 / 550
- Product in an environment: 400 / 500 / 650
- Product + 1 character: 550 / 750 / 1000
- Product + 2 characters: 750 / 950 / 1200
- Resolution: 720p included · 1080p +20% · 4K +50%

**AI images** (sets of 5 min): product only 250 · 1 char + product 380 · 2–3 char + product 600 · set of 10 = 900

**Effects / transformations:** from 150 each (morphing, set/season change, relighting, object/colour swap, motion design)
**Sound & finishing:** voice-over from 100 · custom music from 100 · end card 150 · captions/subtitles 75
**Characters:** speaking-to-camera from 100 · 2-character dialogue from 200 · custom-character exclusivity 300
**Other:** storyboard from 150 · script from 200 · extra revision 75–150 · rush +30–50%
**Real estate:** animated tour from 300 · +character 150 · photo enhancement from 25/photo · virtual staging from 75/photo
**Full campaign pack:** 3 videos, same concept (Reel/Story/Feed) = 1 500–2 000

**Terms:** all prices exclude VAT · 2 revisions included · standard delivery 7–10 business days ·
source files/prompts/workflows NOT delivered (Lou's property) · **image rights & licence: to be
defined to suit your needs** · 50% deposit before starting · no work without a validated brief + signed agreement.

### Quote-simulator upsell (Lou loves this — keep it)
Under the live estimate, two boxes appear **once a video is configured**: **Pack of 3 videos −20%**
and **Pack of 10 videos −40%**, showing the discounted per-video price + pack total. Discount applies
to the video subtotal only (not image lots / real-estate). Savings shown in black (pink is hover-only).
Before a video is picked, a small grey hint shows instead of the boxes. (Distinct from the "Full
campaign pack" on the rate card, which is 3 formats of ONE concept.)

---

## 8. HOW TO MAKE COMMON CHANGES

- **Change a price:** edit `prices.json` → rebuild `rate.html` (+ `rate-en.html`), the two rate-card
  PDFs (templates are hand-kept in sync with prices.json), and the simulator constants in
  `templates/simulateur-devis.html` (+ `make_devis_en.py`). Then push.
- **Add a model:** Lou adds a folder inside her `MODEL CATALOG` → face-crop + base64-embed into
  `build-tools/dark-mode-tools/model_assets.json` → add the entry to the `DATA` list in
  `build_models_d2.py` → rerun the dark-mode rebuild (section 4) → push. The public link never changes.
- **Add a video to "the work":** give the YouTube link, say 16:9 or vertical → add the ID to the
  `IDS_169` or `IDS_916` list in `build-tools/dark-mode-tools/build_travail_d2.py` → rerun the
  dark-mode rebuild → push. (Landscape play inline with a fullscreen button; verticals open in a
  large centred lightbox player.)
- **Any text/wording tweak:** edit the relevant generator/template → rebuild that page → push.
- Always keep FR and EN in sync (the `make_*_en.py` scripts hold the FR→EN string maps —
  if you change a FR string, update the matching entry in the EN script or it won't translate).

---

## 9. ROADMAP / IDEAS NOT YET BUILT (Lou's own directions)

- **Two-tier home page (agreed direction, not built):** move the client-logo band UP near the top;
  then **two big, image-led boxes** — The Work (a video still) and The Models (a small face grid) —
  then a lighter row of **three text cards** below: Rate card, Simulator, Video brief. Keep the rate
  card (agencies may want to print a flat price list without building a quote). Goal: less busy, "go big"
  like creative/ad-agency sites — the big boxes should be *images with a label over them*, not text cards.
- **Work page, when it grows:** it's fine stacked (16:9 section, then verticals) up to ~10–12 landscape
  videos. Past that, add a small filter pill row at the top — "Tout · 16:9 · Vertical" — instead of columns
  (columns don't work: the mismatched aspect ratios make ugly rows). Most client demand is expected to be vertical.
- **Pending content:** a cartoon/animation video to add to the work page.

---

## 10. LOU'S SUGGESTED "Website" FOLDER (on her Mac)

Make one folder called **Website** and keep the source assets there so nothing gets hunted for later:
- `MODEL CATALOG/` — the model images (one subfolder per model; `*_CS` = 16:9 sheet, `*_CU`/`*_ECU` = portrait)
- `LOGOS BRAND/` — the client logos (colour) used in the marquee
- `LD Logos/` — Lou Denim's own logo files
- this `PROJECT.md` — the master reference
- drop any new bits (new logos, new model folders, notes) in here as they come.

---

*Everything above reflects the site as pushed on 14 July 2026. A companion, more technical
maintenance log lives with the build scripts as `SETUP-DEVIS-IA.md` (in the skill folder).*
