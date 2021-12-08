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
import sys
import json

#modules perso
import Usefull

def create(player_name):
	#constructeur
	assert type(player_name) is str
	l = dict()
	l['dict'] = dict()
	l['filename'] = 'leaderboard.json'
	l['current_player_name'] = player_name

	#récupération du leaderboard
	flux = open(l['filename'], "r")
	l['dict'] = json.load(flux)
	flux.close()

	if l['current_player_name'] in l['dict'].keys():
		l['current_best_score'] = l['dict'][l['current_player_name']]
	else:
		l['current_best_score'] = 0
	return l 


def clear(l):
	# fonction qui va vider le leaderboard
	assert type(l) is dict
	l['dict'] = { 'Default' : 0}
	l['map'] = list()
	l['current_best_score'] = 0
	flux = open(l['filename'], 'w')
	json.dump(l['dict'], flux)
	flux.close()

def update(l, score):
	#mise à jour du leaderboard
	assert type(l) is dict
	assert type(score) is int

	# récupération du leaderboard
	flux = open(l['filename'], 'r')
	l['dict'] = json.load(flux)
	flux.close()

	# si le score est meilleur que le meilleur enregistré pour le joueur on le met à jour
	if score-1 > l['current_best_score']:
		l['current_best_score'] = score-1
		l['dict'][l['current_player_name']] = l['current_best_score']


	# mise a jour du fichier des scores
	flux = open(l['filename'], 'w')
	json.dump(l['dict'], flux)
	flux.close()


def show(l):
	# affichage du leaderboard
	assert type(l) is dict
	param_posx = 75
	param_posy = 22

	sys.stdout.write(Usefull.getAsciiColor('white'))

	keys = l['dict'].keys()
	values = l['dict'].values()

	# tri par ordre décroissant des scores
	for i in range(0, len(keys)-1):
		for i in range(0, len(keys)-1):
			if values[i+1] > values[i]:
				values[i+1], values[i] = values[i], values[i+1]
				keys[i+1], keys[i] = keys[i], keys[i+1]

	# affichage des scores 
	for i in range(0, len(keys))[::-1]:
		key, value = keys[i], values[i]
		spacers = '-'*(40-len(key) - len(str(value)))
		toprint = str(key) + ' ' + spacers + ' ' + str(value)
		Usefull.priint(toprint)
		sys.stdout.write('\033[' + str(param_posy+i) + ';' + str(param_posx) + 'H')
		sys.stdout.write(toprint)
		sys.stdout.flush()
		
	return