#!/usr/bin/python2.7
# coding: utf-8

def create(dt, loose, niveau, state, delta_t):
    u'''
    game_data = Game_data.create(dt, loose, niveau, state)
    constructeur de la classe game_data
    param : le pas de temps, la variable d'état state, la variable d'état pour l'état de la partie
    
    retourne le dictionaire game_data 
    '''
    assert type(dt) is float
    assert type(loose) is bool
    assert type(niveau) is int
    assert type(state) is str
    assert niveau > 0
    assert dt > 0
    

    gd = dict()
    gd['dt'] = dt
    gd['loose'] = loose
    gd['niveau'] = niveau
    gd['state'] = state
    
    gd['dt_init'] = dt
    gd['loose_init'] = loose
    gd['niveau_init'] = niveau
    gd['state_init'] = state
    

    return gd

def getDeltaT(gd):
    assert type(gd) is dict
    return gd['delta_t']

def getPlayerName(gd):
    assert type(gd) is dict
    return gd['player_name']

def getDt(gd):
    assert type(gd) is dict
    return gd['dt']

def getLoose(gd):
    assert type(gd) is dict
    return gd['loose']

def getNiveau(gd):
    assert type(gd) is dict
    return gd['niveau']

def getState(gd):
    assert type(gd) is dict
    return gd['state']

   

def reset(gd):
    assert type(gd) is dict
    gd['dt'] = gd['dt_init']
    gd['loose'] = gd['loose_init']
    gd['niveau'] = gd['niveau_init']
    gd['state'] = gd['state_init']
    return
    
def changeState(gd, new_state):
    assert type(gd) is dict
    assert type(new_state) is str
    gd['state'] = new_state

def setDeltaT(gd, delta_t):
    assert type(gd) is dict
    assert type(delta_t) is float

    gd['delta_t'] = delta_t

def setPlayerName(gd, player_name):
    assert type(gd) is dict
    assert type(player_name) is str
    gd['player_name'] = player_name
    gd['player_name_init'] = player_name
    


def niveauUp(gd):
    assert type(gd) is dict
    gd['niveau'] +=1 
    return

    