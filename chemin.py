# Librairies

import datetime
from tkinter import *
from tkinter.ttk import *
import codecs  # Pour encoder en UTF-8 sinon problème au niveau de l'affichage des accents


# ##########################
root = Tk()
root.title("La RATP")
root.geometry('600x300')

# Variable
filename = "stations.txt"


# ##########################
# Fonctions

def quadruple_1val(val):
    """
    Un nombre est transformé en un nombre à 4 chiffres
    Exemple: 2 est transformée en "0002"

    INPUT: valeur / nombre de 4 caractères max
    OUTPUT: string de 4 caractères
    """
    val = str(val)
    while len(val) != 4:
        val = "0"+val

    return val


def lecture_fichier(file):
    """Lit les E"""
    with open(file, "r") as f:
        lignes = f.readlines()

        liste = []
        for ligne in lignes:
            if ligne[0] == "E":
                ligne = ligne[2: len(ligne)-1]
                liste.append(ligne.split(" "))

    return(liste)


def lecture_fichier_stations(file):
    """Lit les V et retourne une liste de la forme
    [n°station, nom station, n°métro, terminus ou non ?, n°station sur la ligne de métro]"""
    with codecs.open(file, "r", "utf-8") as f:
        lignes = f.readlines()

        liste = []
        for ligne in lignes:
            if ligne[0] == "V":
                ligne = ligne[2: len(ligne)-1]
                i = ligne.find("/")
                liste.append([ligne[0:4], ligne[5: i-1], ligne[i+2:i+4],
                             ligne[i+5:i+10], ligne[i+11: len(ligne)-1]])

    return(liste)


def quadruplet_valeur(filename):
    """
    Fait en sorte que les valeurs des stations soient les memes dans la partie V et E
    c'est-à-dire qu'elles soient toutes sous la forme de 4 caractères
    """
    liste = lecture_fichier(filename)
    for i in range(len(liste)):
        for j in range(2):
            while len(liste[i][j]) != 4:
                liste[i][j] = "0"+liste[i][j]

    return liste


def trouve_arete(i, filename):
    """
    Trouve les voisins d'un sommet i.
    INPUT:
        - i: un numero de sommet de 4 caractères (str)
        - filename: fichier.txt
    OUTPUT:
        - liste de toutes les arretes de i sous la forme [[i, voisin1, temps], [i, voisin2, temps], [...]]
    """
    liste = quadruplet_valeur(filename)
    res = []
    for sous_liste in liste:
        if str(i) in sous_liste[0: 2]:
            res.append(sous_liste)

    return res


# #################################
# Plus court Chemin


def secondes_to_hms(temps):
    """
    INPUT: temps: int, représente des secondes
    Converti des secondes en heure(s), minute(s), seconde(s)
    OUTPUT: h, m, s: int, représentent respectivement les heures, minutes et secondes.
    """
    temps = int(temps)
    temps = str(datetime.timedelta(seconds=temps))
    h, m, s = [i for i in temps.split(':')]
    return h, m, s


def trouve_num_metro(station, filename):
    """Renvoie le numero de métro d'une station de métro."""
    stations = lecture_fichier_stations(filename)
    return stations[int(station)][2]


def trouve_nom_station(station, filename):
    """Renvoie le nom d'une station de métro."""
    stations = lecture_fichier_stations(filename)
    return stations[int(station)][1]


def doublon_station(arbo, depart, arrivee, liste_arcs, tmin, filename):
    """
    Supprime de l'arborescence les stations qui ont le meme nom si elles sont au début
    ou à la fin du plus court chemin.
    Recalcule la valeur du temps minimum pour aller d'une station à une autre.

    INPUT:
        - arbo: liste, arborescence du plus court chemin trouve par la fonction dijkstra
        - depart: str, la station de depart
        - arrivee: str, station d'arrivee
        - liste_arcs: liste
        - tmin: int, distance minimale
        - filename: str, ichier.txt

    OUTPUT:
        - arbo: liste
        - tmin: int
    """
    nom_depart = trouve_nom_station(depart, filename)
    nom_station2 = trouve_nom_station(arbo[1], filename)
    nom_arrivee = trouve_nom_station(arrivee, filename)
    nom_av_dernier = trouve_nom_station(arbo[len(arbo)-2], filename)

    if nom_depart == nom_station2:
        # Si la station de départ à le meme nom que la station suivante
        del arbo[0]
        tmin -= int(liste_arcs[int(depart)][4])
        # Enlève le temps d'aller de la station de départ à la station suivante
    if nom_av_dernier == nom_arrivee:
        # si la station d'arrivée est la meme que l'avant dernière station
        del arbo[len(arbo)-1]
        tmin -= int(liste_arcs[int(arrivee)][4])
        # Enlève le temps d'aller de l'avant dernière station à la dernière

    return arbo, tmin


