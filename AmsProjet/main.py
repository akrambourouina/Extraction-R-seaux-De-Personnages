from lieux import lieux_detectes_global
from extraction_personnage import extraire_personnages
from alias import *
from occurences import detecter_cooccurrences
from graphes import generer_graphe, visualiser_graphe
# Chemin vers le fichier texte
fichier =r"C:\Users\akram\Desktop\Extraction-automatique-main\prelude_a_fondation\chapter_1.txt.preprocessed"
fichier_antidictionnaire = r"antidictionnaire.txt"
chapitre_id = "paf1"  
personnages = extraire_personnages(fichier, fichier_antidictionnaire)
alias = grouper_noms_par_mots_cles(personnages)
occurrences = detecter_cooccurrences(fichier, fichier_antidictionnaire,25)
graphml = generer_graphe(occurrences, alias, chapitre_id)

print(personnages)
print(alias)
print(occurrences)

output_file = f"{chapitre_id}_graphe.graphml"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(graphml)

print(f"Graphe exporté avec succès dans le fichier : {output_file}")
with open(output_file, "r", encoding="utf-8") as f:
     graphml_content = f.read()
visualiser_graphe(graphml_content)