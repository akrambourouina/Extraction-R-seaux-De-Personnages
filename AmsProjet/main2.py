from extraction import extraire_textes_pdf
from nettoyage import nettoyer_textes
from extraction_personnage import extraire_personnages
from alias import grouper_noms_par_mots_cles, creer_dictionnaire_alias
from occurences import detecter_cooccurrences
from relation import analyser_relations, agreger_relations, sauvegarder_relations
from visualisation import generer_graphe
from visualisation_web import generer_graphe_interactif
from analyse_clique import construire_graphe_amitie, detecter_cliques, groupes_selon_distance

def pipeline_complet(fichier_pdf, fichier_antidictionnaire):
    fichier_txt = "texte_extrait.txt"
    extraire_textes_pdf(fichier_pdf, fichier_txt)

    fichier_txt_nettoye = "texte_nettoye.txt"
    nettoyer_textes(fichier_txt, fichier_txt_nettoye)

    personnages = extraire_personnages(fichier_txt_nettoye, fichier_antidictionnaire)
    groupes_alias = grouper_noms_par_mots_cles(personnages)
    alias_dict = creer_dictionnaire_alias(groupes_alias)

    relations, poids_relations, compteur_relations = analyser_relations(
        fichier_txt_nettoye, fichier_antidictionnaire, alias_dict)

    relations_agregees = agreger_relations(relations)

    fichier_relations = "relations_detectees.txt"
    sauvegarder_relations(fichier_relations, relations_agregees)

    generer_graphe_interactif(
        relations_agregees,
        poids_relations,
        compteur_relations,
        "graphe_fondation_interactif.html"
    )

    return relations_agregees  # <-- Pour l’analyse des cliques ensuite


if __name__ == "__main__":
    fichier_antidictionnaire = "antidictionnaire.txt"
    fichier_pdf = "Fondation_et_empire_sample.pdf"
    
    # Exécuter le pipeline et récupérer les relations
    relations_agregees = pipeline_complet(fichier_pdf, fichier_antidictionnaire)

    # Analyse des cliques
    G_amitie = construire_graphe_amitie(relations_agregees)

    print("🔹 Cliques complètes d'amitié :")
    for clique in detecter_cliques(G_amitie):
        if len(clique) >= 3:
            print(clique)

    print("\n🔹 Groupes d’amis à distance ≤ 2 :")
    for groupe in groupes_selon_distance(G_amitie, distance_max=2):
        if len(groupe) >= 3:
            print(groupe)
