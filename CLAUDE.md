# CLAUDE.md — AI Studio (loudenim)

**Read `PROJECT.md` first — it is the full master reference for this site.** This file is the quick brief.

## What this repo is
The bilingual (FR/EN) AI-studio website for Lou Denim. Live at **https://ai.loudenim.com**
(GitHub Pages, repo `LouDenim/ai-studio`, branch `main`; custom domain via `CNAME` = `ai.loudenim.com`,
DNS at 123 Reg). Push to `main` → live in ~1 min.

## Critical facts before editing
- **Pages are GENERATED, not hand-edited.** The generator scripts + `prices.json` (single source of
  all prices) live OUTSIDE this repo, in the Claude skill folder `/root/.claude/skills/pdf-lou/`
  (`tools/` = generators, `templates/` = PDF/simulator sources). Edit those, then rebuild, then push.
- **Rebuild order matters** — `build_landing.py` runs LAST (some scripts write `index.html`). Full
  order + commands are in `PROJECT.md §4`.
- **f-string trap:** `build_landing.py`, `build_grille_web.py`, `build_brief_web.py` use Python
  f-strings — double every literal `{`/`}` in injected CSS/JS. Others use single braces.
- **Keep FR and EN in sync:** the `make_*_en.py` scripts hold FR→EN string maps; change a FR string
  and you must update its EN mapping or the translation silently won't apply.

## Locked design rules (do not break)
- White background; "comet on dot-grid" canvas FX on every page.
- Accent pink `#E7549F` is **hover-only** (except FR/EN pills). Form fields hover **blue**, never pink.
- Font Jost; logo 86px; colour client-logo marquee; footers carry email/phone + 5 social icons.
- Lou dislikes the em dash "—" in prose (use commas/colons). Banned brand words are listed in `PROJECT.md §6`.

## Approval rule
Lou reviews before publishing. **Do not push without her go-ahead** unless she explicitly says to.
Forms submit to lou@loudenim.com (Web3Forms public key in the code).
