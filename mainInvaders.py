#!/usr/bin/python2.7
# coding: utf-8

################
# main.py     
# Théophile Roos       
# 24 mai 2019 
# S2P-IPI
# Fichier principal
################

#modules externes
import sys
import os
import time
import select
import tty 
import termios

#mes modules


import Vaisseau
import Aliens
import Missiles
import Backgrounds
import Usefull
import Game_data
import Widgets
import Jouer
import Hud
import Leaderboard


#recuperation interaction clavier
old_settings = termios.tcgetattr(sys.stdin)

### PARAMETRES DU JEU ###
# game_data_init contient les variables à modifier pour l'équilibrage du jeu

dt = 0.01
state = 'accueil'
loose = False
niveau = 1
speed_spawn_aliens = 2
speed_vaisseau = 120
alien_number = 10
speed_aliens = 10
vaisseau_posx = 91
vaisseau_posy = 53
vaisseau_vie = 3
player_name = str()

game_data_init = {'player_name' : player_name, 'vaisseau_vie' : vaisseau_vie, 'vaisseau_posx' : vaisseau_posx, 'vaisseau_posy' : vaisseau_posy, 'state' : state, 'loose' : loose, 'dt' : dt, 'niveau' : niveau, 'speed_spawn_aliens' : speed_spawn_aliens, 'speed_vaisseau' : speed_vaisseau , 'alien_number' : alien_number, 'speed_aliens' : speed_aliens}

### Fin PARAM DU JEU ###

## sous donnees de backgrounds
background_map = None
background_accueil = None
background_settings = None
background_leaderboard = None
background_loose = None

#dictionnaire qui contiendra tous les backgrounds
backgrounds = {'background_map' : background_map, 'background_accueil' : background_accueil, 'background_settings' : background_settings, 'background_leaderboard' : background_leaderboard}


# sous donnees
widget_accueil = None
widget_settings = None
widget_leaderboard = None
#dictionnaire qui contiendra tous les widgets
widgets = {'widget_accueil' : widget_accueil, 'widget_settings' : widget_settings, 'widget_leaderboard' : widget_leaderboard}






missiles = None
game_data = None
aliens = None
vaisseau = None
transition = None
hud = None
leaderboard = None

#dictionnaire principal qui contiendra tous les 'objets' et les dictionnaire d'objets comme les backgrounds ou les windgets par exemples
game ={'leaderboard' : leaderboard, 'hud' : hud, 'widgets' : widgets , 'game_data_init' : game_data_init, 'missiles' : missiles, 'aliens' : aliens, 'game_data' : game_data, 'backgrounds' : backgrounds, 'vaisseau' : vaisseau}




def init():
    global game
    Usefull.whipeSortieOut() # effacement du contenu du fichier out.txt qui sert à obtenir une sortie standard pour debugger

    #####   Création de tous les dictionnaires qui se comportent comme des objets   #####

    #création des background
    game['backgrounds']['background_map'] = Backgrounds.create(filename = 'ascii_images/background_map.txt', color = 'white', static = True, on = False, time = 0)
    game['backgrounds']['background_accueil'] = Backgrounds.create(filename = 'ascii_images/background_accueil.txt', color = 'white', static = True, on = False, time = 0)
    game['backgrounds']['background_settings'] = Backgrounds.create(filename = 'ascii_images/background_settings.txt', color = 'white', static = True, on = False, time = 0)
    game['backgrounds']['background_leaderboard'] =  Backgrounds.create(filename = 'ascii_images/background_leaderboard.txt', color = 'white', static = True, on = False, time = 0)
    game['backgrounds']['background_loose'] =  Backgrounds.create(filename = 'ascii_images/background_loose.txt', color = 'white', static = False, on = False, time = 200)
    
    #création des widgets
    game['widgets']['widget_accueil'] = Widgets.create(filename = 'ascii_images/widget_accueil.txt', color = Usefull.getAsciiColor('white'), posx = 70, posy = 10)
    game['widgets']['widget_settings'] = Widgets.create(filename = 'ascii_images/widget_settings.txt', color = Usefull.getAsciiColor('white'), posx = 50, posy = 10)
    game['widgets']['widget_leaderboard'] = Widgets.create(filename = 'ascii_images/widget_leaderboard.txt', color = Usefull.getAsciiColor('white'), posx = 62, posy = 10)

    #création du vaisseau
    game['vaisseau'] = Vaisseau.create(posx = game['game_data_init']['vaisseau_posx'] , posy = game['game_data_init']['vaisseau_posy'], minx = 2 , maxx = 181,vx = game['game_data_init']['speed_vaisseau'] , color = 'blue', vie = 3, layout = 1, filename = 'ascii_images/layout_vaisseau1.txt')
    #création des aliens
    game['aliens'] = Aliens.create(number = game['game_data_init']['alien_number'] , speed_spawn = game['game_data_init']['speed_spawn_aliens'], speed_aliens =game['game_data_init']['speed_aliens'])
    # création des variable de la base de jeu
    game['game_data'] = Game_data.create(dt = game['game_data_init']['dt'] , loose = game['game_data_init']['loose'], niveau = game['game_data_init']['niveau'], state = game['game_data_init']['state'], delta_t = 0)
    #créations des missiles
    game['missiles'] = Missiles.create(speed_missiles = -50, color = 'red', layout = '|')
    #création des information en jeu
    game['hud'] = Hud.create(color = 'yellow')


    Jouer.setup(game) # Vérification de la taille du terminal et aquisition du nom du joueur

    #création du leaderboard
    game['leaderboard'] = Leaderboard.create(player_name = Game_data.getPlayerName(game['game_data']))


    # interaction clavier
    tty.setcbreak(sys.stdin.fileno())


