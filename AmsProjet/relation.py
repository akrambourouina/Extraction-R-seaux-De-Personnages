import os
from collections import defaultdict, Counter
import spacy
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from extraction_personnage import extraire_personnages
from alias import creer_dictionnaire_alias

# Chargement du modèle spaCy pour les phrases
nlp = spacy.load("fr_dep_news_trf")

# Chargement du modèle de sentiment multilingue
tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-xlm-roberta-base-sentiment")
model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-xlm-roberta-base-sentiment")

def analyser_sentiment(text):
    tokens = tokenizer(text, return_tensors="pt", truncation=True)
    output = model(**tokens)
    scores = softmax(output.logits.detach().numpy()[0])
    labels = ["negative", "neutral", "positive"]
    return dict(zip(labels, scores))

def analyser_relations(fichier_entree, fichier_antidictionnaire, alias_dict):
    if not os.path.isfile(fichier_entree):
        raise FileNotFoundError(f"Le fichier spécifié n'existe pas : {fichier_entree}")

    personnages = extraire_personnages(fichier_entree, fichier_antidictionnaire)

    with open(fichier_entree, 'r', encoding='utf-8') as f:
        texte = f.read()

    doc = nlp(texte)
    relations = defaultdict(lambda: defaultdict(list))
    poids_relations = defaultdict(lambda: defaultdict(float))
    compteur_relations = Counter()
    stats = {"ami": 0, "ennemi": 0, "neutre": 0}

    for sent in doc.sents:
        personnages_trouves = [p for p in personnages if p in sent.text]
        if len(personnages_trouves) < 2:
            continue

        sentiment_scores = analyser_sentiment(sent.text)
        sentiment_score = sentiment_scores["positive"] - sentiment_scores["negative"]

        if sentiment_score > 0.1:
            relation_type = "ami"
        elif sentiment_score < -0.1:
            relation_type = "ennemi"
        else:
            relation_type = "neutre"

        poids = abs(sentiment_score)

        for i in range(len(personnages_trouves)):
            for j in range(i + 1, len(personnages_trouves)):
                personnage1 = alias_dict.get(personnages_trouves[i], personnages_trouves[i])
                personnage2 = alias_dict.get(personnages_trouves[j], personnages_trouves[j])

                if personnage1 != personnage2:
                    relations[personnage1][personnage2].append(relation_type)
                    poids_relations[personnage1][personnage2] += poids
                    compteur_relations[personnage1] += 1
                    compteur_relations[personnage2] += 1
                    stats[relation_type] += 1

                    print(f"{personnage1} ↔ {personnage2} | relation: {relation_type} | score: {sentiment_score:.2f} | pos: {sentiment_scores['positive']:.2f} | neg: {sentiment_scores['negative']:.2f}")

    print("\n--- Résumé des relations détectées ---")
    for type_relation, count in stats.items():
        print(f"{type_relation.capitalize()} : {count} relation(s)")

    print("\n--- Personnages les plus connectés ---")
    for perso, nb in compteur_relations.most_common(10):
        print(f"{perso} : {nb} relations")

    return relations, poids_relations, compteur_relations

def agreger_relations(relations):
    relations_finales = {}
    for personnage1, liens in relations.items():
        for personnage2, types in liens.items():
            dominant = max(set(types), key=types.count)
            relations_finales[(personnage1, personnage2)] = dominant
    return relations_finales

def sauvegarder_relations(fichier_sortie, relations):
    with open(fichier_sortie, 'w', encoding='utf-8') as f:
        for (perso1, perso2), relation in relations.items():
            f.write(f"{perso1}\t{perso2}\t{relation}\n")