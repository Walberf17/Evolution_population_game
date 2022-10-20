"""
This module creates a individual and the population. the individual is calculated and will scalate with time, reproduce , mutate and evolve. evolve with population
"""
import statistics

import pygame as pg
from pygame.sprite import Group , Sprite
from animations import Animations
import random
import math
from definitions import *
from shoots import Shoot
import statistics as stt
from timer import Timer
from functools import partial

# variables
# STAGES_AGES = [0 , 100 , 300 , 700 , 2100 , 4500 , 11000]
STAGES_AGES = [x*5 for x in range(7)]

EVOLUTIONARY_STAGES = {
	0:{
		'hp':10,
		'agility': 10,
		'mutation': 3,
		'range': 2,
		'strength': 2,
		'color': 'red'
	},
	1:{
		'hp':40,
		'agility': 30,
		'mutation': 3,
		'range': 10,
		'strength': 5,
		'color': 'orange'
	},
	2:{
		'hp':60,
		'agility': 30,
		'mutation': 3,
		'range': 30,
		'strength': 5,
		'color': 'yellow'
	},
	3:{
		'hp':10,
		'agility': 10,
		'mutation': 3,
		'range': 30,
		'strength': 2,
		'color': 'green'
	},
	4:{
		'hp':10,
		'agility': 10,
		'mutation': 3,
		'range': 30,
		'strength': 2,
		'color': 'blue'
	},
	5: {
		'hp': 10 ,
		'agility': 10 ,
		'mutation': 3 ,
		'range': 50 ,
		'strength': 2,
		'color': 'royalblue4'
	} ,
	6: {
		'hp': 10 ,
		'agility': 10 ,
		'mutation': 3 ,
		'range': 80,
		'strength': 2,
		'color': 'violet'
	} ,
	7: {
		'hp': 10 ,
		'agility': 10 ,
		'mutation': 3 ,
		'range': 100 ,
		'strength': 2,
		'color': 'white'
	} ,
}

