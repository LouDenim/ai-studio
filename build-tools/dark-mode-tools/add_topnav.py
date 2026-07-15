#!/usr/bin/env python3
"""Add a top nav bar (site nav + AI STUDIO brand + FR/EN toggle) to the white
form pages (grille/devis/brief, FR+EN), matching the dark pages' nav, so users
can navigate away from a form page without going back to the browser."""

CSS = """
.topnav{position:sticky;top:0;z-index:30;background:#fff;border-bottom:1px solid #eee}
.topnav a{text-decoration:none}
.topnav .hbar{max-width:1180px;margin:0 auto;padding:22px 28px;display:flex;justify-content:space-between;
  align-items:center;flex-wrap:wrap;gap:10px}
.topnav nav{display:flex;gap:22px;align-items:center;flex-wrap:wrap}
.topnav nav a{font-size:14px;letter-spacing:.06em;color:#333}
.topnav nav a:hover,.topnav nav a.on{color:#E7549F}
.topnav .brand{display:flex;align-items:center;gap:14px}
.topnav .brand span{font-size:13px;letter-spacing:.14em;font-weight:700;color:#E7549F}
.topnav .langs{display:flex;gap:6px}
.topnav .langs a{font-size:11px;letter-spacing:.1em;border:1px solid #E7549F;color:#E7549F;padding:5px 11px;border-radius:999px}
.topnav .langs a.on{background:#E7549F;color:#fff;border-color:#E7549F}
.topnav .burger{display:none}
@media (max-width:760px), (max-height:500px) and (orientation:landscape){
  .topnav .hbar{position:relative;padding:16px 20px}
  .topnav .burger{display:flex;flex-direction:column;justify-content:center;gap:5px;width:30px;height:26px;cursor:pointer;order:-1;z-index:40}
  .topnav .burger span{display:block;width:26px;height:2px;background:#333;border-radius:2px;transition:transform .25s,opacity .2s}
  .topnav .navtoggle:checked ~ .burger span:nth-child(1){transform:translateY(7px) rotate(45deg)}
  .topnav .navtoggle:checked ~ .burger span:nth-child(2){opacity:0}
  .topnav .navtoggle:checked ~ .burger span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
  .topnav nav{position:absolute;top:100%;left:0;right:0;flex-direction:column;align-items:stretch;gap:0;background:#fff;border-bottom:1px solid #eee;padding:6px 0;display:none;box-shadow:0 18px 40px rgba(0,0,0,.12)}
  .topnav .navtoggle:checked ~ nav{display:flex}
  .topnav nav a{padding:14px 20px;font-size:15px;border-bottom:1px solid #f0f0f0}
  .topnav nav a:last-child{border-bottom:0}
  .topnav .brand{margin-left:auto}
}
"""

PAGES = {
    "rate.html":   dict(home="home.html", portfolio="portfolio.html", models="modeles.html",
                           grille="rate.html", devis="simulator.html", brief="brief.html",
                           self="grille", lang_self="rate.html", lang_other="rate-en.html",
                           nav_home="Accueil", nav_portfolio="Portfolio", nav_models="Modèles",
                           nav_grille="Grille tarifaire", nav_devis="Simulateur", nav_brief="Brief vidéo"),
    "rate-en.html": dict(home="home-en.html", portfolio="portfolio-en.html", models="models-en.html",
                            grille="rate-en.html", devis="simulator-en.html", brief="brief-en.html",
                            self="grille", lang_self="rate-en.html", lang_other="rate.html",
                            nav_home="Home", nav_portfolio="Portfolio", nav_models="Models",
                            nav_grille="Rate card", nav_devis="Simulator", nav_brief="Video brief"),
    "simulator.html":    dict(home="home.html", portfolio="portfolio.html", models="modeles.html",
                           grille="rate.html", devis="simulator.html", brief="brief.html",
                           self="devis", lang_self="simulator.html", lang_other="simulator-en.html",
                           nav_home="Accueil", nav_portfolio="Portfolio", nav_models="Modèles",
                           nav_grille="Grille tarifaire", nav_devis="Simulateur", nav_brief="Brief vidéo"),
    "simulator-en.html": dict(home="home-en.html", portfolio="portfolio-en.html", models="models-en.html",
                           grille="rate-en.html", devis="simulator-en.html", brief="brief-en.html",
                           self="devis", lang_self="simulator-en.html", lang_other="simulator.html",
                           nav_home="Home", nav_portfolio="Portfolio", nav_models="Models",
                           nav_grille="Rate card", nav_devis="Simulator", nav_brief="Video brief"),
    "brief.html":    dict(home="home.html", portfolio="portfolio.html", models="modeles.html",
                           grille="rate.html", devis="simulator.html", brief="brief.html",
                           self="brief", lang_self="brief.html", lang_other="brief-en.html",
                           nav_home="Accueil", nav_portfolio="Portfolio", nav_models="Modèles",
                           nav_grille="Grille tarifaire", nav_devis="Simulateur", nav_brief="Brief vidéo"),
    "brief-en.html": dict(home="home-en.html", portfolio="portfolio-en.html", models="models-en.html",
                           grille="rate-en.html", devis="simulator-en.html", brief="brief-en.html",
                           self="brief", lang_self="brief-en.html", lang_other="brief.html",
                           nav_home="Home", nav_portfolio="Portfolio", nav_models="Models",
                           nav_grille="Rate card", nav_devis="Simulator", nav_brief="Video brief"),
}

def on(cur, key):
    return ' class="on"' if cur == key else ''

def nav_html(p):
    s = p["self"]
    fr = (p["nav_home"] == "Accueil")
    lang_fr_href, lang_en_href = (p["lang_self"], p["lang_other"]) if fr else (p["lang_other"], p["lang_self"])
    return f"""<div class="topnav"><div class="hbar">
  <input type="checkbox" id="navtoggle" class="navtoggle" hidden>
  <label for="navtoggle" class="burger" aria-label="Menu"><span></span><span></span><span></span></label>
  <nav>
    <a{on(s,'home')} href="{p['home']}">{p['nav_home']}</a>
    <a{on(s,'portfolio')} href="{p['portfolio']}">{p['nav_portfolio']}</a>
    <a{on(s,'models')} href="{p['models']}">{p['nav_models']}</a>
    <a{on(s,'grille')} href="{p['grille']}">{p['nav_grille']}</a>
    <a{on(s,'devis')} href="{p['devis']}">{p['nav_devis']}</a>
    <a{on(s,'brief')} href="{p['brief']}">{p['nav_brief']}</a>
  </nav>
  <div class="brand"><span>AI STUDIO</span>
    <div class="langs"><a class="{'' if fr else 'on'}" href="{lang_en_href}">EN</a><a class="{'on' if fr else ''}" href="{lang_fr_href}">FR</a></div>
  </div>
</div></div>
"""

DIR = "/root/catalogue-models/"

for fname, p in PAGES.items():
    path = DIR + fname
    with open(path, encoding="utf-8") as f:
        html = f.read()
    if 'class="topnav"' in html:
        print(f"{fname}: topnav already present, skipping")
        continue
    html = html.replace("</style>", CSS + "</style>", 1)
    html = html.replace("<body>\n<canvas", "<body>\n" + nav_html(p) + "<canvas", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"{fname}: nav added")
