#!/usr/bin/python2.7
# coding: utf-8


import os
import sys
import Usefull




def create(posx, posy, minx, maxx,vx, color, vie, layout, filename): #done 
    u'''

    Vaisseau.create(55, 50, 1, 155, 5, 1, 'blue', 3, 1)
    constructeur de l'objet vaisseau
    param : position x et y, min et max en x, vitesse horizontale, degats du vaisseau, couleur, pts de vie, layout(1 ou 2)

    retourne le vaisseau ainsi construit
    '''
    assert type(posx) is int
    assert type(posy) is int
    assert type(minx) is int
    assert type(maxx) is int
    assert type(vx) is int
    assert type(color) is str
    assert type(vie) is int
    assert type(layout) is int

    vaisseau = dict()
    vaisseau['posx'] = posx
    vaisseau['posy'] = posy
    vaisseau['minx'] = minx
    vaisseau['maxx'] = maxx
    vaisseau['vx'] = vx
    vaisseau['color'] = color
    vaisseau['vie'] = vie 
    vaisseau['layout'] = layout
    vaisseau['last_posx'] = posx
    vaisseau['last_posy'] = posy

    myfile = open(filename, "r")
    chaine = myfile.read()


    vaisseau['map'] = list()
    listeLignes = chaine.splitlines()
    vaisseau["map"] = listeLignes
    myfile.close()

    return vaisseau  #retourne le vaisseau cree


def reset(vaisseau, posx, posy, vx, vie):
    u'''
    Vaisseau.reset(vaisseau, posx, posy, minx, maxx,vx, degats, color, vie, layout)
    fonction qui remet au parametres de depart les caracteristoques du vaisseau
    param : vaisseau, position x et y, min et max en x, vitesse horizontale, degats du vaisseau, couleur, pts de vie, layout(1 ou 2)

    ne retourne rien
    '''
    assert type(vaisseau) is dict
    assert type(posx) is int
    assert type(posy) is int
    
    assert type(vx) is int
    
    assert type(vie) is int
    
    

    vaisseau['posx'] = posx
    vaisseau['posy'] = posy
    vaisseau['vx'] = vx
    
    vaisseau['vie'] = vie 
    return 

def move(vaisseau, dt):
    u'''
    Vaisseau.move(game['vaisseau'])
    fonction qui update la pos du vaisseau en faissant attention aux collisions
    param : vaisseau

    ne retourne rien
    '''
    assert type(vaisseau) is dict
    assert type(dt) is float
    posx, posy = getCoord(vaisseau)

    setLastCoord(vaisseau, posx, posy)
    new_posx, new_posy = computeNextPos(vaisseau, dt)
    minx, maxx = getMaxi(vaisseau)
    if not (new_posx<minx or new_posx>maxx):
        setCoord(vaisseau, new_posx, new_posy)
    





def computeNextPos(vaisseau, dt):
    u'''
    x,y = Vaisseau.computeNextPos(vaisseau)
    fonction qui renvoie la nouvelle position du vaisseau
    param : vaisseau et dt

    renvoie un tuple x, y
    '''
    assert type(vaisseau) is dict
    assert type(dt) is float
    posx = vaisseau['posx']
    
    new_posx = posx + dt*vaisseau['vx']

    x=new_posx
    y=vaisseau['posy']



    return x,y




def getPointGenerateur(vaisseau):
    u'''
    x,y = Vaisseau.getPointGenerateur(vaisseau)
    fonction qui renvoie les coordonnee du pt generateur de missile
    param : vaisseau

    retourne un tuple x, y qui sont les coord du pt generateur de missiles
    '''
    assert type(vaisseau) is dict
    x,y = getCoord(vaisseau)
    
    x,y = x+4, y-3
    return x,y



def changeSens(vaisseau):
    u'''
    Vaisseau.changeSens(vaisseau)
    fonction qui change le sens d'avance du vaisseau
    param : le dict vaisseau
    ne retourne rien
    '''
    assert type(vaisseau) is dict
    vaisseau['vx'] = -vaisseau['vx']

def getCoord(vaisseau): 
    u'''
    posx,posy = Vaisseau.getCoord(vaisseau)
    fonction qui renvoie les coordonnee du vaisseau
    param : vaisseau

    retourne un tuple posx, posy qui sont les coord du vaisseau
    '''
    assert type(vaisseau) is dict
    posx,posy = vaisseau['posx'], vaisseau['posy']
    return posx,posy



def setLastCoord(vaisseau, last_x, last_y):
    vaisseau['last_posx'] = last_x
    vaisseau['last_posy'] = last_y

def getLastCoord(vaisseau): 
    u'''
    posx,posy = Vaisseau.getCoord(vaisseau)
    fonction qui renvoie les coordonnee passe du vaisseau
    param : vaisseau

    retourne un tuple last_posx, last_posy qui sont les coord passee du vaisseau
    '''
    assert type(vaisseau) is dict
    last_posx,last_posy = vaisseau['last_posx'], vaisseau['last_posy']
    return last_posx,last_posy



def setCoord(vaisseau, x, y):
    vaisseau['posx'] = x
    vaisseau['posy'] = y



def setColor(vaisseau, color):
    u'''
    Vaisseau.setColor(vaisseau, color)
    set la couleur du vaisseau
    param : vaisseau,color 

    ne retourne rien
    '''
    assert type(vaisseau) is dict
    assert type(color) is str
    vaisseau['color'] = Usefull.getAsciiColor(color)
    

def show(vaisseau):
    u'''
    Vaisseau.show(vaisseau)
    print le vaisseau
    param : vaisseau

    ne retourne rien
    '''
    #couleur fond
    sys.stdout.write("\033[40m")
    #couleur définie
    sys.stdout.write(Usefull.getAsciiColor(vaisseau['color']))

    for y in range(0,len(vaisseau['map'])):
        #goto
        py = y+vaisseau['posy']-2
        strpy = str(int(py))
        strpx = str(int(vaisseau['posx']))

        txt="\033["+strpy+";"+strpx+"H"
       
        sys.stdout.write(txt)


        #print
        sys.stdout.write(str(getLine(vaisseau, y)))
    sys.stdout.flush()


    
    return 


def getLine(vaisseau,y):
    assert type(vaisseau) is dict
    assert type(y) is int
    #renvoie le contenu d une ligne donnee
    return (vaisseau["map"][y])


def getMaxi(vaisseau):
    assert type(vaisseau) is dict
    return vaisseau['minx'], vaisseau['maxx']


def getTirer(vaisseau):
    # la fonction va renvoyer un booléen 
    last_posx, last_posy = getLastCoord(vaisseau)
    posx, posy = getCoord(vaisseau)
    
    if int(posx) == int(last_posx) : #and not (getCoord(vaisseau) == (3.0, 53) or getCoord(vaisseau) == (181.0,53)) 
        return False
    else:
        return True

