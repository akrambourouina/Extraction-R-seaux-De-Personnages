import os
from extraction_personnage import extraire_personnages  # Assurez-vous que ce fichier contient extraire_personnages.

def detecter_cooccurrences(fichier_entree, fichier_antidictionnaire, distance_max=25):
    """
    Détecte les cooccurrences entre les personnages dans un fichier texte.

    Args:
        fichier_entree (str): Chemin du fichier contenant le texte.
        fichier_antidictionnaire (str): Chemin du fichier antidictionnaire.
        distance_max (int): Distance maximale en tokens pour considérer une cooccurrence.

    Returns:
        list: Liste de tuples représentant les cooccurrences (personnage1, personnage2).
    """
    if not os.path.isfile(fichier_entree):
        raise FileNotFoundError(f"Le fichier spécifié n'existe pas : {fichier_entree}")

    # Extraire les personnages détectés
    personnages = extraire_personnages(fichier_entree, fichier_antidictionnaire)

    # Lire le fichier pour le traitement des tokens
    with open(fichier_entree, 'r', encoding='utf-8') as f:
        texte = f.read()

    # Tokenisation des mots du texte
    tokens = texte.split()
    cooccurrences = []

    # Parcourir tous les personnages pour détecter les cooccurrences
    for i, personnage1 in enumerate(personnages):
        for j, personnage2 in enumerate(personnages):
            if i < j:  # Éviter les doublons et auto-cooccurrences
                indices_personnage1 = [k for k, token in enumerate(tokens) if personnage1 in token]
                indices_personnage2 = [k for k, token in enumerate(tokens) if personnage2 in token]

                # Vérifier si les indices des personnages respectent la distance
                for index1 in indices_personnage1:
                    for index2 in indices_personnage2:
                        if abs(index1 - index2) <= distance_max:
                            cooccurrences.append((personnage1, personnage2))
                            break  # Une seule occurrence suffit pour ce couple

    return cooccurrences
