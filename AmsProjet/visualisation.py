import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches



def charger_relations(fichier_relations):
    """
    Charge les relations depuis un fichier et retourne une liste de tuples.
    
    Args:
        fichier_relations (str): Chemin du fichier contenant les relations.

    Returns:
        list: Liste de tuples (personnage1, personnage2, type_relation).
    """
    relations = []
    with open(fichier_relations, 'r', encoding='utf-8') as f:
        for line in f:
            perso1, perso2, relation = line.strip().split('\t')
            relations.append((perso1, perso2, relation))
    return relations




def generer_graphe(relations):
    """
    Génère un graphe des relations entre personnages.

    Args:
        relations (dict): Dictionnaire des relations.
    """
    G = nx.Graph()

    for (perso1, perso2), relation in relations.items():
        G.add_node(perso1)
        G.add_node(perso2)

    # Supprimer les relations où un personnage n’existe pas dans le graphe
    relations_filtres = {k: v for k, v in relations.items() if k[0] in G.nodes and k[1] in G.nodes}

    for (perso1, perso2), relation in relations_filtres.items():
        color = "green" if relation == "ami" else "red" if relation == "ennemi" else "gray"
        G.add_edge(perso1, perso2, color=color)

    # Affichage du graphe
    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=1800)
    colors = [G[u][v]['color'] for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color=colors, width=2, alpha=0.8)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

    # Légende
    legend_patches = [
        mpatches.Patch(color="green", label="Ami / Alliés"),
        mpatches.Patch(color="red", label="Ennemi / Opposant"),
        mpatches.Patch(color="gray", label="Neutre / Indifférent")
    ]
    plt.legend(handles=legend_patches, loc="upper right")

    plt.title("Graphique des relations entre personnages")
    plt.show()