def interact():
    #interaction jeu/joueur
    global game
    

    if isData():
        touche = sys.stdin.read(1) 
        if touche == '\x1b':  # x1b is ESC
            quitGame() # on quitte le jeu quand Echap est pressé

        if Game_data.getState(game['game_data']) == 'accueil':           
            Jouer.interactAccueil(touche, game) # exécution des interactions quand le système est en état 'accueil'

        elif Game_data.getState(game['game_data']) == 'jouer' :

            Jouer.interactJouer(touche, game) # exécution des interactions quand le système est en état 'jouer'

        elif Game_data.getState(game['game_data']) == 'leaderboard' :

            Jouer.interactleaderboard(touche, game) # exécution des interactions quand le système est en état 'leaderboard'

        elif Game_data.getState(game['game_data']) == 'settings' :
            
            Jouer.interactSettings(touche, game) # exécution des interactions quand le système est en état 'settings'

def update():
    #mise à jour du système
    global game

    if Game_data.getState(game['game_data']) == 'accueil' :

        Jouer.updateAccueil(game) # mise à jour du système quand il est en état 'accueil'

    elif Game_data.getState(game['game_data']) == 'jouer' : 

        Jouer.updateJouer(game) # mise à jour du système quand il est en état 'jouer'

    elif Game_data.getState(game['game_data']) == 'leaderboard' :

        Jouer.updateleaderboard(game) # mise à jour du système quand il est en état 'leaderboard'

    elif Game_data.getState(game['game_data']) == 'settings' :

        Jouer.updateSettings(game) # mise à jour du système quand il est en état 'settings'

def show():
    #affichage du système
    global game

    if Game_data.getState(game['game_data']) == 'accueil' :

        Jouer.showAccueil(game) # affichage des différents éléments quand le système est en état 'accueil'

    elif Game_data.getState(game['game_data']) == 'jouer' : 

        Jouer.showJouer(game) # affichage des différents éléments quand le système est en état 'jouer'

    elif Game_data.getState(game['game_data']) == 'leaderboard' :

        Jouer.showleaderboard(game) # affichage des différents éléments quand le système est en état 'leaderboard'

    elif Game_data.getState(game['game_data']) == 'settings' :

        Jouer.showSettings(game) # affichage des différents éléments quand le système est en état 'settings'

def run():
    #boucle de jeu

    global game
    while 1:
        t0 = time.time() 
       
        update()
        show()
        interact()

        time.sleep(Game_data.getDt(game['game_data'])) # delay de dt

        # chronométre qui donne le temps d'éxécution d'une itération de la boucle
        t1 = time.time()
        delta_t = t1-t0
        Game_data.setDeltaT(game['game_data'], delta_t) 





##########################################################################################

#Fonction à ne pas éditer après le 10 mai 2019, elle sont finies et validées

def quitGame():
    #restoration parametres terminal

    global old_settings # récupération des aciens paramètres

    #couleur white
    sys.stdout.write("\033[37m")
    sys.stdout.write("\033[40m")

    # Effacement de tout le contenu du terminal
    for y in range(0,100): 
        for x in range (0,300):
            sys.stdout.write('\033[' + str(y) + ';' + str(x) + 'H')
            sys.stdout.write(' ')

    # remise à 0 du curseur         
    sys.stdout.write('\033[1;1H') 

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    sys.exit()

def isData():
    #recuperation evenement clavier
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

##########################################################################################
init()
run()
quitGame()