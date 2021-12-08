#!/usr/bin/python2.7
# coding: utf-8

################
# main.py     
# Théophile Roos       
# 24 mai 2019 
# S2P-IPI
# Module Aliens
################

#modules externes
import random
import sys
import os
import math

#mes modules
import Usefull

def create(number, speed_spawn, speed_aliens): 
    u'''
    aliens = Aliens.create(2,3,5)
    constructeur de l'objet alien
    param : number (int), speed_spawn(int), speed_aliens(int)

    retourne le vaisseau ainsi construit
    '''
    #création du dict aliens
    aliens = dict()
    aliens['number'] = number
    aliens['speed_spawn'] = speed_spawn
    aliens['speed_aliens'] = speed_aliens
    aliens['liste'] = list()
    aliens['aliens_remaning'] = number
    aliens['time'] = 0.0
    aliens['color'] = 'white'

    return aliens 



def reset(a, number, speed_spawn, speed_aliens):
    u'''
    Aliens.reset(aliens, 2, 5, 5)
    reset l'objet alien en cas de fin de partie
    param : dict aliens, le nombre d'aliens, la vitesse de spawn, la vitesse les aliens

    ne retourne rien
    '''
    a['number'] = number
    a['speed_spawn'] = speed_spawn
    a['speed_aliens'] = speed_aliens
    a['aliens_remaning'] = number
    a['liste'] = list()
    a['time'] = 0.0

    return


def addAlien(a, delta_t): 
    u'''
    Aliens.addAlien()
    fonction qui ajoute un alien avec une position random
    param : le dict alien, le temps d'exécution de la dernière itération du système

    ne retourne rien
    '''
    #gestion de l'autoriastion de tirer
    autorisation = False
    a['time'] = a['time'] + delta_t
    wait_time = 1.0/a['speed_spawn']
    
    if a['time']>wait_time and a['aliens_remaning']>=1:
        a['aliens_remaning'] += -1
        a['time'] = 0.0
        autorisation = True

   
    if autorisation == True :

        assert type(a) is dict
        y = 2 
        x =2*random.randint(4,91)
        position_alien = x, y
        a['liste'].append(position_alien)


def setListe(a, list_missiles):
    #mutateur de la liste des missiles
    a['liste'] = list_missiles


def show(a): 
    u'''
    Aliens.show(aliens)
    fonction qui affiche les aliens
    param : dict aliens
    ne retourne rien
    '''

    for elem in a['liste']:
        # pour chacun des aliens, on se place au bon endroit dans le terminal, on setup la couleur et on affiche l'alien
        # goto
        x=int(elem[0])
        y=int(elem[1])
        txt="\033["+str(int(y))+";"+str(int(x))+"H"
        sys.stdout.write(txt)
        #couleur
        sys.stdout.write(Usefull.getAsciiColor(a['color']))
        #couleur fond noire
        sys.stdout.write("\033[40m")
        #print
        sys.stdout.write('()')
        sys.stdout.flush() # vidange du buffer de la sortie standard forçée 

       
def collision(a, liste_missile):
    # fonction qui prend en paramètre le dict alien et la liste des missiles
    # elle va ajouter aux listes d'aliens et de missiles  à supprimer les missiles et aliens en collision
    # elle va ensuite supprimer les aliens dans cette liste et renvoyer la liste des missiles à supprimer qui va être traitée par la fonction collision du module Missiles

    #listes de missiles et d'aliens à supprimer
    liste_missile_to_del = list()
    liste_alien_to_del = list()

    for missile in liste_missile:
        missile_int = [int(missile[0]), int(missile[1])] # version du missiles avec les coordonnées entières
        for hitbox in getHitbox(a):
            hitbox_int = [int(hitbox[0]), int(hitbox[1])] # version de la hitbox avec les coordonnées entières
            if missile_int == hitbox_int: # pour chacun des hitbox et des missiles, on vérifie si leur coordonées entière sont les mêmes, si oui on les ajoute  à la liste des missiles et aliens à supprimer
                liste_missile_to_del.append(missile)
                liste_alien_to_del.append(hitbox)
                hitbox_gauche = [hitbox[0] -1 , hitbox[1]]
                liste_alien_to_del.append(hitbox_gauche)

    # pour chacun des aliens on vérifie si il est dans la liste des aliens à supprimer, si non, on l'ajoute à la nouvelle liste des aliens
    new_liste_aliens = list()
    for alien in getPositionAll(a): 
        alien = list(alien)
        if not (alien in liste_alien_to_del):
            new_liste_aliens.append(tuple(alien))

    setListe(a, new_liste_aliens) # on met a jour la liste des aliens

    return liste_missile_to_del # on renvoie la liste des missiles à supprimer



def getHitbox(a): 
    #fonction qui renvoie les hitboxs des aliens
    
    hitboxs = list()
    for alien in a['liste']:

        #pour chacun des aliens on ajoute les coordonnées de ses deux hitbox à la liste hitboxs 

        hitboxs.append(list(alien))
        hitboxs.append([alien[0] + 1, alien[1]])
    return hitboxs

def getPositionAll(a):
    #fonction qui renvoie une liste contenant la position de tout les aliens
    return a['liste']







def win(a):
    #fonction qui renvoie True si un Aliens touche le bas
    
    win = False

    for elem in a['liste']:
        if elem[1]>=53.0:

            #Pour chacun des aliens on vérifie si il touche le bas de la zone de jeu, si oui on renvoie True

            win = True
            a['color'] = 'blue'

    return win

def move(a, dt):
    #fonction qui met à jour la position des aliens
    new_liste = list()

    for elem in a['liste']:
        #on définit la position à t+1 pour chaque aliens et on la met à jour si il n'est pas en bas de la zone de jeu

        x,y = elem[0], elem[1]
        new_x,new_y = elem[0], elem[1] + a['speed_aliens']*dt

        if new_y<=54:
            y = new_y

        x = new_x
        listeposal = [x,y] # nouvelles coordonnée 
        new_liste.append(tuple(listeposal))

    a['liste'] = new_liste


def getAliensNotDead(a):
    # fonction qui renvoie le nombre d'alien dans la zone de jeu plus ceux qui restent à afficher
    assert type(a) is dict

    number_aliens_not_dead = len(a['liste']) + a['aliens_remaning']
    return int(number_aliens_not_dead)


def loose(a):
    #fonction qui renvoie True si les aliens ont perdu : ce qui signifie qu'il n'y a plus d'aliens en attente d'apparition ni dans la zone de jeu
    assert type(a) is dict
    if a['liste'] == [] and a['aliens_remaning'] == 0:
        return True
    else:
        return False
    

def up(a, niveau):
    #fonction qui augmente le nombre d'aliens, leur vitesse, leur vitesse d'apparition
    assert type(a) is dict
    assert type(niveau) is int
    a['number'] = int(1.2*a['number'])
    a['speed_aliens'] = int(1.4*a['speed_aliens'])
    a['speed_spawn'] = int(1.4*a['speed_spawn'])
    a['aliens_remaning'] = a['number']
    a['liste'] = list()
    a['time'] = 0.0