def arborescence(liste, depart, arrivee):
    """
    Recrée l'arborescence du plus court chemin entre la station de départ et d'arrivée

    INPUT:
        - Liste: liste provenant de la fonction Dikstra()
        - depart: quadruplet de valeur (str)
        - arrivee: quadruplet de valeur (str)

    OUTPUT: Liste arborescence
    """

    arbo = [arrivee]
    station_act = arrivee

    while station_act != depart:
        station_act = liste[int(station_act)][2]
        arbo.append(station_act)

    return (list(reversed(arbo)))


def dijkstra(depart, arrivee, filename):
    """NE FONCTIONNE QUE SI GRAPHE CONNEXE
    Algorithme de Dijkstra

    INPUT:
        - depart: quadruplet de valeur (str)
        - arrivee: quadruplet de valeur (str)
        - filename: fichier.txt

    OUTPUT liste de la forme: [Plus courte distance en secondes, [arborescence du + court chemin]]"""

    sommets_traites = []
    liste_stations = lecture_fichier_stations(filename)
    res = [[i,  "NULL", "pere"] for i in range(len(liste_stations))]

    # Initialisation des valeurs
    arcs = trouve_arete(depart, filename)
    for sous_liste in arcs:
        if arrivee in sous_liste and depart in sous_liste:
            # s'il existe un chemin direct entre l'arrivee et le depart
            return [sous_liste[2], [depart, arrivee]]
        else:
            if sous_liste[0] != depart:
                res[int(sous_liste[0])][1] = int(sous_liste[2])
                res[int(sous_liste[0])][2] = depart
            else:
                res[int(sous_liste[1])][1] = int(sous_liste[2])
                res[int(sous_liste[1])][2] = depart
    sommets_traites.append(depart)

    # Boucle principale
    while len(sommets_traites) != len(liste_stations):
        first = True
        id_min = "NULL"
        dmin = "NULL"
        for i in range(len(res)):
            # Cherche le sommet de plus courte temps qui n'a pas encore été traité
            if res[i][1] != "NULL" and res[i][0] not in sommets_traites:
                if first:
                    id_min = i
                    dmin = int(res[i][1])
                    first = False
                elif int(res[i][1]) < dmin:
                    id_min = i
                    dmin = res[i][1]
        if id_min == "NULL" and dmin == "NULL":  # Si graphe non connexe
            print("Erreur")

        arcs = trouve_arete(quadruple_1val(id_min), filename)
        for sous_liste in arcs:  # Pour chaque voisins du sommet traité faire:
            if (sous_liste[0] != quadruple_1val(id_min)
               and sous_liste[0] not in sommets_traites
               and (res[int(sous_liste[0])][1] == "NULL"
               or res[int(sous_liste[0])][1] > dmin + int(sous_liste[2]))):
                # Si le sommet n'a pas déjà été traité et la valeur actuelle de la distance
                # et plus grande que la future valeur de distance faire
                # ou si le sommet n'a pas encore de valeur de distance faire:
                res[int(sous_liste[0])][1] = dmin + int(sous_liste[2])
                res[int(sous_liste[0])][2] = quadruple_1val(id_min)
            elif (sous_liste[1] not in sommets_traites
                  and (res[int(sous_liste[1])][1] == "NULL"
                  or res[int(sous_liste[1])][1] > dmin + int(sous_liste[2]))):
                # Si le sommet n'a pas déjà été traité et la valeur actuelle de la distance
                # et plus grande que la future valeur de distance faire
                # ou si le sommet n'a pas encore de valeur de distance faire:
                res[int(sous_liste[1])][1] = dmin + int(sous_liste[2])
                res[int(sous_liste[1])][2] = quadruple_1val(id_min)
        sommets_traites.append(id_min)

    arbo = arborescence(res, depart, arrivee)
    tmin_finale = res[int(arrivee)][1]
    arbo, tmin_finale = doublon_station(arbo, depart, arrivee, liste_stations,
                                        tmin_finale, filename)
    return [tmin_finale, arbo]