# POPULATION_CLASSES
class Population(Animations):
	"""
	the population will manage the individuals
	and spread the info throught them.
	init
	manage stage of evolution
	create a individual
	evolve the individuals
	reproduce pop
	mutate pop
	move pop
	click_down
	click_up
	"""

	def __init__(self , age = None , pop_size = 100 , evolution_stage = None , main_group = None , main_enemies_group = None , groups = None , movement_speed = (0,0) , center = None , area = (.6 , .2) , image_name = None , dict_with_images = None , children_image = None , children_dict = None):

		if (age is None) ^ (evolution_stage is None):
			if age is not None:
				self.age = age
				self.ev_stage = self.check_stage()  # Evolutionary stage of the pop
			else:
				self.age = STAGES_AGES[evolution_stage]
				self.ev_stage = evolution_stage
		else:
			raise AssertionError('Just send 1 one of [age , evolution_stage]')
		this_dict = EVOLUTIONARY_STAGES.get(self.ev_stage)
		self.hp_default = this_dict.get("hp")
		self.agility_default = this_dict.get("agility")
		self.mutation_default = this_dict.get("mutation")
		self.strength_default = this_dict.get("strength")
		self.range_default = this_dict.get("range")

		color = this_dict.get("color")
		Animations.__init__(self , image_name = image_name , dict_with_images = dict_with_images , groups = groups ,
		                    area = area , center = center , color = color)
		self.pop_size = 0
		self.children_image = children_image
		self.children_dict = children_dict
		self.movement_speed = pg.Vector2(movement_speed)
		self.clicked = False
		self.children_size = (.05 , .1)
		self.main_group = main_group
		self.enemies = main_enemies_group
		self.population = Group()
		self.update_ev_stage()
		self.create_children(new_pop = pop_size)

	def check_stage(self):
		i = 0
		while i <= len(STAGES_AGES) - 1 and STAGES_AGES[i] <= self.age:
			i += 1
		return max([i - 1 , 0])

	def check_change_state(self):
		"""
		Check if the population changed its evolutionary state, checking throught STAGES_AGES.
		Return the difference of the stages
		"""
		i = 0
		old = self.ev_stage
		self.ev_stage = self.check_stage()
		return self.ev_stage != old

	def update_ev_stage(self):
		if self.check_change_state():
			this_dict = EVOLUTIONARY_STAGES.get(self.ev_stage)
			if this_dict is not None:
				d_range = this_dict.get('range') - self.range_default
				d_hp = this_dict.get('hp') - self.hp_default
				d_agility = this_dict.get('agility') - self.agility_default
				d_strength = this_dict.get('strength') - self.strength_default
				new_color = this_dict.get('color' , 'red')
			self.uptade_stats(d_range , d_hp, d_agility, d_strength , new_color)

	def change_age(self , years = 1):
		self.age += years
		self.age = min([0 , self.age])

	def set_evolutionary_stage(self , new_stage):
		"""
		forces a evolutionary stage, changing the 
		correspodenting age.
		return the difference of the ages
		"""
		self.age = STAGES_AGES[new_stage]
		return self.check_change_state()

	def create_children(self , new_pop = 1):
		for _ in range(new_pop):
			new_age = random.randint(-5 , 5)
			new_age += self.age
			center_pos = []
			for _ in range(2):
				center_pos.append(random.randrange(10 , 90) / 100)

			Individual(age = new_age , ev_stage = self.ev_stage , hp = self.hp_default, range = self.range_default,
			           agility = self.agility_default , mutation_chance = self.mutation_default,
			           strength = self.strength_default , groups = [self.population , self.main_group] ,
			           main_group = self.main_group , main_enemies_group = self.enemies ,
			           area = self.children_size ,color = self.color , image_name = self.children_image,
			           dict_with_images = self.children_dict, rect_to_be = self.rect , center = center_pos , species = self)
			self.pop_size += 1

	def draw(self , screen_to_draw):
		# Animations.draw(self , screen_to_draw)
		for ind in self.population:
			ind.draw(screen_to_draw)

	def move(self):
		self.rect.move_ip(self.movement_speed)

		if self.clicked:
			ds = pg.mouse.get_rel()
		else:
			ds = None

		for ind in self.population:
			ind.move(self.movement_speed, ds)

	def click_down(self , click):
		self.clicked = True

	def click_up(self , click):
		self.clicked = False

	def key_up(self, event):
		for ind in self.population:
			ind.key_up(event)

	def key_down(self , event):
		for ind in self.population:
			ind.key_down(event)

	def update(self):
		self.check_kill()


		Animations.update(self)


		for ind in self.population:
			ind.update(population = self.population , always_on_rect = True)

	def update_strength(self , value = 1):
		self.strength_default += value
		for ind in self.population:
			ind.update_strength(value)

	def update_agility(self , value = 1):
		self.agility_default += value
		for ind in self.population:
			ind.update_agility(value)

	def update_hp(self , value = 1):
		self.hp_default += value
		for ind in self.population:
			ind.update_hp(value)

	def update_age(self , value = 1):

		self.age += value
		for ind in self.population:
			ind.update_age(value)

		self.update_ev_stage()

	def update_range(self , value = 1):
		self.range_default += value
		for ind in self.population:
			ind.update_range(value)

	def uptade_stats(self , d_range , d_hp, d_agility, d_strength , new_color):
		self.update_hp(d_hp)
		self.update_range(d_range)
		self.update_agility(d_agility)
		self.update_strength(d_strength)
		self.update_color(new_color)

	def update_color(self , new_color):
		self.color = new_color
		for ind in self.population:
			ind.update_color(new_color)

	def get_mean_age(self):
		list_1 = []
		for ind in self.population:
			list_1.append(ind.get_age())
		return stt.mean(list_1)

	def get_mean_hp(self):
		list_1 = []
		for ind in self.population:
			list_1.append(ind.get_hp())
		return stt.mean(list_1)

	def get_mean_strength(self):
		list_1 = []
		for ind in self.population:
			list_1.append(ind.get_strength())
		return stt.mean(list_1)

	def get_mean_agility(self):
		list_1 = []
		for ind in self.population:
			list_1.append(ind.get_agility())
		return stt.mean(list_1)

	def get_mean_range(self):
		list_1 = []
		for ind in self.population:
			list_1.append(ind.get_range())
		return stt.mean(list_1)

	def check_kill(self):
		if len(self.population) == 0:
			self.kill()
			return

		if self.rect.collidelist([screen_rect , creation_rect]) == -1:
			self.kill()
			return

	def kill(self):
		for ind in self.population:
			ind.kill()
		Animations.kill(self)


