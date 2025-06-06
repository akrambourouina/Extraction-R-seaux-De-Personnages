import networkx as nx

def construire_graphe_amitie(relations_agregees):
    G = nx.Graph()
    for (perso1, perso2), relation in relations_agregees.items():
        if relation == "ami":
            G.add_edge(perso1, perso2)
    return G

def detecter_cliques(G):
    return list(nx.find_cliques(G))

def groupes_selon_distance(G, distance_max=2):
    groupes = []
    for noeud in G.nodes():
        voisins = nx.single_source_shortest_path_length(G, noeud, cutoff=distance_max)
        groupe = set(voisins.keys())
        groupes.append(groupe)
    # Supprimer les doublons
    groupes_uniques = []
    for g in groupes:
        if g not in groupes_uniques:
            groupes_uniques.append(g)
    return groupes_uniques
