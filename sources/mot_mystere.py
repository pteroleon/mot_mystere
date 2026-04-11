import pandas as pd
import random
import math
import matplotlib.pyplot as plt
import os

# Frequences des lettres sur les pages wikipedia
FREQ_FR = {
    'e': 12.1, 'a': 7.11, 'i': 6.59, 's': 6.51, 'n': 6.39, 'r': 6.07,
    't': 5.92, 'o': 5.02, 'l': 4.96, 'u': 4.49, 'd': 3.67, 'c': 3.18,
    'm': 2.62, 'p': 2.49, 'g': 1.23, 'b': 1.14, 'v': 1.11, 'h': 1.11,
    'f': 1.11, 'q': 0.65, 'y': 0.46, 'x': 0.38, 'j': 0.34, 'k': 0.29,
    'w': 0.17, 'z': 0.15
}


def charger_mots():
    """Génère la liste des mots à partir du fichier"""
    df = pd.read_csv("liste_francais_22k.txt")
    # Filtrage
    df = df[df['mot'].str.contains('!', regex=True) == False]
    df = df[df['mot'].str.match('^[a-z]+$', na=False)]
    df = df[df['mot'].str.len() > 4]
    return df['mot'].str.lower().tolist()


liste_mots = charger_mots()


def choix_mot(liste):
    return random.choice(liste)


def rating(mot):
    """renvoie une note (sur 10) pour le mot"""

    # Recupere que les lettres (unisques)
    lettres_uniques = set(mot)
    if "-" in lettres_uniques:
        lettres_uniques.remove("-")
    if " " in lettres_uniques:
        lettres_uniques.remove(" ")

    # Calcul de la rareté grace a la frequence des lettres
    score_rarete = 0
    for lettre in lettres_uniques:
        freq = FREQ_FR[lettre]
        score_rarete += (10 / freq)

    # Un mot court est plus dur
    ratio_longueur = 8.0 / max(len(mot), 3)

    # Densité des lettres : un mots avec des lettres différentes est plus dure
    ratio_unicite = len(lettres_uniques) / len(mot)

    score_brut = score_rarete * ratio_longueur * ratio_unicite

    # Normalisation (avec une fonction exponentielle (car quand x->-inf, lim exp->0) qui tend vers 10)
    note_calculee = 10 * (1 - math.exp(-0.04 * score_brut))

    return round(note_calculee, 1)


def choix_mot_filtre(liste, r_min, r_max):
    """Choisit un mot dont le rating est compris entre r_min et r_max"""
    tentatives = 0
    while tentatives < 2000:
        mot = random.choice(liste)
        if r_min <= rating(mot) <= r_max:
            return mot
        tentatives += 1
    return choix_mot(liste)  # Si on en trouve pas


def mot_mystere(mot):
    """création d’un « mot_mystere » à partir du « mot » qui est passé en argument"""
    new_mot=""
    for i in mot:
        if i == "-":
            new_mot+= "- "
        else :
            new_mot+="_ "
    return new_mot[:-1]


def verification(lettre, mot):
    """teste si la lettre figure dans le mot, renvoie un booléen"""
    return lettre in mot


def completer_mot(lettre, mot, myst):
    """renvoie le mot mystere complété avec la lettre
qui vient d’être trouvée
"""
    new_myst=""
    for i in range(len(mot)):
        if lettre == mot[i]:
            new_myst += lettre + " "
        else :
            new_myst+=myst[i*2]+ " "

    return new_myst[:-1]


def reset_tableau():
    """Permet de rénitiliser ou de créer un classement"""
    df = pd.DataFrame({"Nom": [], "Note": [], "Mot": []})
    df.to_csv("tableau_score.csv", index=False)


def ajouter_tableau(nom, note, mot):
    """Permet d'ajouter une personne au classement"""
    if not os.path.exists("tableau_score.csv"):
        reset_tableau()

    tableau = pd.read_csv("tableau_score.csv")
    dico = {"Nom": tableau["Nom"].tolist(), "Note": tableau["Note"].tolist(), "Mot": tableau["Mot"].tolist()}

    if nom in dico["Nom"]: #Si la personne existe déjà
        for i in range(len(dico["Nom"])):
            if dico["Nom"][i] == nom and note >= dico["Note"][i]: # Si sa note est plus élevé
                dico["Mot"][i] = mot
                dico["Note"][i] = note
    else: #Si la personne n'existe pas
        dico["Nom"].append(nom)
        dico["Note"].append(note)
        dico["Mot"].append(mot)

    # Enregistrement
    pd.DataFrame(dico).to_csv('tableau_score.csv', index=False)


def generer_graphique_notes(liste):
    """Permet l'affichage d'un graphique de la répartition des notes"""
    # Calcule de la note pour chaque mot
    notes = [rating(mot) for mot in liste]

    plt.figure(figsize=(10, 6))

    # Création de l'histogramme
    plt.hist(notes, bins=20, color='skyblue', edgecolor='black', alpha=0.7)

    # Ajout des titres
    plt.title("Distribution des notes")
    plt.xlabel("Note (Difficulté)")
    plt.ylabel("Nombre de mots")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Ajout d'une ligne pour la moyenne
    moyenne = sum(notes) / len(notes)
    plt.axvline(moyenne, color='red', linestyle='dashed', linewidth=1, label=f'Moyenne: {moyenne:.2f}')
    plt.legend()

    # Affichage
    plt.show()


if __name__ == "__main__":
    generer_graphique_notes(liste_mots)