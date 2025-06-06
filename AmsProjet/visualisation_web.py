from pyvis.network import Network
import networkx as nx
import random
import webbrowser

def generer_graphe_interactif(relations, poids_relations, compteur_relations, nom_fichier_html):
    G = nx.Graph()

    # Ajouter les relations
    for (perso1, perso2), relation in relations.items():
        weight = float(poids_relations[perso1][perso2])
        color = "green" if relation == "ami" else "red" if relation == "ennemi" else "gray"
        G.add_edge(perso1, perso2, color=color, width=1 + 4 * weight)

    # Détection de cliques
    from analyse_clique import detecter_cliques, construire_graphe_amitie
    G_amitie = construire_graphe_amitie(relations)
    cliques = [c for c in detecter_cliques(G_amitie) if len(c) >= 3]

    # Générer des couleurs pour chaque clique
    clique_colors = {}
    color_palette = ['#f94144', '#f3722c', '#f8961e', '#f9844a', '#f9c74f',
                     '#90be6d', '#43aa8b', '#577590', '#277da1', '#9b5de5']

    for idx, clique in enumerate(cliques):
        color = color_palette[idx % len(color_palette)]
        for node in clique:
            clique_colors[node] = color

    # Création du réseau PyVis
    net = Network(height="750px", width="100%", notebook=False, directed=False)

    for node in G.nodes():
        net.add_node(
            node,
            label=node,
            color=clique_colors.get(node, "#97c2fc"),
            size=15
        )

    for u, v, d in G.edges(data=True):
        net.add_edge(u, v, color=d["color"], width=d["width"])

    net.show_buttons(filter_=[])

    net.write_html(nom_fichier_html)
    webbrowser.open(nom_fichier_html)
