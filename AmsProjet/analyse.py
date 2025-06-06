def analyser_fichier(chemin_fichier):
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        texte = fichier.read()
        nb_caracteres = len(texte)
        nb_mots = len(texte.split())
        nb_phrases = texte.count('.') + texte.count('!') + texte.count('?')
        return nb_caracteres, nb_mots, nb_phrases
