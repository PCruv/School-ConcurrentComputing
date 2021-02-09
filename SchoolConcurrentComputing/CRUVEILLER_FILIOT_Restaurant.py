# Réalisation d’un système muti-tâches de simulation d’un restaurant
# Code par Pierre CRUVEILLER et Jules FILIOT

# Quelques codes d'�chappement (tous ne sont pas utilis�s)
CLEARSCR = "\x1B[2J\x1B[;H"  #  Clear SCReen
CLEAREOS = "\x1B[J"  #  Clear End Of Screen
CLEARELN = "\x1B[2K"  #  Clear Entire LiNe
CLEARCUP = "\x1B[1J"  #  Clear Curseur UP
GOTOYX = "\x1B[%.2d;%.2dH"  #  ('H' ou 'f') : Goto at (y,x), voir le code

DELAFCURSOR = "\x1B[K"  #  effacer apr�s la position du curseur
CRLF = "\r\n"  #  Retour � la ligne

# VT100 : Actions sur le curseur
CURSON = "\x1B[?25h"  #  Curseur visible
CURSOFF = "\x1B[?25l"  #  Curseur invisible

# VT100 : Actions sur les caract�res affichables
NORMAL = "\x1B[0m"  #  Normal
BOLD = "\x1B[1m"  #  Gras
UNDERLINE = "\x1B[4m"  #  Soulign�

import multiprocessing as mp
from multiprocessing import Process
import time, random, ctypes

lock = mp.Lock()  #Le mutex
timer = mp.Value(ctypes.c_bool, True)


def effacer_ecran():
    print(CLEARSCR, end='')


def erase_line_from_beg_to_curs():
    print("\033[1K", end='')


def curseur_invisible():
    print(CURSOFF, end='')


def curseur_visible():
    print(CURSON, end='')


def move_to(lig, col):
    print("\033[" + str(lig) + ";" + str(col) + "f", end='')


def serveur(num_serv, Pile, liste_serveur, com_en_traitmnt, liste_client,
            liste_commande, stop):
    """Traite la commande d'un client"""
    client_com = 0
    while stop.value > 0 or timer.value:
        st = False
        for i in range(len(Pile) // 2):
            if i in liste_client:
                None
            else:
                if Pile[2 * i + 1] != -1:
                    liste_client[i] = i
                    for j in range(len(liste_serveur)):

                        if j == num_serv and liste_serveur[j] == -1:
                            liste_serveur[j] = 2 * i
                            client_com = 2 * i
                            liste_commande[num_serv] = (Pile[client_com + 1])
                            st = True
                            break
                    break
        if st == True:
            com_en_traitmnt[num_serv] = 1
            time.sleep(random.randint(3, 6))
            Pile[client_com + 1] = -1
            liste_serveur[num_serv] = -1
            com_en_traitmnt[num_serv] = 0
            liste_client[client_com // 2] = -1
            liste_commande[num_serv] = -1


def client(Stack):
    """Simule aléatoirement les commandes des clients selon une loi uniforme.
 Emet une commande aléatoire toutes les p secondes à l’adresse des serveurs"""
    L = []
    while timer.value:
        p = -1
        for i in range(len(Stack) // 2):
            if Stack[2 * i + 1] == -1:
                L.append(i)
                p = i
                break
        if p != -1:
            time.sleep(0.5)
            com = ord('A') + int(random.uniform(10, 15))
            Stack[2 * p + 1] = com


def major_dHomme(Stack, com_en_traitmnt, liste_serveur, liste_commande, stop):
    """Gere l'affichage à l'écran"""
    while timer.value or stop.value > 0:
        L = []
        for i in range(len(Stack) // 2):
            if Stack[2 * i + 1] != -1:
                L.append((Stack[2 * i], chr(Stack[2 * i + 1])))
        move_to(1, 150)
        erase_line_from_beg_to_curs()
        move_to(1, 1)
        print('Commande(s) en attente : ', L)
        move_to(2, 100)
        erase_line_from_beg_to_curs()
        move_to(2, 1)
        print('Nombre de commandes en attente : ', (len(L)))
        for i in range(5):
            move_to(3 + i, 100)
            erase_line_from_beg_to_curs()
            move_to(3 + i, 1)
            if com_en_traitmnt[i] == 1 and Stack[liste_serveur[i]] != -1:
                print('Statut serveur ' + str(i) + ' : ' +
                      "traite la commande : " + str(chr(liste_commande[i])) +
                      " du client : " + str(Stack[liste_serveur[i]]))
            else:
                print("Statut serveur " + str(i) + " : " + "en attente")
        stop.value -= stop.value
        stop.value += len(L)


def dureeService():
    """Définit pendant combien de temps on génère des commandes"""
    try:
        duree = int(
            input("Pendant combien de secondes prenons-nous les commandes ? "))
    except:
        print("Veuillez rentrer un entier :")
        Restaurant()
    return (duree)


def Restaurant():
    """Initialise le restaurant : génère les processuss et les lances"""
    duree = dureeService()
    effacer_ecran()
    curseur_invisible()
    stop = mp.Value('i', 1)
    mes_serv = [0, 1, 2, 3, 4]
    Stack = mp.Array(
        'i',
        [0, -1, 1, -1, 2, -1, 3, -1, 4, -1, 5, -1, 6, -1, 7, -1, 8, -1, 9, -1])
    liste_serveur = mp.Array('i', [-1, -1, -1, -1, -1])
    CmdEnTraitement = mp.Array('i', [0, 0, 0, 0, 0])
    liste_client = mp.Array('i', [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1])
    liste_commande = mp.Array('i', [-1, -1, -1, -1, -1])
    for i in range(5):
        mes_serv[i] = Process(
            target=serveur,
            args=(
                i,
                Stack,
                liste_serveur,
                CmdEnTraitement,
                liste_client,
                liste_commande,
                stop,
            ))
        mes_serv[i].start()

    maj_dhomme = Process(
        target=major_dHomme,
        args=(
            Stack,
            CmdEnTraitement,
            liste_serveur,
            liste_commande,
            stop,
        ))
    maj_dhomme.start()
    clients = Process(target=client, args=(Stack, ))
    clients.start()

    time.sleep(duree)
    timer.value = False


if __name__ == "__main__":
    Restaurant()
