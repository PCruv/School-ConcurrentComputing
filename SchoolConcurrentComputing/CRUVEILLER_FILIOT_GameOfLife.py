#Game Of Life - 4 Juin 2020
#Code par Pierre CRUVEILLER et Jules FILIOT

##  -----Règles du jeu-----

#   *Dans ce Game of Life, les limites de la grille sont des murs

#   *grille de 15x15

#   *The universe of the Game of Life is an infinite two-dimensional orthogonal grid of square cells,
#    each of which is inone of two possible states, alive or dead.

#   *Every cell interacts with its eight neighbours, which are the cells that are horizontally, vertically, or diagonallyadjacent.
#
#   *At each step in time, the following transitions occur :
# -Any live cell with fewer than two live neighbours dies, as if caused by under-population.
# -Any live cell with two or three live neighbours lives on to the next generation.
# -Any live cell with more than three live neighbours dies, as if by overcrowding.
# -Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
#
#   *The initial pattern constitutes the seed of the system.

#   *The first generation is created by applying the above rules simultaneously to every cell in the seed-births and
#    deathsoccur simultaneously, and the discrete moment at which this happens is sometimes called a tick
#    (in other words, each generation is a pure function of the preceding one).

#   *The rules continue to be applied repeatedly to create further generations.

## Code :
##Bibliotheques :

import multiprocessing as mp
from multiprocessing import Process
import os, time, math, random, sys, ctypes, signal
lock = mp.Lock()  #Pour le mutex

##Fonctions :


def clear_ecran():
    """Nettoie l'écran"""
    print("\x1B[2J\x1B[;H", end=' ')


def move_to(lig, col):
    """Bouge le curseur à la ligne et à la colonne indiquée"""
    print("\033[" + str(lig) + ";" + str(col) + "f", end='')


