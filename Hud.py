#!/usr/bin/python2.7
# coding: utf-8

import sys
import Usefull
def create(color):
    assert type(color) is str
    hud = dict()
    hud['posx'] = 2 
    hud['posy'] = 55
    hud['aliens_remaining'] = int()
    hud['player_name'] = str()
    hud['niveau_actuel'] = int()
    hud['color'] = color


    return hud

def update(hud, aliens_remaining, niveau_actuel, player_name):
    assert type(hud) is dict
    assert type(aliens_remaining) is int
    assert type(niveau_actuel) is  int
    assert type(player_name) is str

    hud['aliens_remaining'] = aliens_remaining
    hud['player_name'] = player_name
    hud['niveau_actuel'] = niveau_actuel
    return

def show(hud):
    assert type(hud) is dict

    texte = "PLAYER : " + hud['player_name'] + " ALIENS RESTANTS : " + str(hud['aliens_remaining']) + ' NIVEAU ACTUEL : ' + str(hud['niveau_actuel'])
    Usefull.priint(texte)
    #goto
    sys.stdout.write("\033[55;2H")
    #couleur
    sys.stdout.write(Usefull.getAsciiColor(hud['color']))
    sys.stdout.write(texte)
    sys.stdout.flush()


    return

