import re
from collections import defaultdict

def normaliser_nom(nom):
    """
    Normalise un nom en supprimant les espaces supplémentaires, 
    les caractères spéciaux et en mettant tout en minuscule.

    Args:
        nom (str): Nom à normaliser.

    Returns:
        str: Nom normalisé.
    """
    nom = nom.lower().strip()
    titres = ['mr', 'mme', 'sir', 'dr', 'miss', 'ms', 'mrs', 'prof']
    for titre in titres:
        nom = re.sub(rf"\b{titre}\b", "", nom)
    return nom.strip()

def grouper_noms_par_mots_cles(noms):
    """
    Regroupe les noms similaires en utilisant des mots-clés partagés.

    Args:
        noms (list): Liste de noms à regrouper.

    Returns:
        list: Liste de groupes, chaque groupe étant une liste de noms similaires.
    """
    groupes = defaultdict(list)
    mots_a_groupes = {}
    
    for nom in noms:
        nom_normalise = normaliser_nom(nom)
        mots = set(nom_normalise.split())
        groupes_associes = set(mots_a_groupes.get(mot, -1) for mot in mots)
        groupes_associes.discard(-1)
        
        if not groupes_associes:
            nouvel_index = len(groupes)
            groupes[nouvel_index].append(nom)
            for mot in mots:
                mots_a_groupes[mot] = nouvel_index
        else:
            index_principal = min(groupes_associes)
            groupes[index_principal].append(nom)
            for mot in mots:
                mots_a_groupes[mot] = index_principal
    
    return list(groupes.values())

def creer_dictionnaire_alias(groupes_alias):
    """
    Crée un dictionnaire qui mappe chaque alias à son nom principal.

    Args:
        groupes_alias (list): Liste de groupes d'alias.

    Returns:
        dict: Dictionnaire mapping alias -> nom principal.
    """
    alias_dict = {}
    for groupe in groupes_alias:
        principal = groupe[0]  # Premier nom du groupe comme principal
        for alias in groupe:
            alias_dict[alias] = principal
    return alias_dict
