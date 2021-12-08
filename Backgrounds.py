#!/usr/bin/python2.7
# coding: utf-8
################
# Background   #
# G.Desmeulles #
# 23/04/2013   #
# S2-P MDD     #
################
import sys
import os
import Usefull

#le module background gere le type abstrait de donnee background 
#un background contient une chaine de caractere qui represente 
#une image de fond d ecran


def create(filename, color, static, on, time):
    #création du dictionnaire
    bg = dict()
    bg['color'] = color
    bg['static'] = static
    bg['time'] = time
    bg['remaining'] = time
    bg['on'] = on
    
    #ouverture fichier
    myfile = open(filename, "r")
    chaine = myfile.read()

    #separation des lignes
    bg["map"] = list()
    listeLignes = chaine.splitlines()
    bg["map"] = listeLignes
    
    myfile.close()
        
    return bg

def getLine(bg,y):
    #renvoie le contenu d une case donnee
    return (bg["map"][y])




def show(bg) : 
    if bg['static'] ==True :


        #couleur fond
        sys.stdout.write("\033[40m")
        #couleur définie
        sys.stdout.write(Usefull.getAsciiColor(bg['color']))
        
        #goto
        for y in range(0,len(bg["map"])):
           
            #goto
            txt="\033["+str(y+1)+";"+str(1)+"H"
            sys.stdout.write(txt)

            #affiche
            sys.stdout.write(getLine(bg,y))



    elif bg['static'] == False and bg['on'] == True:

        
        #couleur fond
        sys.stdout.write("\033[40m")
        #couleur définie
        sys.stdout.write(Usefull.getAsciiColor(bg['color']))
        
        #goto
        for y in range(0,len(bg["map"])):
           
            #goto
            txt="\033["+str(y+1)+";"+str(1)+"H"
            sys.stdout.write(txt)

            #affiche
            sys.stdout.write(getLine(bg,y))

        #timeout
        bg['remaining'] = bg['remaining'] - 1

    if (bg['remaining'] == 0 and bg['on'] == True):
        #reset 
        bg['remaining'] = bg['time']
        bg['on'] = False
    sys.stdout.flush()

    
def setOn(bg):
    bg['on'] = True

def getOn(bg):
    assert type(bg) is dict

    if bg['static']:
        return 'static'

    else:
        if bg['on'] :
            return True
        else:
            return False