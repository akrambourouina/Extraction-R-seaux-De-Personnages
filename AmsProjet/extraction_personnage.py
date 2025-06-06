import os
import stanza
from flair.data import Sentence
from flair.models import SequenceTagger

# Initialisation des modèles Stanza et Flair
nlp = stanza.Pipeline('fr', processors='tokenize,ner')
tagger = SequenceTagger.load("flair/ner-french")

def charger_antidictionnaire(fichier_antidictionnaire):
    """
    Charge le fichier antidictionnaire et retourne un ensemble des mots ou expressions.

    Args:
        fichier_antidictionnaire (str): Chemin du fichier antidictionnaire.

    Returns:
        set: Ensemble des mots ou expressions à exclure.
    """
    if not os.path.isfile(fichier_antidictionnaire):
        raise FileNotFoundError(f"Le fichier spécifié n'existe pas : {fichier_antidictionnaire}")

    with open(fichier_antidictionnaire, 'r', encoding='utf-8') as f:
        return set(line.strip().lower() for line in f if line.strip())

def extraire_personnages(fichier_entree, fichier_antidictionnaire):
    """
    Extrait les personnages d'un fichier texte en utilisant Stanza pour le NER,
    exclut les lieux en utilisant Flair, et exclut les mots du fichier antidictionnaire.

    Args:
        fichier_entree (str): Chemin du fichier d'entrée contenant le texte.
        fichier_antidictionnaire (str): Chemin du fichier antidictionnaire.

    Returns:
        list: Liste des personnages détectés.
    """
    if not os.path.isfile(fichier_entree):
        raise FileNotFoundError(f"Le fichier spécifié n'existe pas : {fichier_entree}")

    # Charger l'antidictionnaire
    mots_antidictionnaire = charger_antidictionnaire(fichier_antidictionnaire)

    # Lire le fichier
    with open(fichier_entree, 'r', encoding='utf-8') as f:
        texte = f.read()

    # Étape 1 : Détection des entités avec Stanza
    doc = nlp(texte)
    personnages_stanza = set()  # Utiliser un set pour éviter les doublons
    for sentence in doc.sentences:
        for ent in sentence.ents:
            if ent.type == 'PER':  # Garder uniquement les entités de type 'PER'
                personnages_stanza.add(ent.text.strip())

    # Étape 2 : Détection des lieux avec Flair
    flair_sentence = Sentence(texte)
    tagger.predict(flair_sentence)
    lieux_flair = set()  # Ensemble pour stocker les lieux détectés
    for entity in flair_sentence.get_spans('ner'):
        if entity.get_label("ner").value == "LOC":  # Garder uniquement les lieux
            lieux_flair.add(entity.text.strip().lower())

    # Étape 3 : Exclure les lieux et les termes du fichier antidictionnaire
    personnages_final = []
    for personnage in personnages_stanza:
        personnage_formate = personnage.title()  # Formater en titre (première lettre majuscule)
        if (personnage.lower() not in lieux_flair and
            personnage.lower() not in mots_antidictionnaire and
            personnage_formate not in personnages_final):
            personnages_final.append(personnage_formate)

    return personnages_final