liste_station = []
with codecs.open(filename, 'r', "utf-8") as f:
    liste = f.readlines()
    for i in liste:
        if i[0] == 'V':
            liste_station.append(i.split())


def terminus(stationa, stationb):
    """
    Permet de savoir vers quel terminus il faut prendre la ligne de métro.
    """

    depart = liste_station[stationa]
    arrivee = liste_station[stationb]
    if depart[-3] == arrivee[-3]:
        # On vérifie bien que les deux stations sont sur la même ligne de métro.
        if depart[-2] == 'True':
            # On teste si la station de départ est l'un des terminus de la ligne.
            # Si c'est le cas, on part automatiquement dans la direction de l'autre terminus.
            if depart[-1] == '1' or depart[-1] == '1b':
                # affiche le nom du terminus dans la direction duquel on va;
                if depart[-3] == '07':
                    if 'b' in arrivee[-1]:
                        for j in liste_station:
                            if j[-3] == '07' and j[-1] == '100b':
                                # Il y a une fourche et doncdeux terminus possibles dans un sens de la ligne 07:
                                # le terminus 100 (Mairie d'ivry) et le terminus 100B (Villejuif, Louis Aragon)
                                # Ici, si la station d'arrivée est sur la partie b de la fourche, on part vers le
                                # terminus 100b (Villejuif, Louis Aragon). 
                                string =""
                                for i in range(2, len(j)):
                                    if j[i] != '/':
                                        string = string + j[i] + " "
                                    else:
                                        break
                                return string
                            else:
                                # Ici, on va vers une station soit avant la fourche, soit vers
                                # une station dans la partie non b de la boucle. On cherche donc 
                                # le terminus 100 (Mairie d'Ivry) de la ligne 07.
                                if j[-3] == '07' and j[-1] == '100':
                                    string =""
                                    for i in range(2, len(j)):
                                        if j[i] != '/':
                                            string = string + j[i] + " "
                                        else:
                                            break
                                    return string
                elif depart[-3] != '07':
                    # Ici on considère toutes les lignes qui n'ont pas de boucles
                    # Dans le sens 1 --> 100.
                    for j in liste_station:
                        if j[-3] == depart[-3] and j[-1] == '100':
                                string =""
                                for i in range(2, len(j)):
                                    if j[i] != '/':
                                        string = string + j[i] + " "
                                    else:
                                        break
                                return string
            elif depart[-1] == '100' or depart[-1] == '100b':
                # Ici on part du terminus 100 sur l'axe 1-100. On doit donc remonter vers
                # le terminus 1.
                if depart[-3] != '13':
                    # Il y a une fourche sur la boucle 13 dans la direction 1(Saint-Denis-Université)
                    # ou la direction 1b (Gabriel Péri, Asnières-Gennevilliers). 
                    # Il faut donc faire une exception pour conserver cette fourche. 
                    # Ici, on traite le cas des lignes sans boucles. 
                    for j in liste_station:
                        if j[-3] == arrivee[-3] and j[-1] == '1':
                                string =""
                                for i in range(2, len(j)):
                                    if j[i] != '/':
                                        string = string + j[i] + " "
                                    else:
                                        break
                                return string
                else:
                    if 'b' in arrivee[-1] or 'b' in depart[-1]:
                        # Ici on gère la ligne 13 et la fourche dans le cas où la
                        # station d'arrivée est sur la branche b de la fourche.
                        for j in liste_station:
                            if j[-3] == arrivee[-3] and j[-1] == '1b':
                                string =""
                                for i in range(2, len(j)):
                                    if j[i] != '/':
                                        string = string + j[i] + " "
                                    else:
                                        break
                                return string
                        else:
                            if j[-3] == arrivee[-3] and (j[-1] == '1'):
                                # Ici, on gère le cas dans lequel la station où on va est
                                # avant la fourche, ou la station est dans la direction du 
                                # terminus 1.
                                string =""
                                for i in range(2, len(j)):
                                    if j[i] != '/':
                                        string = string + j[i] + " "
                                    else:
                                        break
                                return string        
        elif arrivee[-2] == 'True':
            # On teste si la station d'arrivée est un terminus.
            # Dans ce cas, on part automatiquement dans la direction de l'arrivée.
            string =""
            for i in range(2, len(arrivee)):
                if arrivee[i] != '/':
                    string = string + arrivee[i] + " "
                else:
                    break
            return string
        else:
            if depart[-1] < arrivee [-1]:   
                # Ici ni la station de départ, ni la station d'arrivée ne sont des terminus.
                # On doit donc voir si la station de départ est avant ou après la station
                # d'arrivée sur l'axe 1--100 de la ligne. 
                # Ici, la station de départ est avant la station d'arrivée: il faut donc 
                # partir dans le sens de la station 100.
                for j in liste_station:
                    if j[-3] == '07':
                        # Ici on gère la fourche de la ligne 07 détaillée ci-dessus.
                        if 'b' in depart[-1] or 'b' in arrivee[-1]:
                            if j[-3] == depart[-3] and j[-1] == '100b':
                                # Permet de garder la boucle de la ligne 07"""
                                string =""
                                for i in range(2, len(j)):
                                    if j[i] != '/':
                                        string = string + j[i] + " "
                                    else:
                                        break
                                return string
                        else:
                            if j[-3] == depart[-3] and j[-1] == '100':
                                # Ici on gère toutes les lignes sans fourches comme
                                # détaillé ci-dessus.
                                string =""
                                for i in range(2, len(j)):
                                    if j[i] != '/':
                                        string = string + j[i] + " "
                                    else:
                                        break
                                return string
                    else:
                        if j[-3] == depart[-3] and (j[-1] == '100' or j[-1] == '100a' or j[-1] == '100b'):
                                string =""
                                for i in range(2, len(j)):
                                    if j[i] != '/':
                                        string = string + j[i] + " "
                                    else:
                                        break
                                return string
            else: 
                # Ici ni la station de départ, ni la station d'arrivée ne sont des terminus.
                # On doit donc voir si la station de départ est avant ou après la station
                # d'arrivée sur l'axe 1--100 de la ligne. 
                # Ici, la station de départ est après la station d'arrivée: il faut donc 
                # partir dans le sens de la station 1.
                for j in liste_station:
                    if j[-3] != '13':
                        # Ici, on gère les lignes n'ayant pas de fourches.
                        if j[-3] == arrivee[-3] and j[-1] == '1':
                                string =""
                                for i in range(2, len(j)):
                                    if j[i] != '/':
                                        string = string + j[i] + " "
                                    else:
                                        break
                                return string
                    else:
                        # ici on gère le cas de la fourche de la ligne 13 comme 
                        # détaillé ci dessus..
                        if 'b' in arrivee[-1] or 'b' in depart[-1]:
                            if j[-3] == arrivee[-3] and j[-1] == '1b':
                                string =""
                                for i in range(2, len(j)):
                                    if j[i] != '/':
                                        string = string + j[i] + " "
                                    else:
                                        break
                                return string
                        else:
                            if j[-3] == arrivee[-3] and (j[-1] == '1'):
                                string =""
                                for i in range(2, len(j)):
                                    if j[i] != '/':
                                        string = string + j[i] + " "
                                    else:
                                        break
                                return string
    else:
        return 'False'


