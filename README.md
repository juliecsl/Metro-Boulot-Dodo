# Metro-Boulot-Dodo
Julie CIESLA , Elise R., Emma L.P.

## Présentation du projet
Ecriture d'un programme permettant de déterminer le plus court itinéraire pour aller d'une station de métro Parisienne à une autre selon le réseau de la RATP.

## Prérequis
* Version Python: 3.8.16
* Librairies: ```tkinter```, ```datetime```et ```codecs```

## Fichiers
* stations.txt: fichier texte permettant de référencer chaque station de métro (numéro de ligne, temps de trajet entre les stations à laquelle elle est directement liée, terminus ou non ? 
* connexe.py: vérifie la connexité du fichier stations.txt
* chemin.py: interface graphique permettant de voir le plus court chemin entre 2 stations sélectionnées.

## Exécution
Les fichiers .py doivent etre exécuter via un interpréteur Python de type VSCODE.

### Utilisation de chemin.py
Exécutez le programme, un onglet représentant l'interface graphique s'ouvre
* sélélectionnez votre sation de départ
* puis votre station d'arrivée
* cliquez sur "trouver itinéraire"
* le résultat s'affiche alors

__Exemple__:
Pour aller d'Anatole France à Porte d'Italie le programme renvoie la solution suivante:

> Vous etes à Anatole France.
Prenez la ligne 03 direction Galliéni
A Opéra, changez et prenez la ligne 07 direction Mairie d'Ivry
Vous devriez arriver à Porte d'Italie dans 0h 23min 43s


## Problème
Le temps indiquer par l'interface graphique reste très théorique, car les temps de changement à pieds entre 2 stations ne sont pas pris en compte.