def test_environnement(uneCase, tab):
    """Teste l'environnement d'une case pour savoir son prochain état"""
    EntourageVivant = 0
    #on sépare les 4 cases angulaires en cas particuliers
    if uneCase == 0:  #case en haut à gauche
        if tab[uneCase + 1] == 1:
            EntourageVivant += 1
        if tab[uneCase + 15] == 1:
            EntourageVivant += 1
        if tab[uneCase + 16] == 1:
            EntourageVivant += 1
        if tab[uneCase] == 1:
            if EntourageVivant in [2, 3]:
                return True
            else:
                return False
        else:
            if EntourageVivant == 3:
                return True
            else:
                return False
    elif uneCase == 14:  #case en haut à droite
        if tab[uneCase - 1] == 1:
            EntourageVivant += 1
        if tab[uneCase + 15] == 1:
            EntourageVivant += 1
        if tab[uneCase + 14] == 1:
            EntourageVivant += 1
        if tab[uneCase] == 1:
            if EntourageVivant in [2, 3]:
                return True
            else:
                return False
        else:
            if EntourageVivant == 3:
                return True
            else:
                return False
    elif uneCase == 210:  #case en bas à gauche
        if tab[uneCase + 1] == 1:
            EntourageVivant += 1
        if tab[uneCase - 15] == 1:
            EntourageVivant += 1
        if tab[uneCase - 14] == 1:
            EntourageVivant += 1
        if tab[uneCase] == 1:
            if EntourageVivant in [2, 3]:
                return True
            else:
                return False
        else:
            if EntourageVivant == 3:
                return True
            else:
                return False
    elif uneCase == 224:  #case en bas à droite
        if tab[uneCase - 1] == 1:
            EntourageVivant += 1
        if tab[uneCase - 15] == 1:
            EntourageVivant += 1
        if tab[uneCase - 16] == 1:
            EntourageVivant += 1
        if tab[uneCase] == 1:
            if EntourageVivant in [2, 3]:
                return True
            else:
                return False
        else:
            if EntourageVivant == 3:
                return True
            else:
                return False

    #on teste les 4 bordures
    elif uneCase < 15:  #La première ligne
        for i in [uneCase, uneCase + 15]:
            for j in [i - 1, i, i + 1]:
                if tab[j] == 1 and j != uneCase:
                    EntourageVivant += 1
        if tab[uneCase] == 1:  # Cas où la cellule est vivante
            if EntourageVivant == 2 or EntourageVivant == 3:
                return True
            else:
                return False
        else:  #Cas où la cellule est morte
            if EntourageVivant == 3:
                return True
            else:
                return False

    elif uneCase % 15 == 0:  #La première colonne
        for i in [uneCase - 15, uneCase, uneCase + 15]:
            for j in [i, i + 1]:
                if tab[j] == 1 and j != uneCase:
                    EntourageVivant += 1
        if tab[uneCase] == 1:  # Cas où la cellule est vivante
            if EntourageVivant == 2 or EntourageVivant == 3:
                return True
            else:
                return False
        else:  #Cas où la cellule est morte
            if EntourageVivant == 3:
                return True
            else:
                return False
    elif uneCase >= 210:  #La dernière ligne
        for i in [uneCase, uneCase - 15]:
            for j in [i - 1, i, i + 1]:
                if tab[j] == 1 and j != uneCase:
                    EntourageVivant += 1
        if tab[uneCase] == 1:  # Cas où la cellule est vivante
            if EntourageVivant == 2 or EntourageVivant == 3:
                return True
            else:
                return False
        else:  #Cas où la cellule est morte
            if EntourageVivant == 3:
                return True
            else:
                return False
    elif (uneCase + 1) % 15 == 0:  #La dernière colonne
        for i in [uneCase - 15, uneCase, uneCase + 15]:
            for j in [i - 1, i]:
                if tab[j] == 1 and j != uneCase:
                    EntourageVivant += 1
        if tab[uneCase] == 1:  # Cas où la cellule est vivante
            if EntourageVivant == 2 or EntourageVivant == 3:
                return True
            else:
                return False
        else:  # Cas où la cellule est morte
            if EntourageVivant == 3:
                return True
            else:
                return False

    else:  #cas général
        for i in [uneCase - 15, uneCase, uneCase + 15]:
            for j in [i - 1, i, i + 1]:
                if tab[j] == 1 and j != uneCase:
                    EntourageVivant += 1
        if tab[uneCase] == 1:  # Cas où la cellule est vivante
            if EntourageVivant == 2 or EntourageVivant == 3:
                return True
            else:
                return False
        else:  # Cas où la cellule est morte
            if EntourageVivant == 3:
                return True
            else:
                return False


def une_case(indiceCase, mutex, tab, tab2, fin):
    """Mets à jour l'etat la case selectionnée (rentre dans le tableau de mise à jour son etat futur)"""
    while fin.value == 0:
        mutex.acquire()
        if not test_environnement(indiceCase, tab):
            tab2[indiceCase] = 0
        else:
            tab2[indiceCase] = 1
        mutex.release()
        time.sleep(1)
    sys.exit(0)


def Grille(mutex, tab, tab2, fin):
    """Ce processus mettra à jour à chaque tick toute la grille en fonction de ce que chaque processus-case a rapporté"""
    time.sleep(0.5)
    Tick = 0
    while fin.value == 0:
        clear_ecran()
        mutex.acquire()
        Cellvivante = 0
        evolution = 0
        for indiceCase in range(len(tab)):
            ma_ligne = 1 + indiceCase // 15  #les indices des cases correspondent aux lignes de la grille par tranche de 15 (de l'indice 0 à 14 c'est la ligne 1, etc...)
            ma_colonne = indiceCase - 15 * (ma_ligne - 1) + 1
            move_to(ma_ligne, ma_colonne)
            if tab2[indiceCase] == 0:
                print('-')
            elif tab2[indiceCase] == 1:
                print('X')
                Cellvivante += 1
            if tab2[indiceCase] != tab[indiceCase]:
                evolution += 1
            tab[indiceCase] = tab2[indiceCase]
        move_to(17, 5)
        Tick += 1
        print('Tour:', Tick)
        move_to(18, 5)
        print('Nombre de cellules vivantes:', Cellvivante)
        move_to(20, 10)
        print('Pour mettre fin à la simulation : Ctrl+C')
        if Cellvivante == 0 or evolution == 0:
            fin.value = 1
        mutex.release()
        time.sleep(1)
    move_to(18, 5)
    print('La grille ne va plus évoluer, la simulation est terminée.\n')
    sys.exit(0)


