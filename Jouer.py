#!/usr/bin/python2.7
# coding: utf-8

################
# main.py     
# Théophile Roos       
# 24 mai 2019 
# S2P-IPI
# Bibliothèque tampon pour éviter de surcharger le main
################

#modules externes
import os
import sys
import time


#mes modules
import Vaisseau
import Aliens
import Missiles
import Backgrounds
import Game_data
import Widgets
import Hud
import Leaderboard

#mes bibliothèques perso
import Usefull


########## INITIALISATION ##############################################################################################################################################


def setup(game):
    u"""
    Fonction qui vérifie que le terminal à la bonne taille avant de lancer le jeu
    """
    rows, columns = 0,0
    while int(rows)<55 or int(columns)<190:
        rows, columns = os.popen('stty size', 'r').read().split() #récupération de la taille actuelle du term

        #Affichage d'un message d'erreur + conseils de correction
        sys.stdout.write("\033[1;1H")
        sys.stdout.write("Le terminal que vous utilisez n'est pas assez grand pour jouer à Space Invaders Remastered, appuyez sur F11 ou agrandissez le terminal")
        sys.stdout.write("\033[2;1H")
        sys.stdout.write("Votre définition actuelle est : " + str(rows) + " x " + str(columns))
        sys.stdout.flush()
        time.sleep(0.5)
        # clean du term
        sys.stdout.write("\033[1;1H")
        sys.stdout.write("                                                                                                                                                                                    ")

        sys.stdout.write("\033[2;1H")
        sys.stdout.write("                                                                                                                                                                                    ")
        sys.stdout.flush()

        #on efface tout le terminal
        for y in range(0,100):
            for x in range (0,300):
                sys.stdout.write('\033[' + str(y) + ';' + str(x) + 'H')
                sys.stdout.write(' ')
        sys.stdout.write('\033[1;1H')

    #Récupération du nom du joueur grâce à la fonction raw_input
    name = str()
    sys.stdout.write('\033[1;1H')
    name = raw_input('Votre nom : ')
    name = name.upper() # On met le nom en majuscule
    Game_data.setPlayerName(gd = game['game_data'], player_name = name)
    return


#########################################################################################################################################################################
########## ACCUEIL ######################################################################################################################################################


def interactAccueil(touche, game):
    #gestion des interactions sur l'écran d'accueil
    if not Backgrounds.getOn(game['backgrounds']['background_loose']):# si le message informant l'utilisateur qu'il a perdu est affiché, on ne fait rien

        if touche == 'j':
            #changement d'état
            Game_data.changeState(game['game_data'], 'jouer')

        elif touche == 'l':
            #changement d'état
            Game_data.changeState(game['game_data'], 'leaderboard')
        
        elif touche == 's':
            #changement d'état
            Game_data.changeState(game['game_data'], 'settings')
        return


def updateAccueil(game):
    return
        

def showAccueil(game):
    #affichage du background_accueil et du widget Accueil
    if not Backgrounds.getOn(game['backgrounds']['background_loose']): # si le message informant l'utilisateur qu'il a perdu est affiché, on ne fait rien
        Backgrounds.show(game['backgrounds']['background_accueil'])
        Widgets.show(game['widgets']['widget_accueil'])
    else:
        Backgrounds.show(game['backgrounds']['background_loose'])
    return


##########################################################################################################################################################################
########## LEADERBOARD ###################################################################################################################################################


def interactleaderboard(touche, game):
    if touche == 'a':
        #changement d'état
        Game_data.changeState(game['game_data'], 'accueil')

    elif touche == 'c':
        Leaderboard.clear(game['leaderboard'])

    return


def updateleaderboard(game):
    # mise à jour du leaderboard
    Leaderboard.update(l = game['leaderboard'], score = Game_data.getNiveau(game['game_data']))
    return


def showleaderboard(game):
    #affichage des éléments du leaderboard
    Backgrounds.show(game['backgrounds']['background_leaderboard'])
    Widgets.show(game['widgets']['widget_leaderboard'])
    Leaderboard.show(game['leaderboard'])
    return


