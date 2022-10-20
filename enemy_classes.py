"""
enemies will inherent from individual, 
but move downwards
shoot the playes population
"""

import random
import pygame as pg
import math
from player_classes import Population , Individual
from animations import Animations
from pygame.sprite import Group
from variables import *
from definitions import *

class EnemyPopulation(Population , Animations):
	
	def __init__(self , age = 0 , pop_size = 5 , evolution_stage = 0 , individual_class = None ,  groups = None):
		Animations.__init__(self , groups = groups , area = [.6 , .2] , center = [.5, .2] , color = 'green')
		self.age = age
		self.hp_default = 10
		self.agility_default = 6
		self.mutation_default = 3
		self.strength_default = 2
		self.individual_class = individual_class
		self.pop_size = 0
		self.population_velocity = pg.Vector2((0,0))
		self.ev_stage = evolution_stage  # Evolutionary etage of the pop
		self.clicked = False
		self.children_size = (.05 , .1)
		self.population = Group()
		self.create_children(new_pop = pop_size)
		self.update_stats()
		
class EnemyIndividual(Individual):
	"""
	enemies different functions
	"""
	def get_enemy(self):
		for player in players_group:
			return get_enemies(player.population)
	
	

	
		
	

