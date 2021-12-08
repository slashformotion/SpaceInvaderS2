#!/usr/bin/python2.7
# coding: utf-8

################
# main.py     
# Théophile Roos       
# 24 mai 2019 
# S2P-IPI
# Module Usefull
# toutes les fonctions utiles facilitant le codage et le debugging
################

#modules externes
import os
import sys

def getAsciiBackgroundColor(color):
    u'''
    43 = Usefull.getAsciiBackgroundColor('blue')
    renvoie la sequence escape pour la couleur selectionnee
    param : color | str()
    '''

    assert type(color) is str
    
    if color == 'black' : 
        color_ascii = '\033[40m'

    elif color == 'red' : 
        color_ascii = '\033[41m'

    elif color == 'green' : 
        color_ascii = '\033[42m'

    elif color == 'yellow' : 
        color_ascii = '\033[43m'

    elif color == 'blue' : 
        color_ascii = '\033[44m'

    elif color == 'magenta' : 
        color_ascii = '\033[45m'

    elif color == 'cyan' : 
        color_ascii = '\033[46m'

    elif color == 'white' : 
        color_ascii = '\033[47m'

    return color_ascii

def getAsciiColor(color):
    u'''
    43 = Usefull.getAsciiColor('blue')
    renvoie la sequence escape pour la couleur selectionnee
    param : color | str()
    '''

    assert type(color) is str
    
    if color == 'black' : 
        color_ascii = '\033[30m'

    elif color == 'red' : 
        color_ascii = '\033[31m'

    elif color == 'green' : 
        color_ascii = '\033[32m'

    elif color == 'yellow' : 
        color_ascii = '\033[33m'

    elif color == 'blue' : 
        color_ascii = '\033[34m'

    elif color == 'magenta' : 
        color_ascii = '\033[35m'

    elif color == 'cyan' : 
        color_ascii = '\033[36m'

    elif color == 'white' : 
        color_ascii = '\033[37m'

    return color_ascii

def priint(truc):
    #sortie personalisée vers un fichier de log
    monfichier = open('out.txt', 'a')
    monfichier.write(str(truc) + '\n')

    monfichier.close

def whipeSortieOut():
    #effacement du fichier de log
    monfichier = open('out.txt', 'w')
    monfichier.write(' ')
    monfichier.close
    return
