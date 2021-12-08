#!/usr/bin/python2.7
# coding: utf-8

################
# main.py     
# Théophile Roos       
# 24 mai 2019 
# S2P-IPI
# Module Widgets
################

#modules externes
import sys
import os


def create(filename, color, posx, posy):
    #création du dictionnaire
    w = dict()
    w['color'] = color
    w['posx'] = posx
    w['posy'] = posy
    
    #ouverture fichier
    myfile = open(filename, "r")
    chaine = myfile.read()
    myfile.close()

    #separation des lignes
    w["map"] = list()
    listeLignes = chaine.splitlines() 
    w["map"] = listeLignes   
    return w


def getLine(w,y):
    #renvoie le contenu d'une ligne donnee pour l'imprimer par la suite
    return (w["map"][y])


def show(w): 
    #affichage du widget

    #couleur fond
    sys.stdout.write("\033[40m")
    #couleur définie
    sys.stdout.write(w['color'])
        
    
    for y in range(0,len(w["map"])): 
        for x in range(0,len(w["map"][y])):
            #goto
            txt="\033["+str(y+w['posy'])+";"+str(w['posx'])+"H"
            sys.stdout.write(txt)
            
            #affichage ligne par ligne
            sys.stdout.write(getLine(w,y))
    sys.stdout.flush() # on vide le buffer


   

        

   

    
