import os
import unicodedata
import re


def nettoyer_textes(fichier_entree, fichier_sortie):
    """
    Nettoie un fichier texte en supprimant les caractères spéciaux.
    
    Args:
        fichier_entree (str): Chemin du fichier d'entrée.
        fichier_sortie (str): Chemin du fichier de sortie nettoyé.
    """
    if not os.path.isfile(fichier_entree):
        raise FileNotFoundError(f"Le fichier spécifié n'existe pas : {fichier_entree}")

    with open(fichier_entree, "r", encoding="utf-8") as f:
        texte = f.read()

    # Normalisation et nettoyage
    texte = unicodedata.normalize('NFC', texte)
    texte_nettoye = re.sub(r'[^a-zA-Z0-9\s.,;:!?\'"éèàêâùôîûçÉÈÀÊÂÙÔÎÛÇ-]', '', texte)

    # Sauvegarde du texte nettoyé
    with open(fichier_sortie, "w", encoding="utf-8") as f:
        f.write(texte_nettoye)

    print(f"✔ Nettoyage terminé : {fichier_entree} → {fichier_sortie}")
            



            
def nettoyer_entites_fichier(fichier_entree, fichier_sortie):
    # Définir les étiquettes à ignorer
    etiquettes_a_ignorer = ['VERB', 'PUNCT', 'AUX', 'SCONJ', 'X']  # 'PROPN' n'est pas ignoré pour conserver des noms propres
    entites_personnages = set()  # Utilisation d'un set pour éviter les doublons

    # Vérifier si le fichier d'entrée existe
    if not os.path.isfile(fichier_entree):
        raise FileNotFoundError(f"Le fichier spécifié n'existe pas : {fichier_entree}")

    # Lire les lignes du fichier
    with open(fichier_entree, 'r', encoding='utf-8') as f:
        lignes = f.readlines()

    for ligne in lignes:
        # Ignorer les lignes vides
        if ligne.strip():
            # Découper la ligne avec tabulation comme séparateur
            elements = ligne.strip().split('\t')

            # Vérifier qu'il y a bien deux éléments (mot + étiquette)
            if len(elements) == 2:
                mot, etiquette = elements
                # Vérifier que l'étiquette n'est pas dans la liste à ignorer
                if etiquette not in etiquettes_a_ignorer:
                    # Nettoyer le mot en supprimant les préfixes indésirables comme "NOUN ", "PUNCT ", etc.
                    if ' ' in mot:
                        mot = mot.split(' ')[-1]  # Ne garder que la dernière partie après le dernier espace
                    entites_personnages.add(mot)

    # Sauvegarder les résultats nettoyés dans le fichier de sortie
    os.makedirs(os.path.dirname(fichier_sortie), exist_ok=True)  # Crée le dossier si nécessaire
    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        for entite in sorted(entites_personnages):  # Optionnel : trier les entités par ordre alphabétique
            f.write(entite + '\n')

