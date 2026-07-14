#!/usr/bin/env python3
"""Deploy the approved Direction D dark redesign + white-form masthead fixes
into the production repo, remapping internal mockup filenames to real
production filenames along the way."""

import re

MOCKUP_DIR = "/root/homepage-mockups/"
PROD_DIR = "/root/catalogue-models/"

# mockup filename -> production filename (order: -en variants first, harmless either way
# since these are distinct full strings, but keeping it explicit/readable)
RENAME_MAP = [
    ("mockup-d20-en.html", "home-en.html"),
    ("mockup-d20.html", "home.html"),
    ("mockup-models-d2-en.html", "models-en.html"),
    ("mockup-models-d2.html", "modeles.html"),
    ("mockup-travail-d2-en.html", "portfolio-en.html"),
    ("mockup-travail-d2.html", "portfolio.html"),
    ("mockup-grille-en-preview.html", "rate-en.html"),
    ("mockup-grille-preview.html", "rate.html"),
    ("mockup-devis-en-preview.html", "simulator-en.html"),
    ("mockup-devis-preview.html", "simulator.html"),
    ("mockup-brief-en-preview.html", "brief-en.html"),
    ("mockup-brief-preview.html", "brief.html"),
]

# Files that need the dark-mode DARK generator output (require href substitution)
DARK_FILES = [
    "mockup-d20.html", "mockup-d20-en.html",
    "mockup-models-d2.html", "mockup-models-d2-en.html",
    "mockup-travail-d2.html", "mockup-travail-d2-en.html",
]

# Files that are near-verbatim copies of production white forms (masthead-only edits)
WHITE_FILES = [
    "mockup-grille-preview.html", "mockup-grille-en-preview.html",
    "mockup-devis-preview.html", "mockup-devis-en-preview.html",
    "mockup-brief-preview.html", "mockup-brief-en-preview.html",
]

def remap(html):
    for src, dst in RENAME_MAP:
        html = html.replace(src, dst)
    return html

report = []

for fname in DARK_FILES:
    with open(MOCKUP_DIR + fname, encoding="utf-8") as f:
        html = f.read()
    before_stray = len(re.findall(r'mockup-[a-z0-9-]+\.html', html))
    html = remap(html)
    after_stray = len(re.findall(r'mockup-[a-z0-9-]+\.html', html))
    dst = dict(RENAME_MAP)[fname]
    with open(PROD_DIR + dst, "w", encoding="utf-8") as f:
        f.write(html)
    report.append((fname, dst, before_stray, after_stray, len(html)))

for fname in WHITE_FILES:
    with open(MOCKUP_DIR + fname, encoding="utf-8") as f:
        html = f.read()
    stray = len(re.findall(r'mockup-[a-z0-9-]+\.html', html))
    dst = dict(RENAME_MAP)[fname]
    with open(PROD_DIR + dst, "w", encoding="utf-8") as f:
        f.write(html)
    report.append((fname, dst, stray, stray, len(html)))

print(f"{'source':35} {'-> dest':22} {'stray-before':13} {'stray-after':12} bytes")
for row in report:
    print(f"{row[0]:35} -> {row[1]:20} {row[2]:13} {row[3]:12} {row[4]}")
