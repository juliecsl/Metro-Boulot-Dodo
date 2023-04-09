filename = "stations.txt"

# Fonctions


def lecture_fichier(file):
    """Lit les E du fichier avec les stations"""
    with open(file, "r") as f:
        lignes = f.readlines()

        liste = []
        for ligne in lignes:
            if ligne[0] == "E":
                ligne = ligne[2: len(ligne)-1]
                liste.append(ligne.split(" "))

    return(liste)


def lecture_fichier_stations(file):
    """Lit les V du fichier avec les stations de métro et retourne une liste de la forme
    [n°station, nom station, n°métro, terminus ou non ?, n°station sur la ligne de métro]"""
    with open(file, "r") as f:
        lignes = f.readlines()

        liste = []
        for ligne in lignes:
            if ligne[0] == "V":
                ligne = ligne[2: len(ligne)-1]
                liste.append([ligne[0:5], ligne[5: len(ligne)]])

    return(liste)


def trouve_arete(i, fichier=filename):
    """
    Trouve les voisins d'un sommet i.
    INPUT:
        - i: un numero de sommet de 4 caractères (str)
        - filename: fichier.txt
    OUTPUT:
        - liste de toutes les arretes de i sous la forme [[i, voisin1, temps], [i, voisin2, temps], [...]]
    """
    liste = lecture_fichier(fichier)
    res = []
    for sous_liste in liste:
        if str(i) in sous_liste[0: 2]:
            res.append(sous_liste)

    return res


NB_STATIONS = 375


def colorier(s, liste, cpt=0):
    """
    Colorie les stations qui sont connexes à la première station de la liste.
    Si une station est bien connexe: alors coloration c=1
    Sinon coloration c=1
    """
    # Initialisation des couleurs à 0
    # 0 signifie non coloré
    if cpt == 0:
        cpt = 1
        for i in range(len(liste)):
            liste[i].append("c=0")

    liste_arete = trouve_arete(s)

    liste[int(s)][2] = "c=1"
    for sous_liste in liste_arete:  # Pour chaque sommet voisin de s faire
        if sous_liste[0] != str(s) and liste[int(sous_liste[0])][2] == "c=0":
            colorier(int(sous_liste[0]), liste, 1)  # recursivité
        elif sous_liste[1] != str(s) and liste[int(sous_liste[1])][2] == "c=0":
            colorier(int(sous_liste[1]), liste, 1)  # récursivité

    return liste


def connexe(filename):
    """Vérifie si un graphe filename est connexe"""
    liste = colorier(0, lecture_fichier_stations(filename))

    for i in range(len(liste)):
        if liste[i][2] != "c=1":
            return False

    return True


print(connexe(filename))