def choixDepart():
    """Permet de choisir la formation de départ (c'est dire les cases en vies au début)"""
    choix = 0
    while choix not in [1, 2, 3, 4, 5, 6, 7]:
        choix = int(
            input(
                'Quelle forme de départ voulez-vous tester ?\n 1: 3 cellules vivantes alignées\n 2: 5 cellules vivantes alignées\n 3: Planeur \n 4: Lightweight Spaceship\n 5: Small Exploder\n 6: Tumbler (se déplace de bas en haut indéfiniment) \n 7: Tests (à modifier dans le code pour tester différentes propriétés) \nRéponse : '
            ))
    return choix


def GameOfLife():
    """Initialise la partie :  génère les process, la grille et démarre les process"""
    clear_ecran()
    choix = choixDepart()
    clear_ecran()
    fin = mp.Value('i', 0)
    Nb_process = 225
    mes_process = [0 for i in range(Nb_process)]
    tab = mp.Array('i', range(Nb_process))
    tab2 = mp.Array('i', range(Nb_process))
    for i in range(Nb_process):
        tab[i] = 0
        tab2[i] = 0
        if choix == 1:
            if i in [19, 34, 49]:  #3 cellules alignées
                tab[i] = 1
        elif choix == 2:
            if i in [80, 81, 82, 83, 84]:  #5 cellules alignées
                tab[i] = 1
        elif choix == 3:
            if i in [2, 18, 31, 32, 33]:  #Glider
                tab[i] = 1
        elif choix == 4:
            if i in [61, 62, 63, 64, 75, 79, 94, 105,
                     108]:  #Lightweight spaceship
                tab[i] = 1
        elif choix == 5:  #Small Exploder
            if i in [112, 126, 127, 128, 141, 143, 157]:
                tab[i] = 1
        elif choix == 6:  #Tumbler
            if i in [
                    65, 66, 68, 69, 80, 81, 83, 84, 96, 98, 109, 111, 113, 115,
                    124, 126, 128, 130, 139, 140, 144, 145
            ]:
                tab[i] = 1
        elif choix == 7:  #Utilisé pour les tests pendant le codage
            if i in [30, 29, 44, 45, 222, 221, 223, 217, 218, 203, 202]:
                tab[i] = 1
        ma_ligne = 1 + i // 15  # les indices des cases correspondent aux lignes de la grille par tranche de 25 (de l'indice 0 à 24 c'est la ligne 1, etc...)
        ma_colonne = i - 15 * (ma_ligne - 1) + 1
        move_to(ma_ligne, ma_colonne)
        if tab[i] == 1:
            print('X')
        else:
            print('-')
        mes_process[i] = Process(
            target=une_case, args=(i, lock, tab, tab2, fin))
    move_to(18, 5)
    print("Formation de départ (X:Vivant, -:Mort) : Départ dans 3 secondes.")
    time.sleep(3)
    for indiceCase in range(len(tab)):
        tab2[indiceCase] = tab[indiceCase]
    grille = mp.Process(target=Grille, args=(lock, tab, tab2, fin))
    grille.start()

    for i in range(Nb_process):
        mes_process[i].start()

    for i in range(Nb_process):
        mes_process[i].join()
    grille.join()


#---------------------------------------------------------------
##Main :

if __name__ == "__main__":
    GameOfLife()