##########################################################################################################################################################################
########## SETTINGS ######################################################################################################################################################


def interactSettings(touche, game):
    # gestion des interaction dans les settings
    if touche == 'a':
        #changement d'état
        Game_data.changeState(game['game_data'], 'accueil')

    return

def updateSettings(game):
    return

def showSettings(game):

    Backgrounds.show(game['backgrounds']['background_settings'])
    Widgets.show(game['widgets']['widget_settings'])
    return


########################################################################################################################################################################
######## JOUER ##########################################################################################################################################################


def interactJouer(touche, game):
    # gestion des interaction en jeu
    if touche == 'a':
        #changement d'état
        Game_data.changeState(game['game_data'], 'accueil')
    elif touche == 'd' or touche == 's' : 
        Vaisseau.changeSens(game['vaisseau'])
    return


def updateJouer(game):
    # mise à jour du système en jeu

   
    if not Aliens.win(game['aliens']) : # si les aliens n'ont pas gagné


        #déplacement des missiles, des aliens et du vaisseau
        Vaisseau.move(game['vaisseau'], Game_data.getDt(game['game_data']))
        Missiles.update(game['missiles'], Game_data.getDt(game['game_data']))
        Aliens.move(game['aliens'], Game_data.getDt(game['game_data']))

        #gestion des collisions
        liste_missile_to_del = Aliens.collision(game['aliens'], Missiles.getPositionAll(game['missiles']))
        Missiles.collision(game['missiles'], liste_missile_to_del)

        #ajout d'un alien  et d'un missile
        Missiles.addMissile(game['missiles'], Vaisseau.getPointGenerateur(game['vaisseau']),autorisation_vaisseau = Vaisseau.getTirer(game['vaisseau']))
        Aliens.addAlien(game['aliens'], Game_data.getDeltaT(game['game_data']))
        Hud.update(hud = game['hud'], aliens_remaining = Aliens.getAliensNotDead(game['aliens']), niveau_actuel = Game_data.getNiveau(game['game_data']), player_name = Game_data.getPlayerName(game['game_data']))

    
        
        if Aliens.loose(game['aliens']): # si les aliens ont perdu
            #augmentation du niveau et de la difficulté au travers de l'augmentation du nombre d'alien et de leur vitesse de déplacement et d'apparition 
            Game_data.niveauUp(gd = game['game_data']) 
            Aliens.up(game['aliens'], Game_data.getNiveau(game['game_data']))

    else : # si les aliens ont gagné
        #on met à jour le tableau des score avec le nouveau score, on démarre l'affichage du background_loose, on passe a l'accueil, on reset la partie jeu (vaisseau, missiles, aliens, game_data)
        Leaderboard.update(l = game['leaderboard'], score = Game_data.getNiveau(game['game_data']))
        Backgrounds.setOn(game['backgrounds']['background_loose'])
        Game_data.changeState(game['game_data'], 'accueil')
        Game_data.reset(game['game_data'])
        Aliens.reset(a = game['aliens'] , number = game['game_data_init']['alien_number'] , speed_spawn = game['game_data_init']['speed_spawn_aliens'], speed_aliens = game['game_data_init']['speed_aliens'])
        Vaisseau.reset(vaisseau = game["vaisseau"], posx = game['game_data_init']['vaisseau_posx'] , posy = game['game_data_init']['vaisseau_posy'], vx = game['game_data_init']['speed_vaisseau'], vie = game['game_data_init']['speed_vaisseau'])
        Missiles.reset(game['missiles'])
        return


def showJouer(game):
    # affichage des différents éléments du jeu
    Backgrounds.show(game['backgrounds']['background_map'])
    Aliens.show(game['aliens'])
    Missiles.show(game['missiles'])
    Vaisseau.show(game['vaisseau'])
    Hud.show(game['hud'])
    return


########################################################################################################################################################################