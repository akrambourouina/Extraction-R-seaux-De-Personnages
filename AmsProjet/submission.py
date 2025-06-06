import os
import pandas as pd
from extraction_personnage import extraire_personnages
from alias import grouper_noms_par_mots_cles
from occurences import detecter_cooccurrences
from graphes import generer_graphe

# Configuration des livres et chapitres
books = [
    (list(range(1, 20)), "paf", r"C:\Users\akram\Desktop\Extraction-automatique-main\prelude_a_fondation"),
    (list(range(1, 19)), "lca", r"C:\Users\akram\Desktop\Extraction-automatique-main\les_cavernes_d_acier"),
]

# Fichier de l'antidictionnaire
fichier_antidictionnaire = r"antidictionnaire.txt"

# Dictionnaire pour stocker les données pour le CSV
df_dict = {"ID": [], "graphml": []}

# Parcours des livres et des chapitres
for chapters, book_code, folder in books:
    for chapter in chapters:
        chapitre_id = f"{book_code}{chapter - 1}"  # Ajustement : le numéro d'ID commence à 0

        # Chemin vers le fichier de chapitre
        fichier_chapitre = os.path.join(folder, f"chapter_{chapter}.txt.preprocessed")

        if not os.path.isfile(fichier_chapitre):
            print(f"Fichier introuvable : {fichier_chapitre}")
            continue

        try:
            # Extraction des personnages
            personnages = extraire_personnages(fichier_chapitre, fichier_antidictionnaire)

            # Génération des alias
            alias = grouper_noms_par_mots_cles(personnages)

            # Détection des cooccurrences
            cooccurrences = detecter_cooccurrences(fichier_chapitre, fichier_antidictionnaire, 25)

            # Génération du graphe
            graphml = generer_graphe(cooccurrences, alias, chapitre_id)

            # Ajouter au dictionnaire
            df_dict["ID"].append(chapitre_id)
            df_dict["graphml"].append(graphml)

            print(f"Graphe pour {chapitre_id} généré avec succès.")
        except Exception as e:
            print(f"Erreur lors du traitement de {chapitre_id}: {e}")

# Création du DataFrame
df = pd.DataFrame(df_dict)
df.set_index("ID", inplace=True)

# Sauvegarde dans un fichier CSV
output_csv = "graphes_co_occurrences.csv"
df.to_csv(output_csv, encoding="utf-8")

print(f"Fichier CSV généré avec succès : {output_csv}")