class Individual(Animations):

	def __init__(self , age , ev_stage = 0 , strength = 2 , hp = 10 , agility=10 , mutation_chance = 0 ,
	             range = 1 , main_group = None , main_enemies_group = None , species = None , **kwargs):
		Animations.__init__(self , **kwargs)
		self.species = species
		self.vel = pg.Vector2([0 , 0])
		self.acc = pg.Vector2([0 , 0])
		self.key_vel = pg.Vector2([0 , 0])
		self.age = max([random.uniform(age-mutation_chance , age+mutation_chance) , 0])
		self.hp = max([random.uniform(hp-mutation_chance , hp+mutation_chance) , 1])
		self.strength = max([random.uniform(strength - mutation_chance , strength + mutation_chance) , 1])
		self.range = max([random.uniform(range - mutation_chance , range + mutation_chance) , 1])
		self.range_pixels = self.calc_range_pixels()
		self.agility = max([random.uniform(agility - mutation_chance , agility + mutation_chance) , 1])
		self.shoot_timer = Timer(time_var = 100 / self.agility , recurrent = True , command = partial(self.shoot))
		self.main_group = main_group
		self.enemies = main_enemies_group
		self.max_distance_from_click = calc_proportional_size(.3)
		self.angle = 0
		self.ev_stage = ev_stage  # Evolutionary etage of the individual

	def set_age(self , value = 0):
		self.age = value

	def set_ev_stage(self , value = 0):
		self.ev_stage = value

	def change_age(self , value):
		self.age += value

	def change_stage(self , value):
		self.ev_stage += value

	def reproduce(self , children_n):
		for _ in range(children_n):
			mut = self.species.mutation_default
			new_age = statistics.mean([self.age , self.species.get_mean_age()])+(random.uniform(-mut , mut))
			new_hp = statistics.mean([self.hp , self.species.get_mean_hp()])+(random.uniform(-mut , mut))
			new_strength = statistics.mean([self.strength , self.species.get_mean_strength()])+(random.uniform(-mut , mut))
			new_range = statistics.mean([self.range , self.species.get_mean_range()])+(random.uniform(-mut , mut))
			new_agility = statistics.mean([self.agility , self.species.get_mean_agility()])+(random.uniform(-mut , mut))
			new_range = statistics.mean([self.range , self.species.get_mean_range()])+(random.uniform(-mut , mut))
			Individual(age = new_age , ev_stage = self.ev_stage , hp = new_hp ,
			          agility = new_agility , mutation_chance = mut , range = new_range,
			          strength = new_strength , groups = [self.species.population , self.main_group] ,
			          main_group = self.main_group , main_enemies_group = self.enemies ,
			          area = self.species.children_size , color = 'red' , image_name = self.species.children_image ,
			          dict_with_images = self.species.children_dict , rect_to_be = self.species.rect , center = [self.rect.centerx , self.rect.centery+2],
			          species = self.species)

	def move(self , ds , mouse_rel = None):
		"""
		Get if the mouse is clicked and how much it moved
		:param ds:
		:param clicked:
		:param mouse_rel:
		:return:
		"""
		# move with the population + self.velocity + mouse_rel
		self.full_vel = ds + self.vel + self.move_on_click(mouse_rel) + self.key_vel*self.agility


		self.rect.move_ip(self.full_vel)

		if self.rect_to_be:
			self.rect.clamp_ip(self.rect_to_be)

	def move_on_click2(self , mouse_rel):
		if mouse_rel:
			ang = math.atan2(*mouse_rel)
			proportion = self.agility / 10 * .7 + .3
			vel = pg.Vector2([math.sin(ang) , math.cos(ang)])*proportion
		else:
			vel = [0,0]
		return vel

	def move_on_click(self , mouse_rel):
		if mouse_rel is not None:
			proportion = self.agility/100*.7 + .3
			mouse_rel = pg.Vector2(mouse_rel)
			mouse_rel *= proportion
		else:
			mouse_rel = pg.Vector2([0,0])
		return mouse_rel

	def get_ang(self , point2):
		"""
		calcs the angle from 2 diferent cards
		:param card1: Card object
		:param card2: Card object
		:return: angle in radians
		"""
		x1 , y1 = self.rect.center
		x2 , y2 = point2
		return math.atan2((y2 - y1) , (x2 - x1))

	def draw(self , screen_to_draw):
		if self.full_vel == [0 , 0]:
			self.angle *= .9
		else:
			self.angle = math.degrees(math.atan2(-self.full_vel[0] , -self.full_vel[1]))

		Animations.draw(self , screen_to_draw , angle = self.angle)

	def update(self , population , **kwargs):

		if self.check_death():
			return

		Animations.update(self , **kwargs)

		self.check_movement(population)

		# shoot
		self.shoot_timer.update()

	def check_death(self):
		if self.hp <= 0:
			self.kill()
			return True

		if self.rect.collidelist([screen_rect , creation_rect]) == -1:
			self.kill()
			return True

	def check_movement(self , population):
		acc = pg.Vector2([0 , 0])
		for ind in population:
			if ind != self:  # not checking with itself
				if self.rect.colliderect(ind):  # if ind collide
					if self.rect.center == ind.rect.center:  # move a little bit if 2 rects are the same possition
						self.rect.move_ip(int(random.random() * 10) , 0)
					ang = get_ang(self , ind)  # calcs the angule
					var = math.pi/10
					ang = ang+(random.uniform(-var,var))*ang
					acc += -pg.math.Vector2((math.cos(ang)) * REPULTION_FORCE , -math.sin(
						ang) * REPULTION_FORCE)  # sums all the vector acc with the new vector from the force for the angule

		# calcs the new velocity
		self.vel += acc
		self.vel *= 0.9

	def shoot(self):
		enemy = self.get_enemy()
		if enemy:
			ang = get_ang(enemy , self)
			Shoot(enemy_list = self.enemies , pos = self.get_relative_pos() ,
			      strenght = self.strength , ang = ang)

	def check_hit(self , rect):
		return self.rect.colliderect(rect)

	def hit(self , value = 1):
		self.hp -= value

	def get_relative_pos(self):
		x , y = self.rect.center
		w , h = screen_rect.size
		return [x/w , y/h]

	def get_enemy(self):
		possibilities = []
		for enemy in self.enemies:
			if enemy:
				if self.range_pixels >= abs(pg.Vector2(self.rect.center).distance_to(enemy.rect.center)):
					possibilities.append(enemy)
		if len(possibilities) > 0:
			return random.choice(possibilities)
		return None

	def key_down(self , event):
		vel = pg.Vector2([0,0])
		proportion = 1
		if event.unicode == 'd':
			vel += [proportion , 0]
		elif event.unicode == 'a':
			vel += [-proportion , 0]
		elif event.unicode == 'w':
			vel += [0 , -proportion]
		elif event.unicode == 's':
			vel += [0 , proportion]
		self.key_vel += vel
		return self.key_vel


	def key_up(self , event):
		vel = pg.Vector2([0,0])
		proportion = 1
		if event.unicode == 'd':
			vel += [-proportion , 0]
		elif event.unicode == 'a':
			vel += [proportion , 0]
		elif event.unicode == 'w':
			vel += [0 , proportion]
		elif event.unicode == 's':
			vel += [0 , -proportion]
		self.key_vel += vel
		return self.key_vel

	def uptade_stats(self , d_hp, d_agility, d_strength):
		self.hp +=  d_hp
		self.agility +=  d_agility
		self.strength +=  d_strength

	def update_strength(self , value = 1):
		self.strength += value

	def update_agility(self , value = 1):
		self.agility += value
		self.agility = max(self.agility , 1)
		self.shoot_timer.set_time_var(10 / self.agility)

	def update_hp(self , value = 1):
		self.hp += value

	def update_age(self , value = 1):
		self.age += value

	def update_range(self , value):
		self.range += value
		self.range_pixels = self.calc_range_pixels()
		
	def calc_range_pixels(self):
		new_range = self.range/100*.7 +.3
		return calc_proportional_size(new_range)	

	def update_color(self , new_color):
		self.color = new_color

	def get_strength(self):
		return self.strength

	def get_agility(self):
		return self.agility

	def get_hp(self):
		return self.hp

	def get_age(self):
		return self.age

	def get_range(self):
		return self.range