def affichage(depart, arrivee, filename):
    liste = dijkstra(depart, arrivee, filename)
    h, m, s = secondes_to_hms(liste[0])

    num_station = trouve_num_metro(liste[1][0], filename)
    num_station_prec = num_station
    texte = "Vous etes à {}. \n".format(trouve_nom_station(liste[1][0], filename))
    num_station = trouve_num_metro(int(liste[1][0]), filename)
    num_station_fin = trouve_num_metro(int(liste[1][len(liste[1])-1]), filename)

    if num_station == "07" and num_station_fin == "07":
        # Si on ne se déplace que sur la ligne 7
        # Cas spécial car on se déplace sur une ligne avec une fourche
        texte += "Prenez la ligne {} direction {}\n".format(num_station, terminus(int(liste[1][0]), int(liste[1][len(liste[1])-1])))
    else:
        texte += "Prenez la ligne {} direction {}\n".format(num_station, terminus(int(liste[1][0]), int(liste[1][1])))
    cpt = True

    for i in range(len(liste[1])):
        num_station = trouve_num_metro(liste[1][i], filename)
        if "0201" in liste[1] and "0145" in liste[1] and "0373" in liste[1] and cpt:
            # Si on fait une boucle dans le metro 10
            cpt = False
            texte += "A {}, changez et prenez la ligne {} direction {} \n".format(
                trouve_nom_station("0145", filename), num_station, terminus(145, 373))
        elif "0259" in liste[1] and "0036" in liste[1] and "0198" in liste[1] and cpt:
            # Si on fait une boucle dans le metro 10
            cpt = False
            texte += "A {}, changez et prenez la ligne {} direction {} \n".format(
                trouve_nom_station("0036", filename), num_station, terminus(36, 198))
        elif "0131" in liste[1] and "0153" in liste[1] and "0039" in liste[1] and cpt:
            if liste[1].index("0131") < liste[1].index("0153") < liste[1].index("0039") and cpt:
                # Si on veut passer de la fourche du haut à la fourche du bas sur la ligne 13
                cpt = False
                texte += "A {}, changez et prenez la ligne {} direction {} \n".format(
                    trouve_nom_station("0153", filename), num_station, terminus(153, 39))
            elif liste[1].index("0131") > liste[1].index("0153") > liste[1].index("0039") and cpt:
                # Si on veyt passer de la fourche du bas à la fourche du haut sur la ligne 13
                cpt = False
                texte += "A {}, changez et prenez la ligne {} direction {} \n".format(
                    trouve_nom_station("0153", filename), num_station, terminus(153, 131))
        elif "0260" in liste[1] and "0184" in liste[1] and "0161" in liste[1] and cpt:
            if liste[1].index("0260") < liste[1].index("0184") < liste[1].index("0161") and cpt:
                # Si on veut passer de la fourche du haut à la fourche du bas sur la ligne 7
                cpt = False
                texte += "A {}, changez et prenez la ligne {} direction {} \n".format(
                    trouve_nom_station("0184", filename), num_station, terminus(184, 161))
            elif liste[1].index("0260") > liste[1].index("0184") > liste[1].index("0161") and cpt:
                # Si on veut passer de la fourche du haut à la fourche du bas sur la ligne 7
                cpt = False
                texte += "A {}, changez et prenez la ligne {} direction {} \n".format(
                    trouve_nom_station("0184", filename), num_station, terminus(184, 260))
        if num_station != num_station_prec:  # si changement de métro
            num_station_prec = num_station
            texte += "A {}, changez et prenez la ligne {} direction {} \n".format(
                trouve_nom_station(int(liste[1][i]), filename), num_station,
                terminus(int(liste[1][i]), int(liste[1][i+1])))
    texte += "Vous devriez arriver à {} dans {}h {}min et {}s \n".format(
        trouve_nom_station(arrivee, filename), h, m, s)

    return texte


