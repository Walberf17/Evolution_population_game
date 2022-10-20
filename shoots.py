"""
This work with the different attacks types for this game.

The attacks change acording to populational size, age , and specification of
the individual.
"""

# import things
import random
import pygame as pg
from definitions import *
from animations import Animations



# create the POPULATION_CLASSES

class Shoot(Animations):
	"""
	Default class for other shoots.
	it creates itself.
	if defines itself with
	"""
	def __init__(self , enemy_list = None , strenght = 2 , pos = (0,0) , area = (.01 , .01), color = 'black' , velocity = 10 , ang = 0):
		if enemy_list is None:
			enemy_list = []
		self.enemy_list = enemy_list
		Animations.__init__(self , color = color , center = pos , groups = (shoots_group) , area = area)
		self.damage = 2+strenght
		self.angule = ang
		self.max_velocity = velocity
		self.velocity = [-math.cos(ang)*self.max_velocity , -math.sin(ang)*self.max_velocity]

	def update(self):
		Animations.update(self)

		self.hit_enemies()

		if not screen_rect.colliderect(self.rect):
			self.kill()

	def hit_enemies(self):
		for ind in self.enemy_list:
			if ind.check_hit(self.rect):
				ind.hit(self.damage)
				self.kill()

	def move(self):
		self.rect.move_ip(self.velocity)

