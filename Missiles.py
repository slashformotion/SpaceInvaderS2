#!/usr/bin/python2.7
# coding: utf-8

################
# main.py     
# Théophile Roos       
# 24 mai 2019 
# S2P-IPI
# Module Missiles
################

#modules externes
import sys
import os
import Usefull

def create(speed_missiles, color, layout):
    u'''
    missiles = Missiles.create(-2, 'blue', '°')
    constructeur de la 'classe' missile
    param : la vitesse des missiles et la couleur des missiles
    '''
    assert type(speed_missiles) is int
    assert type(color) is str
    assert type(layout) is str

    missiles = dict()
    missiles['speed_missiles'] = speed_missiles
    missiles['color'] = Usefull.getAsciiColor(color)
    missiles['liste'] = list()
    missiles['layout'] = layout
    return missiles


def setListe(m, list_alien):
    #mise  à jour de la liste contenant la position des aliens
    assert type(m) is dict
    assert type(list_alien) is list
    m['liste'] = list_alien


def addMissile(m, posPointGenerateur, autorisation_vaisseau):
    u'''
    Missiles.addMissile(missiles, (50, 50))
    fonction qui ajoute un missile quand le vaisseau s'est décalé d'un caractère et qu'il n'y a pas de missiles déjà présent à la coordonnée du nouveau missile à la liste de l'objet m
    param : le dict missiles et la position du point générateur

    ne retourne rien
    '''
    assert type(posPointGenerateur) is tuple
    assert type(m) is dict

    autorisation = True
    for missile in getPositionAll(m):
        if missile[1] == posPointGenerateur[1]:
            autorisation = False
    if autorisation and autorisation_vaisseau :
        m['liste'].append(tuple(posPointGenerateur))
    return


def reset(m):
    #fonction qui supprime tout les aliens
    assert type(m) is dict
    m['liste'] = list()
    

def getPositionAll(m):
    u'''
    liste_pos_missiles = Missiles.getPositionAll(m)
    fonction qui renvoie une liste des positions des missiles
    param : le dict missiles
    '''
    assert type(m) is dict
    liste_pos_missiles = m['liste']
    return liste_pos_missiles


def move(m, dt):
    u'''
    Missiles.move(m)
    fonction qui met à jour tout les missiles
    param : le dict m
    
    ne retourne rien
    '''
    assert type(m) is dict
    nouvelle_liste = list()
    for elem in m['liste']:
        new_elem = list()
        elem = list(elem)
        # calcul de la nouvelle pos
        new_posx, new_posy = elem[0],elem[1] + dt*m['speed_missiles'] 
        new_elem = [new_posx, new_posy]
        new_elem = tuple(new_elem)
        nouvelle_liste.append(new_elem)
    
    # mise  à jour de la liste des aliens
    m['liste'] = nouvelle_liste


def update(m, dt):
    # vérification que les missiles ne sont pas avec une coordonée verticale négative
    assert type(m) is dict
    move(m, dt)
    new_liste = list()

    for missile in m['liste'] :
        if not (missile[1]<=1) :
            new_liste.append(missile)

    # mise à jour de la liste sans les missiles trop haut qui ne servent plus à rien
    m['liste'] = new_liste        
            

def collision(m, liste_missile_to_del):
    # gestion des collisions avec les aliens via la destruction des missiles qui sont en collision avec eux
    new_liste_missiles = list()

    for missile in getPositionAll(m):
        missile = tuple(missile)

        if not(missile in liste_missile_to_del):
            new_liste_missiles.append(tuple(missile))

    setListe(m, new_liste_missiles)



def show(m):
    u'''
    Missiles.show(m)
    fonction qui affiche les missiles
    param : le dict m 
    
    ne retourne rien
    '''
    assert type(m) is dict

    for elem in m['liste']:

        #définition des coord du missile
        elem = list(elem)
        x = elem[0]
        y = elem[1]

        #goto
        txt = txt="\033["+str(int(y))+";"+str(int(x))+"H"
        sys.stdout.write(txt)

        ##couleur fond noire
        sys.stdout.write("\033[40m")

        #couleur du missile
        sys.stdout.write(m['color'])

        #affichage du missile
        txt = str(m['layout']) + '\n'
        sys.stdout.write(txt)

    sys.stdout.flush()

def changeLayout(new_layout, m):
    u'''
    Missile.changeLayout('|')
    fonction qui change le layout du missile
    param : le dict missile et le nouveau layout

    ne retourne rien
    '''
    m['layout'] = new_layout

