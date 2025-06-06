import networkx as nx
import matplotlib.pyplot as plt
def generer_graphe(cooccurrences, groupes_alias, chapitre_id):
    """
    Génère un graphe à partir des cooccurrences et des alias des personnages.

    Args:
        cooccurrences (list): Liste des cooccurrences [(personnage1, personnage2)].
        groupes_alias (list): Liste des groupes d'alias. Chaque groupe est une liste.
        chapitre_id (str): Identifiant du chapitre (utilisé pour l'exportation).

    Returns:
        str: Le graphe au format GraphML.
    """
    # Créer un graphe non orienté
    G = nx.Graph()

    # Créer un dictionnaire alias -> groupe
    alias_to_group = {alias: ";".join(group) for group in groupes_alias for alias in group}

    # Ajouter les nœuds avec l'attribut "names"
    personnages_uniques = set([item for sublist in cooccurrences for item in sublist])
    for personnage in personnages_uniques:
        alias_group = alias_to_group.get(personnage, personnage)
        G.add_node(personnage, names=alias_group)

    # Ajouter les arêtes avec un poids
    for personnage1, personnage2 in cooccurrences:
        if G.has_edge(personnage1, personnage2):
            G[personnage1][personnage2]['weight'] += 1
        else:
            G.add_edge(personnage1, personnage2, weight=1)

    # Exporter le graphe au format GraphML
    graphml = "".join(nx.generate_graphml(G))
    return graphml





def visualiser_graphe(graphml_content, title="Graphe des Relations"):
    """
    Visualise un graphe à partir d'un contenu GraphML.

    Args:
        graphml_content (str): Le contenu du fichier GraphML.
        title (str): Titre du graphe.
    """
    try:
        # Charger le graphe à partir du contenu GraphML
        with open("temp_graph.graphml", "w", encoding="utf-8") as temp_file:
            temp_file.write(graphml_content)
        
        G = nx.read_graphml("temp_graph.graphml")

        # Générer la position des nœuds pour une meilleure visualisation
        pos = nx.spring_layout(G, seed=42)

        # Extraire les labels des nœuds
        labels = {node: G.nodes[node]['names'] for node in G.nodes() if 'names' in G.nodes[node]}

        # Dessiner le graphe
        plt.figure(figsize=(12, 8))
        nx.draw(
            G,
            pos,
            with_labels=True,
            labels=labels,
            node_color='lightblue',
            edge_color='gray',
            node_size=3000,
            font_size=10,
            font_weight='bold'
        )

        # Ajouter un titre
        plt.title(title, fontsize=16)
        plt.show()

    except Exception as e:
        print(f"Erreur lors de la visualisation du graphe : {e}")



