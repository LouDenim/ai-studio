#!/usr/bin/env python3
"""Transpose modeles.html (FR) -> models-en.html (EN). Usage: make_models_en.py <dir>"""
import sys
d = sys.argv[1] if len(sys.argv) > 1 else "/root/catalogue-models"
h = open(f"{d}/modeles.html").read()
rep = [
 ('<html lang="fr">','<html lang="en">'),
 ('LOU DENIM — Catalogue Modèles IA','LOU DENIM — AI Model Catalogue'),
 ('Catalogue Modèles IA','AI Model Catalogue'),
 ('Directeur artistique IA','AI Creative Director'),
 ("Des modèles générés en IA, disponibles pour vos campagnes.\n  Chaque modèle a son identité préservée d'une image à l'autre et peut être mis en scène avec votre produit.\n  Cliquez sur un visage pour voir sa fiche complète.",
  "AI generated characters, available for your campaigns.\n  Every character stays consistent from one image to the next and can be staged with your product.\n  Click a face to see their full sheet."),
 ('"Femmes"','"Women"'), ('"Hommes"','"Men"'), ('"Ados"','"Teens"'), ('"Enfants"','"Kids"'), ('"Seniors"','"Seniors"'),
 ('>Femmes<','>Women<'), ('>Hommes<','>Men<'),
 ("modèle${sec.models.length>1?'s':''}", "model${sec.models.length>1?'s':''}"),
 ('Fermer ✕','Close ✕'), ('← Précédent','← Previous'), ('Suivant →','Next →'),
 ('Demander ce modèle','Request this model'),
 ('Ce modèle vous plaît&nbsp;? Dites-moi pour quel projet — je vous réponds avec un devis.',
  'Like this model? Tell me about your project — I will come back with a quote.'),
 ('Demande modèle — Catalogue IA','Model request — AI Catalogue'),
 ("'Demande modèle — '","'Model request — '"),
 ('Un modèle vous intéresse&nbsp;?','Interested in a model?'),
 ('Estimez votre projet&nbsp;:','Estimate your project:'),
 ('simulateur de devis en ligne','online quote simulator'),
 ('© Lou Denim — modèles générés par IA, tous droits réservés','© Lou Denim — AI-generated models, all rights reserved'),
 (' — fiche"',' — sheet"'),
]
rep.append(('href="devis.html"','href="devis-en.html"'))
for a,b in rep: h = h.replace(a,b)
open(f"{d}/models-en.html","w").write(h)
print("models-en.html ok")