# ##############
# Interface graphique

### Liste des stations dans pour le menu déroulant

option = []
with codecs.open(filename, "r", "utf-8") as f:
    """
    Permet de mettre toutes les stations de métro dans une liste
    """
    for i in f.readlines():
        if i[0] == 'V':
            i = i[0:-1]
            option.append(i)


### Widgets

# Crée le menu déroulant station de départ
station_depart = StringVar()
station1 = Combobox(root, textvariable=station_depart, width="50")
station1['values'] = option
station1['state'] = 'readonly'

# Crée le menu déroulant station d'arrivée
station_arrivee = StringVar()
station2 = Combobox(root, textvariable=station_arrivee, width="50")
station2['values'] = option
station2['state'] = 'readonly'


label = Label(text="Choisir la station de départ et la station d'arrivée:")
label2 = Label(text="Station de départ")
label3 = Label(text="Station d'arrivée")
label4 = Label(root, text ="Choisir la station de départ et la station d'arrivée")

# Lance fonction cheminpluscourt
bouton = Button(root, text="Trouver itinéraire",
                command=lambda: label4.configure(text=(affichage(
                    station_depart.get()[2:6], station_arrivee.get()[2:6], filename))))

# Positionnement des widgets

label.pack()
label2.pack()
station1.pack()
label3.pack()
station2.pack()
bouton.pack()
label4.pack()

root.mainloop()
